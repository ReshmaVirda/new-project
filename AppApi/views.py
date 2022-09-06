# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from calendar import month
from datetime import datetime, timedelta, date as d
import email
from multiprocessing import context
import profile
from telnetlib import LOGOUT

from django import http
from .models import User, Subscription,Income,Expense,Goal,Exchangerate,Transaction,Location,Periodic,Setting,SourceIncome,Reltionsourceincome,Debt,Tag
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# from AppApi.renderer import UserRenderer
from rest_framework.permissions import IsAuthenticated
from AppApi.serializers import  ResetPasswordSerializer,UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, UserSubscriptionSerializer, IncomeSerializer,ExpenseSerializer,GoalsSerializer,ExchangerateSerializer,TransactionSerializer,LocationSerializer,PeriodicSerializer,SettingSerializer,SourceIncomeSerializer,ReltionsourceincomeSerializer,DebtSerializer,TagSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from .mypaginations import MyPageNumberPagination
from rest_framework.generics import ListAPIView
from django.db.models import Count,Sum

from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.core.mail import send_mail
from django.template.loader import get_template
from .utils import render_to_pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
import xlwt

from django.views.decorators.csrf import csrf_protect, csrf_exempt,ensure_csrf_cookie


  
# Create your views here.

# Generate Manual Token Code Start #
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh)
,
      'access': str(refresh.access_token),
  }
# def get_tokens_for_user(user):
#   refresh = RefreshToken.for_user(user)
#   refresh_token = refresh
#   access_token = refresh.access_token

# #   refresh_token.set_exp(lifetime=timedelta(days=60))
# #   access_token.set_exp(lifetime=timedelta(minutes=5))
#   return {
#       'refresh': str(refresh_token),
#       'access': str(access_token),
#   }
# Generate Manual Token Code End #

# User Registration Api Code Start #
class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)#
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = get_tokens_for_user(user)
            user = User.objects.get(email=user)
            country = ''
            birthdate = ''
            device_token = ''
            social_id = ''
            subscription_id = ''
            profile_pic = ''
            
            if user.country != '':
                country = user.country
            else:
                country = "null"

            if user.birthdate != '':
                birthdate = user.birthdate
            else:
                birthdate = "null"

            if user.device_token != '':
                device_token = user.device_token
            else:
                device_token = "null"
            
            if user.social_id != '':
                social_id = user.social_id
            else:
                social_id = "null"

            if user.subscription_id != '':
                subscription_id = user.subscription_id
            else:
                subscription_id = "null"
            
            if user.image_url != None:
                profile_pic = request.build_absolute_uri(user.image_url)
            else:
                profile_pic = "null"
            
            User_data = {
                'id':user.id,
                'firstname':user.firstname,
                'lastname':user.lastname,
                'email':user.email,
                'mobile':user.mobile,
                'gender':user.gender,
                'country':country,
                'birthdate':birthdate,
                'is_agree':user.is_agree,
                'registered_by':user.registered_by,
                'profile_pic':profile_pic,
                'subscription_id':subscription_id,
                'social_id':social_id,
                'device_token':device_token,
                'is_verified':user.is_verified,
                'access_token':token.get('access'),
                'refresh_token':token.get('refresh')
            }
            return Response({"status":True, "message":"Register Successfully", "data":User_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"false", "message":"Some Fields Are Missing"}, status=status.HTTP_400_BAD_REQUEST)
# User Registration Api Code End #

# User Login Api Code Start #
class UserLoginView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                try:
                    user = User.objects.get(email=serializer.data.get('email'))
                except User.DoesNotExist:
                    return Response({"status":"false", "message":"User Detail Not Found"}, status=status.HTTP_404_NOT_FOUND)

                country = ''
                birthdate = ''
                device_token = ''
                social_id = ''
                subscription_id = ''
                profile_pic = ''

                if user.country != '':
                    country = user.country
                else:
                    country = "null"

                if user.birthdate != '':
                    birthdate = user.birthdate
                else:
                    birthdate = "null"

                if user.device_token != '':
                    device_token = user.device_token
                else:
                    device_token = "null"
                
                if user.social_id != '':
                    social_id = user.social_id
                else:
                    social_id = "null"

                if user.subscription_id != '':
                    subscription_id = user.subscription_id
                else:
                    subscription_id = "null"
                
                if user.image_url != None:
                    profile_pic = request.build_absolute_uri(user.image_url)
                else:
                    profile_pic = "null"
             
                User_data = {
                    'id':user.id,
                    'firstname':user.firstname,
                    'lastname':user.lastname,
                    'email':user.email,
                    'mobile':user.mobile,
                    'gender':user.gender,
                    'country':country,
                    'birthdate':birthdate,
                    'is_agree':user.is_agree,
                    'registered_by':user.registered_by,
                    'profile_pic':profile_pic,
                    'subscription_id':subscription_id,
                    'social_id':social_id,
                    'device_token':device_token,
                    'is_verified':user.is_verified,
                    'access_token':token.get('access'),
                    'refresh_token':token.get('refresh')
                }
                return Response({"status":True, "message":"Login Successfully", "data":User_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false", "message":{"non_field_errors":["Email or Password is not valid"]}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":"false", "message":"Some Fields Are Missing"}, status=status.HTTP_400_BAD_REQUEST)
# User Login Api Code End #

# User Profile API Code Start #
class UserProfileView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        country = ''
        birthdate = ''
        profile_pic = ''
        subscription_id = ''
        social_id = ''
        device_token = ''

        if serializer.data.get('country') != '':
            country = serializer.data.get('country')
        else:
            country = 'null'

        if serializer.data.get('birthdate') != '':
            birthdate = serializer.data.get('birthdate')
        else:
            birthdate = 'null'
    
        if serializer.data.get('profile_pic') != None:
            profile_pic = request.build_absolute_uri(serializer.data.get('profile_pic'))
        else:
            profile_pic = 'null'

        if serializer.data.get('subscription_id') != '':
            subscription_id = serializer.data.get('subscription_id')
        else:
            subscription_id = 'null'

        if serializer.data.get('social_id') != '':
            social_id = serializer.data.get('social_id')
        else:
            social_id = 'null'

        if serializer.data.get('device_token') != '':
            device_token = serializer.data.get('device_token')
        else:
            device_token = 'null'

        user_profile = {
            'id':serializer.data.get('id'),
            'firstname':serializer.data.get('firstname'),
            'lastname':serializer.data.get('lastname'),
            'email':serializer.data.get('email'),
            'mobile':serializer.data.get('mobile'),
            'gender':serializer.data.get('gender'),
            'country':country,
            'birthdate':birthdate,
            'is_agree':serializer.data.get('is_agree'),
            'registered_by':serializer.data.get('registered_by'),
            'profile_pic':profile_pic,
            'subscription_id':subscription_id,
            'social_id':social_id,
            'device_token':device_token,
            'is_verified':serializer.data.get('is_verified'),
        }
        return Response({"status":True, "message":"Fetch UserData Successfully", "data":user_profile}, status=status.HTTP_200_OK)
    def put(self, request, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({"status":"false", "message":"User Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            profile = User.objects.get(id=user)
        except User.DoesNotExist:
            return Response({"status":"false", "message":"Subscription Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":True, "message":"update data Successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"false", "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    
# User Profile API Code End #

# User Change Password Code Start #
class UserChangePasswordView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'status':'true', 'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response({'status':'false', 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# User Change Password Code End #

# User Subscription API Code Start #
class UserSubscriptionView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserSubscriptionSerializer(data=request.data, context={'request':request})#
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":True, "message":"Subscribed Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"false", "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({"status":"false", "message":"User Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
    
        try:
            subscription_data = Subscription.objects.get(user_id=user)
        except Subscription.DoesNotExist:
            return Response({"status":"false", "message":"Subscription Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSubscriptionSerializer(subscription_data, many=False)
        return Response({"status":True, "message":"Retrieve data Successfully", "data":serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({"status":"false", "message":"User Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            subscription_data = Subscription.objects.get(user_id=user)
        except Subscription.DoesNotExist:
            return Response({"status":"false", "message":"Subscription Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSubscriptionSerializer(subscription_data, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":True, "message":"update data Successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"false", "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# User Subscription API Code End #

# User Income API Code Start #
class IncomeCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        serializer = IncomeSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=False):
            if (('is_setup' in request.data and request.data['is_setup'] != "") and ('setupcount' in request.data and request.data['setupcount'] != "")):
                User.objects.filter(email=request.user).update(is_setup=request.data['is_setup'], setup_count=request.data['setupcount'], is_registered=True)
            serializer.save()
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"Add Income Successfully"}), email=request.user, status=True)
            return Response({"status":True, "message":"Add Income Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            message = ''
            if 'icon' in serializer.errors:
                message = "icon is the required and cannot be blank"
            elif 'title' in serializer.errors:
                message = "title is the required and cannot be blank"
            elif 'amount' in serializer.errors:
                message = "amount is required and cannot be blank"
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':serializer.errors}), email=request.user, status=False)
            return Response({'status':False, 'message':message}, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request, pk=None, format=None):
        Incomes = ''
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user data not found'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            Incomes = Income.objects.filter(user=user)
        except Income.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any income detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any income detail'}, status=status.HTTP_404_NOT_FOUND)

        if pk is not None and pk != "":
            Incomes = Income.objects.filter(user=user, id=pk)
            if len(Incomes) <= 0:
                # header = {
                #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not income with id %s'%(pk)}), email=request.user, status=False)
                return Response({'status':False, 'message':'user have not income with id %s'%(pk)}, status=status.HTTP_404_NOT_FOUND)

        Incomeserializer = IncomeSerializer(Incomes, many=True)
        # header = {
        #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        # }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"Retrieve income data Successfully", "data":Incomeserializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"Retrieve data Successfully", "data":Incomeserializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        if pk is not None and pk != "":
            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':'user data not found'}), email=request.user, status=False)
                return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                income = Income.objects.get(id=pk, user_id=user)
            except Income.DoesNotExist:
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':'user have not any income with id'+pk}), email=request.user, status=False)
                return Response({'status':False, 'message':'user have not any income with id '+pk}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = IncomeSerializer(income, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                if request.data != {}:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"update data Successfully", "data":serializer.data}), email=request.user, status=True)
                    return Response({"status":True, "message":"update data Successfully", "data":serializer.data}, status=status.HTTP_205_RESET_CONTENT)
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"Changes are not occured", "data":serializer.data}), email=request.user, status=True)
                    return Response({"status":True, "message":"Changes are not occured", "data":serializer.data}, status=status.HTTP_205_RESET_CONTENT)
            else:
                message = ""
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }

                if ('title' in serializer.errors and serializer.errors['title'][0] == "This field may not be blank."):
                    message = "title cannot be blank"

                if ('icon' in serializer.errors and serializer.errors['icon'][0] == "This field may not be blank."):
                    message = "icon cannot be blank"

                if ('amount' in serializer.errors and serializer.errors['amount'][0] == "A valid integer is required."):
                    message = "amount cannot be blank and must be an integer"
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":message}), email=request.user, status=False)   
                return Response({"status":False, "message":message}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':'provide income id in url/<id>'}), email=request.user, status=False)   
            return Response({'status':False, 'message':'provide income id in url/<id>'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,format=None):
        if request.query_params != {}:
            try:
                user = User.objects.get(email=request.user)
            except User.DoesNotExist:
                    # header = {
                    #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    # }
                    # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user data not found'}), email=request.user, status=False)
                    return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
            print(user, "user")   
            try:
                income = Income.objects.filter(user_id=user.email, id=str(request.query_params.get('id')))
            except Income.DoesNotExist:
            #     header = {
            # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            #     LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
                return Response({"status":False, "message":"user have not any income data"},status=status.HTTP_404_NOT_FOUND)

            ### Fetch All Transaction ###
            transactions = Transaction.objects.filter(income_from_id=income[0].id)
            for x in transactions:
                if x.income_to_id is not None:
                    income_to_data = Income.objects.filter(id=x.income_to_id)
                    update_amount = int(income_to_data[0].amount) - int(x.amount)
                    income_to_data.update(amount=update_amount)

                if x.expense_id is not None:
                    expense = Expense.objects.filter(id=x.expense_id)
                    update_amount = int(expense[0].amount_limit) - int(x.amount)
                    expense.update(amount_limit=update_amount)

                if x.goal_id is not None:
                    goal_data = Goal.objects.filter(id=x.goal_id)
                    update_amount = int(goal_data[0].amount) - int(x.amount)
                    goal_data.update(amount=update_amount)


            
            transactions = Transaction.objects.filter(income_to_id=income[0].id)
            for x in transactions:
                if x.source_id is not None:
                    source_data = SourceIncome.objects.filter(id=x.source_id)
                    update_amount = int(source_data[0].amount) + int(x.amount)
                    source_data.update(amount=update_amount)
                
                if x.location_id is not None:
                    location_data = Location.objects.filter(id=x.location_id)
                    location_data.delete()
                
                if x.periodic_id is not None:
                    periodic_data = Periodic.objects.filter(id=x.periodic_id)
                    periodic_data.delete()
            
            income.delete()
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #         }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"income data was successfully delete"}), email=request.user, status=True)
            return Response({"status":True,"message":"income data was successfully delete"},status=status.HTTP_200_OK)
        else:
            # header = {
            # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide exchangerate id in request parameter"}), email=request.user, status=False)
            return Response({"status":False, "message":"provide income id in request parameter"},status=status.HTTP_404_NOT_FOUND)
# User Income API Code End #  


 

# User Expens API Code start # 
class ExpenseCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":True, "message":"Add Expense Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"false", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        user = request.user
        if user is not None:
            Expenses = Expense.objects.filter(user=user)
            
        Expenseserializer = ExpenseSerializer(Expenses, many=True)
        return Response({"status":True, "message":"Retrieve data Successfully", "data":Expenseserializer.data}, status=status.HTTP_201_CREATED)   
   
# User Expens API Code End # 

# User goal API Code start #
class GoalsCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GoalsSerializer(data=request.data, context={'request':request})
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"status":True, "message":"Add Goal Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
           
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        try:
            goal = Goal.objects.filter(user=user)
        except Goal.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any goal data"}), email=request.user, status=False)
            return Response({"status":False, "message":"user have not any goal data"},status=status.HTTP_404_NOT_FOUND)
        
        if request.query_params != {}:
            goal_id = request.query_params.get('id', None)
            if goal_id is not None and goal_id != '':
                try:
                    goal = Goal.objects.filter(user=user, id=goal_id)
                except Goal.DoesNotExist:
                #     header = {
                # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                #     LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any goal data"}), email=request.user, status=False)
                    return Response({"status":False, "message":"user have not any goal data"})
            else:
                # header = {
                # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide goal id in request parameter"}), email=request.user, status=False)
                return Response({"status":False, "message":"provide goal id in request parameter"})


        goal_serializer = GoalsSerializer(goal, many=True)
        # header = {
        #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #         }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"goal data Fetched Succcessfully","data":goal_serializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"goal data Fetched Succcessfully", "data":goal_serializer.data})

    def put(self, request):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        if request.query_params != {}:
            goal_id = request.query_params.get('id', None)
            if goal_id is not None and goal_id != '':
                try:
                    goal = Goal.objects.get(user=user, id=goal_id)
                except Goal.DoesNotExist:
                #     header = {
                # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                #     LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"user have not any goal data"}), email=request.user, status=False)
                    return Response({"status":False, "message":"user have not any goal data"},status=status.HTTP_404_NOT_FOUND)
            else:
                # header = {
                # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"provide goal id in request parameter"}), email=request.user, status=False)
                return Response({"status":False, "message":"provide goal id in request parameter"},status=status.HTTP_404_NOT_FOUND)

        serializer = GoalsSerializer(goal,data=request.data)
        if serializer.is_valid():
            serializer.save()
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"goal data updated successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True, "message":"goal data updated successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":""}), email=request.user, status=False)
            return Response({"status":False,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,format=None):
        if request.query_params != {}:
            try:
                user = User.objects.get(email=request.user)
            except User.DoesNotExist:
                    # header = {
                    #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    # }
                    # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user data not found'}), email=request.user, status=False)
                    return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
            print(user, "user")   
            try:
                goal = Goal.objects.filter(user_id=user.id, id=str(request.query_params.get('id')))
            except Goal.DoesNotExist:
            #     header = {
            # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            #     LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any goal data"}), email=request.user, status=False)
                return Response({"status":False, "message":"user have not any goal data"},status=status.HTTP_404_NOT_FOUND)

            ### Fetch All Transaction ###
            transactions = Transaction.objects.filter(goal_id=goal[0].id)
            for x in transactions:

                if x.income_from_id is not None:
                    income_data = Income.objects.filter(id=x.income_from_id)
                    update_amount = int(income_data[0].amount) + int(x.amount)
                    income_data.update(amount=update_amount)

                if x.location_id is not None:
                    location_data = Location.objects.filter(id=x.location_id)
                    location_data.delete()
                
                if x.periodic_id is not None:
                    periodic_data = Periodic.objects.filter(id=x.periodic_id)
                    periodic_data.delete()


            goal.delete()
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #         }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"goal data was successfully delete"}), email=request.user, status=True)
            return Response({"status":True,"message":"goal data was successfully delete"},status=status.HTTP_200_OK)
        else:
            # header = {
            # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide goal id in request parameter"}), email=request.user, status=False)
            return Response({"status":False, "message":"provide goal id in request parameter"},status=status.HTTP_404_NOT_FOUND)



# User goal API Code End # 

# User Exchange API Code Start#
class ExchangerateCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = ExchangerateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # user=request.MyUser.id
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':True, 'message':"Exchangerate data add successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':""}), email=request.user, status=False)
            return Response({"status":False, "data":serializer.error}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
         
        exchangerate = ''
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
           
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        try:
            exchangerate = Exchangerate.objects.filter(user=user)
        except Exchangerate.DoesNotExist:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
            return Response({"status":False, "message":"user have not any exchangerate data"},status=status.HTTP_404_NOT_FOUND)
        
        if request.query_params != {}:
            exchangerate_id = request.query_params.get('id', None)
            if exchangerate_id is not None and exchangerate_id != '':
                try:
                    exchangerate = Exchangerate.objects.filter(user=user, id=exchangerate_id)
                except Exchangerate.DoesNotExist:
                    header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
                    return Response({"status":False, "message":"user have not any exchangerate data"})
            else:
                header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide exchangerate id in request parameter"}), email=request.user, status=False)
                return Response({"status":False, "message":"provide exchangerate id in request parameter"})


        exchangerate_serializer = ExchangerateSerializer(exchangerate, many=True)
        header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
        LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"Exchangerate data Fetched Succcessfully","data":exchangerate_serializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"Exchangerate data Fetched Succcessfully", "data":exchangerate_serializer.data})


    def put(self, request):
         # print(request)
        exchangerate = ''
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        if request.query_params != {}:
            exchangerate_id = request.query_params.get('id', None)
            if exchangerate_id is not None and exchangerate_id != '':
                try:
                    exchangerate = Exchangerate.objects.get(user=user, id=exchangerate_id)
                except Exchangerate.DoesNotExist:
                    header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
                    return Response({"status":False, "message":"user have not any exchangerate data"},status=status.HTTP_404_NOT_FOUND)
            else:
                header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"provide exchangerate id in request parameter"}), email=request.user, status=False)
                return Response({"status":False, "message":"provide exchangerate id in request parameter"},status=status.HTTP_404_NOT_FOUND)

        serializer = ExchangerateSerializer(exchangerate,data=request.data)
        if serializer.is_valid():
            serializer.save()
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"Exchangerate data updated successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True, "message":"Exchangerate data updated successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"Exchangerate data updated successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":False,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

    
    def delete(self, request):
         # print(request)
        exchangerate = ''
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        if request.query_params != {}:
            exchangerate_id = request.query_params.get('id', None)
            if exchangerate_id is not None and exchangerate_id != '':
                try:
                    exchangerate = Exchangerate.objects.filter(user=user, id=exchangerate_id)
                except Exchangerate.DoesNotExist:
                    header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
                    return Response({"status":False, "message":"user have not any exchangerate data"},status=status.HTTP_404_NOT_FOUND)
            else:
                header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide exchangerate id in request parameter"}), email=request.user, status=False)
                return Response({"status":False, "message":"provide exchangerate id in request parameter"},status=status.HTTP_404_NOT_FOUND)

        exchangerate.delete()
        header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
        LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"Exchangerate data was successfully delete"}), email=request.user, status=True)
        return Response({"status":True,"message":"Exchangerate data was successfully delete"},status=status.HTTP_200_OK)


        

    
# User Exchange API Code end#

# User Transaction API Code Start#
class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,  request, pk=None, format=None):
        data_dict = {}
        data = {}
        if request.data != {}:
            location_serializer = ''
            periodicSerializer = ''
            status_days = ""
            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                return Response({"status":False, "message":"User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            if ('longitude' in request.data and 'latitude' in request.data and request.data["longitude"] != 0 and request.data["latitude"] != 0):
                
                data = {
                    "longitude":request.data['longitude'],
                    "latitude":request.data['latitude']
                }  
                location_serializer = LocationSerializer(data=data) 
                if location_serializer.is_valid(raise_exception=True):
                    location_serializer.save()
                else:
                    message = ""
                    if 'latitude' in location_serializer.errors:
                        message = "latitude cannot be blank must be double max_length 15 digit."
                    
                    if 'longitude' in location_serializer.errors:
                        message = "longitude cannot be blank must be double max_length 15 digit."
                    return Response({"status":False, "message":message},status=status.HTTP_400_BAD_REQUEST)   
        
            if ('start_date' in request.data and 'end_date' in request.data and 'prefix' in request.data and 'prefix_value' in request.data and request.data["start_date"] != 0 and request.data["end_date"] != 0 and request.data["prefix"] != 0 and request.data["prefix_value"] != 0):

                if 'week_days' in request.data and request.data["week_days"] != "":
                    Date_List = str(request.data["week_days"]).split(",")
                    for x in Date_List:
                        x = False
                        status_list.append(str(x))
                    status_days = ','.join(status_list)
                    data = {
                        "start_date":request.data['start_date'],
                        "end_date":request.data['end_date'],
                        "prefix":request.data['prefix'],
                        "prefix_value":request.data['prefix_value'],
                        "week_days":request.data["week_days"],
                        "status_days":status_days
                    }  
                else:
                    # Changes Server #
                    start_date = None
                    if request.data['start_date'] != "":
                        start_date = request.data['start_date']
                    else:
                        start_date = date.today()

                    if "month" in request.data['prefix'] and request.data['prefix_value'] != 0:
                        del status_list[:]
                        Date_Dict = Get_Dates(prefix=request.data['prefix'], prefix_value=int(request.data['prefix_value']), enddate=request.data['end_date'], startdate=start_date)
                        print(Date_Dict)
                        Date_List = Date_Dict["Date_Months"].split(",")
                        for x in Date_List:
                            x = False
                            status_list.append(str(x))
                        status_days = ','.join(status_list)
                        data = {
                            "start_date":start_date,
                            "end_date":request.data['end_date'],
                            "prefix":request.data['prefix'],
                            "prefix_value":request.data['prefix_value'],
                            "week_days":Date_Dict["Date_Months"],
                            "status_days":status_days
                        }

                    elif "year" in request.data['prefix'] and request.data['prefix_value'] != 0:
                        del status_list[:]
                        Date_Dict = Get_Dates(prefix=request.data['prefix'], prefix_value=int(request.data['prefix_value']), enddate=request.data['end_date'], startdate=start_date)
                        Date_List = Date_Dict["Date_Years"].split(",")
                        for x in Date_List:
                            x = False
                            status_list.append(str(x))
                        status_days = ','.join(status_list)
                        data = {
                            "start_date":start_date,
                            "end_date":request.data['end_date'],
                            "prefix":request.data['prefix'],
                            "prefix_value":request.data['prefix_value'],
                            "week_days":Date_Dict["Date_Years"],
                            "status_days":status_days
                        }

                    elif "day" in request.data['prefix'] and request.data['prefix_value'] != 0:
                        del status_list[:]
                        Date_Dict = Get_Dates(prefix=request.data['prefix'], prefix_value=int(request.data['prefix_value']), enddate=request.data['end_date'], startdate=start_date)
                        Date_List = Date_Dict["Date_Days"].split(",")
                        for x in Date_List:
                            x = False
                            status_list.append(str(x))
                        status_days = ','.join(status_list)
                        data = {
                            "start_date":start_date,
                            "end_date":request.data['end_date'],
                            "prefix":request.data['prefix'],
                            "prefix_value":request.data['prefix_value'],
                            "week_days":Date_Dict["Date_Days"],
                            "status_days":status_days
                        }
                    else:
                        return Response({"status":False, "message":"prefix_value cannot be blank must be integer"}, status=status.HTTP_400_BAD_REQUEST)
                    # Changes on server # 
                periodicSerializer = PeriodicSerializer(data=data) 
                if periodicSerializer.is_valid(raise_exception=False):
                    periodicSerializer.save()
                else:
                    message = ""
                    if 'start_date' in periodicSerializer.errors:
                        message = "provide valid date yyyy-mm-dd."
                    if 'end_date' in periodicSerializer.errors:
                        message = "provide valid date yyyy-mm-dd."
                    if 'week_days' in periodicSerializer.errors:
                        message = "week_days cannot be blank and must be comma saparated string like 2022-07-12,2022-07-13."
                    if 'prefix' in periodicSerializer.errors:
                        message = "prefix cannot be blank must be string choice like day,month,year,week."
                    if 'prefix_value' in periodicSerializer.errors:
                        message="prefix_value must be integer."
                    if 'status_days' in periodicSerializer.errors:
                        message = "status_days cannot be blank must be comma saparated string like false,false,false."
                    return Response({"status":False, "message":message}, status=status.HTTP_400_BAD_REQUEST)

            if (('amount' in request.data and 'source' in request.data and 'income_to' in request.data) and ('income_from' not in request.data) and ('expense' not in request.data) and ('goal' not in request.data)):
                if (request.data["amount"] != "" and request.data["source"] != ""  and request.data["income_to"] != ""):
                    if 'title' not in request.data or request.data['title'] == "":
                        title = None
                    else:
                        title = request.data['title']

                    if 'description' not in request.data or request.data['description'] == "":
                        description = None
                    else:
                        description = request.data['description']

                    try:
                        source = SourceIncome.objects.get(user_id=user, id=str(request.data["source"]))
                    except SourceIncome.DoesNotExist:
                        return Response({"status":False, "message":"User haven't any source income by id %s"%(request.data["source"])}, status=status.HTTP_404_NOT_FOUND)
                    
                    try:
                        income = Income.objects.get(user_id=user, id=str(request.data["income_to"]))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"User haven't any income by id %s"%(request.data["income_to"])}, status=status.HTTP_404_NOT_FOUND)
                    
                    source_amount = float(source.spent_amount) + float(request.data["amount"])
                    income_amount = float(income.amount) + float(request.data["amount"])

                    if location_serializer != "" and periodicSerializer == "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "source":source.id,
                            "income_to":income.id,
                            "location":location_serializer.data.get('id')
                        }
                    elif location_serializer == "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "source":source.id,
                            "income_to":income.id,
                            "periodic":periodicSerializer.data.get('id')
                        }
                    elif location_serializer != "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "source":source.id,
                            "income_to":income.id,
                            "location":location_serializer.data.get('id'),
                            "periodic":periodicSerializer.data.get('id')
                        }
                    else:
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "source":source.id,
                            "income_to":income.id
                        }

                    if 'tags' in request.data and request.data["tags"] != []:
                        data_dict.update({"tag":request.data["tags"]})

                    if 'created_at' in request.data and "modified_at" in request.data:
                        data_dict.update({"created_at":request.data["created_at"]})
                        data_dict.update({"modified_at":request.data["modified_at"]})

                    if 'is_completed' in request.data:
                        data_dict.update({"is_completed":request.data["is_completed"]})
                    
                    transaction_serializer = TransactionSerializer(data=data_dict, context={"user":user})
                    if transaction_serializer.is_valid(raise_exception=False):
                        transaction_id = transaction_serializer.save()
                        if len(str(transaction_id)) > 0 and transaction_id is not None:
                            SourceIncome.objects.filter(title=source.title, id=source.id, user_id=user).update(spent_amount=source_amount)
                            Income.objects.filter(title=income.title, id=income.id, user_id=user).update(amount=income_amount)
                        else:
                            return Response({"status":False, "message":" transaction fail from Source %s to Income %s"%(source.title, income.title)}, status=status.HTTP_400_BAD_REQUEST)
                        # changes on server #
                        transaction_dict = transaction_serializer.data
                        transaction_dict["income_to_name"] = income.title
                        transaction_dict["source_name"] = source.title

                        if periodicSerializer != "" and location_serializer == "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                        elif periodicSerializer == "" and location_serializer != "":
                            transaction_dict.update({"location":location_serializer.data})
                        elif periodicSerializer != "" and location_serializer != "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                            transaction_dict.update({"location":location_serializer.data})
                       
                        # changes on server #
                        return Response({"status":True, "message":"Transfer amount from source %s to income %s"%(source.title, income.title), "data":transaction_dict}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":False, "message":"amount, income_to, source are required fields. title and description is optional"}, status=status.HTTP_400_BAD_REQUEST)

            elif (('amount' in request.data and 'income_from' in request.data and 'income_to' in request.data) and ('source' not in request.data) and ('expense' not in request.data) and ('goal' not in request.data)):
                if (request.data["amount"] != "" and request.data["income_from"] != "" and request.data["income_to"] != ""):
                    
                    if 'title' not in request.data or request.data['title'] == "":
                        title = None
                    else:
                        title = request.data['title']

                    if 'description' not in request.data or request.data['description'] == "":
                        description = None
                    else:
                        description = request.data['description']
                    
                    try:
                        income_from = Income.objects.get(user_id=user, id=str(request.data['income_from']))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"From Income detail not found by id %s"%(request.data['income_from'])}, status=status.HTTP_404_NOT_FOUND)

                    try:
                        income_to = Income.objects.get(user_id=user, id=str(request.data['income_to']))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"To Income detail not found by id %s"%(request.data['income_to'])}, status=status.HTTP_404_NOT_FOUND)

                    income_from_amount = float(income_from.amount) - float(request.data["amount"])
                    income_to_amount = float(income_to.amount) + float(request.data["amount"])

                    if location_serializer != "" and periodicSerializer == "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income_from.id,
                            "income_to":income_to.id,
                            "location":location_serializer.data.get('id')
                        }
                    elif location_serializer == "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income_from.id,
                            "income_to":income_to.id,
                            "periodic":periodicSerializer.data.get('id')
                        }
                    elif location_serializer != "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income_from.id,
                            "income_to":income_to.id,
                            "location":location_serializer.data.get('id'),
                            "periodic":periodicSerializer.data.get('id')
                        }
                    else:
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income_from.id,
                            "income_to":income_to.id
                        }

                    if 'tags' in request.data and request.data["tags"] != []:
                        data_dict.update({"tag":request.data["tags"]})

                    if 'created_at' in request.data and "modified_at" in request.data:
                        data_dict.update({"created_at":request.data["created_at"]})
                        data_dict.update({"modified_at":request.data["modified_at"]})
                        
                    if 'is_completed' in request.data:
                        data_dict.update({"is_completed":request.data["is_completed"]})
                
                    transaction_serializer = TransactionSerializer(data=data_dict, context={"user":user})
                    if transaction_serializer.is_valid(raise_exception=False):
                        transaction_id = transaction_serializer.save()
                        if len(str(transaction_id)) > 0 and transaction_id is not None:
                            Income.objects.filter(title=income_from.title, id=income_from.id, user_id=user).update(amount=income_from_amount)
                            Income.objects.filter(title=income_to.title, id=income_to.id, user_id=user).update(amount=income_to_amount)
                        else:
                            return Response({"status":False, "message":" transaction fail from Income %s to Income %s"%(income_from.title, income_to.title)}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # changes on server #
                        transaction_dict = transaction_serializer.data
                        transaction_dict["income_from_name"] = income_from.title
                        transaction_dict["income_to_name"] = income_to.title

                        if periodicSerializer != "" and location_serializer == "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                        elif periodicSerializer == "" and location_serializer != "":
                            transaction_dict.update({"location":location_serializer.data})
                        elif periodicSerializer != "" and location_serializer != "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                            transaction_dict.update({"location":location_serializer.data})
                        # changes on server #
                        return Response({"status":True, "message":"Transfer amount from Income %s to Income %s"%(income_from.title, income_to.title), "data":transaction_dict}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":False, "message":"amount, income_from, income_to are required fields. title and description is optional"}, status=status.HTTP_400_BAD_REQUEST)
            
            elif (('amount' in request.data and 'income_from' in request.data and 'goal' in request.data) and ('source' not in request.data) and ('expense' not in request.data) and ('income_to' not in request.data)): 
                if (request.data["amount"] != "" and request.data["income_from"] != "" and request.data["goal"] != ""):
                    
                    if 'title' not in request.data or request.data['title'] == "":
                        title = None
                    else:
                        title = request.data['title']

                    if 'description' not in request.data or request.data['description'] == "":
                        description = None
                    else:
                        description = request.data['description']
                    
                    try:
                        income = Income.objects.get(user_id=user, id=str(request.data["income_from"]))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"Income detail not found by id %s"%(request.data["income_from"])}, status=status.HTTP_404_NOT_FOUND)

                    try:
                        goal = Goal.objects.get(user_id=user, id=str(request.data["goal"]))
                    except Goal.DoesNotExist:
                        return Response({"status":False, "message":"Goal detail not found by id %s"%(request.data["goal"])}, status=status.HTTP_404_NOT_FOUND)

                    income_amount = float(income.amount) - float(request.data["amount"])
                    goal_amount = float(goal.added_amount) + float(request.data["amount"])

                    if location_serializer != "" and periodicSerializer == "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "goal":goal.id,
                            "location":location_serializer.data.get('id')
                        }
                    elif location_serializer == "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "goal":goal.id,
                            "periodic":periodicSerializer.data.get('id')
                        }
                    elif location_serializer != "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "goal":goal.id,
                            "location":location_serializer.data.get('id'),
                            "periodic":periodicSerializer.data.get('id')
                        }
                    else:
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "goal":goal.id
                        }

                    if 'tags' in request.data and request.data["tags"] != []:
                        data_dict.update({"tag":request.data["tags"]})

                    if 'created_at' in request.data and "modified_at" in request.data:
                        data_dict.update({"created_at":request.data["created_at"]})
                        data_dict.update({"modified_at":request.data["modified_at"]})
                        
                    if 'is_completed' in request.data:
                        data_dict.update({"is_completed":request.data["is_completed"]})

                    transaction_serializer = TransactionSerializer(data=data_dict, context={"user":user})
                    if transaction_serializer.is_valid(raise_exception=False):
                        if goal.amount != goal.added_amount and not goal.is_completed:
                            transaction_id = transaction_serializer.save()
                            if len(str(transaction_id)) > 0 and transaction_id is not None:
                                Income.objects.filter(title=income.title, id=income.id, user_id=user).update(amount=income_amount)
                                Goal.objects.filter(title=goal.title, id=goal.id, user_id=user).update(added_amount=goal_amount)
                            else:
                                return Response({"status":False, "message":" transaction fail from Income %s to Goal %s"%(income.title, goal.title)}, status=status.HTTP_400_BAD_REQUEST)
                        
                            # changes on server #
                            transaction_dict = transaction_serializer.data
                            transaction_dict["income_from_name"] = income.title
                            transaction_dict["goal_name"] = goal.title

                            if periodicSerializer != "" and location_serializer == "":
                                transaction_dict.update({"periodic":periodicSerializer.data})
                            elif periodicSerializer == "" and location_serializer != "":
                                transaction_dict.update({"location":location_serializer.data})
                            elif periodicSerializer != "" and location_serializer != "":
                                transaction_dict.update({"periodic":periodicSerializer.data})
                                transaction_dict.update({"location":location_serializer.data})
                            # changes on server #
                            return Response({"status":True, "message":"Transfer amount from Income %s to Goal %s"%(income.title, goal.title), "data":transaction_dict}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"status":False, "message":"Goal is Completed"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":False, "message":"amount, income_from, goal are required fields. title and description is optional"}, status=status.HTTP_400_BAD_REQUEST)
            
            elif (('amount' in request.data and 'income_from' in request.data and 'expense' in request.data) and ('source' not in request.data) and ('goal' not in request.data) and ('income_to' not in request.data)):
                if (request.data["amount"] != "" and request.data["income_from"] != "" and request.data["expense"] != ""):
                    
                    if 'title' not in request.data or request.data['title'] == "":
                        title = None
                    else:
                        title = request.data['title']

                    if 'description' not in request.data or request.data['description'] == "":
                        description = None
                    else:
                        description = request.data['description']
                    
                    try:
                        income = Income.objects.get(user_id=user, id=str(request.data["income_from"]))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"Income doesn't exist with id %s"%(request.data["income_from"])}, status=status.HTTP_404_NOT_FOUND)

                    try:
                        expense = Expense.objects.get(user_id=user, id=str(request.data["expense"]))
                    except Expense.DoesNotExist:
                        return Response({"status":False, "message":"Expense doesn't exist with id %s"%(request.data["expense"])}, status=status.HTTP_404_NOT_FOUND)

                    income_amount = float(income.amount) - float(request.data["amount"])
                    expense_amount = float(expense.spent_amount) + float(request.data["amount"])

                    if location_serializer != "" and periodicSerializer == "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "expense":expense.id,
                            "location":location_serializer.data.get('id')
                        }
                    elif location_serializer == "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "expense":expense.id,
                            "periodic":periodicSerializer.data.get('id')
                        }
                    elif location_serializer != "" and periodicSerializer != "":
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "expense":expense.id,
                            "location":location_serializer.data.get('id'),
                            "periodic":periodicSerializer.data.get('id')
                        }
                    else:
                        data_dict ={
                            "title":title,
                            "description":description,
                            "amount":request.data["amount"],
                            "income_from":income.id,
                            "expense":expense.id
                        }
                    
                    if 'tags' in request.data and request.data["tags"] != []:
                        data_dict.update({"tag":request.data["tags"]})

                    if 'created_at' in request.data and "modified_at" in request.data:
                        data_dict.update({"created_at":request.data["created_at"]})
                        data_dict.update({"modified_at":request.data["modified_at"]})
                        
                    if 'is_completed' in request.data:
                        data_dict.update({"is_completed":request.data["is_completed"]})

                    transaction_serializer = TransactionSerializer(data=data_dict, context={"user":user})
                    if transaction_serializer.is_valid(raise_exception=False):
                        transaction_id = transaction_serializer.save()
                        if len(str(transaction_id)) > 0 and transaction_id is not None:
                            Income.objects.filter(title=income.title, id=income.id, user_id=user).update(amount=income_amount)
                            Expense.objects.filter(title=expense.title, id=expense.id, user_id=user).update(spent_amount=expense_amount)
                        else:
                            return Response({"status":False, "message":" transaction fail from Income %s to expense %s"%(income.title, expense.title)}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # changes on server #
                        transaction_dict = transaction_serializer.data

                        transaction_dict["income_from_name"] = income.title
                        transaction_dict["expense_name"] = expense.title

                        if periodicSerializer != "" and location_serializer == "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                        elif periodicSerializer == "" and location_serializer != "":
                            transaction_dict.update({"location":location_serializer.data})
                        elif periodicSerializer != "" and location_serializer != "":
                            transaction_dict.update({"periodic":periodicSerializer.data})
                            transaction_dict.update({"location":location_serializer.data})
                        # changes on server #
                        return Response({"status":True, "message":"Transfer amount from Income %s to expense %s"%(income.title, expense.title), "data":transaction_dict}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":False, "message":"amount, income_from, expense are required fields. title and description is optional"}, status=status.HTTP_400_BAD_REQUEST)     
        
            elif (('amount' in request.data and 'income_from' in request.data and 'debt' in request.data) and ('source' not in request.data) and ('goal' not in request.data) and ('income_to' not in request.data) and ('expense' not in request.data)):
                if (request.data["amount"] != "" and request.data["income_from"] != "" and request.data["debt"] != ""):
                    
                    if 'title' not in request.data or request.data['title'] == "":
                        title = None
                    else:
                        title = request.data['title']

                    if 'description' not in request.data or request.data['description'] == "":
                        description = None
                    else:
                        description = request.data['description']
                    
                    try:
                        income = Income.objects.get(user_id=user, id=str(request.data["income_from"]))
                    except Income.DoesNotExist:
                        return Response({"status":False, "message":"Income doesn't exist with id %s"%(request.data["income_from"])}, status=status.HTTP_404_NOT_FOUND)

                    try:
                        debt = Debt.objects.get(user_id=user, id=str(request.data["debt"]))
                    except Debt.DoesNotExist:
                        return Response({"status":False, "message":"Debt doesn't exist with id %s"%(request.data["debt"])}, status=status.HTTP_404_NOT_FOUND)

                    income_amount = float(income.amount) - float(request.data["amount"])
                    debt_amount = ""
                    if float(debt.amount) == float(request.data["amount"]):
                        debt_amount = float(debt.paid_amount) + float(request.data["amount"])
                    else:
                        if float(request.data["amount"]) < float(debt.amount):
                            debt_amount = float(debt.paid_amount) + float(request.data["amount"])
                        else:
                            return Response({"status":False, "message":"Paid amount %s is grater then the Debt amount %s"%(request.data["amount"], debt.amount)}, status=status.HTTP_400_BAD_REQUEST)

                    data_dict ={
                        "title":title,
                        "description":description,
                        "amount":request.data["amount"],
                        "income_from":income.id,
                        "debt":debt.id
                    }
                    
                    if 'created_at' in request.data and "modified_at" in request.data:
                        data_dict.update({"created_at":request.data["created_at"]})
                        data_dict.update({"modified_at":request.data["modified_at"]})

                    transaction_serializer = TransactionSerializer(data=data_dict, context={"user":user})
                    if transaction_serializer.is_valid(raise_exception=False):
                        transaction_id = transaction_serializer.save()
                        if transaction_id > 0 and transaction_id is not None:
                            Income.objects.filter(title=income.title, id=income.id, user_id=user).update(amount=income_amount)
                            if float(debt.amount) == float(request.data["amount"]):
                                Debt.objects.filter(name=debt.name, id=debt.id, user_id=user).update(paid_amount=debt_amount)
                            else:
                                if float(request.data["amount"]) < float(debt.amount):
                                    if float(debt_amount) == float(debt.amount):
                                        Debt.objects.filter(name=debt.name, id=debt.id, user_id=user).update(paid_amount=debt_amount)
                                    Debt.objects.filter(name=debt.name, id=debt.id, user_id=user).update(paid_amount=debt_amount, is_partial_paid=True)
                        else:
                            return Response({"status":False, "message":" transaction fail from Income %s to debt %s"%(income.title, debt.name)}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # changes on server #
                        transaction_dict = transaction_serializer.data
                        transaction_dict["income_from_name"] = income.title
                        transaction_dict["debt_paid_to"] = debt.name
                        # changes on server #
                        return Response({"status":True, "message":"Transfer amount from Income %s to debt %s"%(income.title, debt.name), "data":transaction_dict}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":False, "message":"amount, income_from, debt are required fields. title and description is optional"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False, "message":"Invalid data Passed"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):

        if pk is not None and pk != "":
            goal = ''
            income_from = ''
            income_to = ''
            source = ''
            expense = ''
            debt = ''
            location=''
            data_dict=''
            location_dict = {}
            periodic_dict = {}
            

            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                return Response({"status":False, "message":"User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                transaction = Transaction.objects.get(user_id=user, id=pk)
            except Transaction.DoesNotExist:
                return Response({"status":False, "message":"Transaction detail not found with id %s"%(pk)}, status=status.HTTP_404_NOT_FOUND)

            if transaction.income_from_id is not None:
                income_from = Income.objects.filter(user_id=user, id=transaction.income_from_id) 
            
            if transaction.income_to_id is not None:
                income_to = Income.objects.filter(user_id=user, id=transaction.income_to_id)

            if transaction.goal_id is not None:
                goal = Goal.objects.filter(user_id=user, id=transaction.goal_id)

            if transaction.source_id is not None:
                source = SourceIncome.objects.filter(user_id=user, id=transaction.source_id)

            if transaction.expense_id is not None:
                expense = Expense.objects.filter(user_id=user, id=transaction.expense_id)

            # if transaction.debt_id is not None:
            #     debt = Debt.objects.filter(user_id=user, id=transaction.debt_id)
            
            if transaction.location_id is not None:
                print("A")
                location = Location.objects.filter(id=transaction.location_id)
                if (('longitude' in request.data and request.data["longitude"] != "") and ('latitude' in request.data and request.data["latitude"] != "")):
                    location_dict["longitude"] = request.data.pop("longitude")
                    location_dict["latitude"] = request.data.pop("latitude")
                    location_serializer = LocationSerializer(location, data=location_dict)
                    if location_serializer.is_valid():
                        location_serializer.save()
                    else:
                        print(location_serializer.errors)
            else:
                print("B")
                if (('longitude' in request.data and request.data["longitude"] != "") and ('latitude' in request.data and request.data["latitude"] != "")):
                    location_dict["longitude"] = float(request.data.pop("longitude"))
                    location_dict["latitude"] = float(request.data.pop("latitude"))
                    location = Location.objects.create(**location_dict)
                    print(location, "id")
                    request.data["location"] = location
                    transaction_serializer = TransactionSerializer( data=location_dict)
                    print(transaction_serializer)
                    if transaction_serializer.is_valid(raise_exception=False):
                        transaction_id = transaction_serializer.save()
                        if len(str(transaction_id)) > 0:
                                Location.update(location=location_dict.data.get('id'))
                    return Response({"status":True,"message":"add successfully", "data":transaction_serializer.data },status=status.HTTP_201_CREATED)
               

                    # print(location_dict, "location data")
                    # location_serializer = LocationSerializer(data=location_dict)
                    # if location_serializer.is_valid(raise_exception=True):
                    #     print(location_serializer.data)
                        
                    #     # Transaction.objects.filter(user_id=user.id, id=request.data.get('transaction_id')).update(location=location_serializer.data.get('id'))
                    #     request.data["location"] = location_serializer.data.get('id')
                    #     print(location)
                        
                    # else:
                    #     return Response({"message":location_serializer})


            if (len(source) > 0 and len(income_to) > 0 and len(goal) <= 0 and len(income_from) <= 0 and len(expense) <= 0 and len(location) <= 0):
                source_amount = ''
                income_to_amount = ''
                updated_transfer_amount = ''
                if float(request.data["amount"]) > float(transaction.amount):
                    updated_transfer_amount = float(request.data["amount"]) - float(transaction.amount)
                    source_amount = float(source[0].spent_amount) + float(updated_transfer_amount)
                    income_to_amount = float(income_to[0].amount) + float(updated_transfer_amount)
                elif float(request.data["amount"]) < float(transaction.amount):
                    updated_transfer_amount =  float(transaction.amount) - float(request.data["amount"])
                    source_amount = float(source[0].spent_amount) - float(updated_transfer_amount)
                    income_to_amount = float(income_to[0].amount) - float(updated_transfer_amount)
                elif float(request.data["amount"]) == float(transaction.amount):
                    request.data.pop("amount")

                
                transaction_serializer = TransactionSerializer(transaction, data=request.data)
                if transaction_serializer.is_valid(raise_exception=False):
                    transaction_id = transaction_serializer.save()
                    if len(str(transaction_id)) > 0:
                        if float(request.data["amount"]) != float(transaction.amount):
                            source.update(spent_amount=source_amount)
                            income_to.update(amount=income_to_amount)
                    else:
                        return Response({"status":False, "message":"Transaction Update Fail by id %s"%(pk)}, status=status.HTTP_304_NOT_MODIFIED)
                    print(transaction_serializer.data)
                    return Response({"status":True, "message":"%s Transaction Amount Update from source %s to income %s"%(pk, source[0].title, income_to[0].title), "data":transaction_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                     
            elif (len(source) <= 0 and len(income_to) > 0 and len(goal) <= 0 and len(income_from) > 0 and len(expense) <= 0):
                income_from_amount = ''
                income_to_amount = ''
                updated_transfer_amount = ''

                if float(request.data["amount"]) > float(transaction.amount):
                    updated_transfer_amount = float(request.data["amount"]) - float(transaction.amount)
                    income_from_amount = float(income_from[0].amount) - float(updated_transfer_amount)
                    income_to_amount = float(income_to[0].amount) + float(updated_transfer_amount)
                elif float(request.data["amount"]) < float(transaction.amount):
                    updated_transfer_amount =  float(transaction.amount) - float(request.data["amount"])
                    income_from_amount = float(income_from[0].amount) + float(updated_transfer_amount)
                    income_to_amount = float(income_to[0].amount) - float(updated_transfer_amount)
                elif float(request.data["amount"]) == float(transaction.amount):
                    request.data.pop("amount")

                transaction_serializer = TransactionSerializer(transaction, data=request.data)
                if transaction_serializer.is_valid(raise_exception=False):
                    transaction_id = transaction_serializer.save()
                    if len(str(transaction_id)) > 0:
                        income_from.update(amount=income_from_amount)
                        income_to.update(amount=income_to_amount)
                    else:
                        return Response({"status":False, "message":"Transaction Update Fail by id %s"%(pk)}, status=status.HTTP_304_NOT_MODIFIED)
                    return Response({"status":True, "message":"%s Transaction Amount Update from Income %s to Income %s"%(pk, income_from[0].title, income_to[0].title), "data":transaction_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
            elif (len(source) <= 0 and len(income_to) <= 0 and len(goal) > 0 and len(income_from) > 0 and len(expense) <= 0):
                income_from_amount = ''
                goal_amount = ''
                updated_transfer_amount = ''

                if float(request.data["amount"]) > float(transaction.amount):
                    updated_transfer_amount = float(request.data["amount"]) - float(transaction.amount)
                    income_from_amount = float(income_from[0].amount) - float(updated_transfer_amount)
                    goal_amount = float(goal[0].added_amount) + float(updated_transfer_amount)
                elif float(request.data["amount"]) < float(transaction.amount):
                    updated_transfer_amount =  float(transaction.amount) - float(request.data["amount"])
                    income_from_amount = float(income_from[0].amount) + float(updated_transfer_amount)
                    goal_amount = float(goal[0].added_amount) - float(updated_transfer_amount)
                elif float(request.data["amount"]) == float(transaction.amount):
                    request.data.pop("amount")

                transaction_serializer = TransactionSerializer(transaction, data=request.data)
                if transaction_serializer.is_valid(raise_exception=False):
                    transaction_id = transaction_serializer.save()
                    if len(str(transaction_id)) > 0:
                        income_from.update(amount=income_from_amount)
                        goal.update(added_amount=goal_amount)
                    else:
                        return Response({"status":False, "message":"Transaction Update Fail by id %s"%(pk)}, status=status.HTTP_304_NOT_MODIFIED)
                    return Response({"status":True, "message":"%s Transaction Amount Update from Income %s to Goal %s"%(pk, income_from[0].title, goal[0].title), "data":transaction_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            elif (len(source) <= 0 and len(income_to) <= 0 and len(goal) <= 0 and len(income_from) > 0 and len(expense) > 0):
                income_from_amount = ''
                expense_amount = ''
                updated_transfer_amount = ''

                if float(request.data["amount"]) > float(transaction.amount):
                    updated_transfer_amount = float(request.data["amount"]) - float(transaction.amount)
                    income_from_amount = float(income_from[0].amount) - float(updated_transfer_amount)
                    expense_amount = float(expense[0].spent_amount) + float(updated_transfer_amount)
                elif float(request.data["amount"]) < float(transaction.amount):
                    updated_transfer_amount =  float(transaction.amount) - float(request.data["amount"])
                    income_from_amount = float(income_from[0].amount) + float(updated_transfer_amount)
                    expense_amount = float(expense[0].spent_amount) - float(updated_transfer_amount)
                elif float(request.data["amount"]) == float(transaction.amount):
                    request.data.pop("amount")
                
                transaction_serializer = TransactionSerializer(transaction, data=request.data)
                if transaction_serializer.is_valid(raise_exception=False):
                    transaction_id = transaction_serializer.save()
                    if len(str(transaction_id)) > 0:
                        income_from.update(amount=income_from_amount)
                        expense.update(spent_amount=expense_amount)
                    else:
                        return Response({"status":False, "message":"Transaction Update Fail by id %s"%(pk)}, status=status.HTTP_304_NOT_MODIFIED)
                    return Response({"status":True, "message":"%s Transaction Amount Update from Income %s to Expense %s"%(pk, income_from[0].title, expense[0].title), "data":transaction_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
            elif (len(source) <= 0 and len(income_to) <= 0 and len(goal) <= 0 and len(income_from) > 0 and len(expense) <= 0 and len(debt) > 0):
                income_from_amount = ''
                debt_amount = ''
                updated_transfer_amount = ''

                if float(request.data["amount"]) > float(transaction.amount):
                    updated_transfer_amount = float(request.data["amount"]) - float(transaction.amount)
                    income_from_amount = float(income_from[0].amount) - float(updated_transfer_amount)
                    debt_amount = float(debt[0].paid_amount) + float(updated_transfer_amount)
                elif float(request.data["amount"]) < float(transaction.amount):
                    updated_transfer_amount =  float(transaction.amount) - float(request.data["amount"])
                    income_from_amount = float(income_from[0].amount) + float(updated_transfer_amount)
                    debt_amount = float(debt[0].paid_amount) - float(updated_transfer_amount)
                elif request.data["amount"] == transaction.amount:
                    request.data.pop("amount")

                transaction_serializer = TransactionSerializer(transaction, data=request.data)
                if transaction_serializer.is_valid(raise_exception=False):
                    transaction_id = transaction_serializer.save()
                    if len(str(transaction_id)) > 0:
                        income_from.update(amount=income_from_amount)
                        debt.update(paid_amount=debt_amount)
                    else:
                        return Response({"status":False, "message":"Transaction Update Fail by id %s"%(pk)}, status=status.HTTP_304_NOT_MODIFIED)
                    return Response({"status":True, "message":"%s Transaction Amount Update from Income %s to Debt %s"%(pk, income_from[0].title, debt[0].name), "data":transaction_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":False, "message":transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False, "message":"Please Provide Transaction Id in url/<id>"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None, format=None):
        if pk is not None and pk != '':
            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False,"message":"user not found"}), email=request.user, status=False)
                return Response({"status":False, "message":"user not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                transaction = Transaction.objects.get(user=user, id=pk)
            except Transaction.DoesNotExist:
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False,"message":"user have not any transaction data"}), email=request.user, status=False)
                return Response({"status":False, "message":"user have not any transaction by id %s"%(pk)}, status=status.HTTP_400_BAD_REQUEST)
        
            if transaction.income_to_id != "":
                income_to = Income.objects.filter(id=transaction.income_to_id)

            if transaction.income_from_id != "":
                income_from = Income.objects.filter(id=transaction.income_from_id)
            
            if transaction.expense_id != "":
                expense = Expense.objects.filter(id=transaction.expense_id)    
            
            if transaction.goal_id != "":
                goal = Goal.objects.filter(id=transaction.goal_id)

            if transaction.source_id != "":
                source = SourceIncome.objects.filter(id=transaction.source_id)  

            if transaction.debt_id is not None:
                debt = Debt.objects.filter(id=str(transaction.debt_id))
            
            if transaction.locaion_id != "":
                location = Location.objects.filter(id=str(transaction.locaion_id))
            
            if transaction.periodic_id != "":
                periodic = Periodic.objects.filter(id=str(transaction.periodic_id))
            
            if len(income_from) > 0 and len(expense) > 0 and len(income_to) <= 0 and len(goal)<= 0 and len(source) <= 0:
        
                income_from_amount = float(income_from[0].amount) + float(transaction.amount) 
                expense_amount = float(expense[0].spent_amount) - float(transaction.amount)
                deleted_transaction = transaction.delete()   
                if len(str(deleted_transaction)) > 0:
                    income_from.update(amount=income_from_amount)
                    expense.update(spent_amount=expense_amount)
                    if transaction.periodic_id != "" and transaction.locaion_id != "":
                        location.delete()
                        periodic.delete()
                    elif transaction.periodic_id != "" and transaction.locaion_id == "":
                        periodic.delete()
                    else:
                        location.delete()
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"transaction data was not delete by id %s"%(pk)}), email=request.user, status=True)
                    return Response({"status":False, "message":"transaction data was not delete by id %s"%(pk)}, status=status.HTTP_403_FORBIDDEN) 
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True,"message":"transaction data was successfully delete by id %s"%(pk)}), email=request.user, status=True)
                return Response({"status":True, "message":"transaction data was successfully delete by id %s"%(pk)}, status=status.HTTP_200_OK)
            
            elif len(income_from) > 0 and len(expense) <= 0 and len(income_to) > 0 and len(goal)<= 0 and len(source) <= 0:
                income_from_amount = float(income_from[0].amount) + float(transaction.amount) 
                income_to_amount = float(income_to[0].amount) - float(transaction.amount)
                
                deleted_transaction = transaction.delete()   
                if len(str(deleted_transaction)) > 0: 
                    income_from.update(amount=income_from_amount)
                    income_to.update(amount=income_to_amount)
                    if transaction.periodic_id != "" and transaction.locaion_id != "":
                        location.delete()
                        periodic.delete()
                    elif transaction.periodic_id != "" and transaction.locaion_id == "":
                        periodic.delete()
                    else:
                        location.delete()
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"transaction data was not delete by id %s"%(pk)}), email=request.user, status=True)
                    return Response({"status":False, "message":"transaction data was not delete by id %s"%(pk)}, status=status.HTTP_403_FORBIDDEN)     
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True,"message":"transaction data was successfully delete by id %s"%(pk)}), email=request.user, status=True)
                return Response({"status":True, "message":"transaction data was successfully delete by id %s"%(pk)}, status=status.HTTP_200_OK)
            
            elif len(income_from) <= 0 and len(expense) <= 0 and len(income_to) > 0 and len(goal)<= 0 and len(source) > 0:
                
                source_amount = float(source[0].spent_amount) - float(transaction.amount) 
                income_to_amount = float(income_to[0].amount) - float(transaction.amount)
                 
                deleted_transaction = transaction.delete()   
                if len(str(deleted_transaction)) > 0:
                    source.update(spent_amount=source_amount)
                    income_to.update(amount=income_to_amount)
                    if transaction.periodic_id != "" and transaction.locaion_id != "":
                        location.delete()
                        periodic.delete()
                    elif transaction.periodic_id != "" and transaction.locaion_id == "":
                        periodic.delete()
                    else:
                        location.delete()
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"transaction data was not delete by id %s"%(pk)}), email=request.user, status=True)
                    return Response({"status":False, "message":"transaction data was not delete by id %s"%(pk)}, status=status.HTTP_403_FORBIDDEN)         
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True,"message":"transaction data was successfully delete by id %s"%(pk)}), email=request.user, status=True)
                return Response({"status":True, "message":"transaction data was successfully delete by id %s"%(pk)}, status=status.HTTP_200_OK)
            
            elif len(income_from) > 0 and len(expense) <= 0 and len(income_to) <= 0 and len(goal)> 0 and len(source) <= 0:
               
                income_from_amount = float(income_from[0].amount) + float(transaction.amount)
                goal_amount = float(goal[0].added_amount) - float(transaction.amount)

                deleted_transaction = transaction.delete()   
                if len(str(deleted_transaction)) > 0:
                    income_from.update(amount=income_from_amount)
                    goal.update(added_amount=goal_amount) 
                    if transaction.periodic_id != "" and transaction.locaion_id != "":
                        location.delete()
                        periodic.delete()
                    elif transaction.periodic_id != "" and transaction.locaion_id == "":
                        periodic.delete()
                    else:
                        location.delete()
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"transaction data was not delete by id %s"%(pk)}), email=request.user, status=True)
                    return Response({"status":False, "message":"transaction data was not delete by id %s"%(pk)}, status=status.HTTP_403_FORBIDDEN)   
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True,"message":"transaction data was successfully delete by id %s"%(pk)}), email=request.user, status=True)
                return Response({"status":True, "message":"transaction data was successfully delete by id %s"%(pk)}, status=status.HTTP_200_OK)

            elif len(income_from) > 0 and len(expense) <= 0 and len(income_to) <= 0 and len(goal)<= 0 and len(source) <= 0 and len(debt) > 0:
               
                income_from_amount = float(income_from[0].amount) + float(transaction.amount)
                debt_amount = float(debt[0].paid_amount) - float(transaction.amount)

                deleted_transaction = transaction.delete()   
                if len(str(deleted_transaction)) > 0:
                    income_from.update(amount=income_from_amount)
                    if float(debt[0].paid_amount) == float(0.00):
                        debt.update(paid_amount=debt_amount, is_partial_paid=False, is_paid=False, is_completed=False) 
                    else:
                        debt.update(paid_amount=debt_amount) 
                    if transaction.periodic_id != "" and transaction.locaion_id != "":
                        location.delete()
                        periodic.delete()
                    elif transaction.periodic_id != "" and transaction.locaion_id == "":
                        periodic.delete()
                    else:
                        location.delete()
                else:
                    header = {
                        "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                    }
                    LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"transaction data was not delete by id %s"%(pk)}), email=request.user, status=True)
                    return Response({"status":False, "message":"transaction data was not delete by id %s"%(pk)}, status=status.HTTP_403_FORBIDDEN)   
                header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
                LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True,"message":"transaction data was successfully delete by id %s"%(pk)}), email=request.user, status=True)
                return Response({"status":True, "message":"transaction data was successfully delete by id %s"%(pk)}, status=status.HTTP_200_OK)
        else:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"Please Provide Transaction id in request param like url/<id>"}), email=request.user, status=False)
            return Response({"status":False, "message":"Please Provide Transaction id in request param like url/<id>"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        transcation = ''
        transaction_list = []
        main_list = []
        income_from = ""
        income_to = ""
        goal = ""
        expense = ""
        location = ""
        periodic = ""
        debt = ""

        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
        
        transcation = Transaction.objects.filter(user=user)
        if pk is not None and request.query_params == {}:
            transcation = Transaction.objects.filter(user=user, id=pk)
            
            if len(transcation) <= 0: 
                return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
        
        elif pk is None and request.query_params != {}:
            if request.query_params != {}:
                if 'income_from' in request.query_params and request.query_params["income_from"] is not None:
                    if request.query_params["income_from"] is None:
                        return Response({"status":False, "message":"Please Provide income_from id in query params like url/?income_from=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, income_from_id=request.query_params["income_from"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
                
                elif 'income_to' in request.query_params and request.query_params["income_to"] is not None:
                    if request.query_params["income_to"] is None:
                        return Response({"status":False, "message":"Please Provide income_to id in query params like url/?income_to=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, income_to_id=request.query_params["income_to"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
                
                elif 'expense' in request.query_params and request.query_params["expense"] is not None:
                    if request.query_params["expense"] is None:
                        return Response({"status":False, "message":"Please Provide expense id in query params like url/?expense=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, expense_id=request.query_params["expense"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
                
                elif 'goal' in request.query_params and request.query_params["goal"] is not None:
                    if request.query_params["goal"] is None:
                        return Response({"status":False, "message":"Please Provide goal id in query params like url/?goal=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, goal_id=request.query_params["goal"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
                    
                elif 'source' in request.query_params and request.query_params["source"] is not None:
                    if request.query_params["source"] is None:
                        return Response({"status":False, "message":"Please Provide source id in query params like url/?source=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, source_id=request.query_params["source"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)   
            
                if 'debt' in request.query_params and request.query_params["debt"] is not None:
                    if request.query_params["debt"] is None:
                        return Response({"status":False, "message":"Please Provide debt id in query params like url/?debt=1"}, status=status.HTTP_400_BAD_REQUEST)
                    transcation = Transaction.objects.filter(user=user, debt_id=request.query_params["debt"])
                    if len(transcation) <= 0: 
                        return Response({"status":False, "message":"transaction history not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"status":False, "message":"provide source, income_to, income_from, goal, expense, debt id in request query_params like url/?source=1"})
            

        for x in transcation:
            transaction_list.append(x)

        transaction_serializer = TransactionSerializer(transaction_list, many=True)

        for y in transaction_serializer.data:
            if y["income_to"] is not None:
                try:
                    income_to = Income.objects.get(id=str(y["income_to"])).title
                except Income.DoesNotExist:
                    return Response({"status":False, "message":"income detail not found"}, status=status.HTTP_404_NOT_FOUND)
                y["income_to_name"] = income_to

            if y["income_from"] is not None:
                try:
                    income_from = Income.objects.get(id=str(y["income_from"])).title
                except Income.DoesNotExist:
                    return Response({"status":False, "message":"income detail not found"}, status=status.HTTP_404_NOT_FOUND)
                y["income_from_name"] = income_from

            if y["source"] is not None:
                try:
                    source = SourceIncome.objects.get(id=str(y["source"])).title
                except SourceIncome.DoesNotExist:
                    return Response({"status":False, "message":"source detail not found"}, status=status.HTTP_404_NOT_FOUND)
                y["source_name"] = source

            if y["goal"] is not None:
                try:
                    goal = Goal.objects.get(id=str(y["goal"])).title
                except Goal.DoesNotExist:
                    return Response({"status":False, "message":"goal detail not found"}, status=status.HTTP_404_NOT_FOUND)
                y["goal_name"] = goal

            if y["expense"] is not None:
                try:
                    expense = Expense.objects.get(id=str(y["expense"])).title
                except Expense.DoesNotExist:
                    return Response({"status":False, "message":"expense detail not found"}, status=status.HTTP_404_NOT_FOUND)
                y["expense_name"] = expense

            if y["periodic"] is not None:
                periodic = Periodic.objects.get(id=str(y["periodic"]))
                y["periodic_data"] = {'id':periodic.id,'start_date':periodic.start_date,'end_date':periodic.end_date,'week_days':periodic.week_days,'prefix':periodic.prefix,'prefix_value':periodic.prefix_value, 'created_at':periodic.created_at, 'modified_at':periodic.modified_at}
            
            if y["location"] is not None:
                location = Location.objects.get(id=str(y["location"]))
                y["location_data"] = {'id':location.id,'latitude':location.latitude,'longitude':location.longitude, 'created_at':location.created_at, 'modified_at':location.modified_at}
            
            if y["debt"] is not None:
                debt = Debt.objects.get(id=str(y["debt"])).name
                y["debt_name"] = debt
            
            main_list.append(y)
        data_dict = main_list
    
        return Response({"status":True, "message":"transaction data Fetched Succcessfully", "data":data_dict}, status=status.HTTP_200_OK)

# User Transaction API Code end#     

# User location API Code Start#
class LocationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
             return Response({"status":False, "message":"location Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)

        
    def get(self, request, format=None):
        try:
            user = User.objects.get(email=str(request.user)).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            location = Location.objects.get(id=trans.location_id)
        except Location.DoesNotExist:
            return Response({'status':False, 'message':'LOCATION data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = LocationSerializer(location)
        return Response(serializer.data)


    def put(self,request,format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if trans.location_id != None:
            try:
                location =Location.objects.get(id=trans.location_id)
            except Location.DoesNotExist:
                return Response({'status':False, 'message':'Location data not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = LocationSerializer(location,data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Transaction.objects.filter(user_id=user.id, id=request.data.get('transaction_id')).update(periodic=serializer.data.get('id'))
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                Transaction.objects.filter(user_id=user.id, id=request.data.get('transaction_id')).update(location=serializer.data.get('id'))
                return Response({"status":"update success", "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self,request, pk=None):
        print("location delete")
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            location = Location.objects.get(id=trans.location_id)
        except Location.DoesNotExist:
            return Response({'status':False, 'message':'LOCATION data not found'}, status=status.HTTP_404_NOT_FOUND)
        # print(location)
        
        location.delete()
        # Transaction.objects.filter(user_id=user, id=request.data.get('transaction_id')).update(location_id="")
        return Response({"message":"data was successfully delete"})
# User location API Code end#

# User periodic API Code Start#
class PeriodicDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Periodic.objects.get(pk=pk)
        except Periodic.DoesNotExist:
             return Response({"status":False, "message":"periodic Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)

        
    def get(self, request, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            periodic = Periodic.objects.get(id=trans.periodic_id)
        except Periodic.DoesNotExist:
            return Response({'status':False, 'message':'periodic data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = PeriodicSerializer(periodic)
        return Response(serializer.data)


    def put(self,request,format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)
        # print(trans.periodic_id, "p")
        if trans.periodic_id != None:
            try:
                periodic = Periodic.objects.get(id=trans.periodic_id)
            except Periodic.DoesNotExist:
                return Response({'status':False, 'message':'periodic data not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PeriodicSerializer(periodic,data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Transaction.objects.filter(user_id=user.id, id=request.data.get('transaction_id')).update(periodic=serializer.data.get('id'))
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            serializer = PeriodicSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                Transaction.objects.filter(user_id=user, id=request.data.get('transaction_id')).update(periodic=serializer.data.get('id'))
                return Response({"status":"update success", "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def delete(self,request):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            trans = Transaction.objects.get(user_id=user, id=request.data.get('transaction_id'))
        except Transaction.DoesNotExist:
            return Response({'status':False, 'message':'transaction data not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            periodic = Periodic.objects.get(id=trans.periodic_id)
        except Periodic.DoesNotExist:
            return Response({'status':False, 'message':'periodic data not found'}, status=status.HTTP_404_NOT_FOUND)
        periodic.delete()
        return Response({"message":"data was successfully delete"})
# User periodic API Code end#

# User setting API Code Start#
class SettingView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        if request.data != {}:
            if (('notification' in request.data and request.data['notification'] == "")):
                return Response({"status":False, "message":"please enter either true or false in notification"})
            elif (('min_pass_3' in request.data and request.data['min_pass_3'] == "")):
                return Response({"status":False, "message":"please enter either true or false in min_pass_3"})
            elif (('language' in request.data and request.data['language'] == "")):
                return Response({"status":False, "message":"please enter text in language"})
            elif (('currency' in request.data and request.data['currency'] == "")):
                return Response({"status":False, "message":"please enter text in currency"})
            else:
                pass


            serializer = SettingSerializer(data=request.data, context={'request':request})
            if serializer.is_valid(raise_exception=True):

                serializer.save()
                # user=request.MyUser.id
                # header = {
                #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':True, 'message':"Data add successfully","data":serializer.data}), email=request.user, status=True)
                return Response({"status":True, "message":"Data add successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                # header = {
                #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                # }
                # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':""}), email=request.user, status=False)
                return Response({"status":False, "data":serializer.error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':"please provide any field like notification, min_pass_3"}), email=request.user, status=False)
            return Response({"status":False, "message":"please provide any field like notification, min_pass_3"},status=status.HTTP_404_NOT_FOUND) 
    def get(self, request):
        user = request.user
        if user is not None:
            setting = Setting.objects.filter(user=user)
            
        settingserializer = SettingSerializer(setting, many=True)
        header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
        LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), response_data=json.dumps({'status':True, 'message':"setting data fetched successfully","data":settingserializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"setting data fetched successfully","data":settingserializer.data}, status=status.HTTP_201_CREATED) 

        
class SettingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk,request):
        try:
            return Setting.objects.get(pk=pk)
        except Setting.DoesNotExist:
            header = {
                    "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), response_data=json.dumps({'status':False, 'message':"The data does not exist"}), email=request.user, status=False)
            return Response({"status":False,'message': 'The data does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
    def get(self, request,pk, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({'status':False, 'message':"User Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            setting = Setting.objects.get(id=pk, user_id=user)
        except:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"setting data not found"}), email=request.user, status=False)
            return Response({'status':False, 'message':'setting data not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SettingSerializer(setting)
        header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
        LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"setting data fetched successfully","data":serializer.data}), email=request.user, status=True)
        return Response({"status":True,"data":serializer.data,"message":"setting data fetched successfully"},status=status.HTTP_200_OK)


    def put(self,request,pk,format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({'status':False, 'message':"User Detail Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            setting = Setting.objects.get(id=pk, user_id=user)
        except:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":"setting data not found"}), email=request.user, status=False)
            return Response({'status':False, 'message':'setting data not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SettingSerializer(setting,data=request.data)
        if serializer.is_valid():
            serializer.save()
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":True, "message":"setting data updated successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True, "message":"setting data updated successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            header = {
                "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
                }
            LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),request_data=json.dumps(request.data), response_data=json.dumps({"status":False, "message":""}), email=request.user, status=False)
            return Response({"status":False,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
# User setting API Code end#



# User SourceIncome Serializer Code Start # 
class SourceIncomeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        if request.data != {}:
            if (('icon' in request.data and request.data['icon'] == "")):
                return Response({"status":False, "message":"please enter icon"})
            elif (('title' in request.data and request.data['title'] == "")):
                return Response({"status":False, "message":"please enter title"})
            elif (('amount' in request.data and request.data['amount'] == "")):
                return Response({"status":False, "message":"please enter  amount"})
            else:
                pass


            serializer = SourceIncomeSerializer(data=request.data, context={'request':request})
            if serializer.is_valid(raise_exception=True):

                serializer.save()
                # user=request.MyUser.id
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False, "data":serializer.error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False, "message":"please provide any field like title, amount"})

    def get(self,request):
        user = request.user
        if user is not None:
            sourceincome = SourceIncome.objects.filter(user=user)
            
        sourceincomeserializer = SourceIncomeSerializer(sourceincome, many=True)
        return Response({"status":True, "data":sourceincomeserializer.data}, status=status.HTTP_201_CREATED)
class SourceIncomeDetailView(APIView):
        permission_classes = [IsAuthenticated]
        def get_object(self, pk):
            try:
                return SourceIncome.objects.get(pk=pk)
            except SourceIncome.DoesNotExist:
                return Response({'message': 'The data does not exist'}, status=status.HTTP_404_NOT_FOUND)

            
        def get(self, request,pk, format=None):
            try:
                user = User.objects.get(id=str(request.user)).id
            except User.DoesNotExist:
                return Response({"status":False})

            try:
                sourceincome = SourceIncome.objects.get(id=pk, user_id=user)
            except:
                return Response({'status':False, 'message':'sourceincome data not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = SourceIncomeSerializer(sourceincome)
            return Response(serializer.data)


        def put(self,request,pk,format=None):
            try:
                user = User.objects.get(id=str(request.user)).id
            except User.DoesNotExist:
                return Response({"status":False})
            try:
                sourceincome = SourceIncome.objects.get(id=pk, user_id=user)
            except:
                return Response({'status':False, 'message':'sourceincome data not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = SourceIncomeSerializer(sourceincome,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

        def delete(self,request,pk):
            try:
                user = request.user
                if user is not None:
                    sourceincome = SourceIncome.objects.get(id=pk, user_id=user)
            except:
                return Response({'status':False, 'message':'sourceincome data not found'}, status=status.HTTP_404_NOT_FOUND)
            sourceincome.delete()
            return Response({"message":"data was successfully delete"}) 
# User SourceIncome Serializer Code end #


class ReltionsourceincomeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        if (('income' in request.data and request.data['income']!="")  and ('source' in request.data and request.data['source'] != "") and ('amount' in request.data and request.data['amount'] != "")):
            try:
                income = Income.objects.filter(id=str(request.data['income']))
            except Income.DoesNotExist:
                return Response({"status":False, "message":"Income Data Not Found"})
            
            try:
                source = SourceIncome.objects.filter(id=str(request.data['source']))
            except SourceIncome.DoesNotExist:
                return Response({"status":False, "message":"SourceIncome Data Not Found"})

            request.data.update({"income":income[0].id})
            request.data.update({"source":source[0].id})

            income_amount = int(income[0].amount)+int(request.data['amount']) 
            source_amount = int(source[0].amount)-int(request.data['amount'])

            relation_serializer = ReltionsourceincomeSerializer(data=request.data)
            if relation_serializer.is_valid(raise_exception=True):
                relation_id = relation_serializer.save()
                if (relation_id > 0 and relation_id != ''):
                    income.update(amount=income_amount)
                    source.update(amount=source_amount)
                else:
                    return Response({"status":False, "message":"Relation Income Source Not Created"}, status=status.HTTP_400_BAD_REQUEST) 
                return Response({"status":True, "message":"Amount Added from Source to Income Successfully", "data":relation_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False, "message":"Some Fields Are Missing", "errors":relation_serializer.errors})
        else:
            return Response({"status":False, "message":"income, source and amount is the required fields and cannot be blank"})

    def get(self, request, format=None):
            if ('source_id' in request.data and request.data['source_id']):
                try:
                    user = User.objects.get(email=request.user).id
                except User.DoesNotExist:
                    return Response({"status":False, "message":"User doesn't exist"})

                try:
                    source = SourceIncome.objects.get(id=request.data['source_id'], user_id=user).id
                except SourceIncome.DoesNotExist:
                    return Response({"status":False, "message":"User doesn't have any source income"})

                try:
                    Relational_data = Reltionsourceincome.objects.filter(source_id_id=source)
                except Reltionsourceincome.DoesNotExist:
                    return Response({"status":False, "message":"User haven't any transaction"})
                
                source_trans_data = ReltionsourceincomeSerializer(Relational_data, many=True)
                return Response({"status":True, "message":"transaction fatched", "data":source_trans_data.data})
            else:
                return Response({"status":False, "message":"please provide source_id in request data"})


    def put(self,request,pk,format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({"status":False, "message":"User doesn't exist"})

        try:
            source = SourceIncome.objects.filter(id=request.data['source_id'], user_id=user)
        except SourceIncome.DoesNotExist:
            return Response({"status":False, "message":"User doesn't have any source income"})
            
        try:
            incom = Income.objects.filter(id=str(request.data['ins_id']), user_id=str(user))
        except Income.DoesNotExist:
            return Response({"status":False, "message":"User doesn't have any income"})  

        try:
            Relational_data = Reltionsourceincome.objects.get(id=pk,source_id_id=source[0].id,ins_id_id=incom[0].id)
        except Reltionsourceincome.DoesNotExist:
            return Response({"status":False, "message":"User haven't any transaction"})
        if (int(request.data['transfer_amount']) > int(Relational_data.amount)):
            
            transfer_amount = int(request.data['transfer_amount']) - int(Relational_data.amount)
            income_amount = int(incom[0].amount)+int(transfer_amount) 
            source_amount = int(source[0].amount)-int(transfer_amount)
        
        elif (int(request.data['transfer_amount']) < int(Relational_data.amount)):    
            
            transfer_amount = int(Relational_data.amount) - int(request.data['transfer_amount'])
            income_amount = int(incom[0].amount)-int(transfer_amount) 
            source_amount = int(source[0].amount)+int(transfer_amount)
        else:
            return Response({"status":False})   
        
        incom.update(amount=income_amount)
        source.update(amount=source_amount)     
        
        relation_dict = {
            'amount':request.data['transfer_amount']
        }
        
        serializer = ReltionsourceincomeSerializer(Relational_data,data=relation_dict)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"update data Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)   
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
# User Reltion API Code end#          
        

class HomeapiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        balancesouce = {}
        balanceincome = {}
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            income = Income.objects.filter(user=user)
        except:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any income detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any income detail'}, status=status.HTTP_404_NOT_FOUND)
        try:
            sourceincome = SourceIncome.objects.filter(user=user)
        except:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any sourceincome detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any sourceincome detail'}, status=status.HTTP_404_NOT_FOUND)     
        
        try:
            expense = Expense.objects.filter(user=user)
        except:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any expense detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any expense detail'}, status=status.HTTP_404_NOT_FOUND)
        try:
            Goals = Goal.objects.filter(user=user)
        except:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any goal detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any goal detail'}, status=status.HTTP_404_NOT_FOUND)

        try:
            debt = Debt.objects.filter(user=user)
        except:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'user have not any debt detail'}), email=request.user, status=False)
            return Response({'status':False, 'message':'user have not any debt detail'}, status=status.HTTP_404_NOT_FOUND)

        try:
            balancesouce = SourceIncome.objects.filter(user=user).aggregate(Sum('amount'))
            if balancesouce['amount__sum'] is None:
                balancesouce['amount__sum'] = 0
        except SourceIncome.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'SourceIncome not found'}), email=request.user, status=False)
            return Response({'status':False, 'message':'SourceIncome not found'},status=status.HTTP_400_BAD_REQUEST)

        try:
            balanceincome = Income.objects.filter(user=user).aggregate(Sum('amount'))
            if balanceincome['amount__sum'] is None:
                balanceincome['amount__sum'] = 0
        except Income.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'Income not found'}), email=request.user, status=False)
            return Response({'status':False, 'message':'Income not found'}, status=status.HTTP_400_BAD_REQUEST)    
        print(balanceincome)

        try:
            balancedebt = Debt.objects.filter(user=user).aggregate(Sum('amount'))
            if balancedebt['amount__sum'] is None:
                balancedebt['amount__sum'] = 0
        except Debt.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            # }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':False, 'message':'Debt not found'}), email=request.user, status=False)
            return Response({'status':False, 'message':'SourceIncome not found'},status=status.HTTP_400_BAD_REQUEST)

        income_serializer = IncomeSerializer(income, many=True)
        sourceincome_serializer = SourceIncomeSerializer(sourceincome, many=True)
        # balance = 0
        # for x in sourceincome_serializer.data:
        #     # print(x['amount'])
        #     balance = float(balance) + float(x['amount'])
        # print(balance)
        expense_serializer = ExpenseSerializer(expense, many=True)
        Goals_serializer = GoalsSerializer(Goals, many=True)
        debt_serializer = DebtSerializer(debt, many=True)
        
        data_dict = {
            "Income":income_serializer.data,
            "Sourceincome":sourceincome_serializer.data,
            "balanceSource":balancesouce['amount__sum'],
            "balanceIncome":balanceincome['amount__sum'],
            "Expense":expense_serializer.data,
            "Goals":Goals_serializer.data,
            "balancedebt":balancedebt['amount__sum'],
            "Debt":debt_serializer.data
        }
        # header = {
        #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #     }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({'status':True, 'message':'get all detail',"data":data_dict}), email=request.user, status=True)
        return Response ({"status":True, "message":"get all detail","data":data_dict},status=status.HTTP_200_OK)
# class HomeVIEW Code End #

# class DebtView Code start #
class DebtView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        if request.data != {}:
            try:
                User = User.objects.get(id=str(request.user))
            except:
                return Response()
            
            if (('name' in request.data and request.data['name'] == "")):
                return Response({"status":False, "message":"please enter name"})
            elif (('date' in request.data and request.data['date'] == "")):
                return Response({"status":False, "message":"please enter date"})
            elif (('amount' in request.data and request.data['amount'] == "")):
                return Response({"status":False, "message":"please enter  amount"})
            
            else:
                pass
           
            serializer = DebtSerializer(data=request.data, context={'request':request})
            if serializer.is_valid(raise_exception=True):

                serializer.save()
                # user=request.MyUser.id
                return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False, "data":serializer.error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False, "message":"please provide any field like name, amount"})


    def get(self,request):
        user = request.user
        if user is not None:
            debt = Debt.objects.filter(user=user)
            
        debtserializer = DebtSerializer(debt, many=True)
        return Response({"status":True, "data":debtserializer.data}, status=status.HTTP_201_CREATED)

# class DebtView Code end #

# class TagView Code start #
class TagView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = TagSerializer(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # user=request.MyUser.id
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':True, 'message':"Exchangerate data add successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':""}), email=request.user, status=False)
            return Response({"status":False, "data":serializer.error}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
         # print(request)
        
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
           
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

        try:
            tag = Tag.objects.filter(user=user)
        except Tag.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any exchangerate data"}), email=request.user, status=False)
            return Response({"status":False, "message":"user have not any tag data"},status=status.HTTP_404_NOT_FOUND)
        
        # if request.query_params != {}:
        #     if 'tag_id' in request.query_params and request.query_params["tag_id"] is not None and request.query_params["tag_id"] != '':
               
        #         tag = Tag.objects.filter(user=user, id=request.query_params["tag_id"])
        #         if len(tag) <= 0: 
        #             # header = {
        #         # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #         # }
        #         # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"tag data not found"}), email=request.user, status=False)
        #             return Response({"status":False, "message":"tag data not found"}, status=status.HTTP_404_NOT_FOUND)
        #     else:
        #         # header = {
        #         # "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #         # }
        #         # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"provide exchangerate id in request parameter"}), email=request.user, status=False)
        #         return Response({"status":False, "message":"provide tag id in request parameter"})


        tag_serializer = TagSerializer(tag, many=True)
        # header = {
        #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #         }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"Exchangerate data Fetched Succcessfully","data":exchangerate_serializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"tag data Fetched Succcessfully", "data":tag_serializer.data},status=status.HTTP_200_OK)


class TagDetailView(APIView):
        permission_classes = [IsAuthenticated]
        def get_object(self, pk):
            try:
                return Tag.objects.get(pk=pk)
            except Tag.DoesNotExist:
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"The data does not exist"}), email=request.user, status=False)
                return Response({"status":False,'message': 'The data does not exist'}, status=status.HTTP_404_NOT_FOUND)

            
        def get(self, request,pk, format=None):
            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
                return Response({"status":False,"message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

            try:
                tag = Tag.objects.get(id=pk, user_id=user)
            except Tag.DoesNotExist:
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"tag data not found"}), email=request.user, status=False)
                return Response({'status':False, 'message':'tag data not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TagSerializer(tag)
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"tag data fetched successfully","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True,"message":"tag data fetched successfully","data":serializer.data},status=status.HTTP_200_OK)


        def put(self,request,pk,format=None):
            try:
                user = User.objects.get(email=request.user).id
            except User.DoesNotExist:
                # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data),response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
                return Response({"status":False,"message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
            
            try:
                tag = Tag.objects.get(id=pk, user_id=user)
            except Tag.DoesNotExist:
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data),response_data=json.dumps({"status":False, "message":"tag data not found"}), email=request.user, status=False)
                return Response({'status':False, 'message':'tag data not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TagSerializer(tag,data=request.data)
            if serializer.is_valid():
                serializer.save()
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data),response_data=json.dumps({"status":True, "message":"tag data updated successfuully","data":serializer.data}), email=request.user, status=True)
                return Response({"status":True, "message":"tag data updated successfuully","data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_data=json.dumps(request.data),response_data=json.dumps({"status":False, "message":""}), email=request.user, status=False)
                return Response({"status":False,"message":"","data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

        def delete(self,request,pk):
            try:
                user = request.user
                if user is not None:
                    tag = Tag.objects.get(id=pk, user_id=user)
            except Tag.DoesNotExist:
                 # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),response_data=json.dumps({"status":False, "message":"tag data not found"}), email=request.user, status=False)
                return Response({'status':False, 'message':'tag data not found'}, status=status.HTTP_404_NOT_FOUND)
            tag.delete()
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header),response_data=json.dumps({"status":True, "message":"tag data was successfully delete"}), email=request.user, status=True)
            return Response({"status":True,"message":"tag data was successfully delete"},status=status.HTTP_200_OK) 

# class TagView Code end #

class ReportView(APIView):
    permission_classes = [IsAuthenticated]
    
   
    def get(self, request, pdf=None):
        print(request.user)
        transaction_data_dict = {}
        transaction_data_list = []
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
            return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            # transcation = Transaction.objects.filter(user=user)
            transaction = Transaction.objects.all().filter(user_id=user.id)
            for x in transaction:
                transaction_data_list.append(x)
        except Transaction.DoesNotExist:
            # header = {
            #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any report data"}), email=request.user, status=False)
            return Response({"status":False, "message":"user have not any report data"},status=status.HTTP_404_NOT_FOUND)

        if 'filter' in request.data and request.data['filter'] is not None:
            if request.data['filter'] == "Today":
                print("A")
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                if request.data["startdate"] == request.data["enddate"]:
                    transaction = Transaction.objects.filter(user=user, created_at__range=[request.data["startdate"], request.data["enddate"]])
                    for x in transaction:
                        transaction_data_list.append(x)
                else:
                    # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                    return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)

            elif request.data['filter'] == "Week":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                transaction = Transaction.objects.filter(user=user,created_at__range=[request.data["startdate"], request.data["enddate"]])
                for x in transaction:
                    transaction_data_list.append(x)

            elif request.data['filter'] == "Month":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                transaction = Transaction.objects.filter(user=user, created_at__range=[request.data["startdate"], request.data["enddate"]])
                for x in transaction:
                    transaction_data_list.append(x)

            elif request.data['filter'] == "Year":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                transaction = Transaction.objects.filter(user=user, created_at__range=[request.data["startdate"], request.data["enddate"]]) 
                for x in transaction:
                    transaction_data_list.append(x)
            else:
                pass
            
        print(transaction_data_list, "asd")                
        if 'filter' in request.data and request.data['filter'] is not None:
            if request.data['filter'] == "income":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                income_id = Income.objects.filter(user_id=user.email)
                print(income_id, "as")
                
                for income in income_id:
                    if 'subfilter' not in request.data:
                        transaction = Transaction.objects.filter(user=user, income_from_id=income)# queryset<[]>
                        for x in transaction:
                            transaction_data_list.append(x)
                    else:
                        if request.data['subfilter'] == "Today":
                            print("B")
                            if request.data["startdate"] == request.data["enddate"]:
                                transaction = Transaction.objects.filter(user=user, income_from_id=income, created_at__range=[request.data["startdate"], request.data["enddate"]])
                                print(transaction, "tra")
                                for x in transaction:
                                    transaction_data_list.append(x)
                            else:
                                        # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                                return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)

                        elif request.data['subfilter'] == "Week":
                            transaction = Transaction.objects.all().filter(user=user, income_from_id=income,created_at__range=[request.data["startdate"], request.data["enddate"]] )
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Month":
                            transaction = Transaction.objects.all().filter(user=user, income_from_id=income, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Year":
                            transaction = Transaction.objects.all().filter(user=user, income_from_id=income, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                        else:
                            pass
                        
                    
            elif request.data['filter'] == "goal":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                goal_id = Goal.objects.filter(user_id=user.id)
                print(goal_id)

                for goal in goal_id:
                    if 'subfilter' not in request.data:
                        transaction = Transaction.objects.filter(user=user, goal_id=goal)# queryset<[]>
                        for x in transaction:
                            transaction_data_list.append(x)
                    else:
                        if request.data['subfilter'] == "Today":
                            if request.data["startdate"] == request.data["enddate"]:
                                transaction = Transaction.objects.filter(user=user, goal_id=goal, created_at__range=[request.data["startdate"], request.data["enddate"]])
                                for x in transaction:
                                    transaction_data_list.append(x)
                            else:
                                        # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                                return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)


                        elif request.data['subfilter'] == "Week":
                            transaction = Transaction.objects.all().filter(user=user, goal_id=goal, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Month":
                            transaction = Transaction.objects.all().filter(user=user, goal_id=goal, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Year":
                            transaction = Transaction.objects.all().filter(user=user, goal_id=goal, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                        else:
                            pass
                        

            elif request.data['filter'] == "expense":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                expense_id = Expense.objects.filter(user_id=user.id)
                print(expense_id)

                for expense in expense_id:
                    if 'subfilter' not in request.data:
                        transaction = Transaction.objects.filter(user=user, expense_id=expense)# queryset<[]>
                        for x in transaction:
                            transaction_data_list.append(x)
                    else:
                        if request.data['subfilter'] == "Today":
                            if request.data["startdate"] == request.data["enddate"]:
                                transaction = Transaction.objects.all().filter(user=user, expense_id=expense, created_at__range=[request.data["startdate"], request.data["enddate"]])
                                for x in transaction:
                                    transaction_data_list.append(x)
                            else:
                                        # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                                return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)

                        elif request.data['subfilter'] == "Week":
                            transaction = Transaction.objects.all().filter(user=user, expense_id=expense, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Month":
                            transaction = Transaction.objects.all().filter(user=user, expense_id=expense, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Year":
                            transaction = Transaction.objects.all().filter(user=user, expense_id=expense, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                        else:
                            pass
                        
                    
            elif request.data['filter'] == "source":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                source_id = SourceIncome.objects.filter(user_id=user.id)
                print(source_id)

                for source in source_id:
                    if 'subfilter' not in request.data:
                        transaction = Transaction.objects.filter(user=user, source_id=source)# queryset<[]>
                        for x in transaction:
                            transaction_data_list.append(x)
                    else:
                        if request.data['subfilter'] == "Today":
                            if request.data["startdate"] == request.data["enddate"]:
                                transaction = Transaction.objects.all().filter(user=user, source_id=source, created_at__range=[request.data["startdate"], request.data["enddate"]])
                                for x in transaction:
                                    transaction_data_list.append(x)
                            else:
                                        # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                                return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)

                        elif request.data['subfilter'] == "Week":
                            transaction = Transaction.objects.all().filter(user=user, source_id=source, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Month":
                            transaction = Transaction.objects.all().filter(user=user, source_id=source, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)

                        elif request.data['subfilter'] == "Year":
                            transaction = Transaction.objects.all().filter(user=user, source_id=source, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                        else:
                            pass

            elif request.data['filter'] == "tag":
                if len(transaction_data_list) > 0:
                    transaction_data_list.clear()
                tag_id = Tag.objects.filter(user_id=user.id)
                print(tag_id)

                for tag in tag_id:
                    if 'subfilter' not in request.data:
                        transaction = Transaction.objects.filter(user=user,tag__id=tag.id)# queryset<[]>
                        for x in transaction:
                            transaction_data_list.append(x)
                        transaction_data_list = [i for n, i in enumerate(transaction_data_list) if i not in transaction_data_list[:n]]
                    else:
                        if request.data['subfilter'] == "Today":
                            if request.data["startdate"] == request.data["enddate"]:
                                transaction = Transaction.objects.filter(user=user, tag__id=tag.id, created_at__range=[request.data["startdate"], request.data["enddate"]])
                                for x in transaction:
                                    transaction_data_list.append(x)
                                transaction_data_list = [i for n, i in enumerate(transaction_data_list) if i not in transaction_data_list[:n]]
                            else:
                                        # header = {
            #           "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #               }
            #           LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"please enter valid date"}), email=request.user, status=False)
                                return Response({"status":False,"message":"please enter valid date"},status=status.HTTP_404_NOT_FOUND)


                        elif request.data['subfilter'] == "Week":
                            transaction = Transaction.objects.all().filter(user=user, tag__id=tag.id, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                            transaction_data_list = [i for n, i in enumerate(transaction_data_list) if i not in transaction_data_list[:n]]

                        elif request.data['subfilter'] == "Month":
                            transaction = Transaction.objects.all().filter(user=user, tag__id=tag.id, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                            transaction_data_list = [i for n, i in enumerate(transaction_data_list) if i not in transaction_data_list[:n]]

                        elif request.data['subfilter'] == "Year":
                            transaction = Transaction.objects.all().filter(user=user, tag__id=tag.id, created_at__range=[request.data["startdate"], request.data["enddate"]])
                            for x in transaction:
                                transaction_data_list.append(x)
                            transaction_data_list = [i for n, i in enumerate(transaction_data_list) if i not in transaction_data_list[:n]]
                        else:
                            pass
                            
        
        # render_to_string('pdf.html', {"transactions":transaction_data_list}) 
        transaction_serializer = TransactionSerializer(transaction_data_list, many=True)
       

        # header = {
        #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #         }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":True, "message":"report data Fetched Succcessfully","data":transaction_serializer.data}), email=request.user, status=True)
        return Response({"status":True, "message":"report data Fetched Succcessfully", "data":transaction_serializer.data},status=status.HTTP_201_CREATED)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    # @csrf_exempt
    # def post(self,request):
    #     data = request.data
    #     email = data['email']
    #     user = User.objects.get(email=email)
    #     if User.objects.filter(email=email).exists():
    #         # send email with otp
    #         send_mail(
    #         'Subject here',
    #         f'Here is the message with {user.otp}.',
    #         'pragneshvmjs@gmail.com',
    #         [user.email],
    #         fail_silently=False,
    #         )
    #         message = {
    #             'detail': 'Success Message'}
    #         return Response(message, status=status.HTTP_200_OK)
    #     else:
    #         message = {
    #             'detail': 'Some Error Message'}
    #         return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # def put(self,request):
    #     """reset_password with email, OTP and new password"""
    #     data = request.data
    #     user = User.objects.get(email=data['email'])
    #     if user.is_active:
    #         # Check if otp is valid
    #         if data['otp'] == user.otp:
    #             if request.data['password'] != '':
    #                 # Change Password
    #                 user.set_password(data['password'])
    #                 user.save() # Here user otp will also be changed on save automatically 
    #                 return Response('any response or you can add useful information with response as well. ')
    #             else:
    #                 message = {
    #                     'detail': 'Password cant be empty'}
    #                 return Response(message, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             message = {
    #                 'detail': 'OTP did not matched'}
    #             return Response(message, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         message = {
    #             'detail': 'Something went wrong'}
    #         return Response(message, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
             # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':True, 'message':"reset password link link send, please check your email","data":serializer.data}), email=request.user, status=True)
            return Response({"status":True,"message":"reset password link send, please check your email" ,"data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            # header = {
            #         "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
            #     }
            # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), request_parameter=json.dumps(request.query_params), request_data=json.dumps(request.data), response_data=json.dumps({'status':False, 'message':""}), email=request.user, status=False)
            return Response({"status":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        LOGOUT(request.data)
        return Response({"status":True})


# class GeneratePdf(APIView):
#      def get(self, request, *args, **kwargs):
        
#         #getting the template
#         pdf = render_to_pdf('pdf.html')
         
#          #rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')
 
# from django.shortcuts import render
# def Templat(request):
#     if request.method == "GET":
#         transaction_data_list = []
#         try:
#             user = User.objects.get(email="reshma@gmail.com")
#         except User.DoesNotExist:
            
#             # header = {
#             #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
#             #     }
#             # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
#             return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             # transcation = Transaction.objects.filter(user=user)
#             transaction = Transaction.objects.all().filter(user_id=user.id)
#             for x in transaction:
#                 transaction_data_list.append(x)
#         except Transaction.DoesNotExist:
#             # header = {
#             #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
#             #     }
#             # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any report data"}), email=request.user, status=False)
#             return Response({"status":False, "message":"user have not any report data"},status=status.HTTP_404_NOT_FOUND)
        
#         transaction_serializer = TransactionSerializer(transaction_data_list, many=True)
#         data_list = []
#         import json
#         for x in transaction_serializer.data:
#             od1 = json.dumps(x)
#             od1 = json.loads(od1)
#             data_list.append(od1)

#         # print(data_list)

        
#         # from collections import OrderedDict
#         # data = OrderedDict(transaction_serializer.data)
#         # print(data_list)
#         return render(request, "pdf.html", {"transactions":data_list})


def export_users_xls(request):
    transaction_data_list=[]
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Id', 'Title', 'Description', 'Amount', 'Source','Income_To','Income_From','Expense','Goal','Location','Periodic','Tags','Created_At','Modified_At']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    try:
        user = User.objects.get(email=request.user)
    except User.DoesNotExist:
        
        # header = {
        #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #     }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"User Detail Doesn't Exist"}), email=request.user, status=False)
        return Response({"status":False, "message":"User Detail Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)
    
    try:
        # transcation = Transaction.objects.filter(user=user)
        transaction = Transaction.objects.all().filter(user_id=user.id)
        for x in transaction:
            transaction_data_list.append(x)
    except Transaction.DoesNotExist:
        # header = {
        #     "HTTP_AUTHORIZATION":request.META['HTTP_AUTHORIZATION']
        #     }
        # LogsAPI.objects.create(apiname=str(request.get_full_path()), request_header=json.dumps(header), response_data=json.dumps({"status":False, "message":"user have not any report data"}), email=request.user, status=False)
        return Response({"status":False, "message":"user have not any report data"},status=status.HTTP_404_NOT_FOUND)
        
    rows = Transaction.objects.all().values_list('id','title', 'description', 'amount', 'source','income_to','income_from','expense','goal','location','periodic','tag','created_at','modified_at')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response