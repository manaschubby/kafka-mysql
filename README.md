# kafka-mysql
Run Confluent Kafka locally and connect it with mySQL databases to automatically stream data from MySQL db onto Kafka


## About *confluent-kafka*
**confluent-kafka-python** provides a high-level Producer, Consumer and AdminClient compatible with all
[Apache Kafka<sup>TM<sup>](http://kafka.apache.org/) brokers >= v0.8, [Confluent Cloud](https://www.confluent.io/confluent-cloud/)
and [Confluent Platform](https://www.confluent.io/product/compare/). The client is:

- **Reliable** - It's a wrapper around [librdkafka](https://github.com/edenhill/librdkafka) (provided automatically via binary wheels) which is widely deployed in a diverse set of production scenarios. It's tested using [the same set of system tests](https://github.com/confluentinc/confluent-kafka-python/tree/master/src/confluent_kafka/kafkatest) as the Java client [and more](https://github.com/confluentinc/confluent-kafka-python/tree/master/tests). It's supported by [Confluent](https://confluent.io).

- **Performant** - Performance is a key design consideration. Maximum throughput is on par with the Java client for larger message sizes (where the overhead of the Python interpreter has less impact). Latency is on par with the Java client.

- **Future proof** - Confluent, founded by the
creators of Kafka, is building a [streaming platform](https://www.confluent.io/product/compare/)
with Apache Kafka at its core. It's high priority for us that client features keep
pace with core Apache Kafka and components of the [Confluent Platform](https://www.confluent.io/product/compare/).



## Usage

- Clone the repository using 
```bash
git clone https://github.com/manaschubby/kafka-mysql.git
```

- Start the docker containers using 
```bash
docker-compose up -d
```

- Wait about 10-15 minutes on a good internet-connection to pull all the required docker image files of Confluent Kafka.

- Once the containers are running ensure that all containers are running continuosly (Especially connect and broker).

- Once connect has started, restart the consumer. (It will automatically restart at continous intervals until connect is not up, however to save time you can manually restart).
  
- You can also run
  ```bash
  python3 consumer.py getting_started.ini
  ```
  in the consumer container terminal to manually start consumer.

- It will automatically initialize the JDBC connector and soon you will see events logged on the consumer logs.

Any changes to the MySQL DB shall reflect there.
  


- **To change the MySQL DB instance open the docker-compose.yaml and change the ENVIRONMENT VARIABLES in the consumer service.**
