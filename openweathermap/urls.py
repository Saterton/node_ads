from django.conf.urls import url
from . import views

app_name = 'openweathermap'

urlpatterns = [
    url(r'^$', views.fetch, name='fetch'),
]
