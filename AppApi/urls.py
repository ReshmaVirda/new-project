from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name="register"),
    path('login', views.UserLoginView.as_view(), name="login"),
    path('income', views.IncomeCreate.as_view(), name="get_income"),
    path('expense', views.ExpenseCreate.as_view(), name="expense"),
    path('goal', views.GoalsCreate.as_view(), name="goal"),
    path('exchangerate', views.ExchangerateCreate.as_view(), name="exchangerate"),
    path('periodic', views.PeriodicDetailView.as_view(), name="periodic"),
    path('transaction', views.TransactionView.as_view(), name="transaction"),
    path('transaction/<int:pk>', views.TransactionView.as_view(), name="transaction"),
    path('setting', views.SettingView.as_view(), name="setting"),
    path('location', views.LocationDetailView.as_view(), name="location"),
    path('sourceincome', views.SourceIncomeView.as_view(), name="sourceincome"),
    path('sourceincome/<int:pk>', views.SourceIncomeDetailView.as_view(), name="sourceincome"),
    path('homeapi', views.HomeapiView.as_view(), name="homeapi"),
    path('debt', views.DebtView.as_view(), name="debt"),
    path('relationsourceincome', views.ReltionsourceincomeDetailView.as_view(), name="relationsourceincome"),
    path('tag', views.TagView.as_view(), name="tag"),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name="tag"),
    path('report', views.ReportView.as_view(), name="report"),
    path('report/pdf', views.ReportView.as_view(), name="report/pdf"),
    path('passwordreset',views.ResetPasswordView.as_view(),name="passwordreset"),
    path('changepassword', views.UserChangePasswordView.as_view(), name="changepassword"),
    path('token',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh',TokenRefreshView.as_view(),name="token_refresh"),
    path('logout', views.LogoutView.as_view(), name="logout"),
   
    path('excel', views.export_users_xls, name="excel"),
    

]
