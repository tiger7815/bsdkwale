import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import telegraph

import core as helper
from utils import progress_bar
from vars import *
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://elearn.reedor.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=4',
}

avc_url_pattern = r'"avc_url":"(.*?)"'
json_pattern = r'<script type="application\/ld\+json">(.*?)<\/script>'

def fetch_video_data(url):
    
    
    response = requests.get(url, headers=headers)
    time.sleep(10)  # Sleep to avoid overwhelming the server
    
    avc_url_match = re.search(avc_url_pattern, response.text)
    if avc_url_match:
        avc_url = avc_url_match.group(1)
        avc_url = re.sub(r'\.json.*', '.m3u8', avc_url)
    else:
        avc_url = "avc_url not found"
    
    json_match = re.search(json_pattern, response.text, re.DOTALL)
    if json_match:
        json_snippet = json_match.group(1)
        data = json.loads(json_snippet)
        name = data.get('name', 'Name not found')
    else:
        name = "JSON snippet not found"

        
    
    return name,avc_url

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("I Am A Bot For Download Links From Your **.TXT** File. \n\n **Bot Made By Leo♌️** \n\n Send /Leo ")


@bot.on_message(filters.command("Restart") & filters.user(ADMINS))
async def restart_handler(_, m):
    await m.reply_text("**Restarted**♌️", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["Leo"]) & filters.user(ADMINS))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('Send me **TXT File**♌️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i)
        
       os.remove(x)
    except:
           await m.reply_text("**Invalid file input.**")
           os.remove(x)
           return

    await editable.edit(f"**Total Links Found Are ** **{len(links)}**\n\n**Send From Where You Want To Download Intial Is** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("Downloaded By or send `no` to skip")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = ""
    if raw_text3 == 'no':
        MR = highlighter
    else:
        MR = raw_text3

    await editable.edit("Now send the **Thumbnail URL**\n\nOr if you don't want any thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    thumb = input6.text
    await editable.delete()
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)



    try:
        for i in range(count - 1, len(links)):
            V = links[i].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = V
            if "player.vimeo.com" in url:
                name, avc_url = fetch_video_data(url)
                url = avc_url
                
                cmd = f'yt-dlp "{url}" -o "{name}.mp4"'
            try:  
                cc = f'**Vid_ID:** {str(count).zfill(3)}\n\n**Title » {name}.mkv\n\n** **Batch** » **{raw_text0}**\n\n**Downloaded By** : **{MR}**'
                Show = f"** Downloading  »**\n\n**Name »** `{name}`\n**Quality »** `Whatever best available`\n\n**URL »** `{url}`"
                prog = await m.reply_text(Show)
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await prog.delete(True)
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1
                time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**Downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**Done Leo♌️**")

bot.run()
