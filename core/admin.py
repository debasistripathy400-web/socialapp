from django.contrib import admin
from .models import User, Post, Like, Comment, Story, ProfileVisit

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_id')
    search_fields = ('username', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('caption', 'user__username')

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(ProfileVisit)
