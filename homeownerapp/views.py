from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import *
from django.utils import timezone 
# Create your views here.
def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()

    totalprojects = Project.objects.filter(homeowner=homeowner).count()

    runningprojects = Project.objects.filter(
        homeowner=homeowner,
        status='under_construction'
    ).count()

    completedprojects = Project.objects.filter(
        homeowner=homeowner,
        status='completed'
    ).count()

    recentprojects = Project.objects.filter(
        homeowner=homeowner
    ).order_by('-id')[:5]

    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'totalprojects':totalprojects,
        'runningprojects':runningprojects,
        'completedprojects':completedprojects,
        'recentprojects':recentprojects
    }

    return render(request,'homeownerdash.html',context)

def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('login')
    
def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner
    }
    return render(request,'homeownerprofile.html',context)

# def changepass(request):
#     if not 'homeownerid' in request.session:
#         messages.error(request,"You are not Logged in as a admin")
#         return redirect('homeownerlogin')
#     adminid = request.session.get('homeownerid')
#     if request.method =='POST':
#         oldpwd = request.POST.get('oldpwd')
#         newpwd = request.POST.get('newpwd')
#         confirmpwd = request.POST.get('confirmpwd')
#         try:
#             admin = LoginInfo.objects.get(username=homeownerid)
#             if homeownerdash.password != oldpwd:
#                 messages.error(request,"Old passward is incorrect")
#             elif newpwd != confirmpwd:
#                 messages.error(request,"New password and Confirm password is same")
#                 return redirect('homechangepass')
#             elif homeowner.password == newpwd:
#                 messages.error(request,"new password is same as old password")
#                 return redirect('homechangepass')
#             else:
#                 homeowner.password = newpwd
#                 homeowner.save()
#                 messages.success(request,"Password changed succesfully")
#                 return redirect('homeownerdash')
#         except LoginInfo.DoesNotExist:
#             messages.error(request,"Something went wrong")
#             return redirect('homeownerdash')
#     return render(request,'homechangepass.html',{'homeownerid':homeownerid})

def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        name = request.POST.get('name')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        homeowner.name =name
        homeowner.contactno = contactno
        homeowner.address = address
        homeowner.bio = bio
        if profile:
            homeowner.picture = profile
        homeowner.save()
        messages.success(request,"Your profiel has been updated")
        return redirect('homeownerprofile')
    return render(request,'homeowneredit.html',context)

def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid ,
        'form':form
    }
    if request.method =="POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request,"PRoject has been added")
            return redirect('addproject')
    return render(request,'addproject.html',context)




def homeownerviewproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects=Project.objects.filter(homeowner=homeowner)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'homeownerviewproject.html',context)








def homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
    }
    return render(request,'homeownerviewapplications.html',context)




def rejectapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app=ContractorApplication.objects.get(id=id)
    app.status='rejected'
    app.save()
    messages.success(request,"application has been rejected")
    return redirect('homeownerviewapplications',id=app.project.id)


def approveapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app=ContractorApplication.objects.get(id=id)
    project=Project.objects.get(id=app.project.id)
    apps=ContractorApplication.objects.filter(project=app.project).update(status="rejected")
    app.status='approved'
    app.save()
    project.contractor=app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request,"application has been Appreoved")
    return redirect('homeownerviewapplications',id=app.project.id)

def runningprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='under_construction')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'runningprojects.html',context)

def viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'updates':updates,
    }
    return render(request,'viewupdates.html',context)

def homeownercompletedproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='completed')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'homeownercompletedproject.html',context)

def homechangepass(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()

    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')

        logininfo = LoginInfo.objects.get(username=homeownerid)

        if logininfo.password != oldpwd:
            messages.error(request,"Old password is incorrect")

        elif newpwd != confirmpwd:
            messages.error(request,"New password and Confirm password do not match")

        else:
            logininfo.password = newpwd
            logininfo.save()
            messages.success(request,"Password changed successfully")
            return redirect('homeownerdash')

    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid
    }

    return render(request,'homechangepass.html',context)