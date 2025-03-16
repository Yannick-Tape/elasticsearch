#! /usr/bin/python
from elasticsearch import Elasticsearch
import json
import os

# Connexion au cluster Elasticsearch
client = Elasticsearch(hosts="http://localhost:9200")

# Vérifier si le dossier "eval" existe, sinon le créer
os.makedirs("eval", exist_ok=True)

# Liste des requêtes à exécuter
queries = {
    "1-1_mapping": {"endpoint": "/eval/_mapping", "body": None},
    "1-2_match_all": {"endpoint": "/eval/_search", "body": {"query": {"match_all": {}}}},
    "2-1_unique_division_names": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"unique_division_names": {"cardinality": {"field": "Division Name.keyword"}}}}
    },
    "2-2_unique_department_names": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"unique_department_names": {"cardinality": {"field": "Department Name.keyword"}}}}
    },
    "2-3_unique_class_names": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"unique_class_names": {"cardinality": {"field": "Class Name.keyword"}}}}
    },
    "2-4_total_articles": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"unique_articles": {"cardinality": {"field": "Clothing ID"}}}}
    },
    "2-5_articles_by_department_division": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "by_division": {
                    "terms": {"field": "Division Name.keyword", "size": 10},
                    "aggs": {
                        "by_department": {
                            "terms": {"field": "Department Name.keyword", "size": 10},
                            "aggs": {
                                "article_count": {"cardinality": {"field": "Clothing ID"}}
                            }
                        }
                    }
                }
            }
        }
    },
    "2-6_unique_department_articles": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"unique_department_names": {"terms": {"field": "Department Name.keyword", "size": 100}}}}
    },
    "3_missing_values": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "missing_values": {
                    "filters": {
                        "filters": {
                            field: {"bool": {"must_not": {"exists": {"field": field.replace("missing_", "")}}}}
                            for field in [
                                "missing_clothing_id", "missing_age", "missing_title", "missing_review_text",
                                "missing_rating", "missing_recommended_ind", "missing_positive_feedback_count",
                                "missing_division_name", "missing_department_name", "missing_class_name"
                            ]
                        }
                    }
                }
            }
        }
    },
    "4-1_age_histogram": {
        "endpoint": "/eval/_search",
        "body": {"size": 0, "aggs": {"age_histogram": {"histogram": {"field": "Age", "interval": 20}}}}
    },
    "4-2_rating_stats": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "average_rating": {"avg": {"field": "Rating"}},
                "median_rating": {"percentiles": {"field": "Rating", "percents": [50]}}
            }
        }
    },
    "4-3_rating_by_class": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "by_class_name": {
                    "terms": {"field": "Class Name.keyword", "size": 20},
                    "aggs": {"average_rating": {"avg": {"field": "Rating"}}}
                }
            }
        }
    },
    "4-4_top_class_by_age": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "age_buckets": {
                    "histogram": {"field": "Age", "interval": 20},
                    "aggs": {"top_class_names": {"terms": {"field": "Class Name.keyword", "size": 1}}}
                }
            }
        }
    },
    "5-1_top_terms_high_rating": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "query": {"term": {"Rating": 5}},
            "aggs": {"top_terms_high_rating": {"terms": {"field": "Review Text.keyword", "size": 10}}}
        }
    },
    "5-2_top_terms_low_rating": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "query": {"term": {"Rating": 1}},
            "aggs": {"top_terms_low_rating": {"terms": {"field": "Review Text.keyword", "size": 10}}}
        }
    },
    "5-3_best_products": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "top_products": {
                    "terms": {"field": "Clothing ID", "size": 10},
                    "aggs": {
                        "average_rating": {"avg": {"field": "Rating"}},
                        "review_count": {"value_count": {"field": "Review Text.keyword"}},
                        "recommended_count": {"sum": {"field": "Recommended IND"}},
                        "positive_feedback": {"sum": {"field": "Positive Feedback Count"}}
                    }
                }
            }
        }
    },
    "5-4_worst_products": {
        "endpoint": "/eval/_search",
        "body": {
            "size": 0,
            "aggs": {
                "worst_products": {
                    "terms": {"field": "Clothing ID", "size": 10, "order": {"average_rating": "asc"}},
                    "aggs": {
                        "average_rating": {"avg": {"field": "Rating"}},
                        "review_count": {"value_count": {"field": "Review Text.keyword"}},
                        "recommended_count": {"sum": {"field": "Recommended IND"}},
                        "positive_feedback": {"sum": {"field": "Positive Feedback Count"}}
                    }
                }
            }
        }
    }
}

# Exécution des requêtes et sauvegarde des résultats
for query_name, query_data in queries.items():
    try:
        print(f"📊 Exécution de la requête {query_name}...")

        # Sauvegarde de la requête
        with open(f"./eval/q_{query_name}_request.json", "w") as f:
            json.dump(query_data["body"], f, indent=2)

        # Exécution de la requête
        response = client.search(index="eval", body=query_data["body"]) if query_data["body"] else client.indices.get_mapping(index="eval")

        # Convertir la réponse en dictionnaire si nécessaire
        response_dict = response.body if hasattr(response, "body") else response

        # Sauvegarde des résultats
        with open(f"./eval/q_{query_name}_response.json", "w") as f:
            json.dump(response_dict, f, indent=2)

        print(f"✅ Résultats enregistrés : eval/q_{query_name}_request.json & eval/q_{query_name}_response.json")

    except Exception as e:
        print(f"❌ Erreur sur {query_name} : {str(e)}")

print("🎯 Toutes les requêtes ont été exécutées et enregistrées ! 🚀")

