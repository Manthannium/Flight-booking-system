from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class seat(models.Model):
    seat_number = models.IntegerField()
    person_name = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False)

