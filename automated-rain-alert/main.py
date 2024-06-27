API_KEY = "0a92dcd7ad2ac7d446332a9d284ac8ea"
MY_LAT = 19.075983
MY_LONG = 72.877655
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

MY_EMAIL = "aanshuvishah@gmail.com"
MY_PASS = "bjzl uorj lywb ddrw"

import requests
import smtplib

params= {
    "lat" : MY_LAT,
    "lon" : MY_LONG,
    "appid" : API_KEY,
    "cnt": 4,
}
response = requests.get(API_ENDPOINT,params=params)
response.raise_for_status()
data = response.json()

will_rain = False
for i in data['list']:
    id = i['weather'][0]['id']
    if int(id) < 700:
        will_rain = True

if will_rain:
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Reminder!\n\n There's a rain alert today!Don't forget to have your umbrella on you."
            )