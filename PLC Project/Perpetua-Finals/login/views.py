from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')
