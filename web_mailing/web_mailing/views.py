from django.shortcuts import render
from django.http import HttpResponse

import os


def home(request):
    print(os.getcwd())
    return render(request, './templates/home.html')