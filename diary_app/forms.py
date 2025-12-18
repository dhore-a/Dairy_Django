from django import forms
from .models import DiaryEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content','mood']



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
