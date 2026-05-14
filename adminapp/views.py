from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

from homeownerapp.models import *
from contractorapp.models import *
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in as a admin")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid':adminid,
        'th':UserInfo.objects.filter(login__usertype="homeowner").count(),
        'tc':UserInfo.objects.filter(login__usertype="contractor").count(),
        'tp':Project.objects.all().count(),
        'trp':Project.objects.filter(status="Under_construction").count(),
        'tcp':Project.objects.filter(status="completed").count(),
        'enqs':Enquiry.objects.all().count(),

    }
    return render(request,'admindash.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"you are logout")
        return redirect('adminlogin')
    else:
        return redirect('index')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    # adminid = redirect.session.get('adminid')
    enqs = Enquiry.objects.all()
    return render(request,'viewenq.html',{'enqs':enqs,})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enq = Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Enquiry Deleted Successfully")
    return render('viewenq')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
def changepass(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in as a admin")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    if request.method =='POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = LoginInfo.objects.get(username=adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old passward is incorrect")
            elif newpwd != confirmpwd:
                messages.error(request,"New password and Confirm password is same")
                return redirect('changepass')
            elif admin.password == newpwd:
                messages.error(request,"new password is same as old password")
                return redirect('changepass')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request,"Password changed succesfully")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Something went wrong")
            return redirect('adminlogin')
    return render(request,'changepass.html',{'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def managecontractors(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in as a admin")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    return render(request,'managecontractors.html',{'admin':adminid})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in as a admin")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    return render(request,'managehomeowners.html',{'admin':adminid})