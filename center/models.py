from django.db import models


class Center(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address
