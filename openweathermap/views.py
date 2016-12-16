import pyowm
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render_to_response
from django.utils import timezone
from geoip2.errors import AddressNotFoundError

from .models import City, Temperature, Weather


def create_models(geo_ip, client_ip):
    city = City()
    city.name = geo_ip.city(client_ip)['city']
    city.latitude = geo_ip.city(client_ip)['latitude']
    city.longitude = geo_ip.city(client_ip)['longitude']
    city.save()

    owm = pyowm.OWM('ff5760a13de6d84ac5de1c793de24c10')
    for day in owm.daily_forecast(city.name, 14).get_forecast().get_weathers():
        weather = Weather()
        weather.date = day.get_reference_time('date')
        weather.city = city
        weather.wind = day.get_wind()['speed']
        weather.clouds = day.get_clouds()
        weather.pressure = day.get_pressure()['press']
        weather.status = day.get_detailed_status()
        weather.save()

        temperature = Temperature()
        temperature.weather = weather
        temperature.day = day.get_temperature('celsius')['day']
        temperature.night = day.get_temperature('celsius')['night']
        temperature.max = day.get_temperature('celsius')['max']
        temperature.min = day.get_temperature('celsius')['min']
        temperature.save()
    return city


def fetch(request):
    geo_ip = GeoIP2()
    # client_ip = request.META.get('REMOTE_ADDR')
    client_ip = '77.47.236.2'
    try:
        city = City.objects.get(name=geo_ip.city(client_ip)['city'])
        if city.date_update.date() != timezone.now().date():
            city.delete()
            city = create_models(geo_ip, client_ip)
    except City.DoesNotExist:
        city = create_models(geo_ip, client_ip)
    except AddressNotFoundError:
        args = dict()
        args['error_message'] = 'Your address was not found'
        return render_to_response('openweathermap/index.htm', args)

    args = dict()
    args['city'] = city
    return render_to_response('openweathermap/index.htm', args)
