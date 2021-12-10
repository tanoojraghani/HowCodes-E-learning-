from django.shortcuts import render,redirect
from firebase_admin import *
from firebase_admin import firestore
from django.contrib import auth
import pyrebase
import time

general_firebaseConfig = {
    
  "apiKey": "AIzaSyA6VxOP79Wx1DxRWIq2BqU5PhUDcOjUOlw",
  "authDomain": "codestorm-hackathon.firebaseapp.com",
  "databaseURL": "",
  "projectId": "codestorm-hackathon",
  "storageBucket": "codestorm-hackathon.appspot.com",
  "messagingSenderId": "92375695203",
  "appId": "1:92375695203:web:b3b6b46a8b1947791e9d56",
  "measurementId": "G-RKP7W5G5ZR"

}
general_database = pyrebase.initialize_app(general_firebaseConfig)
general_auth_user = general_database.auth()
user_database = general_database.database()
cred = credentials.Certificate("general_service_account_key.json")
try:
    initialize_app(cred)
except Exception as ex:
    print(ex)
general_db = firestore.client()


def home(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')


def courses(request):
    return render(request,'courses.html')

def trainers(request):
    return render(request,'trainers.html')

def events(request):
    return render(request,'events.html')

def forum(request):

    
    forum_db = general_db.collection("Discussion")
    

    message_id_list = []

    forum_database = forum_db.get()
    for i in forum_database:
            message_id_list.append(i.id)

    message_details_list = []

    for i in message_id_list:
        course_details = general_db.collection("Discussion").document(i)
        message_details_list.append(course_details)
        
    message_list = []
    for i in message_details_list:
        message_list.append(i.get().to_dict())

    if request.method == "POST":
        uid = request.session['uid']
        user_db = general_db.collection("Users").document(uid).get().to_dict()
        
        current_timestamp = time.time()
        message = request.POST.get('message')
        chat_forum = forum_db.document(str(current_timestamp))
        sender = user_db['Username']
        forum_message = {
            "Sender":sender,
            "Message": message
        }
        chat_forum.set(forum_message)
        
        return redirect('/general/forum')
        
    else:
        return render(request,'general_forum.html',{'message_list':message_list})







