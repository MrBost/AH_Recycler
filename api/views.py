#from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.utils import get_lnglat, send_sms
from subscriber.models import Subscriber, Dropoff
from center.models import Center


def users(request):
    phone = request.GET.get('number')
    score = Dropoff.objects.filter(subscriber__phone=phone).count() * 10
    return JsonResponse({'score': score})


@csrf_exempt
def ussd(request):
    print(request.POST)
    txt = request.POST['text']
    print(txt)
    if not txt:
        return HttpResponse('CON Please enter 1 for list of centers and 2 for dropoff')
    else:
        parts = txt.split('*')
        tag = parts[0].strip()
        if len(parts) == 1:
            body = ''
        else:  # extra info
            body = '*'.join(parts[1:])

        if tag == '1':
            return centers(body, request.POST)
        else:
            return dropoff(body, request.POST)

        # find if 1 or 2 then return response

    if len(txt.split('*')) == 1:
        return HttpResponse('CON send your address')
    return HttpResponse('END thanks')


#@csrf_exempt
def dropoff(txt, extra):
    #print(request.POST)
    #txt = request.POST['text']
    # phone = request.POST['phoneNumber']
    parts = txt.split('*')
    if not txt:
        return HttpResponse('CON Please enter the phone number')
    elif len(parts) == 1:
        phone = parts[0]
        try:
            client = Subscriber.objects.get(phone=phone)
        except Subscriber.DoesNotExist:
            client = Subscriber.objects.create(phone=phone)
        return HttpResponse(
            'CON Please enter the data in format NUMBOTTLES,NUMBAGS')
    else:
        phone = parts[0]
        num_bottles = parts[1].split(',')[0]
        num_bags = parts[1].split(',')[1]
        client = Subscriber.objects.get(phone=phone)
        Dropoff.objects.create(
            subscriber=client,
            num_bottles=num_bottles,
            num_bags=num_bags)
        score = Dropoff.objects.filter(subscriber=client).count() * 10
        msg = 'Number of points for {} is {}'.format(phone, score)
        return HttpResponse('END Thank you. ' + msg)


@csrf_exempt
def centers(txt, extra):
    #print(request.POST)
    #txt = request.POST['text']
    #phone = request.POST['phoneNumber']
    phone = extra['phoneNumber'][1:]
    if not txt:
        return HttpResponse('CON Please enter your address')
    else:
        #address = request.POST['text']
        address = txt
        locations = get_center_locations(address)
        msg = '\n'.join([loc['address'] for loc in locations])
        #msg = 'Testing again'
        send_sms(msg, phone)
        return HttpResponse('END Thank you, we will send the nearby collection centers by SMS')
    #return HttpResponse('END Thanks')
    #return JsonResponse({'status': 'ok'})


def get_points(request):
    return JsonResponse({'points': 50})


def get_center_locations(address):
    return [
        {
            'address': item.address,
            'lat': item.latitude,
            'lng': item.longitude
        }
        for item in Center.objects.all()[:3]
    ]
    #return [
    #    {
    #        'address': '10, Ademola St',
    #        'lng': 3.567,
    #        'lat': 6.567
    #    },
    #    {
    #        'address': '10, Ademola St',
    #        'lng': 3.567,
    #        'lat': 6.567
    #    },
    #    {
    #        'address': '10, Ademola St',
    #        'lng': 3.567,
    #        'lat': 6.567
    #     }
    #]


def get_locations(request):
    address = request.GET.get('address')
    lng_lat = get_lnglat(address)
    print(address)
    centers = get_center_locations(address)
    return JsonResponse(
        {
            'location': lng_lat,
            'centers': centers
        }
    )
