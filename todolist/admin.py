from django.contrib import admin
from .models import ToDoItem, EventsItem

# Register your models here.
admin.site.register(ToDoItem)
admin.site.register(EventsItem)