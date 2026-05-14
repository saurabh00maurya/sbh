from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from homeownerapp.models import *
from .models import *
from decimal import Decimal


# Contractor Dashboard
def contractordash(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')

    contractor = UserInfo.objects.filter(email=contractorid).first()

    totalprojects = Project.objects.filter(contractor=None).count()

    appliedprojects = ContractorApplication.objects.filter(
        contractor=contractor
    ).count()

    assignedprojects = Project.objects.filter(
        contractor=contractor
    ).count()

    recentapplications = ContractorApplication.objects.filter(
        contractor=contractor
    ).order_by('-id')[:5]

    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'totalprojects': totalprojects,
        'appliedprojects': appliedprojects,
        'assignedprojects': assignedprojects,
        'recentapplications': recentapplications
    }

    return render(request,'contractordash.html',context)



# Logout
def contractorlogout(request):

    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('login')

    return redirect('login')



# Change Password
def changepasscontractor(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    if request.method == "POST":

        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')

        logininfo = LoginInfo.objects.get(username=contractorid)

        if logininfo.password != oldpwd:

            messages.error(request,"Old password is incorrect")

        elif newpwd != confirmpwd:

            messages.error(request,"New password and confirm password do not match")

        else:

            logininfo.password = newpwd
            logininfo.save()

            messages.success(request,"Password changed successfully")
            return redirect('contractordash')

    context = {
        'name':contractor.name,
        'contractorid':contractorid
    }

    return render(request,'changepasscontractor.html',context)



# Contractor Profile
def contractorprofile(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor
    }

    return render(request,'contractorprofile.html',context)



# Edit Profile
def contractoredit(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    if request.method == "POST":

        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')

        contractor.name = name
        contractor.contactno = contactno
        contractor.address = address
        contractor.bio = bio

        if profile:
            contractor.picture = profile

        contractor.save()

        messages.success(request,"Your profile has been updated")
        return redirect('contractorprofile')

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor
    }

    return render(request,'contractoredit.html',context)



# View Available Projects
def contractorviewprojects(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    projects = Project.objects.filter(contractor=None)

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
        'projects':projects
    }

    return render(request,'contractorviewproject.html',context)



# Apply for Project
def applyproject(request,id):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    project = Project.objects.get(id=id)

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
        'project':project
    }

    application = ContractorApplication.objects.filter(
        project=project,
        contractor=contractor
    )

    if application.exists():

        messages.warning(request,"You have already applied for this project")
        return redirect('contractorviewprojects')


    if request.method == "POST":

        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget = request.POST.get('estimated_budget')

        try:
            estimated_budget = Decimal(estimated_budget)

        except:

            messages.error(request,"Invalid estimated budget")
            return redirect('contractorviewprojects')


        estimated_duration = request.POST.get('estimated_duration')

        app = ContractorApplication(

            contractor = contractor,
            project = project,
            proposal_text = proposal_text,
            design_file = design_file,
            estimated_budget = estimated_budget,
            estimated_duration = estimated_duration

        )

        app.save()

        messages.success(request,"Project Application Submitted Successfully")
        return redirect('contractorviewprojects')

    return render(request,'applyproject.html',context)



# Contractor Applications
def contractorapplications(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    applications = ContractorApplication.objects.filter(contractor=contractor)

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
        'applications':applications
    }

    return render(request,'contractorapplications.html',context)



# Assigned Projects
def assignedprojects(request):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    projects = Project.objects.filter(contractor=contractor)

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects
    }

    return render(request,'assignedprojects.html',context)



# Add Progress
def addprogress(request,id):

    if 'contractorid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    project = Project.objects.get(id=id)

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project
    }

    if request.method == 'POST':

        update_text = request.POST.get('update_text')
        image = request.FILES.get('image')
        progress_percent = int(request.POST.get('progress_percent'))

        if progress_percent > 100:

            messages.error(request,"Progress cannot be more than 100%")
            return redirect('addprogress',id=id)

        elif progress_percent < project.progress:

            messages.error(request,"Progress cannot be less than previous progress")
            return redirect('addprogress',id=id)


        pu = ProgressUpdate(

            project = project,
            update_text = update_text,
            image = image,
            progress_percent = progress_percent,
            updated_by = contractor

        )

        if progress_percent == 100:
            project.status = 'completed'

        project.progress = progress_percent
        project.save()

        pu.save()

        messages.success(request,"Progress updated successfully")
        return redirect('assignedprojects')

    return render(request,'addprogress.html',context)