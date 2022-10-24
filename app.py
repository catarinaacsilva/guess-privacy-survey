from flask import Flask, render_template
import requests, json
import config


app = Flask(__name__)

api_key = config.api_key


@app.route('/')
def guessPQ():
    response_api = request.get('https://api.elsevier.com/content/search/scopus?apiKey='+api_key+'&query=TITLE-ABS-KEY(privacy%20AND%20quantification%20AND%20NOT%20proceedings)&date=2020')

    return render_template ("index.html", results=json.loads(response_api.text)['search-results']['opensearch:totalResults'])
    

