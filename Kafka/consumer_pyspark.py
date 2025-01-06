from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaConsumerPySpark") \
    .config("spark.driver.host", "192.168.0.43") \
    .getOrCreate()

# Lire les messages depuis Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "gold-data") \
    .option("startingOffsets", "earliest") \
    .load()

messages_df = kafka_df.selectExpr("CAST(value AS STRING) as message")

query = messages_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
