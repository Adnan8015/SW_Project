# from django.contrib import admin
# from django.urls import path
# from .views import *

# urlpatterns = [
#    path('', home , name = 'home'),
#    path('register' , register_attempt , name = 'register_attempt'),
#    path('mainapp/login/' , login_attempt , name = 'login_attempt'),
#    path('token' , token_send , name = 'token_send'),
#    path('success' , success , name = 'success'),
#    path('verify/<auth_token>' , verify , name = "verify"),
#    path('error' , error_page , name = "error"),
#    path('home_page' , home_page , name = 'home_page'),
#    path('forgot_password/', forgot_password, name='forgot_password'),
#    path('reset_password/<str:token>/', reset_password, name='reset_password'),
#    path('verify_otp/<str:token>/', verify_otp, name='verify_otp'),
#    path('', homepage, name='homepage')

# ]

from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home , name = 'home'),
    #path('homepage', homepage, name='homepage'),
    path('register', register_attempt, name='register_attempt'),
    path('mainapp/login/', login_attempt, name='login_attempt'),
    path('token', token_send, name='token_send'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name="verify"),
    path('error', error_page, name="error"),
    #path('home_page', homepage, name='home_page'),
    path('home_page', home_page, name='home_page'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', reset_password, name='reset_password'),
    path('verify_otp/<str:token>/', verify_otp, name='verify_otp'),
    path('expected_salary/', expected_salary, name='expected_salary'),
    path('calculate_expected_salary/', calculate_expected_salary, name='calculate_expected_salary'),
    path('profile/', user_profile, name='user_profile'),
    path('top_companies/', top_companies, name='top_companies')
    #path('home_page/', company_selection, name='company_selection'),
    #path('selected_companies/', selected_companies, name='selected_companies')
    #path('select_company/<int:company_id>/', select_company, name='select_company')
]
