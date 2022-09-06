import email
from pyexpat import model
from urllib import request, response
from xml.dom import ValidationErr
from rest_framework import serializers
from AppApi.models import User, Subscription,Income,Expense,Goal,Exchangerate,Transaction,Location,Periodic,Setting,SourceIncome,Reltionsourceincome,Debt,Tag
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Registration Serializer Code Start #
class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' User Register by firstname, lastname, email, mobile, gender, country, birthdate, is_agree,
    registered_by,  password. Here, country and birthdate is optional fields'''
    profile_pic = serializers.ImageField(required=False, default="")
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'mobile', 'country', 'birthdate', 'gender', 'registered_by', 'device_token', 'social_id', 'subscription_id', 'profile_pic', 'is_agree', 'password']
        extra_kwargs={
            'password':{'write_only':True},
            'country':{'required':False},
            'birthdate':{'required':False},
            'device_token':{'required':False},
            'subscription_id':{'required':False},
            'social_id':{'required':False},
            'profile_pic':{'required':False}
        }
    
    def create(self, validate_data):
        user = User.objects.create(
            firstname=validate_data['firstname'],
            lastname=validate_data['lastname'],
            email=validate_data['email'],
            mobile=validate_data['mobile'],
            gender=validate_data['gender'],
            is_agree=validate_data['is_agree'],
            registered_by=validate_data['registered_by']
        )
    
        user.set_password(validate_data['password'])
        user.save()
        
        return user
# Registration Serializer Code End #

# Login Serializer Code Start #
class UserLoginSerializer(serializers.ModelSerializer):
    ''' User Login by email and password '''
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
# Login Serializer Code End #

# User Profile Serializer Code Start #
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email','mobile', 'country', 'birthdate', 'gender', 'registered_by', 'device_token', 'social_id', 'subscription_id', 'profile_pic', 'is_agree']
# User Profile Serializer Code End #

# User Change Password Serializer Code Start #
class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, write_only=True, style={'input_type':'password'})
    new_password2 = serializers.CharField(max_length=255, write_only=True, style={'input_type':'password'})

    class Meta:
        fields = ['new_password', 'new_password2']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        user = self.context.get('user')
        if new_password != new_password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't Match")
        user.set_password(new_password)
        user.save()
        return attrs
# User Change Password Serializer Code End #

# User Subscription Serializer Code Start #
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'subscription_type', 'subscription_amount', 'user']

        extra_kwargs={
            'id':{'read_only':True},
            'user':{'read_only':True}
        }
    
    def create(self, validate_data):
        subscription = Subscription.objects.create(
            subscription_type = validate_data['subscription_type'],
            subscription_amount = validate_data['subscription_amount'],
            user = self.context['request'].user
        )
        subscription.save()
        return subscription
# User Subscription Serializer Code End #

# User Income Serializer Code Start #
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','icon','title','amount','created_at','modified_at']
        extra_kwargs = {
            "user":{'write_only':True},
            "title":{'required':False},
            "icon":{'required':False}
        }

    def create(self, validated_data):
       validated_data['user'] = self.context['request'].user
       return Income.objects.create(**validated_data)
# User Income Serializer Code End #

# User Expense Serializer Code Start #
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','icon','title','amount_limit','time_range']
        extra_kwargs = {
            "user":{'write_only':True}
        }

    def create(self, validated_data):
       validated_data['user'] = self.context['request'].user
       return Expense.objects.create(**validated_data)
# User Expense Serializer Code End #

# User goal Serializer Code Start #
class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id','icon','title','amount','modified_at']
        extra_kwargs = {
            "user":{'write_only':True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Goal.objects.create(**validated_data)
# User goal Serializer Code End #

# User exchange Serializer Code Start # 
class ExchangerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchangerate
        fields = ['id','currency_name','is_default']
        extra_kwargs = {
            "user":{'write_only':True},
            'is_default':{'required':False},
        }

    def create(self, validated_data):
        exchangerate = Exchangerate.objects.create(
            user=self.context['request'].user, 
            currency_name=validated_data['currency_name'], 
            is_default=validated_data['is_default'])
        exchangerate.save()
        return exchangerate
# User exchange Serializer Code End #

# User Transaction Serializer Code Start #
class TransactionSerializer(serializers.ModelSerializer):
    # income_from = serializers.SlugRelatedField(slug_field="title", queryset=Income.objects.all())
    # expense = serializers.SlugRelatedField(slug_field="title", queryset=Expense.objects.all())
    # goal = serializers.SlugRelatedField(slug_field="title", queryset=Goal.objects.all())
    # source = serializers.SlugRelatedField(slug_field="title", queryset=SourceIncome.objects.all())
    # user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    # location = serializers.SlugRelatedField(slug_field="__str__", queryset=Location.objects.all())
    # periodic = serializers.SlugRelatedField(slug_field="__str__", queryset=Periodic.objects.all())
    # location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False)
    class Meta:
        model = Transaction
        fields = ['id','title','description','amount','income_to', 'income_from', 'expense', 'goal', 'source', 'location','periodic', 'tag','created_at', 'modified_at']
        extra_kwargs = {
            # "user":{'write_only':True},
            'title':{'required':False},
            'description':{'required':False},
            'amount':{'required':False},
            'income_from':{'required':False},
            'expense':{'required':False},
            'income_to':{'required':False},
            'goal':{'required':False},
            'source':{'required':False},
            'location':{'required':False},
            'periodic':{'required':False},
            "created_at":{'read_only':True, 'required':False},
            "modified_at":{'required':False},
            "tag":{"required":False}   
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        tags = ""
        if 'tag' in validated_data and validated_data['tag'] is not None:
            tags = validated_data.pop('tag')
        
        Transaction_Data = Transaction.objects.create(**validated_data)

        if tags is not None:
            for x in tags:
                Transaction_Data.tag.add(x)
        return Transaction_Data
# User Transaction Serializer Code End #

# User loction Serializer Code Start #
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','latitude','longitude']

        extra_kwargs = {
            'id':{'read_only':True}
        }

    def create(self, validated_data):
        location = Location.objects.create(
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'])
        location.save()
        return location
# User loction Serializer Code End #

# User Periodic Serializer Code Start #
class PeriodicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodic
        fields = ['id','start_date','end_date','prefix','prefix_value']

        extra_kwargs = {
            'id':{'read_only':True}
        }

    def create(self, validated_data):
        periodic = Periodic.objects.create(
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            prefix=validated_data['prefix'],
            prefix_value=validated_data['prefix_value'])
        periodic.save()
        return periodic 
# User Periodic Serializer Code End #

# User setting Serializer Code Start #
class SettingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Setting
        fields = ['id','notification','min_pass_3','language','currency','modified_at','user']
        extra_kwargs = {
            "notification":{"required":False},
            "min_pass_3":{"required":False},
            "language":{"required":False},
            "currency":{"required":False},
            "user_id":{"read_only":True}
        }


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Setting.objects.create(**validated_data)        
# User setting Serializer Code End #

# User SourceIncome Serializer Code Start #        
class SourceIncomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SourceIncome
        fields = ['id','icon','title','amount','created_at','modified_at']
        extra_kwargs = {
            "icon":{"required":False},
            "title":{"required":False},
            "amount":{"required":False},
           
            # "user_id":{"read_only":True}
        }


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return SourceIncome.objects.create(**validated_data) 
# User SourceIncome Serializer Code end # 
        

# User Reltionsourceincome Serializer Code Start # 
class ReltionsourceincomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reltionsourceincome
        fields = ['id','source_id','ins_id','amount','created_at','modified_at',]
        extra_kwargs = {
            "source_id":{"required":False},
            "ins_id":{"required":False},
            "amount":{"required":True},
           
            # "user_id":{"read_only":True}
        }


    def create(self, validated_data):
        # validated_data['user'] = self.context['request'].user
        return Reltionsourceincome.objects.create(**validated_data)                
# User Reltionsourceincome Serializer Code end #         



# User Debt Serializer Code Start # 
class DebtSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Debt
        fields = ['id','icon','name','date','amount','created_at','modified_at',]
        extra_kwargs = {
            "name":{"required":False},
            "date":{"required":False},
            "amount":{"required":False},
            "icon":{"required":False},
           
            # "user_id":{"read_only":True}
        }


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Debt.objects.create(**validated_data)
# User Debt Serializer Code end # 


# User Tag Serializer Code Start # 
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['id','name']
        extra_kwargs = {
            "name":{"required":False},
            
           
            # "user_id":{"read_only":True}
        }


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Tag.objects.create(**validated_data)
# User Tag Serializer Code end # 


class ResetPasswordSerializer(serializers.ModelSerializer):
    ''' User Login by email and password '''
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.get(email=email)
        print(user)
        if user:
            print(user)
            uid = urlsafe_base64_encode(force_bytes(user.email))
            print(uid)
            email=urlsafe_base64_decode(uid)
            print(email)
            # link = 'http://127.0.0.1:8000/api/user/passwordreset/'+uid+ '/' +token
            # print(link)
            return email
        else:
            return response({"message":"you are not register user"})
