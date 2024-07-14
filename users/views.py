
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                else:
                    return redirect('doctor_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def patient_dashboard(request):
    if not request.user.is_authenticated or request.user.user_type != 'patient':
        return redirect('login')
    return render(request, 'users/patient_dashboard.html')

def doctor_dashboard(request):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return redirect('login')
    return render(request, 'users/doctor_dashboard.html')
    