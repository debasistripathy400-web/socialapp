from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Post, Like, Comment, Story, ProfileVisit, Notification
from .forms import RegistrationForm, LoginForm, PostForm, UserUpdateForm
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

@login_required
def home(request):
    # Get active stories (from public accounts OR accounts the user follows)
    all_stories = Story.objects.filter(
        Q(user__is_private=False) | Q(user=request.user) | Q(user__in=request.user.following.all()),
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('created_at')
    
    seen_users = set()
    starting_stories = []
    for story in all_stories:
        if story.user_id not in seen_users:
            starting_stories.append(story)
            seen_users.add(story.user_id)

    # Filter posts: Show if public OR if user is owner OR if user is follower
    posts = Post.objects.filter(
        Q(user__is_private=False) | Q(user=request.user) | Q(user__in=request.user.following.all())
    ).order_by('-created_at')
    
    # Check if current user likes each post
    for post in posts:
        post.is_liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'posts': posts,
        'stories': starting_stories,
    }
    return render(request, 'core/home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {
        'form': form, 
        'hide_nav': True
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else 'home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {
        'form': form,
        'hide_nav': True
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    
    # Record visit if not visiting own profile
    if request.user != profile_user:
        ProfileVisit.objects.get_or_create(visitor=request.user, profile=profile_user)

    is_following = request.user.following.filter(id=profile_user.id).exists()
    
    # Check if content should be hidden
    can_view_content = True
    if profile_user.is_private and request.user != profile_user and not is_following:
        can_view_content = False

    context = {
        'profile_user': profile_user,
        'posts': posts if can_view_content else None,
        'is_following': is_following,
        'post_count': posts.count(),
        'follower_count': profile_user.followers.count(),
        'following_count': profile_user.following.count(),
        'can_view_content': can_view_content,
    }
    return render(request, 'core/profile.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query)).exclude(id=request.user.id)
    
    # SQLite compatibility for visited profiles
    visited_profiles_ids = ProfileVisit.objects.filter(visitor=request.user).values_list('profile_id', flat=True).distinct()[:10]
    visited_profiles = User.objects.filter(id__in=visited_profiles_ids)

    context = {
        'users': users,
        'query': query,
        'visited_profiles': visited_profiles,
    }
    return render(request, 'core/search.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj = Like.objects.filter(post=post, user=request.user)
    
    if like_obj.exists():
        like_obj.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        # Trigger Notification
        if post.user != request.user:
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type='LIKE',
                post=post,
                text='liked your post'
            )
        liked = True
        
    return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('text')
        if comment_text:
            comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
            # Trigger Notification
            if post.user != request.user:
                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    notification_type='COMMENT',
                    post=post,
                    text=f'commented: {comment.text[:30]}...'
                )
            return JsonResponse({
                'username': comment.user.username,
                'profile_pic': comment.user.profile_picture.url if comment.user.profile_picture else '/static/img/default.jpg',
                'text': comment.text,
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
            target_user.followers.remove(request.user)
            followed = False
        else:
            request.user.following.add(target_user)
            target_user.followers.add(request.user)
            # Trigger Notification
            Notification.objects.create(
                recipient=target_user,
                sender=request.user,
                notification_type='FOLLOW',
                text='started following you'
            )
            followed = True
        return JsonResponse({'followed': followed})
    return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def create_story(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        if media:
            Story.objects.create(user=request.user, media=media)
            return redirect('home')
    return render(request, 'core/create_story.html')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    # Mark all as read when viewed
    notifications.update(is_read=True)
    return render(request, 'core/notifications.html', {'notifications': notifications})

@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    # Privacy Check
    is_following = request.user.following.filter(id=story.user.id).exists()
    if story.user.is_private and request.user != story.user and not is_following:
        return redirect('profile', username=story.user.username)
    # Find next story for the same user within 24h
    next_story = Story.objects.filter(
        user=story.user, 
        created_at__gt=story.created_at,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('created_at').first()
    
    # Find previous story for same user within 24h
    prev_story = Story.objects.filter(
        user=story.user, 
        created_at__lt=story.created_at,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at').first()
    
    return render(request, 'core/view_story.html', {
        'story': story, 
        'next_story': next_story,
        'prev_story': prev_story,
        'hide_nav': True
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('home')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        caption = request.POST.get('caption')
        if caption:
            post.caption = caption
            post.save()
            return redirect('home')
    return render(request, 'core/edit_post.html', {'post': post})

@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)
    story.delete()
    return redirect('home')
