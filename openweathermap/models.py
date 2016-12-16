from django.db import models


class City(models.Model):
    name = models.CharField(verbose_name='Город', max_length=60)
    latitude = models.FloatField(verbose_name='Ширина')
    longitude = models.FloatField(verbose_name='Долгота')
    date_update = models.DateTimeField(verbose_name='Дата обноления', auto_now_add=True)

    def __str__(self):
        return self.name


class Weather(models.Model):
    date = models.DateTimeField(verbose_name='Дата')
    city = models.ForeignKey(City, related_name='weathers', on_delete=models.CASCADE)
    wind = models.FloatField(verbose_name='Ветер')
    clouds = models.IntegerField(verbose_name='Облачность')
    pressure = models.FloatField(verbose_name='Давление')
    status = models.CharField(verbose_name='Описание', max_length=60)


class Temperature(models.Model):
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)
    max = models.FloatField(verbose_name='Максимум')
    min = models.FloatField(verbose_name='Минимум')
    day = models.FloatField(verbose_name='Днем')
    night = models.FloatField(verbose_name='Ночью')