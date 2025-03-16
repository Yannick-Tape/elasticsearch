#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv

# Connexion à Elasticsearch
es = Elasticsearch(hosts="http://localhost:9200")

# Fonction pour nettoyer les valeurs et s'assurer du bon format
def clean_row(row):
    try:
        # Vérification et conversion des types
        row["Clothing ID"] = row["Clothing ID"].strip() if row["Clothing ID"] else None
        row["Age"] = int(row["Age"]) if row["Age"].isdigit() else None
        row["Title"] = row["Title"].strip() if row["Title"] else None
        row["Review Text"] = row["Review Text"].strip() if row["Review Text"] else None
        row["Rating"] = int(row["Rating"]) if row["Rating"].isdigit() else None
        row["Recommended IND"] = bool(int(row["Recommended IND"])) if row["Recommended IND"].isdigit() else None
        row["Positive Feedback Count"] = int(row["Positive Feedback Count"]) if row["Positive Feedback Count"].isdigit() else None

        # Assurer que "Division Name", "Department Name" et "Class Name" ne sont pas vides
        row["Division Name"] = row["Division Name"].strip() if row["Division Name"] else "Unknown"
        row["Department Name"] = row["Department Name"].strip() if row["Department Name"] else "Unknown"
        row["Class Name"] = row["Class Name"].strip() if row["Class Name"] else "Unknown"

        return row
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage de la ligne : {row} | {str(e)}")
        return None  # Ignore les lignes incorrectes

# Lire le fichier CSV et préparer les données pour Elasticsearch
with open('Womens_Clothing.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    actions = []
    for row in reader:
        cleaned_row = clean_row(row)
        if cleaned_row:
            actions.append({
                "_index": "eval",
                "_source": cleaned_row
            })
    
    try:
        helpers.bulk(es, actions)
        print("✅ Importation réussie.")
    except Exception as e:
        print(f"❌ Erreur d'indexation : {str(e)}")

