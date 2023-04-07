# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip \
    pip install confluent_kafka

# install app
COPY consumer.py /
COPY getting_started.ini /


CMD python3 consumer.py getting_started.ini