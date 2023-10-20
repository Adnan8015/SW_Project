# from django.db import models
# from django.contrib.auth.models import User
# from .models import CompanyList


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     auth_token = models.CharField(max_length=100)
#     is_verified = models.BooleanField(default=False)
#     reset_password_otp = models.CharField(max_length=6, null=True, blank=True)  # Add this field
#     created_at = models.DateTimeField(auto_now_add=True)
#     selected_companies = models.ManyToManyField(CompanyList, blank=True)  # Add this field

#     def __str__(self):
#         return self.user.username

# class CompanyList(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


from django.db import models
from django.contrib.auth.models import User

class CompanyList(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    reset_password_otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #selected_companies = models.ManyToManyField(CompanyList, blank = True)


    def __str__(self):
        return self.user.username


from django.db import models, IntegrityError

class UserSelectedCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="selected_companies")
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, verbose_name="Selected Company", related_name="users")

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

    class Meta:
        verbose_name = "User Selected Company"
        verbose_name_plural = "User Selected Companies"
        constraints = [
            models.UniqueConstraint(fields=['user', 'company'], name='unique_user_selected_company')
        ]
