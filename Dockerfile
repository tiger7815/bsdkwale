FROM ubuntu:latest
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app/
RUN pip install --no-cache-dir --upgrade --requirement /app/requirements.txt
CMD python3 modules/main.py
