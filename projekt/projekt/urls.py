"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('lista_studenta/', views.lista_studenata, name='lista_studenta'),
    path('lista_predmeta/', views.lista_predmeta, name='lista_predmeta'),
    path('dodaj_predmet/', views.dodaj_predmet, name='dodaj_predmet'),
    path('edit_predmet/<int:predmet_id>', views.edit_predmet, name='edit_predmet'),
    path('predmet/<int:predmet_id>', views.predmet, name='predmet'),
    path('delete_predmet/<int:predmet_id>', views.delete_predmet, name='delete_predmet'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('lista_profesora/', views.lista_profesora, name='lista_profesora'),
    path('dodaj_profesora', views.dodaj_profesora, name='dodaj_profesora'),
    path('dodaj_studenta', views.dodaj_studenta, name='dodaj_studenta'),
    path('edit_profesor/<int:user_id>', views.edit_profesor, name='edit_profesor'),
    path('edit_student/<int:user_id>', views.edit_student, name='edit_student'),
    path('prof_page/', views.prof_page, name='prof_page'),
    path('student_page/', views.student_page, name='student_page'),
    path('upisni_list/', views.upisni_list, name='upisni_list'),
    path('studenti_na_predmetu/<int:predmet_id>', views.studenti_na_predmetu, name='studenti_na_predmetu'),
    path('upis_predmeta', views.upis_predmeta, name='upis_predmeta'),
    path('ispis_predmeta', views.ispis_predmeta, name='ispis_predmeta'),
    path('promijeni_status/<int:user_id>/<int:predmet_id>/', views.promijeni_status, name='promijeni_status'),
    path('izgubili_potpis/<int:predmet_id>', views.izgubili_potpis, name='izgubili_potpis'),
    path('dobili_potpis/<int:predmet_id>', views.dobili_potpis, name='dobili_potpis'),
    path('polozili_predmet/<int:predmet_id>', views.polozili_predmet, name='polozili_predmet'),
    path('ispis', views.ispis, name='ispis'),
]
