from flask import Flask, request, render_template, make_response
import feedparser
import json
import requests
#import urllib2
import urllib
import urllib.parse
import datetime

app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
                'cnn':'http://rss.cnn.com/rss/edition.rss',
                'fox':'http://feeds.foxnews.com/foxnews/latest',
                'iol':'http://www.iol.co.za/cmlink/1.640',
                'vanguard':'https://investornews.vanguard/feed/rss',}

def get_rate(frm, to):
    exc_url = 'https://openexchangerates.org/api/latest.json?app_id=f10174cc4cea4065979cf6e922dec3a4'
    all_currency = urllib.request.urlopen(exc_url).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate,parsed.keys())


 
@app.route("/")
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    city_name = request.args.get('city')
    if not city_name:
        city = 'Lagos'
    else:
        city = city_name 
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = 'USD'
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = 'NGN'
    rate,currencies = get_rate(currency_from, currency_to)
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=f36c595fc022f460067bb28e64378d75'
    exc_url = 'https://openexchangerates.org/api/latest.json?app_id=f10174cc4cea4065979cf6e922dec3a4'
    source = requests.get(api_url)
    # converting JSON data to a dictionary 
    x = source.json()
    y =x['main']
    z = x['weather']
    weather = {'description':z[0]['description'],
                    'temperature':y['temp'],
                    'city':x['name'],'country':x['sys']['country']}

    return render_template('newspage.html',articles=feed['entries'],a = weather['description'],
                            b=weather['temperature'],c=weather['city'],d=weather['country'],
                            currency_from=currency_from,currency_to=currency_to,rate=rate,currencies=sorted(currencies),publication=publication.upper())
    


if __name__ == '__main__':
    app.run(debug=True)