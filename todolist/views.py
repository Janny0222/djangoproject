from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
# import User from Django
from django.contrib.auth.models import User
# import authenticate form from Django for authentication
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Local imports
from .models import ToDoItem, EventsItem
from .forms import LoginForm, AddTaskForm, UpdateTaskForm, RegisterForm, AddEventForm, UpdateEventForm, ChangePasswordForm

# Create your views here.
def index(request):
  todoitem_list = ToDoItem.objects.filter(user_id=request.user.id)
  eventitem_list = EventsItem.objects.filter(user_id=request.user.id)
  context = {
    "todoitem_list": todoitem_list,
    "eventitem_list": eventitem_list,
    "user": request.user
    }
  print(eventitem_list)
  return render(request, "todolist/index.html", context)

def todoitem(request, todoitem_id):
  # retreives the item objects using the id or primary key
  todoitem = get_object_or_404(ToDoItem, pk=todoitem_id)
  # response = "You are viewing the details of %s"
  return render(request, "todolist/todoitem.html", model_to_dict(todoitem))

def eventitem(request, eventitem_id):
  # retreives the item objects using the id or primary key
  eventitem = get_object_or_404(EventsItem, pk=eventitem_id)
  # response = "You are viewing the details of %s"
  return render(request, "todolist/eventitem.html", model_to_dict(eventitem))

def register(request):
    context = {}

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            context['registration_success'] = True
        else:
            context['error'] = True

    else:
        form = RegisterForm()

    context['form'] = form
    return render(request, "todolist/register.html", context)


@login_required
def change_password(request):
    is_password_changed = False

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            is_password_changed = True
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'is_password_changed': is_password_changed,
        'user': request.user,
    }

    return render(request, "todolist/change_password.html", context)

def login_view(request):
    # username = "johndoe"
    # password = "johndoe1"

    # user = authenticate(username=username, password=password)

    context = {}

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        if form.is_valid() == False:
            # Returns a blank login form
            form = LoginForm()
        else:
            # Retrieves the information from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            context = {
                "username": username,
                "password": password
            }

        if user is not None:
            # Saves the user's ID in the session using Django's Session framework
            login(request, user)
            return redirect("todolist:index")
        else:
            # Provides context with error to conditionally render the error message
            context = {
                "error": True
            }

    return render(request, "todolist/login.html", context)


def logout_view(request):
    # Removes the saved data in session upon login
    logout(request)
    return redirect("todolist:index")

def add_task(request):
    context = {}

    if request.method == 'POST':
        form = AddTaskForm(request.POST)

        if form.is_valid() == False:
            form = AddTaskForm()
        else:
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']

            # Checks the database if a task already exists
            duplicates = ToDoItem.objects.filter(task_name=task_name)

            if not duplicates:
                ToDoItem.objects.create(task_name=task_name, description=description, date_created=timezone.now(), user_id=request.user.id)
            else:
                context = {"error": True}

    return render(request, "todolist/add_task.html", context)


def update_task(request, todoitem_id):
    todoitem = ToDoItem.objects.filter(pk=todoitem_id)
    context = {
        "user": request.user,
        "todoitem_id": todoitem_id,
        "task_name": todoitem[0].task_name,
        "description": todoitem[0].description,
        "status": todoitem[0].status
    }

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST)

        if form.is_valid() == False:
            form = UpdateTaskForm()
        else:
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if todoitem:
                todoitem[0].task_name = task_name
                todoitem[0].description = description
                todoitem[0].status = status

                todoitem[0].save()
                return redirect("todolist:index")
            else:
                context = {
                    "error": True
                }

    return render(request, "todolist/update_task.html", context)

def delete_task(request, todoitem_id):
    todoitem = ToDoItem.objects.filter(pk=todoitem_id).delete()
    return redirect("todolist:index")


def add_event(request):
    context = {}

    if request.method == 'POST':
        form = AddEventForm(request.POST)

        if form.is_valid() == False:
            form = AddEventForm()
        else:
            event_name = form.cleaned_data['event_name']
            description = form.cleaned_data['description']

            event_date_str = request.POST.get('event_date')  # Adjust this line based on your actual form field name
            event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')  # Adjust the date format
            # Checks the database if a task already exists
            duplicates = EventsItem.objects.filter(event_name=event_name)

            if not duplicates:
                EventsItem.objects.create(
                    event_name=event_name, 
                    description=description, 
                    event_date=event_date, 
                    user_id=request.user.id)
            else:
                context = {"error": True}

    return render(request, "todolist/add_event.html", context)

def update_event(request, eventitem_id):
    eventitem = EventsItem.objects.filter(pk=eventitem_id)
    context = {
        "user": request.user,
        "eventitem_id": eventitem_id,
        "event_name": eventitem[0].event_name,
        "description": eventitem[0].description,
        "status": eventitem[0].status,
        "event_date": eventitem[0].event_date.strftime('%Y-%m-%dT%H:%M') if eventitem[0].event_date else ""
    }

    if request.method == 'POST':
        form = UpdateEventForm(request.POST)

        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            event_date = form.cleaned_data['event_date']

            if eventitem:
                eventitem[0].event_name = event_name
                eventitem[0].description = description
                eventitem[0].status = status
                if event_date:  # Check if event_date is provided before updating
                    # Ensure event_date is a string before applying strptime
                    if isinstance(event_date, datetime):
                        event_date = event_date.strftime('%Y-%m-%dT%H:%M')

                    eventitem[0].event_date = datetime.strptime(event_date, '%Y-%m-%dT%H:%M')

                eventitem[0].save()

                context['update_success'] = True
            else:
                context = {
                    "error": True
                }
        else:
            context['form'] = form

    return render(request, "todolist/update_event.html", context)

def delete_event(request, eventitem_id):
    eventitem = EventsItem.objects.filter(pk=eventitem_id).delete()
    return redirect("todolist:index")