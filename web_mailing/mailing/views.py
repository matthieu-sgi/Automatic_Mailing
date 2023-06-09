from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def index(request):
    return HttpResponse("Hello, world. You're at the mailing index.")

def digit_psswd(request, digit : str):
    global psswd
    psswd = digit
    return HttpResponse(f'Password entered.')

