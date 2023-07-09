from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnik(AbstractUser):
    ROLES=(('ADMINISTRATOR','Administrator'), ('PROFESOR','Profesor'), ('STUDENT','Student'))
    STATUS=(('NONE','None'), ('REDOVNI', 'Redovni'), ('IZVANREDNI', 'Izvanredni'))
    role=models.CharField(max_length=13, choices=ROLES, default='STUDENT')
    status=models.CharField(max_length=20, choices=STATUS, default='NONE')

    def __str__(self):
        return self.username

class Predmeti(models.Model):
    ime=models.CharField(max_length=100)
    kod=models.CharField(max_length=10)
    program=models.CharField(max_length=50)
    bodovi=models.IntegerField(null=False)
    sem_red=models.IntegerField(null=False)
    sem_izv=models.IntegerField(null=False)
    IZBORNI=(('DA', 'da'), ('NE', 'ne'))
    izborni=models.CharField(max_length=50, choices=IZBORNI)

    nositelj=models.ForeignKey(Korisnik, on_delete=models.CASCADE,  limit_choices_to={'role': 'PROFESOR'}, null=True)

    def __str__(self):
        return self.ime

class Upisi(models.Model):
    STATUS = (('UPISAN', 'Upisan'), ('POLOZEN', 'Polozen'), ('IZGUBIO POTPIS', 'Izgubio Potpis'), ('DOBIO POTPIS', 'Dobio Potpis'))
    student_id=models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet_id=models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status=models.CharField(max_length=64, choices=STATUS, default='UPISAN', null=True)

    def __str__(self):
        return self.status