# from mainapp.models import Profile
# from mainapp.models import CompanyList
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

import random
import string

import re

from django.shortcuts import render
import pickle
import numpy as np


@login_required
def home(request):
    return render(request , 'home.html')

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/mainapp/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/mainapp/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/mainapp/login')
        
        login(request , user)
        return redirect('/home_page')

    return render(request , 'login.html')





# def register_attempt(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(password)

#         try:
#             if User.objects.filter(username = username).first():
#                 messages.success(request, 'Username is taken.')
#                 return redirect('/register')

#             if User.objects.filter(email = email).first():
#                 messages.success(request, 'Email is taken.')
#                 return redirect('/register')
            
#             user_obj = User(username = username , email = email)
#             user_obj.set_password(password)
#             user_obj.save()
#             auth_token = str(uuid.uuid4())
#             profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
#             profile_obj.save()
#             send_mail_after_registration(email , auth_token)
#             return redirect('/token')

#         except Exception as e:
#             print(e)


#     return render(request , 'register.html')



def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check password length
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('/register')

        # Check for character, special character, and digit
        if not (re.search(r'[a-zA-Z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
            messages.error(request, 'Password must contain at least one character, one digit, and one special character.')
            return redirect('/register')

        try:
            # ... rest of your code ...
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')




def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')

def home_page(request):
    return render(request , 'home_page.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/mainapp/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/mainapp/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')





def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            otp = generate_otp()
            user.profile.reset_password_otp = otp
            user.profile.save()

            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}'
            from_email = 'adnanahmad8015@gmail.com'  # Update with your email
            recipient_list = [email]
            try:
                send_mail(subject, message, from_email, recipient_list)
                return redirect('verify_otp', token=user.profile.reset_password_otp)
            except Exception as e:
                print(e)
                messages.error(request, 'Failed to send OTP. Please try again later.')

        else:
            messages.error(request, 'User with this email does not exist.')

    return render(request, 'forgot_password.html')


# def reset_password(request, token):
#     user = User.objects.filter(profile__reset_password_otp=token).first()

#     if user:
#         if request.method == 'POST':
#             new_password = request.POST.get('new_password')
#             user.set_password(new_password)
#             user.profile.reset_password_otp = None
#             user.save()
#             messages.success(request, 'Password reset successfully. You can now login with your new password.')
#             return redirect('login_attempt')

#         return render(request, 'reset_password.html')
#     else:
#         messages.error(request, 'Invalid or expired OTP.')
#         return redirect('forgot_password')



def reset_password(request, token):
    user = User.objects.filter(profile__reset_password_otp=token).first()

    if user:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            
            # Check password length
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('/reset_password/' + token)  # Redirect back to the reset password page with an error message.

            # Check for character, special character, and digit
            if not (re.search(r'[a-zA-Z]', new_password) and
                    re.search(r'[0-9]', new_password) and
                    re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)):
                messages.error(request, 'Password must contain at least one character, one digit, and one special character.')
                return redirect('/reset_password/' + token)  # Redirect back to the reset password page with an error message.

            # If password constraints are met, proceed to set the new password
            user.set_password(new_password)
            user.profile.reset_password_otp = None
            user.save()
            messages.success(request, 'Password reset successfully. You can now login with your new password.')
            return redirect('login_attempt')

        return render(request, 'reset_password.html')
    else:
        messages.error(request, 'Invalid or expired OTP.')
        return redirect('forgot_password')



def verify_otp(request, token):
    user = User.objects.filter(profile__reset_password_otp=token).first()

    if user:
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')
            stored_otp = user.profile.reset_password_otp

            if entered_otp == stored_otp:
                return redirect('reset_password', token=token)
            else:
                messages.error(request, 'Incorrect OTP. Please try again.')
                return redirect('verify_otp', token=token)

        return render(request, 'otp.html')
    else:
        messages.error(request, 'Invalid or expired OTP.')
        return redirect('forgot_password')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


# def homepage(request):
#     companies = CompanyList.objects.all()
#     # print(companies)
#     # for a in companies:
#     #     print(a.name)
#     data ={
#        'companies': companies
#     }
#     return render(request, "home_page.html", data )
from django.shortcuts import render
from .models import UserSelectedCompany  # Import the UserSelectedCompany model




def expected_salary(request):
    return render(request, 'expected_salary.html')




def calculate_expected_salary(request):
    if request.method == 'POST':
        experience = float(request.POST['experience'])
        cgpa = float(request.POST['cgpa'])
        skill = request.POST['skill']

       
        model = pickle.load(open('model.pkl', 'rb'))

        
        skill_mapping = {
            'ML': [1, 0],  # ML
            'AppDev': [0, 0],  # AppDev
            'WebDev': [0, 1],  # WebDev
        }

        skill_encoded = np.array(skill_mapping.get(skill, [0, 0, 0]))  # Encode the skill

        input_data = np.array([[experience, cgpa, *skill_encoded]])  # Combine input features

       
        predicted_salary = model.predict(input_data)

        return render(request, 'salary_result.html', {'predicted_salary': predicted_salary[0]})

    return render(request, 'salary_calculator.html')





from django.shortcuts import render, redirect
from .models import CompanyList, UserSelectedCompany
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home_page(request):
    companies = CompanyList.objects.all()
    user = request.user
    selected_company_ids = UserSelectedCompany.objects.filter(user=user).values_list('company', flat=True)

    if request.method == 'POST':
        selected_company_ids = request.POST.getlist('selected_companies')

        # Clear existing selections for the user
        UserSelectedCompany.objects.filter(user=user).delete()

        # Create new entries for selected companies
        for company_id in selected_company_ids:
            company = CompanyList.objects.get(pk=company_id)
            UserSelectedCompany.objects.create(user=user, company=company)
        
        messages.success(request, 'Company selection updated successfully.')

        # Redirect to the user's profile page or another page
        return redirect('home_page')

    return render(request, 'home_page.html', {'companies': companies, 'selected_company_ids': selected_company_ids})






from django.shortcuts import render
from .models import UserSelectedCompany


@login_required
def user_profile(request):
    user = request.user
    selected_companies = UserSelectedCompany.objects.filter(user=user)

    return render(request, 'profile.html', {'selected_companies': selected_companies})


import pandas as pd
from django.shortcuts import render

def top_companies(request):
    df = pd.read_csv('sorted_company_data.csv')
    top_10_companies = df.head(10)

    # Convert the DataFrame to a list of dictionaries for rendering in the template
    top_10_companies_data = top_10_companies.to_dict('records')

    return render(request, 'top_companies.html', {'top_companies_data': top_10_companies_data})
