from contextlib import redirect_stderr, redirect_stdout
from imaplib import _Authenticator
from telnetlib import AUTHENTICATION
from urllib import request, response
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import seat
from django.http import JsonResponse
import io
import time
from django.http import FileResponse
from reportlab.lib.utils import ImageReader
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def home(request):
    # for i in range(20):
    #     r = seat.objects.create(seat_number=i)
    #     r.save()
    return render(request,"index.html")

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        rollnum = request.POST['username']
        email = request.POST['email']
        passw = request.POST['passworry']
        myuser=User.objects.create_user( username=rollnum,email=email, password=passw)
        myuser.first_name=name
        myuser.save()
        messages.success(request,"accunt successfully created")
        return redirect('signin')
    return render(request,"signup.html")

def signin(request):
    data={}
    inte=   seat.objects.all()
   
    if request.method=='POST':
            namer = request.POST['username']
            passw=request.POST['passw']
            User=authenticate(username=namer, password=passw)
            # print(User.username)
            if  User is not None:
                login(request,User)
                data={  
                    'name':User.first_name,
                    'hell':inte,
                }
                return render(request,"index.html",data)
            else:
                messages.error(request,"bad credentials")
                return render(request,"signin.html",data)
    return render(request,"signin.html")


def invoice(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    use= request.user
    name= use.first_name
    tickets = seat.objects.filter(person_name=name)
    lines = []

    for ticket in tickets:
        lines.append(ticket.seat_number)
        lines.append(ticket.person_name)
        lines.append(ticket.status)
        lines.append(" ")

    for line in lines:
        textob.textLine(str(line))

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='invoice.pdf')

def signout(request):
    time.sleep(5)
    logout(request)
    
    messages.success(request,"loged out successfully")
    return render(request,"index.html")
    
def seat_data(request):
    if request.method=="POST":
        print(request.user)
        name = request.POST['person_name']
        rnum= request.POST['rno']
        seat_info = seat.objects.get(seat_number=rnum)
        seat_info.person_name=name
        seat_info.status=True
        seat_info.save()      
        inte= seat.objects.all()
        data={
            'name':name,
            'hell':inte,                
        }
        messages.success(request,"seat was alloted successfully")
        return render(request,"index.html",data)
    return HttpResponse("hello world") 
