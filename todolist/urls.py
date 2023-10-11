from django.urls import path
from . import views
'''
	path()
		Syntax:
			path(route, view, name)

'''
app_name = 'todolist'
urlpatterns = [
  # /todoitem route
  path('', views.index, name='index'),
  
  # /todoitem/<todoitem_id> route
  path('<int:todoitem_id>/', views.todoitem, name='viewtodoitem'),

  # /register
  path('register/', views.register, name='register'),

  # /change_password
  path('change_password/', views.change_password, name='change_password'),

  # /login_view
  path('login/', views.login_view, name="login"),

  # /logout_view
  path('logout/', views.logout_view, name="logout"),

  # /add_task
  path('add_task/', views.add_task, name="add_task"),

  # /edit
  path('<int:todoitem_id>/edit', views.update_task, name="update_task"),

  # /delete
  path('<int:todoitem_id>/delete', views.delete_task, name='delete_task'),

  path('add_event/', views.add_event, name="add_event"),

  path('event/<int:eventitem_id>/', views.eventitem, name='vieweventitem'),

   path('event/<int:eventitem_id>/edit', views.update_event, name="update_event"),

     path('event/<int:eventitem_id>/delete', views.delete_event, name='delete_event'),

]