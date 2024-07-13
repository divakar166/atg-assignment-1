# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address_line1 = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    pincode = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'profile_picture', 'address_line1', 'city', 'state', 'pincode']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        
        if password != confirm_password:
            self.add_error('password2', "Passwords do not match")
