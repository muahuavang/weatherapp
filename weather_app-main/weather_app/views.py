import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):

    API_KEY = "c4545cf5a2cab17458420bbce4b0ea95"
    current_location_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid={}"
    if request.method == "POST":
        city1 = request.POST['city1']

        weather_data1 = fetch_weather_and_forecast(city1, API_KEY, current_location_url, forecast_url)
        context = {
            "weather_data1": weather_data1
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")

def get_bg_class(description):
    desc = description.lower()
    if 'clear' in desc or 'sun' in desc:
        return 'sunny'
    elif 'cloud' in desc:
        return 'cloudy'
    elif 'rain' in desc or 'shower' in desc or 'drizzle' in desc:
        return 'rainy'
    elif 'snow' in desc:
        return 'snowy'
    elif 'thunder' in desc or 'storm' in desc:
        return 'stormy'
    else:
        return 'neutral'

def fetch_weather_and_forecast(city, api_key, current_location_url, forecast_url):
    # get response from api
    response = requests.get(current_location_url.format(city, api_key)).json()

    # Print the data into the console so you can see what data you are fetching from the API
    print('FETCH RESPONSE BELOW: ')
    print(response)

    # format so it can easily pass into template
    if 'main' in response and 'weather' in response:
        lat = response['coord']['lat']
        lon = response['coord']['lon']
        weather_data = {
            "city": city,
            "temperature": round(response['main']['temp']),
            "description": response['weather'][0]['description'],
            "icon": response['weather'][0]['icon'],
        }
        weather_data["bg_class"] = get_bg_class(weather_data["description"])
        print("BG CLASS for current weather:", weather_data["bg_class"])
        # Fetch forecast
        forecast_response = requests.get(forecast_url.format(city, api_key)).json()
        print('FORECAST RESPONSE BELOW: ')
        print(forecast_response)
        if 'list' in forecast_response:
            daily_forecasts = []
            current_date = None
            max_temp = float('-inf')
            description = ''
            icon = ''
            for item in forecast_response['list']:
                date_str = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date_str != current_date:
                    if current_date is not None:
                        daily_forecasts.append({
                            "date": current_date,
                            "temperature": round(max_temp),
                            "description": description,
                            "icon": icon,
                            "bg_class": get_bg_class(description),
                        })
                    current_date = date_str
                    max_temp = item['main']['temp_max']
                    description = item['weather'][0]['description']
                    icon = item['weather'][0]['icon']
                else:
                    max_temp = max(max_temp, item['main']['temp_max'])
            # add the last day
            if current_date is not None:
                daily_forecasts.append({
                    "date": current_date,
                    "temperature": round(max_temp),
                    "description": description,
                    "icon": icon,
                    "bg_class": get_bg_class(description),
                })
            weather_data["forecast"] = daily_forecasts[:7]  # up to 7 days
    else:
        weather_data = {
            "city": city,
            "temperature": "N/A",
            "description": "City not found. Please check spelling.",
            "icon": "",
            "forecast": [],
        }
        weather_data["bg_class"] = "neutral"

    return weather_data
