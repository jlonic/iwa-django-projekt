from django.shortcuts import render, redirect
from .forms import RegistrationForm, PredmetForm, UpisiForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Korisnik, Predmeti, Upisi
from django.views.decorators.csrf import requires_csrf_token
from django.urls import reverse

# Create your views here.

def register(request):
    if request.method=='GET':
        registrationForm=RegistrationForm()
        return render(request, 'registration.html', {'form': registrationForm})
    
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registration.html', {'form': form}) 

def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)

        if user.role=='ADMINISTRATOR':
            login(request, user)
            return redirect('admin_page')
        if user.role=='PROFESOR':
            login(request, user)
            return redirect('prof_page')
        else:
            login(request, user)
            return redirect('student_page')
    
    return render(request, 'login.html')

@login_required
def lista_studenata(request):
    studenti=Korisnik.objects.all()

    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    return render(request, 'lista_studenta.html', {'studenti': studenti})

@login_required
def lista_predmeta(request):
    predmeti=Predmeti.objects.all()

    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    return render(request, 'lista_predmeta.html', {'predmeti': predmeti})

@login_required
def dodaj_predmet(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    if request.method=='GET':
        form=PredmetForm()
        return render(request, 'dodaj_predmet.html', {'form': form})

    if request.method=='POST':
        form=PredmetForm()

        if form.is_valid():
            form.save()
            return redirect('lista_predmeta')

@login_required
def edit_predmet(request, predmet_id):
    predmet=Predmeti.objects.filter(id=predmet_id).first()

    if request.method=='GET':
        form=PredmetForm(instance=predmet)
        return render(request, 'edit_predmet.html', {'form': form})

    if request.method=='POST':
        form=PredmetForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            return redirect('lista_predmeta')

@login_required
def predmet(request, predmet_id):
    predmet=Predmeti.objects.filter(id=predmet_id)
    ime_studenta=Korisnik.objects.filter(upisi__predmet_id=predmet_id, role='STUDENT').distinct()
    broj_studenata=ime_studenta.count()

    return render(request, 'predmet.html', {'predmet': predmet, 'broj_studenata': broj_studenata, 'ime_studenta': ime_studenta})

@login_required
def delete_predmet(request, predmet_id):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    predmet=Predmeti.objects.get(id=predmet_id)
    predmet.delete()

    return redirect('lista_predmeta')

@requires_csrf_token
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_page(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    
    predmeti=Predmeti.objects.all()
    studenti=Korisnik.objects.filter(role='student')
    profesori=Korisnik.objects.filter(role='professor')

    return render(request, 'admin_page.html', {'predmeti':predmeti, 'studenti':studenti, 'profesori':profesori})


@login_required
def lista_profesora(request):
    profesori=Korisnik.objects.all()

    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    return render(request, 'lista_profesora.html', {'profesori': profesori})


@login_required
def dodaj_profesora(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')

    if request.method=='GET':
        registrationForm=RegistrationForm()
        registrationForm.fields.pop('status')
        registrationForm.initial['role']='PROFESOR'
        registrationForm.fields['role'].disabled=True
   
        return render(request, 'dodaj_profesora.html', {'form': registrationForm})
    
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        form.fields['status'].disabled=True
        form.fields['role'].disabled=True
        form.fields.pop('status')
        form.initial['role']='PROFESOR'
        
        if form.is_valid():
            user=form.cleaned_data['username']
            if Korisnik.objects.filter(username=user).exists():
                form.add_error('user', f'korisnik sa username {user} vec postoji')
                return render(request, 'dodaj_profesora.html', {'form': form})

            form.save()
            return redirect('lista_profesora')
        else:
            return render(request, 'dodaj_profesora.html', {'form': form}) 
        
@login_required
def dodaj_studenta(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    
    if request.method=='GET':
        registrationForm=RegistrationForm()
        registrationForm.initial['role']='STUDENT'
        registrationForm.fields['role'].disabled=True
        return render(request, 'dodaj_studenta.html', {'form': registrationForm})
    
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        form.initial['role']='STUDENT'
        form.fields['role'].disabled=True
        if form.is_valid():
            form.save()
            return redirect('lista_studenta')
        else:
            return render(request, 'dodaj_studenta.html', {'form': form}) 
        
@login_required
def edit_profesor(request, user_id):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    
    user=Korisnik.objects.filter(id=user_id).first()

    if request.method=='GET':
        form=RegistrationForm(instance=user)
        form.fields.pop('status')
        form.fields.pop('role')

        return render(request, 'edit_profesor.html', {'form': form})

    if request.method=='POST':
        form=RegistrationForm(request.POST, instance=user)
        form.fields['status'].disabled=True
        form.fields['role'].disabled=True
        form.fields.pop('status')
        form.fields.pop('role')
        if form.is_valid():
            form.save()
            return redirect('lista_profesora')
        else:
            return render(request, 'edit_profesor.html', {'form': form})
    
@login_required
def edit_student(request, user_id):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('login')
    
    user=Korisnik.objects.filter(id=user_id).first()

    if request.method=='GET':
        form=RegistrationForm(instance=user)
        return render(request, 'edit_student.html', {'form': form})

    if request.method=='POST':
        form=RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('lista_studenta')
        
@login_required
def student_page(request):
    if request.user.role != 'STUDENT':
        return redirect('login')
    
    predmeti=Predmeti.objects.all()
    studenti=Korisnik.objects.filter(role='student')
    profesori=Korisnik.objects.filter(role='professor')

    return render(request, 'student_page.html', {'predmeti':predmeti, 'studenti':studenti, 'profesori':profesori})

@login_required
def upisni_list(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('logout')
    predmeti=Predmeti.objects.all()
    if request.method=='GET':
        upisi=UpisiForm()
        upisi.initial['status']='UPISAN'
        upisi.fields['status'].disabled=True
        return render(request, 'upisni_list.html', {'form': upisi, 'predmeti': predmeti})
    
    if request.method=='POST':
        form=UpisiForm(request.POST)
        form.initial['status']='UPISAN'
        form.fields['status'].disabled=True
        if form.is_valid():
            student_id=form.cleaned_data['student_id']
            predmet_id=form.cleaned_data['predmet_id']
            if Upisi.objects.filter(student_id=student_id, predmet_id=predmet_id).exists():
                form.add_error('predmet_id', f'student je vec upisan na  predmet {predmet_id}')
                return render(request, 'upisni_list.html', {'form': form})
            
            form.save()
            return redirect('upisni_list')
        else:
            return render(request, 'upisni_list.html', {'form': form, 'predmeti': predmeti}) 


        
@login_required
def prof_page(request):
    if request.user.role !='PROFESOR':
        return redirect('logout')
    
    user=request.user
    predmeti=Predmeti.objects.filter(nositelj=user)

    if request.user.role != 'PROFESOR':
        return redirect('login')
    return render(request, 'prof_page.html', {'predmeti': predmeti})

@login_required
def studenti_na_predmetu(request, predmet_id):
    ime_studenta=Korisnik.objects.filter(upisi__predmet_id=predmet_id, role='STUDENT').exclude(upisi__status='POLOZEN').exclude(upisi__status='DOBIO POTPIS').exclude(upisi__status='IZGUBIO POTPIS').distinct()
    broj_studenata=ime_studenta.count()

    return render(request, 'studenti_na_predmetu.html', {'broj_studenata': broj_studenata, 'ime_studenta': ime_studenta, 'predmet_id': predmet_id})

@login_required
def upis_predmeta(request):
    if request.user.role != 'STUDENT':
        return redirect('logout')
    predmeti=Predmeti.objects.all()
    user=request.user
    if request.method=='GET':
        upisi=UpisiForm()
        upisi.initial['student_id']=user
        upisi.fields['student_id'].disabled=True
        upisi.initial['status']='UPISAN'
        upisi.fields.pop('status')
        upisi.fields['predmet_id'].queryset=Predmeti.objects.exclude(upisi__student_id=user)

        return render(request, 'upis_predmeta.html', {'form': upisi, 'predmeti':predmeti})
    
    if request.method=='POST':
        form=UpisiForm(request.POST)
        form.initial['student_id']=user
        form.fields['student_id'].disabled=True
        form.initial['status']='UPISAN'
        form.fields.pop('status')
        form.fields['predmet_id'].queryset=Predmeti.objects.exclude(upisi__student_id=user)

        if form.is_valid():
            form.save()
            return redirect('upis_predmeta')
        else:
            return render(request, 'upis_predmeta.html', {'form': form, 'predmeti':predmeti}) 

@login_required
def ispis_predmeta(request):
    if request.user.role != 'STUDENT':
        return redirect('logout')
    
    user=request.user
    if request.method=='GET':
        upisi=UpisiForm()
        upisi.initial['student_id']=user
        upisi.fields['student_id'].disabled=True
        upisi.initial['status']='UPISAN'
        upisi.fields.pop('status')
        upisi.fields['predmet_id'].queryset=Predmeti.objects.filter(upisi__student_id=user, upisi__status='UPISAN')

        return render(request, 'ispis_predmeta.html', {'form': upisi})
    
    if request.method=='POST':
        form=UpisiForm(request.POST)
        form.initial['student_id']=user
        form.fields['student_id'].disabled=True
        form.initial['status']='UPISAN'
        form.fields.pop('status')
        form.fields['predmet_id'].queryset=Predmeti.objects.filter(upisi__student_id=user, upisi__status='UPISAN')

        if form.is_valid():
            Upisi.objects.filter(student_id=user, predmet_id=form.cleaned_data['predmet_id']).delete()
            return redirect('ispis_predmeta')
        else:
            return render(request, 'ispis_predmeta.html', {'form': form}) 

@login_required
def promijeni_status(request, user_id, predmet_id):
    if request.user.role != 'PROFESOR':
        return redirect('logout')
    
    upisi=Upisi.objects.filter(student_id=user_id, predmet_id=predmet_id).first()
    if request.method=='GET':
        form=UpisiForm(instance=upisi)
        form.initial['student_id']=user_id
        form.fields['student_id'].disabled=True
        form.initial['predmet_id']=predmet_id
        form.fields['predmet_id'].disabled=True
        form.fields['status'].choices=[(choice[0], choice[1]) for choice in Upisi.STATUS if choice[0] != 'UPISAN']

        return render(request, 'promijeni_status.html', {'form': form})

    if request.method=='POST':
        form=UpisiForm(request.POST, instance=upisi)
        form.initial['student_id']=user_id
        form.fields['student_id'].disabled=True
        form.initial['predmet_id']=predmet_id
        form.fields['predmet_id'].disabled=True
        form.fields['status'].choices=[(choice[0], choice[1]) for choice in Upisi.STATUS if choice[0] != 'UPISAN']

        if form.is_valid():
            form.save()
            return redirect(reverse('promijeni_status', args=[user_id, predmet_id]))
        else:
            return render(request, 'promijeni_status.html', {'form': form})

@login_required
def izgubili_potpis(request, predmet_id):
    if request.user.role != 'PROFESOR':
        return redirect('logout')
    
    studenti=Korisnik.objects.filter(upisi__predmet_id=predmet_id, role='STUDENT', upisi__status='IZGUBIO POTPIS')
    broj_studenata=studenti.count()
    
    return render(request, 'izgubili_potpis.html', {'studenti': studenti, 'broj_studenata':broj_studenata, 'predmet_id':predmet_id}) 

@login_required
def dobili_potpis(request, predmet_id):
    if request.user.role != 'PROFESOR':
        return redirect('logout')
    
    studenti=Korisnik.objects.filter(upisi__predmet_id=predmet_id, role='STUDENT', upisi__status='DOBIO POTPIS')
    broj_studenata=studenti.count()

    return render(request, 'dobili_potpis.html', {'studenti': studenti, 'broj_studenata':broj_studenata, 'predmet_id':predmet_id}) 

@login_required
def polozili_predmet(request, predmet_id):
    if request.user.role != 'PROFESOR':
        return redirect('logout')
    
    studenti=Korisnik.objects.filter(upisi__predmet_id=predmet_id, role='STUDENT', upisi__status='POLOZEN')
    broj_studenata=studenti.count()

    return render(request, 'polozili_predmet.html', {'studenti': studenti, 'broj_studenata':broj_studenata, 'predmet_id':predmet_id}) 


@login_required
def ispis(request):
    if request.user.role != 'ADMINISTRATOR':
        return redirect('logout')
    
    if request.method=='GET':
        upisi=UpisiForm()
        upisi.fields.pop('status')
        return render(request, 'ispis.html', {'form': upisi})
    
    if request.method=='POST':
        form=UpisiForm(request.POST)
        form.fields.pop('status')
        if form.is_valid():
            student_id=form.cleaned_data['student_id']
            predmet_id=form.cleaned_data['predmet_id']
            Upisi.objects.filter(student_id=student_id, predmet_id=predmet_id).delete()
            return redirect('ispis')
        else:
            return render(request, 'ispis.html', {'form': form}) 