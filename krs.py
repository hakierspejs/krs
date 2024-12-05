# a flask hello world

import pathlib
import datetime
import sys

import lxml.html
import requests

from flask import Flask, redirect
app = Flask(__name__)

KRS_URL = 'https://krs-pobierz.pl/stowarzyszenie-hakierspejs-lodz-i7113260'

def get_time_since_caching():
    cache_file = pathlib.Path('cache.txt')
    # if mtime is younger than 10 minutes, return hello world
    ts = datetime.datetime.fromtimestamp(cache_file.stat().st_mtime)
    elapsed = (datetime.datetime.now() - ts)
    return cache_file, elapsed


def get_krs_last_updated():

    # if cache file is younger than 1 minute, return cached information
    # about when the KRS was last updated, so that we don't have stress
    # the KRS website too much
    cache_file, elapsed = get_time_since_caching()
    if cache_file.exists() and elapsed.seconds < 3600:
        sys.stderr.write(f'{elapsed=}, reusing cache\n')
        with cache_file.open() as f:
            return f.read()

    # otherwise, fetch the KRS website and cache the information
    r = requests.get(KRS_URL)
    h = lxml.html.fromstring(r.text)
    last_updated = h.xpath('//div [@class="lastDownloaded"]/p[2]/text()')[0]

    # store the last_updated information in a cache file
    with cache_file.open('w') as f:
        f.write(last_updated)

    return last_updated


@app.route('/')
def serve_krs():
    last_updated = get_krs_last_updated()
    if last_updated != '2024-08-07 05:19:56':
        # redirect to KRS URL
        return redirect(KRS_URL)

    with open('krs.html') as f:
        krs_cached = f.read()

    return krs_cached



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
