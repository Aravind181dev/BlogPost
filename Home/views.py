from django.shortcuts import render,redirect
from django.contrib.auth import login , authenticate
from django.contrib.auth.models import User , auth
from . models import Post
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all().order_by('-id')
    return render(request,'index.html',{'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})


@login_required
def blogadmin(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            print(f"Title: {title}, Content: {content}, User: {request.user}")
            if title and content:
                # Create a new post associated with the current user
                Post.objects.create(title=title, content=content, author=request.user)
                return redirect('home')
            else:
                error_message = 'Please provide a title and content for the post.'
                return render(request, 'blogadmin.html', {'error_message': error_message})
        elif 'update' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            # Ensure the post belongs to the current user
            if post.author == request.user:
                post.title = request.POST.get('title')
                post.content = request.POST.get('content')
                post.save()
            return redirect('home')
        elif 'delete' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            # Ensure the post belongs to the current user
            if post.author == request.user:
                post.delete()
            return redirect('home')
        else:
            return redirect('home')
    else:
        # Fetch posts associated with the current user
        posts = Post.objects.filter(author=request.user)
        return render(request, 'blogadmin.html', {'posts': posts})
    

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                error_message = 'Username already exists'
            elif User.objects.filter(email=email).exists():
                error_message = 'Email already exists'
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                
                return redirect('home')
        else:
            error_message = 'Passwords do not match'
    else:
        error_message = ''

    return render(request, 'signup.html', {'error_message': error_message})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''

    return render(request,'signin.html',{'error_message': error_message})

def logout(request):
    auth.logout(request)
    return redirect('home')