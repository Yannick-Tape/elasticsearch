# elasticsearch







1-1 Afficher et sauvegarder votre mapping
GET /eval/_mapping



1-2 Une recherche "match_all" de votre nouvel index nommé impérativement "eval"
GET /eval/_search
{
  "query": {
    "match_all": {}
  }
}



2-1 Établir le nombre de valeurs uniques pour le champ "Division Name"
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "unique_division_names": {
      "cardinality": {
        "field": "Division Name.keyword"
      }
    }
  }
}



2-2 Établir le nombre de valeurs uniques pour le champ "Department Name"
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "unique_department_names": {
      "cardinality": {
        "field": "Department Name.keyword"
      }
    }
  }
}



2-3 Établir le nombre de valeurs uniques pour le champ "Class Name"
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "unique_class_names": {
      "cardinality": {
        "field": "Class Name.keyword"
      }
    }
  }
}



2-4 Combien d'articles sont disponibles dans le dataset ?GET /eval/_search
{
  "size": 0,
  "aggs": {
    "unique_articles": {
      "cardinality": {
        "field": "Clothing ID"
      }
    }
  }
}


2-5 Déterminer le nombre d'articles du champ "Department Name" appartenant à sa Division (champ "Division Name").

GET /eval/_search
{
  "size": 0,
  "aggs": {
    "by_division": {
      "terms": {
        "field": "Division Name.keyword",
        "size": 10
      },
      "aggs": {
        "by_department": {
          "terms": {
            "field": "Department Name.keyword",
            "size": 10
          },
          "aggs": {
            "article_count": {
              "cardinality": {
                "field": "Clothing ID"
              }
            }
          }
        }
      }
    }
  }
}


2-6 Déterminer les articles uniques du champ "Department Name".
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "unique_department_names": {
      "terms": {
        "field": "Department Name.keyword",
        "size": 100
      }
    }
  }
}



3- Vérifier l’existence ou non de valeurs nulles dans le jeu de données
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "missing_values": {
      "filters": {
        "filters": {
          "missing_clothing_id": { "bool": { "must_not": { "exists": { "field": "Clothing ID" } } } },
          "missing_age": { "bool": { "must_not": { "exists": { "field": "Age" } } } },
          "missing_title": { "bool": { "must_not": { "exists": { "field": "Title" } } } },
          "missing_review_text": { "bool": { "must_not": { "exists": { "field": "Review Text" } } } },
          "missing_rating": { "bool": { "must_not": { "exists": { "field": "Rating" } } } },
          "missing_recommended_ind": { "bool": { "must_not": { "exists": { "field": "Recommended IND" } } } },
          "missing_positive_feedback_count": { "bool": { "must_not": { "exists": { "field": "Positive Feedback Count" } } } },
          "missing_division_name": { "bool": { "must_not": { "exists": { "field": "Division Name" } } } },
          "missing_department_name": { "bool": { "must_not": { "exists": { "field": "Department Name" } } } },
          "missing_class_name": { "bool": { "must_not": { "exists": { "field": "Class Name" } } } }
        }
      }
    }
  }
}



4-1 Créer un histogramme du champ "age" avec une valeur d'intervalle à "20"
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "age_histogram": {
      "histogram": {
        "field": "Age",
        "interval": 20
      }
    }
  }
}


4-2 Faire une analyse statistique des notes, déterminer la moyenne et la médiane parmi tous les produits présents dans le dataset
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "average_rating": {
      "avg": {
        "field": "Rating"
      }
    },
    "median_rating": {
      "percentiles": {
        "field": "Rating",
        "percents": [50]
      }
    }
  }
}


4-3 Faire une agrégation des notes pour chaque classe de produit (Champ "Class Name")
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "by_class_name": {
      "terms": {
        "field": "Class Name.keyword",
        "size": 20
      },
      "aggs": {
        "average_rating": {
          "avg": {
            "field": "Rating"
          }
        }
      }
    }
  }
}



4-4 Avec votre histogramme "age", créer un bucket des produits "Class Name" et déterminer les articles les plus représentés selon l'âge des clients.
GET /eval/_search
{
  "size": 0,
  "aggs": {
    "age_buckets": {
      "histogram": {
        "field": "Age",
        "interval": 20
      },
      "aggs": {
        "top_class_names": {
          "terms": {
            "field": "Class Name.keyword",
            "size": 1
          }
        }
      }
    }
  }
}



5-1 Quels sont les termes les plus présents parmi les articles les MIEUX notés ?
GET /eval/_search
{
  "size": 0,
  "query": {
    "term": {
      "Rating": 5
    }
  },
  "aggs": {
    "top_terms_high_rating": {
      "terms": {
        "field": "Review Text.keyword",
        "size": 10
      }
    }
  }
}


5-2 Quels sont les termes les plus présents parmi les articles les MOINS bien notés ?
GET /eval/_search
{
  "size": 0,
  "query": {
    "term": {
      "Rating": 1
    }
  },
  "aggs": {
    "top_terms_low_rating": {
      "terms": {
        "field": "Review Text.keyword",
        "size": 10
      }
    }
  }
}


5-3 Quels produits votre client devrait garder en priorité dans son catalogue ?

Les meilleurs produits à conserver dans le catalogue doivent être :

Les produits les mieux notés → Note (Rating) élevée
Les produits les plus populaires → Nombre d'avis (Review Text non vide) élevé
Les produits les plus recommandés → Recommended IND = True
Les produits avec le plus de feedback positif → Positive Feedback Count élevé
Nous allons utiliser une combinaison d'agrégations pour trouver les articles qui remplissent ces critères.


GET /eval/_search
{
  "size": 0,
  "aggs": {
    "top_products": {
      "terms": {
        "field": "Clothing ID",
        "size": 10
      },
      "aggs": {
        "average_rating": {
          "avg": {
            "field": "Rating"
          }
        },
        "review_count": {
          "value_count": {
            "field": "Review Text.keyword"
          }
        },
        "recommended_count": {
          "sum": {
            "field": "Recommended IND"
          }
        },
        "positive_feedback": {
          "sum": {
            "field": "Positive Feedback Count"
          }
        }
      }
    }
  }
}


5-4 À l'inverse, sur quels produits votre client NE devrait PAS investir ?

Les produits à éviter sont ceux qui :

Ont une mauvaise note (Rating faible)
Reçoivent peu d’avis (Review Text vide ou peu nombreux)
Sont rarement recommandés (Recommended IND = False)
Ont peu ou pas de feedback positif (Positive Feedback Count faible)
Nous allons utiliser une agrégation terms sur "Clothing ID", combinée avec des agrégations avg, value_count et sum pour identifier les produits les moins performants.


GET /eval/_search
{
  "size": 0,
  "aggs": {
    "worst_products": {
      "terms": {
        "field": "Clothing ID",
        "size": 10,
        "order": {
          "average_rating": "asc"
        }
      },
      "aggs": {
        "average_rating": {
          "avg": {
            "field": "Rating"
          }
        },
        "review_count": {
          "value_count": {
            "field": "Review Text.keyword"
          }
        },
        "recommended_count": {
          "sum": {
            "field": "Recommended IND"
          }
        },
        "positive_feedback": {
          "sum": {
            "field": "Positive Feedback Count"
          }
        }
      }
    }
  }
}













