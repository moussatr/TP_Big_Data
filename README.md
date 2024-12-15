# Configuration de l'accès à Azure Blob Storage dans Databricks

# Ce guide explique comment configurer l'accès à Azure Blob Storage dans Databricks, créer les dossiers nécessaires, et charger des données au format Parquet directement dans le dossier ds-bronze sur Azure Blob Storage, sans utiliser Airbyte, car celui-ci n'est pas encore utilisé pour l'instant.

# Création des dossiers requis.

Dans votre conteneur Azure, créez les dossiers nécessaires pour organiser les données.

/ds-bronze/emdat/current.

/ds-silver/emdat/current.

/ds-gold/emdat/current.

# Charger les données en format Parquet.

Placez le fichier source public-emdat.parquet dans le dossier local ou une autre source accessible.

# Ajouter la dépendance Maven pour Iceberg.

Pour utiliser Iceberg avec Databricks, ajoutez la dépendance suivante à votre cluster Spark :

org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.2.1

# Instructions pour ajouter la dépendance :

Accédez à l'onglet Compute dans Databricks.

Sélectionnez votre cluster, puis cliquez sur Libraries > Install New.

Choisissez Maven comme source et ajoutez l'artefact ci-dessus.

# Après cela, vous pouvez suivre le notebook en toute tranquillité.
