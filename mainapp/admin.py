from django.contrib import admin
# from django.contrib.admin.sites import site
# from django.contrib.admin import ModelAdmin

from .models import * 
from .models import CompanyList
from .models import UserSelectedCompany


admin.site.register(Profile)
admin.site.register(CompanyList)
admin.site.register(UserSelectedCompany)
# Register your models here.

