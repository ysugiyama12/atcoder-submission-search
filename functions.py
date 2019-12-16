import os,sys
import json
from elasticsearch import Elasticsearch
import requests
es = Elasticsearch()
index_name = "atcoder_submissions"

def getContestDict():
    req = requests.get("https://kenkoooo.com/atcoder/resources/contests.json")
    req = json.loads(req.text)
    data = {}
    for r in req:
        data[r["id"]] = r["title"]
    return data

def getProblemDict():
    req = requests.get("https://kenkoooo.com/atcoder/resources/problems.json")
    req = json.loads(req.text)
    data = {}
    for r in req:
        data[r["id"]] = r["title"]
    return data

def getSearchResults(params):
    keyword = params["keyword"]
    user_id = params["user_id"]
    language = params["language"]
    result = params["result"]

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
                    },
                    {
                        "query_string": {
                            "query": result,
                            "fields": [
                                "result"
                            ]
                        }
                    },  
                ]
            }
        }
    }
    res = es.search(index=index_name, body=query)

    contest_dict = getContestDict()
    problem_dict = getProblemDict()
    # print(problem_dict)
    res = list(map(lambda hit: hit['_source'], res['hits']['hits']))
    for i in range(len(res)):
        res[i]['contest_name'] = contest_dict.get(res[i]['contest_id'], '')
        res[i]['problem_name'] = problem_dict.get(res[i]['problem_id'], '')

    return res

