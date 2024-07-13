# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    # Use Django's built-in authentication views or define your own
    pass

def patient_dashboard(request):
    return render(request, 'users/patient_dashboard.html')

def doctor_dashboard(request):
    return render(request, 'users/doctor_dashboard.html')
