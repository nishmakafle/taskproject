from django_summernote.widgets import SummernoteWidget
from django import forms
from .models import *


class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Username...',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter the Password",
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter password again..."
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your First_Name'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Last_Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Email...'}))

    def clean_confirm_password(self):
        c_p = self.cleaned_data['confirm_password']
        p = self.cleaned_data['password']
        if c_p != p:
            raise forms.ValidationError("Your passwords didnot match.")
        return c_p

    def clean_username(self):
        uname = self.cleaned_data['username']
        if NewUser.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "User with this username already exists. Please choose different username. ")

        return uname


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username...',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password...'
    }))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description',
                  'assigned_to', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter  Task Title...'
            }),
            'description': SummernoteWidget(),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control select2-single',

            }),

            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
