from django.db import models
from django.conf import settings


# Create your models here.

class Workout(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)  # Field name made lowercase.
    date = models.DateField(null=True)  # Field name made lowercase.
    duration = models.CharField(null=True, max_length=40)  # Field name made lowercase.


# many to one relationship
class Exercises(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    ex_name = models.CharField(max_length=40, default="N/A")


class ExSets(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    ex_weight = models.IntegerField(default=0)
    ex_reps = models.IntegerField(default=0)
