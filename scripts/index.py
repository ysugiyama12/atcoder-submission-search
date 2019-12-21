import os, sys
import json
import urllib.request
import requests
from html.parser import HTMLParser
from elasticsearch import Elasticsearch
from tqdm import tqdm

es = Elasticsearch()

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = False
        self.link = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # print(tag, attrs)
        if tag == "pre":
            self.data.append({})
            self.title = True
            self.link = True

        if tag == "a" and self.link == True:
            self.data[-1].update({"link": attrs["href"]})

    def handle_data(self, data):
        if self.title == True or self.link == True:
            self.data[-1].update({"title": data})
            self.title = False
            self.link = False

def getSubmissionCode(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        return body



if __name__ == "__main__":
    user_name = "yuji9511"
    url_api = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + user_name
    # print(url_api)
    res = requests.get(url_api)
    data = json.loads(res.text)
    # print(data)
    for i, d in tqdm(enumerate(data)):
        sub_id = d["id"]
        contest_id = d["contest_id"]
        url = "https://atcoder.jp/contests/" + str(contest_id) + "/submissions/" + str(sub_id)
        res = getSubmissionCode(url)
        res = str(res)
        parser = Parser()
        parser.feed(res)
        parser.close()
        code = ""
        for i in parser.data:
            code = i['title'].replace("\\r\\n", "\n").replace("\\t", "    ")
            break
        body = {
            "user_id": user_name,
            "url": url,
            "code": code,
            "submission_id": str(sub_id),
            "contest_id": str(contest_id),
            "language": d["language"],
            "result": d["result"],
            "problem_id": d["problem_id"],
            "point": d["point"]
        }
        es.index(index="atcoder_submissions", body=body)