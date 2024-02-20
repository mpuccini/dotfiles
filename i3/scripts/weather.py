#!/usr/bin/env python
import requests
import json
import argparse
import sys
import logging

DEFAULT_LATITUDE='42.0885'
DEFAULT_LONGITUDE='12.2776'
OW_API_KEY='bcaeb260f55a8fed41aa8999320abcd5'
IS_API_KEY='980a3b71df94634c1aa87cc0798a1b64'

parser = argparse.ArgumentParser(description='Check weather data')
parser.add_argument('-l',
                    '--log',
                    dest='logLevel',
                    choices=['DEBUG','INFO','WARNING','ERROR'],
                    help='Log level',
                    default='INFO')
parser.add_argument('--latitude',                        
                    help='Specify latitude',
                    default=DEFAULT_LATITUDE)
parser.add_argument('--longitude',
                    help='Specify logitude',
                    default=DEFAULT_LONGITUDE)
parser.add_argument('--ow_api_key',
                    help='OpenWeatherMap api key',
                    default=OW_API_KEY)
parser.add_argument('--is_api_key',
                    help='IPStack api key',
                    default=IS_API_KEY)
args = parser.parse_args()

# Logging
level = logging.getLevelName(args.logLevel)
logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
log = logging.getLogger(__name__)



def get_coordinates():
    try:
        myip = requests.get('http://ip.42.pl/raw').text
        log.debug("My IP: ", myip)
    except Exception as e:
        log.error("Cannot retrieve local IP: ", e)
        sys.exit(1)

    payload = {'access_key': args.is_api_key}
    ipstack_url = 'http://api.ipstack.com/{}'.format(myip)
    try:
        r = requests.get(ipstack_url, params=payload)
        log.debug("URL: ", r.url)
        
    except Exception as e:
        log.error("Cannot fetch coordinates: ", e)
        sys.exit(2)
        
    j = json.loads(r.text)
    log.debug("IPStack response: %s" % (j))
    lat = str(j['latitude'])
    lon = str(j['longitude'])
    return (lat, lon)

def main():
    # This can be done directly with ArgumentParser too but I'm too lazy to
    # look up documentation...
    if not args.latitude or not args.longitude:
        log.info("Trying to find coordinates from IP...")
        lat, lon = get_coordinates()
    else:
        lat, lon = args.latitude, args.longitude
    
    payload = {
        'appid': args.ow_api_key,
        'lat': lat,
        'lon': lon,
    }
    log.debug("PAYLOAD: %s" % (payload))
        
    ow_url = 'https://api.openweathermap.org/data/2.5/weather'
    try:
        weather_data = requests.get(ow_url, params=payload).json()
        log.debug("Raw OpenWeather data: %s" % (weather_data))
    except Exception as e:
        log.error("Cannot get OpenWeather data: ", e)
    
    #image = requests.get('http://openweathermap.org/img/wn/'+weather_data['weather'][0]['icon']+'@2x.png')
    name = weather_data['name']
    descr = weather_data['weather'][0]['description']
    tc = round(weather_data['main']['temp'] - 272.15)
    tcf = round(weather_data['main']['feels_like'] - 272.15)
    p = round(weather_data['main']['pressure'])
    h = round(weather_data['main']['humidity'])
#    text=name+': '+descr+' / T: '+str(tc)+'°C h: '+str(h)+'%'
    text=descr+' / T: '+str(tc)+'°C / h: '+str(h)+'%'
    print(text)               

if __name__ == '__main__':
    main()

