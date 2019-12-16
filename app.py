from flask import Flask, render_template, request
import json
from functions import *

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    params = {}
    keys = ["keyword", "user_id", "language", "result"]
    for key in keys:
        params[key] = ""
    for key in keys:
        if not key in request.args:
            return render_template("index.html", params=params, data=[])
        params[key] = request.args.get(key)

    search_results = getSearchResults(params)
    return render_template("index.html", params=params, data=search_results)

if __name__ == "__main__":
    app.run(debug=True)