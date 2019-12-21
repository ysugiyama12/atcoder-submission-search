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
    print(language)
    must_query = []
    if keyword != "":
        must_query.append(
            {
                "query_string": {
                    "query": keyword,
                    "fields": [
                        "code"
                    ]
                }
            }
        )
    if user_id != "":
        must_query.append(
            {
                "query_string": {
                    "query": user_id,
                    "fields": [
                        "user_id"
                    ]
                }
            }
        )

    if language != "-":
        must_query.append(
            {
                "query_string": {
                    "query": '"' + language + '"',
                    "fields": [
                        "language"
                    ]
                }
            }
        )
    if result != "-":
        must_query.append(
            {
                "query_string": {
                    "query": result,
                    "fields": [
                        "result"
                    ]
                }
            }
        )

    query = {
        "_source": "*",
        "size": 50,
        "query": {
            "bool": {
                "must": must_query
            }
        }
    }
    res = es.search(index=index_name, body=query)

    contest_dict = getContestDict()
    problem_dict = getProblemDict()
    # print(problem_dict)
    res = list(map(lambda hit: hit['_source'], res['hits']['hits']))
    # res = sorted(res, key=lambda x: int(x["submission_id"]), reverse=True)
    for i in range(len(res)):
        res[i]['contest_name'] = contest_dict.get(res[i]['contest_id'], '')
        res[i]['problem_name'] = problem_dict.get(res[i]['problem_id'], '')
        res[i]['contest_url'] = "https://atcoder.jp/contests/" + res[i]['contest_id'] + "/tasks/" + res[i]["problem_id"]

    return res

