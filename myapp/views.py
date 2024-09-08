from django.shortcuts import render, redirect
from .models import Features
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
from django.contrib import messages

def index(request):
    features = Features.objects.all()
    return render(request, 'index.html', {'features': features})

def register(request):
    if request.method == 'POST' or request.method == 'post':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        if password == password_repeat:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            else:
                user = User.objects.create(username=username, email=email, password=password)
                user.password = make_password(password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not identical')
            return redirect('register')

    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST' or request.method == 'post':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        print(user)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

        # if User.objects.filter(username=username).exists():
        #     if User.objects.filter(password=password).exists():
        #         return render(request, 'index.html')
        #     else:
        #         messages.info(request, 'Incorrect Password')
        #         return render(request, 'login.html')
        # else:
        #     messages.info(request, 'Incorrect Username')
        #     return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})

def counter(request):
    text = request.POST['text']
    text_len = len(text.split())
    return render(request, 'counter.html', {'text':text, 'text_len': text_len})