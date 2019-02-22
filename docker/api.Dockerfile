FROM python:3.7.2-alpine

WORKDIR /usr/src/app

COPY ./api/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "rest_api.py" ]