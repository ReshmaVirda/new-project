# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import email
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import random
# from django.dispatch import receiver
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail  
# import random

#Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, mobile, country, birthdate, gender, registered_by, device_token, social_id, subscription_id, profile_pic, is_agree,  password=None):
        """
        Creates and saves a User with the given email, mobile, gender and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            gender=gender,
            country=country,
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate,
            is_agree=is_agree,
            device_token=device_token,
            social_id=social_id,
            subscription_id=subscription_id,
            profile_pic=profile_pic,
            registered_by=registered_by
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, email, mobile, country, birthdate, gender, registered_by, device_token, social_id, subscription_id, profile_pic, is_agree, password=None):
        """
        Creates and saves a superuser with the given email, mobile, gender and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            mobile=mobile,
            gender=gender,
            country=country,
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate,
            is_agree=is_agree,
            device_token=device_token,
            social_id=social_id,
            subscription_id=subscription_id,
            profile_pic=profile_pic,
            registered_by=registered_by
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def upload_to(instance, filename):
    return '/'.join([str(instance), filename])

class User(AbstractBaseUser):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=15)
    country = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.CharField(default='', blank=True, null=True, max_length=100)
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    Register_Choices = (
        ('manual', 'manual'),
        ('facebook', 'facebook'),
        ('gmail', 'gmail'),
        ('apple', 'apple')
    )
    registered_by = models.CharField(max_length=10, choices=Register_Choices)
    device_token = models.CharField(max_length=500, default='', blank=True, null=True)
    social_id = models.CharField(max_length=250, default='', blank=True, null=True)
    subscription_id = models.CharField(default="", max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=upload_to, blank=True, null=True)

    is_agree = models.BooleanField(default=0)
    is_registered = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    # otp = models.CharField(max_length=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'mobile', 'country', 'birthdate', 'gender', 'registered_by', 'device_token', 'social_id', 'subscription_id', 'profile_pic', 'is_agree']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.firstname

    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, "url"):
            return self.profile_pic.url
        else:
            return None

    # def save(self, *args, **kwargs):
    #     number_list = [x for x in range(10)]  # Use of list comprehension
    #     code_items_for_otp = []

    #     for i in range(6):
    #         num = random.choice(number_list)
    #         code_items_for_otp.append(num)

    #     code_string = "".join(str(item)
    #         for item in code_items_for_otp)  # list comprehension again
    #     # A six digit random number from the list will be saved in top field
    #     self.otp = code_string
    #     super().save(*args, **kwargs)

class Subscription(models.Model):
    Subscription_CHOICES = (
        ('regular', 'regular'),
        ('bestdeal', 'bestdeal'),
        ('recommended', 'recommended')
    )
    subscription_type = models.CharField(max_length=11, choices=Subscription_CHOICES)
    subscription_amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)

class Income(models.Model):
    user = models.ForeignKey(User,related_name='income', on_delete=models.CASCADE,to_field="email")
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default="0.00")
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Expense(models.Model):
    user = models.ForeignKey(User, related_name='expense',on_delete=models.CASCADE)
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    amount_limit = models.DecimalField(max_digits=20, decimal_places=2, default="0.00")
    time_range = models.TimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)      

class Goal(models.Model):
    user = models.ForeignKey(User,related_name='goal', on_delete=models.CASCADE)
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default="0.00")
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)        

class Exchangerate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_name = models.CharField(max_length=255)
    is_default=models.BooleanField()

    def __str__(self):
        return str(self.id)           

class Location(models.Model):
    latitude = models.FloatField(blank=True ,null=True)
    longitude = models.FloatField(blank=True ,null=True)

    def __str__(self):
        return str(self.id)

class Periodic(models.Model):
    start_date = models.DateField(blank=True ,null=True)
    end_date = models.DateField(blank=True ,null=True)
    prefix = models.CharField(max_length=255,blank=True ,null=True)
    prefix_value = models.IntegerField(blank=True ,null=True)

    def __str__(self):
        return str(self.id)   

class SourceIncome(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)   



class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tags", default="") 
    name = models.CharField(max_length=255)
    # created_at=models.DateField(auto_now_add=True)
    # modified_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name  

class Transaction(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    income_to = models.ForeignKey(Income, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="transaction_to_income")
    income_from = models.ForeignKey(Income, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="transaction_from_income")
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="transaction_expense")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="transaction_goal")
    source = models.ForeignKey(SourceIncome, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="transaction_source")
    location=models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="location")
    periodic=models.ForeignKey(Periodic, on_delete=models.CASCADE, blank=True, null=True, default="", related_name="periodic")
    tag = models.ManyToManyField(Tag, related_name="tags")
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Setting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True) 
    notification = models.BooleanField()
    min_pass_3 = models.BooleanField()
    language = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    modified_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user  



class Reltionsourceincome(models.Model):
    source_id = models.ForeignKey(SourceIncome, on_delete=models.SET_NULL, blank=True, null=True)
    ins_id = models.ForeignKey(Income, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)       



class Debt(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="") 
    icon = models.CharField(max_length=255,default="")
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.name


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
       
#         [reset_password_token.user.email],
#         print(User.email)
#     )
