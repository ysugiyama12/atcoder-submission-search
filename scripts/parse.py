import os, sys
import json
import urllib.request
import requests
from html.parser import HTMLParser
from elasticsearch import Elasticsearch
from tqdm import tqdm

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = False
        self.link = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "option":
            print(tag, attrs)
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

if __name__ == "__main__":
    url = "https://atcoder.jp/contests/soundhound2018-summer-qual/submissions?f.Task=&f.Language=3515&f.Status=WA&f.User="
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        res = str(body)
    # print(res)
    parser = Parser()
    parser.feed(res)
    parser.close()
    for i in parser.data:
        code = i
        # print(code)
        break