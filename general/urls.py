from django.contrib import admin
from django.urls import path
from . import views
from .views import *

# general_user = General_Users()

urlpatterns = [
    path('', views.home, name="Home"),
    path('about', views.about, name="About"),
    path('trainers', views.trainers, name="Trainers"),
    path('events', views.events, name="Events"),
    path('forum', views.forum, name="Discussion"),

    
]
