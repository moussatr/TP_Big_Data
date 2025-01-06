# Ce script Spark permet de publier en continu des données simulées, représentant une table Delta (Gold), vers un topic Kafka.
# Les données sont transformées en JSON, puis envoyées à Kafka pour une intégration ou une consommation en temps réel.
#
# Actuellement, ce script est configuré pour fonctionner en local avec :
# - Des données simulées pour représenter une table Delta.
# - Une configuration Kafka locale (broker sur localhost:9092).
#
# Dans un environnement cloud comme Databricks, il faudrait adapter :
# - La source de données pour pointer vers une table Delta réelle (exemple : `my_cataloggold.fact_disasters`).
# - Le broker Kafka pour utiliser une infrastructure managée ou accessible depuis le cloud.
# - Les options de sécurité (SSL, autorisations) et de checkpoint adaptées au cloud (par exemple : DBFS pour Databricks).
#
# Ce script est conçu pour tester et valider le fonctionnement en local avant une migration dans un environnement cloud.

from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Créer une session Spark
spark = SparkSession.builder \
    .appName("LocalKafkaPublish") \
    .getOrCreate()

# Définir le schéma pour les données simulées
schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("event_date", StringType(), True),
    StructField("region_id", IntegerType(), True),
    StructField("event_type_id", IntegerType(), True),
    StructField("impact_cost_usd", DoubleType(), True)
])

# Créer un DataFrame avec des données simulées
data = [
    ("E001", "2025-01-01", 1, 1001, 12345.67),
    ("E002", "2025-01-02", 2, 1002, 54321.89),
    ("E003", "2025-01-03", 3, 1003, 67890.12)
]

fact_disasters_stream = spark.createDataFrame(data, schema=schema)

# Préparer les données pour Kafka (JSON)
fact_disasters_stream_json = fact_disasters_stream.select(
    to_json(
        struct(
            "event_id",
            "event_date",
            "region_id",
            "event_type_id",
            "impact_cost_usd"
        )
    ).alias("value")
)

# Configuration Kafka
kafka_topic = "gold-data"

# Écrire les données dans Kafka (mode batch)
fact_disasters_stream_json.write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", kafka_topic) \
    .save()

# Instructions pour le mode streaming :
# Remplacer write par writeStream
# Remplacer save par start
# Ajouter .awaitTermination() pour maintenir le flux actif
