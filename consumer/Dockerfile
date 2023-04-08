# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# install app dependencies
RUN pip install confluent_kafka requests

# install app
COPY consumer.py /
COPY getting_started.ini /


CMD ["python3", "consumer.py", "getting_started.ini"]