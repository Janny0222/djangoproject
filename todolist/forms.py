from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
  username = forms.CharField(label='Username', max_length=20)
  password = forms.CharField(label='Password', max_length=20)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Firstname', max_length=50)
    last_name = forms.CharField(label='Lastname', max_length=50)
    email = forms.EmailField(label='Email', max_length=50)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email"]

class AddTaskForm(forms.Form):
  task_name = forms.CharField(label="Task Name", max_length=50)
  description = forms.CharField(label="Description", max_length=200)

class UpdateTaskForm(forms.Form):
  task_name = forms.CharField(label='Task Name', max_length=50)
  description = forms.CharField(label="Description", max_length=200)
  status = forms.CharField(label='Status', max_length=50)

class AddEventForm(forms.Form):
  event_name = forms.CharField(label="Event Name", max_length=50)
  description = forms.CharField(label="Description", max_length=200)

class UpdateEventForm(forms.Form):
  event_name = forms.CharField(label='Event Name', max_length=50)
  description = forms.CharField(label="Description", max_length=200)
  status = forms.CharField(label='Status', max_length=50)
  event_date = forms.DateTimeField(label='Event Date', input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
