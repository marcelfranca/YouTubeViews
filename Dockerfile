FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install \
    gcc libc-dev tor -y
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app

CMD python youtube.py 1 youtubeLinks.txt 55 60