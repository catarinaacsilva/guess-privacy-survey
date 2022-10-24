from flask import Flask, render_template
import urllib.request, json


app = Flask(__name__)

@app.route('/')
def guessPQ():
    url = 'https://api.elsevier.com/content/search/scopus?apiKey=APIKEY&query=TITLE-ABS-KEY(privacy%20AND%20quantification%20AND%20NOT%20proceedings)&date=2020'
    
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    results = dict['search-results']['opensearch:totalResults'] 

    print(results)

    return render_template ("index.html", results)
    

