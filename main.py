import requests
import datetime as dt
import smtplib

my_email = 'yor_email'
my_password = 'yor_password'

MY_LAT = 'enter_yor_latitude_float'
MY_LONG = 'enter_your_longitude_float'

response = requests.get('http://api.open-notify.org/iss-now.json')
data = response.json()
longitude = data['iss_position']['longitude']
latitude = data['iss_position']['latitude']

parameters = {
    'lat': MY_LAT,
    'lng': MY_LONG,
    'formatted': 0
}
response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
response.raise_for_status()

data = response.json()
sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

time_now = dt.datetime.now().hour


def is_overhead():
    lat_bool = False
    long_bool = False
    time = False

    for lat in range(int(MY_LAT) - 5, int(MY_LAT) + 5):
        if lat == int(float(latitude)):
            lat_bool = True
    for long in range(int(MY_LONG) - 5, int(MY_LONG) + 5):
        if long == int(float(longitude)):
            long_bool = True
    if time_now > sunset or time_now < sunrise:
        time = True
    if lat_bool and long_bool and time:
        return True
    else:
        return False


if is_overhead():
    with smtplib.SMTP('smtp.inbox.ru') as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs='enter_email',
                            msg='Subject: Look at the sky\n\nLook at the sky, ISS must be in sight')
else:
    print('ISS is not overhead')
