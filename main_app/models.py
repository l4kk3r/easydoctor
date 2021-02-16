from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    doctor_ops = [('Никифорова Елизавета Юрьевна', 'Никифорова Елизавета Юрьевна'), ('Анотьева Ирина Михайловна', 'Анотьева Ирина Михайловна') ]
    time_ops = [("18:00", "18:00"), ("19:00", "19:00"), ("20:00","20:00"),("21:00","21:00"),("22:00","22:00")]
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    doctor = models.CharField(max_length=200, choices=doctor_ops)
    time = models.CharField(max_length=200, choices=time_ops)


    def __str__(self):
        return self.doctor + ' на ' + self.time
