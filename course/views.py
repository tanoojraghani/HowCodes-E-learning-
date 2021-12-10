from django.shortcuts import render,redirect
from firebase_admin import *
from firebase_admin import firestore
from django.contrib import auth
import pyrebase
import time

class General_Details:
    
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






class Course:
    
    def __init__(self):

        self.gen_user = General_Details()
        self.j = 0


    def home_courses(self,request):

        page_number = request.GET.get('page')
        self.lect_docs = self.gen_user.general_db.collection("Courses").get()
        # self.first_query = self.lect_docs.order_by('Fees').limit(2).stream()
        
        try:

            # for i in self.first_query:
            #     print(i.id)


            # self.last_doc = i.to_dict()

            
            # next_query = self.lect_docs.order_by('Fees').start_at({
            #     'Fees':175,
            # })
            # print(next_query)
            # for i in next_query:
            #     print("Hello")
            #     print(i.id)
            course_id_list = []
            for i in self.lect_docs:
                course_id_list.append(i.id)

            
            course_details_list = []
            for i in course_id_list:
                course_details = self.gen_user.general_db.collection("Courses").document(i)
                course_details_list.append(course_details)

            
            courses_list = []

            for i in course_details_list:

                courses_list.append(i.get().to_dict())
            
            print(courses_list)

            educator_details = self.gen_user.general_db.collection("Users").document(courses_list['Educator_Id']).get().to_dict()

            
            

            
            # main_course_dict = {}
            # n = len(course_id_list)
            # k = 0
            # page = 0
            # temp = []
            # for i in range(n):

            #     for j in range(2):

            #         try:
            #             t = course_details_list[k]
            #             k += 1
            #             temp.append(t.get().to_dict())

            #         except Exception as ex:
            #             print(ex)

            #     if temp != []:
            #         main_course_dict[page] = temp
            #         temp = []
            #         page += 1
            
            #     print(main_course_dict) ,'educator_name':educator_name

        except Exception as ex:
            print(ex)
        return render(request,'courses.html',{'courses_list':courses_list})
    
    def lecture_details(self,request):

        if request.method == 'POST':
            
            try:
                course_details_docs = self.gen_user.general_db.collection("Courses").document()
                course_name = request.POST.get('course_name')
                description_course = request.POST.get('description_course')
                overview_course = request.POST.get('overview_course')
                course_domain = request.POST.get('domain')
                hrs = int(request.POST.get('hrs'))
                fee = int(request.POST.get('fee'))
                # thumbnail = request.POST.get('url')

                self.course_details_docs_id = course_details_docs.id
                self.uid = request.POST.get('user_id')


                educator_details = self.gen_user.general_db.collection("Users").document(self.uid).get().to_dict()
                educator_name = educator_details['Username']

                course_dict = {
                    "Educator_Id":self.uid,
                    "Educator_Name":educator_name,
                    "Course_Id":course_details_docs.id,
                    "Course_Name":course_name,
                    "Course_Description":description_course,
                    "Course_Overview":overview_course,
                    "Course_Duration":hrs,
                    "Course_Fee": fee,
                    "Course_Domain":course_domain,
                }
                course_details_docs.set(course_dict)

                details_docs = self.gen_user.general_db.collection("Users").document(self.uid).collection("Courses").document(course_details_docs.id)

                details_docs.set(course_dict)


                
                
                return redirect("/course/add_lecture_details")
            
            except Exception as ex:
                print(ex)
                return render(request,"educator_upload_lecture_details.html")

        else:
                return render(request,"educator_upload_lecture_details.html")

    
## Educator adds a lecture to the course playlist
    def add_lecture_details(self,request):

        if request.method == "POST":
            lecture_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Lectures').document()
            lecture_name = request.POST.get('lecture_name')
            description_lecture = request.POST.get('description_lecture')

            lecture_dict = {
                "Lecture_Id":lecture_db.id,
                "Lecture_Name":lecture_name,
                "Course_Description":description_lecture,
            }

            lecture_db.set(lecture_dict)
            return redirect("/")
        
        else:
            return render(request,"educator_lecture_details.html")



    #Get the course details for the student
    def coursedetails(self,request):

        course_id = request.GET.get('course_id')

        lecture_db = self.gen_user.general_db.collection("Courses").document(course_id).get().to_dict()

        self.lecture_details_shown = self.gen_user.general_db.collection("Courses").document(course_id).collection('Lectures').get()

        lecture_id_list = []
        for i in self.lecture_details_shown:
            lecture_id_list.append(i.id)

            
        lecture_details_list = []
        for i in lecture_id_list:
            course_details = self.gen_user.general_db.collection("Courses").document(course_id).collection('Lectures').document(i)
            lecture_details_list.append(course_details)

        
            
        lecture_list = []

        for i in lecture_details_list:

            lecture_list.append(i.get().to_dict())

        
        
        

        return render(request,'course-details.html',{'lecture_db':lecture_db,'lecture_list':lecture_list,'course_id':course_id})
        
    
## Add new lecture to the existing course playlist
    def add_new_lecture_details(self,request):
        course_id = request.GET.get('course_id')
        
        self.course_details_docs_id = course_id

        return redirect(f'/course/add_lecture_details?course_id={course_id}')



        
    def educator_coursedetails(self,request):

        course_id = request.GET.get('course_id')
        lecture_db = self.gen_user.general_db.collection("Courses").document(course_id).get().to_dict()
        print(lecture_db)
        return render(request,'educator_add_new_lecture_to_course.html',{'lecture_db':lecture_db})


    
    def my_added_courses(self,request):
        
        self.uid = request.session['uid']
        self.details_docs = self.gen_user.general_db.collection("Users").document(self.uid).collection("Courses").get()

        try:
            course_id_list = []
            for i in self.details_docs:
                course_id_list.append(i.id)

            
            course_details_list = []
            for i in course_id_list:
                course_details = self.gen_user.general_db.collection("Users").document(self.uid).collection("Courses").document(i)
                course_details_list.append(course_details)

            
            courses_list = []

            for i in course_details_list:

                courses_list.append(i.get().to_dict())
            
            print(courses_list)

        except Exception as ex:
            print(ex)

        return render(request,'educator_courses.html',{'courses_list':courses_list})



        # print(lecture_db)

        # return render(request,'educator_course_details.html',{'lecture_db':lecture_db})

    def forum_chat(self,request):

        course_id = request.GET.get('course_id')
        self.course_details_docs_id = course_id

        self.uid = request.session['uid']

        forum_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Forum')

        user_db = self.gen_user.general_db.collection("Users").document(self.uid).get().to_dict()

        message_id_list = []
        forum_database = forum_db.get()
        for i in forum_database:
            message_id_list.append(i.id)
        message_details_list = []
        for i in message_id_list:
            course_details = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Forum').document(i)
            message_details_list.append(course_details)
        message_list = []
        for i in message_details_list:
            message_list.append(i.get().to_dict())



        if request.method == "POST":
            current_timestamp = time.time()
            message = request.POST.get('message')
            chat_forum = forum_db.document(str(current_timestamp))
            sender = user_db['Username']
            forum_message = {
                "Sender":sender,
                "Message": message
            }

            chat_forum.set(forum_message)

            
            return redirect(f'/course/forum?course_id={course_id}')
            # return render(request,'forum.html',{'message_list':message_list})
        
        else:

            print(message_list)


            return render(request,'forum.html',{'message_list':message_list})

    



    def add_quiz(self,request):

        course_id = request.GET.get('course_id')

        self.course_details_docs_id = course_id

        quiz_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Quiz').document()

        if request.method == "POST":

            question = request.POST.get('question1')
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            correct_answer = request.POST.get('correct_answer')


            quiz_questions = {
                "Question":question,
                "Option1": option1,
                "Option2": option2,
                "Option3": option3,
                "Option4": option4,
                "Correct_Option": correct_answer,
            }

            quiz_db.set(quiz_questions)

            
            return redirect(f'/course/add_quiz?course_id={course_id}')
            # return render(request,'forum.html',{'message_list':message_list})
        
        else:




            return render(request,'add_quiz.html')

    
    def quiz(self,request):

        course_id = request.GET.get('course_id')

        self.course_details_docs_id = course_id

        self.uid = request.session['uid']

        quiz_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Quiz')

        # user_db = self.gen_user.general_db.collection("Users").document(self.uid).get().to_dict()

        quiz_question_id_list = []

        quiz_database = quiz_db.get()
        for i in quiz_database:
            quiz_question_id_list.append(i.id)

        quiz_details_list = []
        for i in quiz_question_id_list:
            question_details = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Quiz').document(i)
            quiz_details_list.append(question_details)

        quiz_list = []
        for i in quiz_details_list:
            quiz_list.append(i.get().to_dict())

        return render(request,'quiz.html',{'quiz_list':quiz_list})




    def enroll(self,request):

        course_id = request.GET.get('course_id')

        self.course_details_docs_id = course_id

        self.uid = request.session['uid']

        course_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).get().to_dict()

        course_db['No_of_lectures_completed'] = 0



        lec_db = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Lectures').get()
        
        enrolled_lecture_id_list = []

        for i in lec_db:
            enrolled_lecture_id_list.append(i.id)
        
        

        quiz_details_list = []
        for i in enrolled_lecture_id_list:
            question_details = self.gen_user.general_db.collection("Courses").document(self.course_details_docs_id).collection('Lectures').document(i)
            quiz_details_list.append(question_details)
        


        quiz_list = []
        temp1 = {}
        for i in quiz_details_list:
            
            temp1 = i.get().to_dict()
            temp1['Completed'] = False

            quiz_list.append(temp1)


        print(quiz_list)
        enroll_db = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(self.course_details_docs_id)

        enroll_db.set(course_db)

        

        for i in quiz_list:
            enroll_db1 = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(self.course_details_docs_id).collection('Lecture').document(i['Lecture_Id'])
            enroll_db1.set(i)

        return redirect('/')
    

    def enrolled_courses(self,request):

        self.uid = request.session['uid']
        self.enrolled_lect_docs = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').get()
        # self.first_query = self.lect_docs.order_by('Fees').limit(2).stream()
        
        try:

            course_id_list = []
            for i in self.enrolled_lect_docs:
                course_id_list.append(i.id)

            
            course_details_list = []
            for i in course_id_list:
                course_details = self.gen_user.general_db.collection("Courses").document(i)
                course_details_list.append(course_details)

            
            courses_list = []

            for i in course_details_list:

                courses_list.append(i.get().to_dict())
            
        except Exception as ex:
            print(ex)
        return render(request,'courses.html',{'courses_list':courses_list})
    

    def assignment(self,request):
        return render(request,'assignment.html')





    def completed_lectures(self,request):

        self.uid = request.session['uid']

        course_id =  request.GET.get('course_id')
        
        lecture_id =  request.GET.get('lecture_id')

        progress_lect_docs = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(course_id).collection('Lecture').document(lecture_id).get().to_dict()

        print(progress_lect_docs)
        if progress_lect_docs['Completed'] == False:
            
            progress_lect_docs['Completed'] = True
            temp_temp = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(course_id).collection('Lecture').document(lecture_id)

            temp_temp.set(progress_lect_docs)
            temp1 = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(course_id).get().to_dict()

            
            temp = int(temp1['No_of_lectures_completed'])
            temp += 1
            temp1['No_of_lectures_completed'] = temp
            print(temp1)
            self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(course_id).set(temp1)
        
        return redirect('/')
        


    def my_lecture_progress(self,request):

        self.uid = request.session['uid']

        progress_lect_docs = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').get()

        try:

            course_id_list = []
            for i in progress_lect_docs:
                course_id_list.append(i.id)

            
            course_details_list = []
            list1 = []
            for i in course_id_list:
                course_details = self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(i)

                n = len(self.gen_user.general_db.collection("Users").document(self.uid).collection('Enrolled Courses').document(i).collection('Lecture').get())
                list1.append(n)
                

                course_details_list.append(course_details)

            
            courses_list = []
            j = 0
            
            for i in course_details_list:

                temp2 = i.get().to_dict()

                temp2['Total_no_of_lectures_in_course'] = list1[j]

                j += 1


                courses_list.append(temp2)
            
            print(courses_list)

            return render(request,'progress.html',{'courses_list':courses_list})
            
        except Exception as ex:
            print(ex)
            return redirect('/')
        











