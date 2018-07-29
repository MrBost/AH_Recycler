import requests


API_KEY = 'AIzaSyCWrd7FMPcVDiwimjq1AG0dhLebVJkR82M'
URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}'


def get_lnglat(address):
    url = URL.format(address, API_KEY)
    response = requests.get(url).json()
    return response['candidates'][0]['geometry']['location']


def send_sms(message, to):
    #url = 'https://api.africastalking.com/restless/send?username=sandbox&Apikey=b392025f61fe88685ec38c5feaea3e405caa2d50404abe75aa36cc00d5d0f40e&to={}&message={}'.format(to, message)
    url = 'https://api.africastalking.com/version1/messaging'
    headers = {'APIKey': '12ae26784e565fa9f368b286346a479a97f25dbcb4ef0e710ec9b560b17c9315'}
    params = {'username': 'cloud', 'to': to, 'message': message, 'from': 'Cloud'}
    print(url)
    requests.post(url, data=params, headers=headers)
