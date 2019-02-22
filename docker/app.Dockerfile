FROM python:3.7.2-alpine

WORKDIR /usr/src/app

COPY ./app/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "twitter_stream.py" ]