from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .forms import LoginForm

from django.urls import reverse 
from django.contrib.auth.models import User,auth

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # login(request, user)
                    # return HttpResponse('Authenticated '\
                    #                     'successfully')
                    context = {}
                    return render(request, 'attendence_system/home2.html', context)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'attendence_system/registration/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'attendence_system/dashboard.html',
                  {'section': 'dashboard'})
@login_required
def home(request):
    return render(request, 'attendence_system/home2.html', {'section': 'home'})



@login_required
def record_attn(request):
    return render(request, 'attendence_system/record_attendence.html', {'section': 'record_attn'})


@login_required
def attn_records(request):
    return render(request, 'attendence_system/attn_records.html', {'section': 'attn_records'})




def register_user(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect ("register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request,'EmailID already used')
                return redirect ("register.html")
            else:

                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save
                print('User created ')
                return redirect('/')
        else:
            messages.info(request,'Password Not Matching')
            return redirect ("register.html")
    else:
        return render(request, 'attendence_system/register.html',  {'section': 'register_user'})