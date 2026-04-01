from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.create_post, name='create_post'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('story/create/', views.create_story, name='create_story'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('story/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
