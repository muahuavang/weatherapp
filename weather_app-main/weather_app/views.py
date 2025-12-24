import datetime

import requests
from django.shortcuts import render

# Create your views here.
def index(request):

    API_KEY = "c4545cf5a2cab17458420bbce4b0ea95"
    current_location_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']

        weather_data1 = fetch_weather_and_forecast(city1, API_KEY, current_location_url)
        context = {
            "weather_data1": weather_data1
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")



def fetch_weather_and_forecast(city, api_key, current_location_url):
    # get response from api
    response = requests.get(current_location_url.format(city, api_key)).json()

    # Print the data into the console so you can see what data you are fetching from the API
    print('FETCH RESPONSE BELOW: ')
    print(response)

    # format so it can easily pass into template
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp']),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
    }


    return weather_data
