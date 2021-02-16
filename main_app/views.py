from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CreateNewRecord

from django.contrib.auth import login, authenticate, logout

from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Record
# Create your views here.
@login_required(login_url='loginPage')
def profilePage(request):
    records = Record.objects.filter(patient=request.user)
    return render(request, 'profile.html', {'records': records})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('profilePage')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginPage')
        else:
            messages.info(request, 'Введены неккоректные данные')
            return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profilePage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('profilePage')
        else:
            messages.info(request, 'Неверный логин или пароль')
            return render(request, 'login.html')


    return render(request, 'login.html')

@login_required(login_url='loginPage')
def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
def createPage(request):
    form = CreateNewRecord()

    if request.method == 'POST':
        form = CreateNewRecord(request.POST)
        if form.is_valid():
            ex_record = Record.objects.get(doctor=request.POST.get("doctor"), time=request.POST.get("time"))
            if ex_record:
                messages.info(request, 'Запись к данному доктору на указанное время уже существует.')
                return render(request, 'create.html', {'form': form})
            instance = form.save(commit=False)
            instance.patient = request.user
            instance.save()
            return redirect('profilePage')
        else:
            messages.info(request, 'Введены неккоректные данные')
            return render(request, 'create.html', {'form': form})

    return render(request, 'create.html', {'form': form})

def homePage(request):
    if request.user.is_authenticated:
        return redirect('profilePage')

    return render(request, 'home.html')
@csrf_exempt
def telegramAddRecord(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        doctor = request.POST.get('doctor')
        time = request.POST.get('time')
        myuser = User.objects.get(username=username)
        new_record = Record(patient=myuser, doctor=doctor, time=time)
        new_record.save()
        return HttpResponse('Succes!')
    return HttpResponse('<h1>Forbidden</h1>')
