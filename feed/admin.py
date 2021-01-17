from django.contrib import admin
from .models import Post,UserProfile
from django.contrib.auth.models import User

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author','publish')
    list_filter = ('publish',)
    search_fields=('title','body')
    date_hierarchy='publish'
    ordering=('publish',)
    raw_id_fields = ('author',)

admin.site.unregister(User)

class User_Prof(admin.TabularInline):
    model = UserProfile

@admin.register(User)
class UserModel(admin.ModelAdmin):
    inlines = [
        User_Prof,
    ]