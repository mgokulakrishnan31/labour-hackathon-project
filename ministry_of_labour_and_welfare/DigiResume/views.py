import base64
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .utilities import *
from .forms import *

# Create your views here.

def index(request):
    if request.GET:
        uid=request.GET.dict()['id'].upper()
        return redirect(f'/{uid}/view_details')
    return render(request,'DigiResume/index.html')



def login(request):
    flag=True
    if request.GET:
        id=request.GET.dict()['id'].upper()
        password=request.GET.dict()['password']
        global sector
        if 'EDU' in id:
            sector=1
            x=Institution.objects.get(inst_code=id).password
        elif 'ORG' in id:
            sector=2
            x=Organisation.objects.get(org_code=id).password
        elif 'SEV' in id:
            sector=3
            x=SevaStore.objects.get(seva_code=id).password
        if password==x:
            return redirect(f'/{id}/home/')
        else:
            flag=False
    return render(request,'DigiResume/login.html',{'flag':flag})



def home(request,code):
    if sector is 1:
        x=Institution.objects.get(inst_code=code)
    elif sector is 2:
        x=Organisation.objects.get(org_code=code)        
    elif sector is 3:
        x=SevaStore.objects.get(seva_code=code)
    return render(request,'DigiResume/home.html',{'sector':sector,'code':code,'x':x})



def register(request,code):
    uid=generateUID()
    if uid in Person.objects.values_list('uid',flat=True):
        return register(request,code)

    if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.uid=uid
                obj.save()
                #card gen
                p_obj = Person.objects.get(uid = uid)
                name= p_obj.name
                dob= p_obj.dob
                gender= p_obj.gender
                photo = p_obj.photo
                info=f'Name:{name}\n\nDOB:{dob}\n\nGender:{gender}'
                card=generateCard(uid,info,photo)
                card.show()
                #updating activity table
                InstitutionActivity(uid=Person(uid = uid), inst_code = Institution(inst_code=code), action = f'User resistered {uid}').save()
                return HttpResponse(f'User resistered {uid}')
    else:
        form = RegisterForm()
    return render(request,'DigiResume/register.html',{'form':form,'sector':sector,'code':code})



def add_course(request,code):
    if request.method == 'POST':
            form = AddCourseForm(request.POST)
            if form.is_valid():
                obj = EducationInfo()
                uid = form.cleaned_data['uid']
                print(type(Person(uid=uid)))
                obj.uid = Person(uid=uid)
                obj.inst_code = Institution(inst_code=code)
                course_name = form.cleaned_data['course_name']
                obj.course_name = course_name
                obj.grade = form.cleaned_data['grade']
                obj.completion_date = form.cleaned_data['completion_date']
                obj.save()
                InstitutionActivity(uid=Person(uid = uid), inst_code = Institution(inst_code=code), action = f'{course_name} Course Added for {uid}').save()
                return HttpResponse(f'{course_name} Course Added for {uid}')


    else:
        form = AddCourseForm()  
    return render(request,'DigiResume/add_course.html',{'code':code,'sector':sector,'form':form})



def add_work(request,code):
    if sector==1:
        if request.method == 'POST':
            form = AddWorkInstitutionForm(request.POST)
            if form.is_valid():
                obj = WorkInfoByInstitution()
                uid = form.cleaned_data['uid']
                obj.uid = Person(uid = uid)
                obj.inst_code = Institution(inst_code=code)
                role = form.cleaned_data['role']
                obj.role = role
                obj.join_date = form.cleaned_data['join_date']
                obj.resign_date = form.cleaned_data['resign_date']
                obj.save()
                InstitutionActivity(uid=Person(uid = Person(uid=uid)), inst_code = Institution(inst_code=code), action = f'{role} Course Added for {uid}').save()
                return HttpResponse(f'{role} Course Added for {uid}')


        else:
            form = AddWorkInstitutionForm()
            
    elif sector==2:
        if request.method == 'POST':
            form = AddWorkOrganisationForm(request.POST)
            if form.is_valid():
                obj = WorkInfoByOrganisation()
                uid = form.cleaned_data['uid']
                obj.uid = Person(uid = uid)
                obj.org_code = Organisation(org_code=code)
                role = form.cleaned_data['role']
                obj.role = role
                obj.join_date = form.cleaned_data['join_date']
                obj.resign_date = form.cleaned_data['resign_date']
                obj.save()
                OrganisationActivity(uid=Person(uid = uid), org_code = Organisation(org_code=code), action = f'{role} Course Added for {uid}').save()
                return HttpResponse(f'{role} Course Added for {uid}')
   
        else:
            form = AddWorkOrganisationForm()

    elif sector==3:
        if request.method == 'POST':
            form = AddUnorganisedWorkForm(request.POST)
            if form.is_valid():
                obj = UnorganisedWorkInfo()
                uid = form.cleaned_data['uid']
                obj.uid = Person(uid = uid)
                obj.seva_code = SevaStore(seva_code=code)
                work = form.cleaned_data['work_name']
                obj.work_name = work
                obj.save()
                SevaActivity(uid=Person(uid = uid), seva_code = SevaStore(seva_code=code), action = f'{work} Course Added for {uid}').save()
                return HttpResponse(f'{work} Course Added for {uid}')
        else:
            form = AddUnorganisedWorkForm()            
    return render(request,'DigiResume/add_work.html',{'code':code,'form':form})




def activity(request,code):
    return render(request,'DigiResume/activity.html',{'code':code})



def view_details(request,uid):
    x=Person.objects.get(uid=uid)
    y = EducationInfo.objects.get(uid=uid)
    return render(request,'DigiResume/view_details.html',{'x':x,'y':y})
