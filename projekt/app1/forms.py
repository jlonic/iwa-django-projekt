from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Korisnik, Predmeti, Upisi

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(max_length=50)
    class Meta:
        model=Korisnik
        fields=("username", "email", 'role', 'status', "password1", "password2")
        
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            user=Korisnik.objects.exclude(pk=self.instance.pk).get(username=username)
            raise forms.ValidationError('Korisnicko ime vec postoji')
        except Korisnik.DoesNotExist:
            return username

class PredmetForm(ModelForm):
    class Meta:
        model=Predmeti
        fields=('ime', 'kod', 'program', 'bodovi', 'sem_red', 'sem_izv', 'izborni', "nositelj")

class UpisiForm(ModelForm):
    student_id=forms.ModelChoiceField(queryset=Korisnik.objects.filter(role='STUDENT'))
    class Meta:
        model=Upisi
        fields=('student_id', 'predmet_id', 'status')