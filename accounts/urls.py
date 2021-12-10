from django.contrib import admin
from django.urls import path
from . import views
from .views import *

general_user = General_Users()

urlpatterns = [
    path('login', general_user.login, name="Login"),
    path('logout', general_user.logout, name="Logout"),
    path('signup', general_user.signup, name="Signup"),
    
]
