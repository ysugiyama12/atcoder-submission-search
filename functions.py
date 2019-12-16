import os,sys
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()
index_name = "atcoder_submissions"

def getSearchResults(params):
    keyword = params["keyword"]
    user_id = params["user_id"]
    language = params["language"]

    query = {
        "_source": "*",
        "size": 30,
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": keyword,
                            "fields": [
                                "code"
                            ]
                        }
                    },
                    {
                        "query_string": {
                            "query": user_id,
                            "fields": [
                                "user_id"
                            ]
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index=index_name, body=query)
    print(res)
    return res

