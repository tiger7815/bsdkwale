import os

api_id = int(os.environ.get("API_ID", '27862677'))
api_hash = os.environ.get("API_HASH", 'e343ce2c81b2b6c2c0d6bee58284e3bd')
bot_token = os.environ.get("BOT_TOKEN", '6871505238:AAF0DiNwF2n5VmmLE77xwdb2zrZrgECWe24')




OWNER = int(os.environ.get("OWNER", '5881684718'))

try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", '').split(',')):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER)
