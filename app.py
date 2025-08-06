import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('CWB_API_KEY')
API_URL = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001'

app = Flask(__name__)

LOCATIONS = [
    '台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市'
]


def fetch_weather(location):
    params = {
        'Authorization': API_KEY,
        'locationName': location
    }
    res = requests.get(API_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    loc = data['records']['location'][0]
    elements = {
        e['elementName']: e['time'][0]['parameter']['parameterName']
        for e in loc['weatherElement']
    }
    temperature = (int(elements['MinT']) + int(elements['MaxT'])) / 2
    return {
        'location': loc['locationName'],
        'temperature': temperature,
        'description': elements['Wx'],
        'rain_probability': elements['PoP']
    }


@app.route('/')
def index():
    return render_template('index.html', locations=LOCATIONS)


@app.route('/api/weather')
def api_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Missing location'}), 400
    try:
        weather = fetch_weather(location)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    return jsonify(weather)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
