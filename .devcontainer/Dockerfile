FROM python:3.11-alpine

RUN apk add curl bash build-base linux-headers && adduser -D abc && mkdir /app && chown abc /app

USER abc 

WORKDIR /app
COPY app/requirements.txt /app/

RUN pip install --no-cache --upgrade pip setuptools && pip install --no-cache -r requirements.txt

COPY app /app

ENTRYPOINT ["sleep", "infinity"]
