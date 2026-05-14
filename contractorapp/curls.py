from django.urls import path
from . import views

urlpatterns = [
    path('contractordash/',views.contractordash,name='contractordash'),
    path('contractorlogout/',views.contractorlogout,name='contractorlogout'),
    path('changepasscontractor/',views.changepasscontractor,name='changepasscontractor'),
    path('contractoredit/',views.contractoredit,name='contractoredit'),
    path('contractorprofile/',views.contractorprofile,name='contractorprofile'),
    path('contractorviewprojects/',views.contractorviewprojects,name='contractorviewprojects'),
    path('contractorapplications/',views.contractorapplications,name='contractorapplications'),
    path('assignedprojects/',views.assignedprojects,name='assignedprojects'),
    path('applyproject/<id>',views.applyproject,name='applyproject'),
    path('addprogress/<id>',views.addprogress,name='addprogress'),
]