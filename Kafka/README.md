# Créer un env virtuel et l'activer
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt

# Démarrer Kafka
docker-compose up -d

# Publication de l'évenement dans Kafka 
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 gold_publish_kafka.py

# Vérifier les topics Kafka
docker exec -it kafka bash
kafka-topics --list --bootstrap-server localhost:9092

# Consommer les messages via le consumer pyspark
docker exec -it kafka bash
kafka-console-consumer --topic gold-data --from-beginning --bootstrap-server localhost:9092
