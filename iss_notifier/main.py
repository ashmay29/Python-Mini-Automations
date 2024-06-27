import requests
import smtplib
from datetime import datetime as dt

MY_LAT = 19.075983
MY_LONG = 72.877655

MY_EMAIL = " "
MY_PASS = " "

def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if MY_LAT-5 <=iss_latitude<= MY_LAT+5 and MY_LONG-5 <=iss_longitude<= MY_LONG+5:
        return True
    
def is_night():
    parameters = {
        "lat":MY_LAT,
        "lng":MY_LONG,
        "formatted":0,
    }

    response = requests.get('https://api.sunrise-sunset.org/json',params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    time_now = dt.now().hour()
    if time_now>= sunset or time_now<= sunrise:
        return True
    
if is_iss_overhead and is_night:
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look above you!\n\n The ISS Satellite is above you!"
            )