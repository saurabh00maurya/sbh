from django.shortcuts import render,redirect
from . models import Enquiry,LoginInfo
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def contactus(request):
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(name=name,contactno=contactno,email=email,subject=subject,message=message)
        enq.save()
        messages.success(request,"Your Enquiry has been sucessfully submitted")
        return redirect('contactus')
    return render(request,'contactus.html')


def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=LoginInfo.objects.get(usertype='admin', username=username,password=password)
            if ad is not None:
                request.session['adminid']=username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
        except:
            messages.error(request,"Invalid Credentials")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')



def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        usertype = request.POST.get('usertype') 
        password = request.POST.get('password')
        u=LoginInfo.objects.filter(username=email)
        if u:
            messages.error(request,"Email already exists")
            return redirect('register')
        log = LoginInfo(usertype=usertype,username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"You are registerd")
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            log = LoginInfo.objects.get(username=username,password=password)
            if log is not None:
                if log.usertype.lower() == "homeowner":
                    request.session['homeownerid'] = username
                    messages.success(request,"Welcome Homeowner")
                    return redirect('homeownerdash')
                elif log.usertype.lower() == "contractor":
                    request.session['contractorid'] = username
                    messages.success(request,"Welcome Contractor")
                    return redirect('contractordash')
                else:
                    messages.error(request,"something went wrong")
                    return redirect('login')   
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')
