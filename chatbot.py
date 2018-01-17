#!/usr/bin/python3
import os
import aiml
import requests
import webbrowser
import datetime
import pytz
import time


def find_city(query):
    for country, cities in pytz.country_timezones.items():
        for city in cities:
            if query in city:
                return pytz.timezone(city)


def find_in_list(str_list, text):
    fg = False
    for i in str_list:
        if i == text:
            fg = True

    return fg


YOUR_API_KEY = 'b7f7a4ec-9595-4a1f-99bb-caea829255bc'
api_key = 'AIzaSyBFy-RvfpeDtXo-wVqNZSEbDrLHXo4dAFM'
api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=281953b3dd825c1de437f6bbb6ecd2eb&q= '
google_addres = 'http://google.com/#q='
BRAIN_FILE = "brain.dump"

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

# Endless loop which passes the input to the bot and prints


while True:
    input_text = input(">> ").lower()
    textin = input_text.lower()
    input_list = textin.split()
    # Getting information from the weather api:
    if find_in_list(input_list, 'weather'):
        city = input('Enter the city >> ')
        new_url = api_address + city
        json_data = requests.get(new_url).json()
        # Parsing the Json Object:
        print('Selected city : ' + city + '\nlat : ' + str(json_data['coord']['lat']) + '\t,lon : ' + str(
            json_data['coord']['lon']))
        print('Weather : ' + json_data['weather'][0]['main'])
        print('Temperature : {:3}'.format(str(json_data['main']['temp'] - 273.15)))
    # time and location:
    elif find_in_list(input_list, 'time') or find_in_list(input_list, 'location'):
        city = input('Enter the city >>')
        new_url = api_address + city
        json_data = requests.get(new_url).json()
        # Parsing the Json Object:
        print('Selected city : ' + city)
        lat = json_data['coord']['lat']
        lng = json_data['coord']['lon']
        print('lat:' + str(lat) + '\tlon:' + str(lng))
        latitude = lat
        longitude = lng
        timestamp = time.time()

        api_response = requests.get(
            'https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key={3}'.format(latitude,
                                                                                                               longitude,
                                                                                                               timestamp,
                                                                                                               api_key))
        api_response_dict = api_response.json()

        if api_response_dict['status'] == 'OK':
            timezone_id = api_response_dict['timeZoneId']
        print('Time zone of the city ' + city + ' is: ' + str(timezone_id))
        print(datetime.datetime.now(tz=pytz.timezone(timezone_id)))

    elif find_in_list(input_list, 'news'):
        try:
            condition = int(input('Select (1) for top headlines or (2) for specific topic >> '))
        except NameError:
            print('Please Enter an integer')
        print('Fetching News....')
        if condition == 1:
            url = ('https://newsapi.org/v2/top-headlines?'
                   'sources=google-news-in&'
                   'apiKey=ad0edb02ef534eab82b20992698a9a71')
            json_news_data = requests.get(url).json()
            for i in range(1, 6):
                print(str(i) + ':')
                print('Source : ' + json_news_data['articles'][i]['source']['name'])
                print('Author : ' + str(json_news_data['articles'][i]['author']))
                print('Title : ' + str(json_news_data['articles'][i]['title']))
                print('Description : ' + str(json_news_data['articles'][i]['description']))
                print('url : ' + json_news_data['articles'][i]['url'])
                print()
                print()
        elif condition == 2:
            topic = input('Enter the topic >>')
            url = ('https://newsapi.org/v2/everything?'
                   'q=' + topic + '&'
                                  'from=2018-01-16&'
                                  'sortBy=popularity&'
                                  'apiKey=ad0edb02ef534eab82b20992698a9a71')
            json_news_data = requests.get(url).json()
            for i in range(1, 6):
                print(str(i) + ':')
                print('Source : ' + json_news_data['articles'][i]['source']['name'])
                print('Author : ' + str(json_news_data['articles'][i]['author']))
                print('Title : ' + str(json_news_data['articles'][i]['title']))
                print('Description : ' + str(json_news_data['articles'][i]['description']))
                print('url : ' + json_news_data['articles'][i]['url'])
                print()
                print()

    # Search google with your own query:
    elif find_in_list(input_list, 'google'):
        address = input('Enter the query >>')
        new_address = google_addres + address
        print('Opening Browser....')
        webbrowser.open(new_address)

    # Print aiml responses from the (aiml)database:
    else:
        response = k.respond(input_text)
        print(response)
