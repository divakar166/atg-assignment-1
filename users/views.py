
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from .models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'patient':
            return render(request,'patient_dashboard.html')
        elif request.user.user_type == 'doctor':
            return render(request,'doctor_dashboard.html')
    else:
        return redirect('login')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST['address']
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST['user_type']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email is already registered.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username is already taken.'})
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=make_password(password),
            address=address,
            profile_picture=profile_picture,
            user_type=user_type
        )
        user.save()
        return JsonResponse({'success': True})
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'User does not exist!'})
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Incorrect password!'})
    
    return render(request, 'login.html')

def patient_dashboard(request):
    if not request.user.is_authenticated or request.user.user_type != 'patient':
        return redirect('login')
    return render(request, 'users/patient_dashboard.html')

def doctor_dashboard(request):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return redirect('login')
    return render(request, 'users/doctor_dashboard.html')
    
def logout_view(request):
    logout(request)
    return redirect('index')