from flask import Flask, render_template, jsonify
from functools import lru_cache, wraps
from datetime import date, datetime, timedelta

import json
import config
import requests

# Create the flask application
app = Flask(__name__)
# Read the config from the ignored config file
api_key = config.api_key


# Code from stackoverflow that extends lru_cache (least recent used)
# to support timeout (in seconds)
def timed_lru_cache(seconds: int, maxsize: int = None):
    def wrapper_cache(func):
        #print('I will use lru_cache')
        func = lru_cache(maxsize=maxsize)(func)
        #print('I\'m setting func.lifetime')
        func.lifetime = timedelta(seconds=seconds)
        #print('I\'m setting func.expiration')
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            #print('Check func expiration')
            #print(f'datetime.utcnow(): {datetime.utcnow()}, func.expiration: {func.expiration}')
            if datetime.utcnow() >= func.expiration:
                #print('func.expiration lru_cache lifetime expired')
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache


# This code request the JSON from scopus and extracts the results
# It contains an cache to speedup the refresh (in seconds, by default 60)
@timed_lru_cache(seconds=60)
def get_scopus_pq_year(year:int)->int:
    # use f-string to create the url for that year
    url = f'https://api.elsevier.com/content/search/scopus?apiKey={api_key}&query=TITLE-ABS-KEY(privacy%20AND%20quantification%20AND%20NOT%20proceedings)&date={year}'
    #print(url)
    response = requests.get(url, headers={'Accept': 'application/json'})
    #print(f'Status code: {response.status_code}/{response.headers["content-type"]}')
    if response.status_code == 200:
        data_json = response.json()
        publication_per_year = data_json['search-results']['opensearch:totalResults']
        return publication_per_year
    else:
        return 0


# Rest method (GET) that call the get_scopus_pq_year method for all the years
@app.route('/getpq')
def get_scopus_pq():
    begin = 2008
    end = date.today().year
    years, publications = [], []
    for i in range(begin, end+1):
        years.append(i)
        publications.append(get_scopus_pq_year(i))
    return jsonify({'years':years, 'publications':publications})


# index.html
@app.route('/')
def guessPQ():
    return render_template ('index.html')
    

# Main method (it only starts the Flask app)
if __name__ == '__main__':
    app.run(debug=True)