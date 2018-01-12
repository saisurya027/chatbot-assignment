#!/usr/bin/python3
import os
import aiml
import requests
import webbrowser


def find_in_list(str_list, text):
    fg = False
    for i in str_list:
        if i == text:
            fg = True

    return fg


api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=281953b3dd825c1de437f6bbb6ecd2eb&q='
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
        print('Selected city : '+ city + '\nlat : '+ str(json_data['coord']['lat']) + '\t,lon : '+ str(json_data['coord']['lon']) )
        print('Weather : '+json_data['weather'][0]['main'])
        print('Temperature :'+str(json_data['main']['temp']))

    # Search google with your own query:
    elif find_in_list(input_list, 'google'):
        address = input('Enter the query >>')
        new_address = google_addres+address
        print('Opening Browser....')
        webbrowser.open(new_address)

    # Print aiml responses from the (aiml)database:
    else:
        response = k.respond(input_text)
        print(response)

