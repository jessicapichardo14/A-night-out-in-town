from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_cors import CORS, cross_origin
from datetime import *
from pygeocoder import Geocoder
from http import HTTPStatus
import dateutil
from dateutil.parser import * 
from dateutil import parser
from datetime import time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, WEEKLY, WE

import time
import json
import requests
import pprint
import logging
import dateutil.parser as dp


app = Flask(__name__)


API_KEY = "Ymvf2vactJxI0QqPrfDQVYhCltRDY-X2RXNEWzurP0r0LPVRsV3K5ThLjU3RoQ271s1OlxWi5MS0YBMrZFd2AWUyPGvfMAP7h3YbxR4-yzU6lUDeIMNL-0SDnU5cXnYx"

GOOGLEMAPS_KEY = "AIzaSyBaBEuO5StvYGx8lAUV2FAETrDEwALewr4"

# Initialize the extension
# GoogleMaps(app)

# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyBaBEuO5StvYGx8lAUV2FAETrDEwALewr4")


def map_generator(response):
    list_events = []
    for event in response['events']:
        e = {}
        e['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        e['lat'] = event['latitude']
        e['lng'] = event['longitude']
        e['infobox'] = "<p><strong>" + event['name'] + "</strong></p><p>People interested: " + \
            str(event['interested_count']) + "</p><p>Event start time: " + \
            str(dateutil.parser.isoparse(event['time_start'])) + "</p>"

        list_events.append(e)
    return list_events


def checkbox():
    if request.method == 'GET':
        check = request.args.get('is_free')
        print(check)
    return 'true' if check else 'false'


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


# Register the template filter with the Jinja Environment
app.jinja_env.filters['formatdatetime'] = format_datetime


@app.route("/", methods=['GET', 'POST', 'OPTIONS'])
def index():
    return render_template("index.html")


@app.route("/search", methods=['GET', 'POST', 'OPTIONS'])
def search():
    event = "https://cors-anywhere.herokuapp.com/https://api.yelp.com/v3/events"
    headers = {'Authorization': 'Bearer %s' % API_KEY,
               'X-Requested-With': 'XMLHttpRequest'}
    params = {'limit': 9,
              'sort_on': 'popularity',
              'radius': 5000,
              'location': request.args.get('location'),
              'categories': request.args.get('categories'),
              'is_free': checkbox()
              }
    response = requests.get(event, params=params, headers=headers)
    event_response = response.json()
    coord = Geocoder(GOOGLEMAPS_KEY).geocode(request.args.get('location'))
    lat = coord.coordinates[0]
    lng = coord.coordinates[1]

    # this is the map
    sndmap = Map(
        identifier="sndmap",
        zoom=12,
        lat=lat,
        lng=lng,
        markers=map_generator(event_response),
        style="height:350px; width:100%; margin:0;",
    )

    return render_template('search.html', event_response=event_response['events'], sndmap=sndmap)
    pprint.pprint(response)


if __name__ == "__main__":
    app.run(debug=True)
