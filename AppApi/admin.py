from django.contrib import admin
from .models import User,Income,Expense,Goal,Exchangerate,Periodic,Setting, SourceIncome,Debt,Transaction,Location,Reltionsourceincome,Tag
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'mobile', 'gender', 'country', 'is_active', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('gender', 'mobile', 'country')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'gender', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('email', 'id')
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Income)
admin.site.register(Expense)

#this is Goal api start#
class GoalAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'title', 'amount', 'icon', 'created_at', 'modified_at', 'user')
    list_filter = ('amount', 'created_at',)
    search_fields = ('title', 'id')
    ordering = ('title', 'id')
    list_per_page = 10
    def has_add_permission(self, request):
        return False

admin.site.register(Goal, GoalAdmin)
#this is Goal api End#

#this is Exchange api start#
class ExchangerateAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'currency_name','is_default', 'user')
    list_filter = ('currency_name', 'is_default',)
    search_fields = ('currency_name','id')
    ordering = ('currency_name','id')
    list_per_page = 10
    def has_add_permission(self, request):
        return False

admin.site.register(Exchangerate, ExchangerateAdmin)
#this is Exchange api end#

#this is transaction api start#
# class TransactionAdmin(admin.ModelAdmin):
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('id', 'title','description', 'amount', 'ins_id','exp','location','periodic', 'created_at', 'modified_at', 'user')
#     list_filter = ('id', 'created_at')
#     search_fields = ('created_at','id')
#     ordering = ('created_at','id')
#     list_per_page = 10
#     def has_add_permission(self, request):
#         return False

# admin.site.register(Transaction, TransactionAdmin)
#this is transaction api end#

#this is loction api start#
class LocationAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'latitude','longitude')
    list_filter = ('id',)
    search_fields = ('id',)
    ordering = ('id',)
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Location, LocationAdmin)
#this is loction api end#

#this is periodic api start#
class PeriodicAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'start_date','end_date','prefix','prefix_value')
    list_filter = ('id',)
    search_fields = ('id',)
    ordering = ('id',)
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Periodic, PeriodicAdmin)
#this is periodic api end#

#this is setting api start#
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'notification', 'min_pass_3', 'language', 'currency', 'modified_at')
    list_filter = ('user','language')
    search_fields = ('id','user')
    ordering = ('id','user')
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Setting,SettingAdmin)
#this is setting api end# 

#this is Source api start#
class SourceIncomeAdmin(admin.ModelAdmin):
    list_display = ('id','icon', 'title', 'amount', 'created_at',  'modified_at','user')
    list_filter = ('id','title')
    search_fields = ('id','title')
    ordering = ('id','title')
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(SourceIncome,SourceIncomeAdmin)
#this is Source api end#

#this is Reltionsourceincome api start#
class ReltionsourceincomeAdmin(admin.ModelAdmin):
    list_display = ('id','source_id', 'ins_id', 'amount', 'created_at',  'modified_at')
    list_filter = ('id',)
    search_fields = ('id',)
    ordering = ('id',)
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Reltionsourceincome,ReltionsourceincomeAdmin)
#this is Reltionsourceincome api end#

#this is Debt api start#
class DebtAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'amount', 'date', 'created_at',  'modified_at')
    list_filter = ('id','name')
    search_fields = ('id','name')
    ordering = ('id','name')
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Debt,DebtAdmin)
#this is Debt api end#

#this is tag api start#
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_filter = ('id','name')
    search_fields = ('id','name')
    ordering = ('id','name')
    list_per_page = 10

    def has_add_permission(self, request):
        return False

admin.site.register(Tag,TagAdmin)
#this is Debt api end#