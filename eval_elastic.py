#! /usr/bin/python
from elasticsearch import Elasticsearch
import json

# Connexion au cluster
client = Elasticsearch(hosts="http://localhost:9200")

# Numéro de la question
question_number = "1-1"

# Récupération du mapping de l'index "eval"
mapping = client.indices.get_mapping(index="eval")

# ⚠️ Convertir en dictionnaire pour éviter l'erreur JSON
mapping_dict = mapping.body if hasattr(mapping, "body") else mapping

# Sauvegarde du mapping dans le dossier "eval/"
with open("./eval/index_mapping.json", "w") as f:
    json.dump(mapping_dict, f, indent=2)

print("✅ Mapping sauvegardé dans eval/index_mapping.json")

