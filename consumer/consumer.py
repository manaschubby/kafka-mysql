import sys
import os
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
import requests
import json



if __name__ == '__main__':
    hostname = os.getenv("MYSQL_HOSTNAME").__str__()
    database = os.getenv("MYSQL_DATABASE").__str__()
    port = os.getenv("MYSQL_PORT").__str__()
    table = os.getenv("MYSQL_TABLE").__str__()
    username = os.getenv("MYSQL_USERNAME").__str__()
    password = os.getenv("MYSQL_PASSWORD").__str__()
    
    url = "http://connect:8083/connectors"

    payload = json.dumps({
    "topics": [
        "jsontest"
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xzHw2iFslXIS1jnibFGhb63wwkisnTLO'
    }
    print(table)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        raise ConnectionError

    if(response.status_code!=200):
        raise ConnectionError
    


    payload = json.dumps({
        "name": "jdbc_source_mysql_01",
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
            "transforms.createKey.type": "org.apache.kafka.connect.transforms.ValueToKey",
            "connection.password": password,
            "connection.user": username,
            "transforms": "createKey,extractInt",
            "transforms.extractInt.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
            "table.whitelist": table,
            "mode": "bulk",
            "topic.prefix": "mysql-01-",
            "transforms.extractInt.field": "id",
            "transforms.createKey.fields": "id",
            "poll.interval.ms": "1000",
            "tasks.max": 1,
            "connection.url": "jdbc:mysql://" + hostname + "/" + database
        }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "mysql-01-"+table
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.

                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()