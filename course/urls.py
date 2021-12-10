from django.contrib import admin
from django.urls import path
from . import views
from .views import *

general_user = Course()

urlpatterns = [
    
    path('', general_user.home_courses, name="All Courses"),
    
    path('lecture_details', general_user.lecture_details, name="All Courses"),
    
    path('add_lecture_details', general_user.add_lecture_details, name="Lecture Details"),
    
    path('coursedetails', general_user.coursedetails, name="Course Details"),
    
    path('educator_added_courses', general_user.my_added_courses, name="Course Details"),
    
    path('add_new_lecture_to_course', general_user.add_new_lecture_details, name="Add New Lecture To Playlist"),
    
    path('educator_coursedetails', general_user.educator_coursedetails, name="Educators See the details of their course"),

    path('forum', general_user.forum_chat, name="Educators See the details of their course"),

    path('add_quiz', general_user.add_quiz, name="Educators Adds Quiz for Students"),

    path('quiz', general_user.quiz, name="Take Quiz"),

    path('enroll', general_user.enroll, name="Enroll To Course"),

    path('enrolled_courses', general_user.enrolled_courses, name="Enroll To Course"),
    
    path('assignment', general_user.assignment, name="Enroll To Course"),

    path('progress', general_user.my_lecture_progress, name="Progress of Course"),

    path('completed', general_user.completed_lectures, name="Progress of Course"),
    
    
]
