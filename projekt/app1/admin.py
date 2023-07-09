from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik, Predmeti, Upisi

# Register your models here.

admin.site.register(Korisnik)
admin.site.register(Predmeti)
admin.site.register(Upisi)