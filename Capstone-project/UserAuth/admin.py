from django.contrib import admin
from .models import UserModel
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email','is_superuser','profile_picture']
    ordering = ['id']


admin.site.register(UserModel,UserModelAdmin)   