from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
import random
import asyncio
import os
import math
from pyrebase import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from more_itertools import random_permutation
from django.http import HttpResponseRedirect
import urllib
from datetime import datetime

cred = credentials.Certificate("main/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'notesync-2184.appspot.com'})
bucket = storage.bucket()

db = firestore.client()
cardclicked = ''
dash_data = ''
user_details = ''
user_pfp = ''
clickeduser = ''
username = ''
adminloginstatus = False
def idgenerator():
    uniquenoteid = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase)for i in range(10))
    uniquenoteid = uniquenoteid + str(random.randint(00000,99999))
    uniquenoteid = ''.join(random_permutation(uniquenoteid))
    return uniquenoteid
# Create your views here.
def index(response):
    return render(response, "main/index.html", {})

def dashboard(response):
    global cardclicked, dash_data, user_details, user_pfp, username
    if username != '':
        dash_data = db.collection(u'Your Work')
        user_img = db.collection(u'User Details')

        result = dash_data.stream()
        result2 = user_img.stream()
        dash_list = []
        dash_new_list = []
        for doc in result:
            dash_list.append(doc.to_dict())
        dash_list = sorted(dash_list, key=lambda i: i['Score'], reverse=True)
        for i in dash_list:
            user_image = db.collection(u'User Details').document(i['Username']).get()
            user_info = user_image.get('PFP_url')
            user_final = {'PFP_url': user_info}
            i.update(user_final)
            dash_new_list.append(i)
        return render(response, "main/Dashboard.html", {'result':dash_new_list,'user_fullname':user_details,'user_pfp':user_pfp})
    else:
        return redirect('/sign')    

def sign_in_up(response):
    global user_details, user_pfp , username
    wrong_cred = False
    if response.POST.get('Sign Up') == 'Sign Up':
        username = response.POST.get('username')
        signup_details = {
            u'Full_Name': response.POST.get('fullname'),
            u'User_Name': username,
            u'Email': response.POST.get('email'),
            u'Password': response.POST.get('password'),
            u'Credit': 0,
            u'Rank': '',
            u'Posts': 0,
            u'Score': 0,
            u'OTP': 0000,
            u'About_me': '',
            u'Profession': '',
            u'PFP_url': ''
        }
        signup_data = db.collection('User Details').document(username)
        signup_data.set(signup_details)
        return redirect('/sign')

    if response.POST.get('Sign In') == 'Sign In':
        email = response.POST.get('signemail')
        password = response.POST.get('signpassword')

        sign_cred = db.collection(u'User Details').where('Email','==', email).where('Password','==',password).get()
        
        if len(sign_cred) == 0:
            wrong_cred = True
        else:
            for i in sign_cred:
                username = i.get('User_Name')
            wrong_cred = False
            profile_info = db.collection('User Details').document(username).get()
            user_details = profile_info.get('Full_Name')
            user_pfp = profile_info.get('PFP_url')
            return redirect('/dashboard')
    return render(response, "main/signinup.html", {'wrong_cred':wrong_cred})

def logout(response):
    global username
    username = ''
    return redirect('/sign')
def adminlogout(response):
    global adminloginstatus
    adminloginstatus = ''
    return redirect('/admin-login')
def your_work(response):
    global bucket,user_details, user_pfp, username

    if username != '':
        Date= ''
        Description  = ''
        PDF = ''
        Rating = 0
        Score = 0
        Subject = ''
        Title = ''
        id_generate = ''
        yourwork_data = db.collection(u'Your Work').where('Username','==',username)
        result = yourwork_data.stream()
        yourwork_list = []
        for doc in result:
            yourwork_list.append(doc.to_dict())
        if response.POST.get('uploadnotes'):
            print(response.POST.get('getpdfurl'))
            uid = idgenerator()
            upload_data = {
            u'Username': username,
            u'Unique_ID': uid,
            u'Date': firestore.SERVER_TIMESTAMP,
            u'Rating': 0,
            u'Title': response.POST.get('title-input'),
            u'Subject': response.POST.get('subject-input'),
            u'Score': 0,
            u'PDF': response.POST.get('getpdfurl'),
            u'Description': response.POST.get('description-input')
            }
            up_data = db.collection('Your Work').document(uid)
            up_data.set(upload_data)
            up_post = db.collection(u'User Details').document(username)
            post_ref = up_post.get()
            current_post = post_ref.get('Posts')
            up_post.update({
                'Posts': current_post + 1,
            })
            return redirect('/yourwork')

        if response.POST.get('editnotes'):
            edit_uniqueID = response.POST.get('edit-uniqueid')
            edit = db.collection('Your Work').document(edit_uniqueID)
            if response.POST.get('edit-title-input') != '':
                edit.update({
                    'Title': response.POST.get('edit-title-input'),
                })
            if response.POST.get('edit-subject-input') != '':
                edit.update({
                    'Subject': response.POST.get('edit-subject-input'),
                })
            if response.POST.get('edit-description-input') != '':
                edit.update({
                    'Description': response.POST.get('edit-description-input'),
                })
            if response.POST.get('edit-getpdfurl') != '':
                edit.update({
                    'PDF': response.POST.get('edit-getpdfurl'),
                }) 
            edit.update({
                    'Date': firestore.SERVER_TIMESTAMP,
                })       
            return redirect('/yourwork')
        if response.POST.get('delbtn'):
            delclicked = response.POST.get('delbtn')
            db.collection(u'Your Work').document(delclicked).delete()
            del_review = db.collection(u'Reviews').where('Unique_ID','==',delclicked).get()
            for del_i in del_review:
                del_i.reference.delete()
            up_post = db.collection(u'User Details').document(username)
            post_ref = up_post.get()
            current_post = post_ref.get('Posts')
            up_post.update({
                'Posts': current_post - 1,
            })    
            return redirect('/yourwork')

        return render(response, "main/your-work.html", {'yourwork_list':yourwork_list,'user_fullname':user_details,'user_pfp':user_pfp})
    else:
        return redirect('/sign')
def leaderboard(response):
    global user_details,user_pfp, clickeduser, username
    j = 0 
    user_list = []
    if username != '':
        user = db.collection(u'User Details')
        details = user.stream()
        for i in details:
            user_list.append(i.to_dict())
        user_list = sorted(user_list, key=lambda i: i['Credit'], reverse=True)
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        for i in user_list:
            j = j + 1
            up_rank = db.collection(u'User Details').document(i['User_Name'])
            up_rank.update({
                'Rank': ordinal(j),
            })
        current_user_login = db.collection(u'User Details').document(username).get()
        user_rank = current_user_login.get('Rank')
        user_score = current_user_login.get('Score')

        if response.POST.get('clickeduser'):
            clickeduser = response.POST.get('clickeduser')
            return redirect('/preview')
        return render(response, "main/leaderboard.html", {'user_list':user_list,'user_fullname':user_details,'user_pfp':user_pfp,'user_rank':user_rank,'user_score':user_score})
    else:
        return redirect('/sign')    
    
def profile(response):
    global user_details, user_pfp, username
    if username != '':
        profile_info = db.collection('User Details').document(username).get()
        profile_details = profile_info.to_dict()
        user_list = []
        j = 0
        user = db.collection(u'User Details')
        details = user.stream()
        for i in details:
            user_list.append(i.to_dict())
        user_list = sorted(user_list, key=lambda i: i['Credit'], reverse=True)
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        for i in user_list:
            j = j + 1
            up_rank = db.collection(u'User Details').document(i['User_Name'])
            up_rank.update({
                'Rank': ordinal(j),
            })
        current_user_login = db.collection(u'User Details').document(username).get()
        user_rank = current_user_login.get('Rank')
        return render(response, "main/profile.html", {'user_rank':user_rank,'details':profile_details,'user_fullname':user_details,'user_pfp':user_pfp})    
    else:
        return redirect('/sign')
def notes_view(response):
    global cardclicked, dash_data, user_details, user_pfp, username
    title = ''
    discription = ''
    username = ''
    rating = 0
    comments = []
    pdf = ''
    dash_data = db.collection(u'Your Work')
    result = dash_data.stream()
    dash_list = [] 
    rated = ''
    if username != '':
        if response.GET.get("view_notes"):
            cardclicked = response.GET.get("view_notes")
        if response.POST.get('submitReview'):
            ratings = response.POST.get('rating')
            comments_user = response.POST.get('review-input')
            review_data = {
            u'username': username,
            u'Unique_ID':cardclicked,
            u'Comment': comments_user,
            u'Rating': int(ratings)
            }
            db.collection(u'Reviews').add(review_data)
            all_ratings = []
            fetch_ratings = db.collection(u'Reviews').where('Unique_ID','==',cardclicked).get()
            for rating in fetch_ratings:
                all_ratings.append(rating.get('Rating'))
            total_ratings = len(all_ratings)
            average_rating = round(sum(all_ratings) / total_ratings)
            up_rating = db.collection(u'Your Work').document(cardclicked)
            up_rating.update({
                    'Rating': average_rating,
                })

            if total_ratings >= 2:
                score = wilson_score(all_ratings, total_ratings)
                if score < 0:
                    up_rating.update({
                    'Score': 0,
                    })
                else:
                    up_rating.update({
                    'Score': round(score,4),
                    })   
            else:
                up_rating.update({
                    'Score': 0,
                })
            get_username = db.collection(u'Your Work').document(cardclicked).get()
            note_username = get_username.get('Username') 
            up_credit = db.collection(u'User Details').document(note_username)
            credit_ref = up_credit.get()
            current_credit = credit_ref.get('Credit')
            current_score = credit_ref.get('Score')
            up_credit.update({
                'Credit': current_credit + int(ratings) * 2,
                'Score': current_score + int(ratings) * 2,
            })

        for doc in result:
            dash_list.append(doc.to_dict())
        for i in dash_list:
            if i['Unique_ID'] == cardclicked:
                title = i['Title']
                discription = i['Description']
                username = i['Username']
                pdf = i['PDF']
                rating = i['Rating']
        existing_reviews = db.collection('Reviews').where('username', '==', username).where('Unique_ID', '==', cardclicked).get()
        if not existing_reviews:
            rated = ''
            
        else:
            rated = 'yes'

        load_reviews = db.collection('Reviews').where('Unique_ID', '==', cardclicked).get()
        for i in load_reviews:
            comments.append(i.to_dict())
        reported_username = db.collection('Your Work').document(cardclicked).get()
        reported_username = reported_username.to_dict()

        cidgen = idgenerator()
        if response.POST.get('smtplagiarism') == 'plagiarism':
            plagiarism_data = {
            u'cid': random.randint(00000, 99999),
            u'Unique_id': cidgen,
            u'copy_url': response.POST.get('curl'),
            u'orignal_url': response.POST.get('ourl'),
            u'reported_user': reported_username['Username'],
            u'reporting_user': username,
            u'reported_note': cardclicked,
            u'type': u'Plagiarism',
            }
            up_data = db.collection('Complaints').document(cidgen)
            up_data.set(plagiarism_data)
        if response.POST.get('smtother') == 'other':
            other_data = {
            u'cid': random.randint(00000, 99999),
            u'Unique_id': cidgen,
            u'reported_user': reported_username['Username'],
            u'discription': response.POST.get('problem-input'),
            u'reporting_user': username,
            u'reported_note': cardclicked,
            u'type': u'Other',
            }
            up_data = db.collection('Complaints').document(cidgen)
            up_data.set(other_data)              


        return render(response, "main/notes-view.html", {'title':title,'discription':discription,'username':username,'pdf':pdf,'rating':rating,
                                                        'comments':comments,'rated':rated,'user_fullname':user_details,'user_pfp':user_pfp 
                                                        })       
    else:
        return redirect('/sign')

def wilson_score(ratings, num_ratings):
    if num_ratings == 0:
        return 0
    z = 1.64 # 90% confidence interval , if 95% confidence then z=1.94
    pos = sum(ratings)
    neg = num_ratings - pos
    phat = 1.0 * pos / num_ratings
    return (phat + z*z/(2*num_ratings) - z*math.sqrt((phat*(phat-1)+z*z/(4*num_ratings))/num_ratings + 1/(4*num_ratings**2))) / (1+z*z/num_ratings)

def adminlogin(response):
    global adminloginstatus

    if response.POST.get('adminbtnclick') == 'Login':
        adminemail = response.POST.get('adminemail')
        adminpass = response.POST.get('adminpass')
        admincred = db.collection(u'Admin').where('Email','==',adminemail).where('Password','==',adminpass).get()
        print(admincred)
        if len(admincred) != 0:
            adminloginstatus = True
            return redirect('/admindashboard')
        else:
            adminloginstatus = False     

    return render(response, "main/adminlogin.html", {})
def admin(response):
    global adminloginstatus

    if adminloginstatus == True:
        cmp_data = db.collection('Complaints')
        cmp_result = cmp_data.stream()
        cmp_list = []
        for i in cmp_result:
            cmp_list.append(i.to_dict())
        if response.POST.get('close-plagiarism'):
            close = response.POST.get('close-plagiarism')
            close_cmp = db.collection('Complaints').document(close)
            close_snapshot = close_cmp.get()
            reporting_user = close_snapshot.get("reporting_user")
            reported_note = close_snapshot.get("reported_note")
            reporting_user_detail = db.collection(u'User Details').document(reporting_user).get()
            reporting_name = reporting_user_detail.get('Full_Name')
            reporting_email = reporting_user_detail.get('Email')
            delete_note = db.collection(u'Your Work').document(reported_note)
            note = delete_note.get()
            note_title = note.get('Title')
            colse_email(note_title,reporting_email, reporting_name)
            close_cmp.delete()
            return redirect('/admindashboard')
        if response.POST.get('delete-plagiarism'):
            delete = response.POST.get('delete-plagiarism')
            del_note = db.collection('Complaints').document(delete)
            del_snapshot = del_note.get()
            reported_note = del_snapshot.get("reported_note")
            reported_user = del_snapshot.get("reported_user")
            reported_user_detail = db.collection(u'User Details').document(reported_user).get()
            reported_name = reported_user_detail.get('Full_Name')
            reported_email = reported_user_detail.get('Email')

            reporting_user = del_snapshot.get("reporting_user")
            reporting_user_detail = db.collection(u'User Details').document(reporting_user).get()
            reporting_name = reporting_user_detail.get('Full_Name')
            reporting_email = reporting_user_detail.get('Email')

            delete_note = db.collection(u'Your Work').document(reported_note)
            note = delete_note.get()
            note_title = note.get('Title')
            delete_note.delete()
            delete_cmp = db.collection(u'Complaints').document(delete)
            delete_cmp.delete()
            del_review = db.collection(u'Reviews').where('Unique_ID','==',reported_note).get()
            for del_i in del_review:
                del_i.reference.delete()
            print(reported_email, reported_name,note_title)
            del_email(reported_email, reported_name,note_title,reporting_email, reporting_name)
            return redirect('/admindashboard')


        return render(response, 'main/admin.html',{'cmp_list':cmp_list})
    else:
        return redirect('/admin-login')
def del_email(to,name,title,reporting_email, reporting_name):
    
    body = f'''
Dear {name},

We regret to inform you that your notes, with the title "{title}", have been deleted from our platform due to the detection of plagiarism in the content.

As a platform that promotes originality and integrity in academic work, we have a zero-tolerance policy towards plagiarism. Our team conducted a thorough review of the notes and found that the content was copied from another source without proper attribution or permission, which violates our terms of service.

As a result, we have taken the necessary action to remove the notes from our platform to maintain the quality and integrity of the content available to our users. We understand that this may be disappointing, but it is important for us to uphold our policies and ensure that all content on our platform is original and properly attributed.

If you have any questions or concerns regarding this matter, please do not hesitate to contact us. We value your understanding and cooperation in maintaining the integrity of our platform.

Thank you for your attention to this matter.

Best regards,
Team NoteSync
    '''
    reciver = []
    reciver.append(to)
    send_mail('Deletion of Notes due to Plagiarism',body,'settings.EMAIL_HOST_USER',reciver,fail_silently=False)
    
    body = f'''
Dear {reporting_name},

We are writing to address the report of plagiarism that you recently submitted to us. We take all reports of academic integrity violations seriously, and we have thoroughly reviewed your report.

After conducting a thorough investigation, we have determined that the content in question, titled "{title}", has indeed violated our plagiarism policy. Our team has identified substantial similarities between the content and another source without proper attribution or permission, which is a violation of our terms of service.

As a platform that promotes originality and integrity in academic work, we have a zero-tolerance policy towards plagiarism. We have taken the necessary action to remove the content from our platform to maintain the quality and integrity of the content available to our users. Additionally, we have implemented measures to prevent similar occurrences in the future.

We appreciate your vigilance in reporting this issue to us. Your efforts in upholding academic integrity are valued and contribute to maintaining the integrity of our platform. We take reports of plagiarism seriously and are committed to taking appropriate action to address such violations.

If you have any further questions or concerns, please do not hesitate to contact us. We are happy to provide any additional information or clarify any aspects of our investigation.

Thank you for your attention to this matter and your continued support in upholding academic integrity on our platform.

Best regards,
Team NoteSync
    '''    
    reporting_reciver = []
    reporting_reciver.append(reporting_email)
    send_mail('Response to Report of Plagiarism',body,'settings.EMAIL_HOST_USER',reporting_reciver,fail_silently=False)

def colse_email(title,reporting_email, reporting_name):
    
    body = f'''
Dear {reporting_name},

We are writing to provide you with an update on the report of plagiarism that you recently submitted to us. After conducting a thorough investigation, we would like to inform you that we did not find any evidence of plagiarism in the content titled '{title}'.

As a platform that promotes originality and integrity in academic work, we take all reports of academic integrity violations seriously. We appreciate your vigilance in reporting this issue to us, and we have a robust process in place to investigate all reports thoroughly.

However, after conducting a detailed review, we did not identify any substantial similarities between the content and any other source without proper attribution or permission. Based on our investigation, the content in question appears to be original and does not violate our plagiarism policy.

We value the importance of maintaining academic integrity on our platform, and we are committed to upholding our policies and standards. We apologize for any inconvenience this may have caused, and we appreciate your understanding in this matter.

If you have any further questions or concerns, please do not hesitate to contact us. We are happy to provide any additional information or address any queries you may have.

Thank you for your attention to this matter and your continued support in upholding academic integrity on our platform.

Best regards,
Team NoteSync
    '''
    reciver = []
    reciver.append(reporting_email)
    send_mail('Response to Report of Plagiarism',body,'settings.EMAIL_HOST_USER',reciver,fail_silently=False)

def edit_profile(response):
    global user_details, user_pfp, username
    if username != '':
        if response.POST.get('prfile-submit') == 'submit':
            about_me = response.POST.get('aboutme')
            prfession = response.POST.get('profession')
            pfp_url = response.POST.get('pfpurl')
            edit = db.collection('User Details').document(username)
            if about_me != '':
                edit.update({
                    'About_me': about_me,
                })
            if prfession != '':
                edit.update({
                    'Profession': prfession,
                })
            if pfp_url != '':
                edit.update({
                    'PFP_url': pfp_url,
                })
            return redirect('/profile')
        return render(response, 'main/edit_profile.html',{'user_fullname':user_details,'user_pfp':user_pfp})
    else:
        return redirect('/sign')
def preview(response):

    global clickeduser, user_pfp,  user_details

    click_user = db.collection(u'User Details').document(clickeduser).get()
    details = click_user.to_dict()
    return render(response, 'main/profile-preview.html',{'details':details,'user_pfp':user_pfp,'user_fullname':user_details})
def reward(response):
    global user_pfp,  user_details, username
    warning = False
    successful = False
    if username != '':
        if response.POST.get('redeemdata') == 'submit':
            CTitle = response.POST.get('courseName')
            CPrice = int(response.POST.get('price'))
            print(CTitle,CPrice)
            credit_ref = db.collection(u'User Details').document(username)
            credit = credit_ref.get()
            email = credit.get('Email')
            name = credit.get('Full_Name')
            credit = credit.get('Credit')
            
            if CPrice > credit:
                warning = True
                successful = False

            else:
                warning = False
                successful = True
                credit_ref.update({
                    'Credit': credit - CPrice,
                })
                send_link(CTitle,email,name)

        if response.POST.get('warning-close') == 'submit':
            warning = False
        if response.POST.get('successful-close') == 'submit':
            successful = False

        return render(response, 'main/redeem.html',{'user_pfp':user_pfp,'user_fullname':user_details,'warning':warning,'successful':successful})
    else:
        return redirect('/sign')
def send_link(title,email,name):
    
    if title == 'Artificial Intelligence: Search Methods for Problem Solving':
        link = 'https://nptel.ac.in/courses/106106126'
    elif title == 'NOC:Introduction to Aerospace Engineering':
        link = 'https://nptel.ac.in/courses/101101079'
    elif title == 'NOC:Earthquake Resistant Design of Foundations':
        link = 'https://nptel.ac.in/courses/105107204'
    elif title == 'Parallel Algorithms':
        link = 'https://nptel.ac.in/courses/106106112'
    elif title == 'Compiler Design':
        link = 'https://nptel.ac.in/courses/106104072'
    elif title == 'Process Mining: Data science in Action':
        link = 'https://www.coursera.org/learn/process-mining'
    elif title == 'Computational Neuroscience':
        link = 'https://www.coursera.org/learn/computational-neuroscience'
    elif title == 'Introduction to Calculus':
        link = 'https://www.coursera.org/learn/introduction-to-calculus'
    elif title == 'Introduction to Cybersecurity Foundations':
        link = 'https://www.coursera.org/learn/introduction-to-cybersecurity-foundations'  
    elif title == 'Discrete Optimization':
        link = 'https://www.coursera.org/learn/discrete-optimization'
    else:
        link = '''We are sorry to inform you that there might be a problem with the redeem link for your course.
Our team is working to resolve the issue as soon as possible.'''                      

    body = f'''
Dear {name},

We are excited to let you know that your requested course has been successfully redeemed and you can now start your learning journey.

As promised, we are providing you with the link to access your course: {link}. This link will take you to the course page where you can start learning at your own pace.

If you face any technical difficulties or have any queries regarding the course, please do not hesitate to contact us. We would be happy to help you out.

Thank you once again for choosing our platform. We look forward to your successful completion of the course.

Best regards,
Team NoteSync
    '''
    reciver = []
    reciver.append(email)
    send_mail(title + ' course access link',body,'settings.EMAIL_HOST_USER',reciver,fail_silently=False)