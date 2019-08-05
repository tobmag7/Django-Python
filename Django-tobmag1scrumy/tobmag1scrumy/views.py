from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from random import randint

from .forms import SignUpForm, CreateGoalForm, OwnerChangeGoalForm, QAVerifyChangegoal, DevMoveGoalForm, AdminPersonalChangeGoalForm,AdminOthersChangeGoalForm, QADoneChangeGoalForm, QAPersonalChangeGoalForm
from tobmag1scrumy.models import GoalStatus, ScrumyGoals, ScrumyHistory

# Create your views here.

content_type_scrumygoals = ContentType.objects.get_for_model(ScrumyGoals)
content_type_goalstatus = ContentType.objects.get_for_model(GoalStatus)


developergroup = Group.objects.get(name='Developer')
admingroup = Group.objects.get(name='Admin')
qualityassurancegroup = Group.objects.get(name='Quality Assurance')
ownergroup = Group.objects.get(name='Owner')
verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
donegoal = GoalStatus.objects.get(status_name="Done Goal")
weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    
def index(request):
    form = SignUpForm()
    if request.method == 'GET':
        return render(request, 'tobmag1scrumy/index.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            formdata = request.POST.copy()
            
            form.save()

            username = formdata.get('username')
            password = formdata.get('password')
            user = authenticate(username=username, password=password)
            user.is_staff=True
            login(request,user)
            devgroupuser = Group.objects.get(name='Developer')
            # user = User.objects.get(username=username, password=password)
            devgroupuser.user_set.add(user)
            successful = 'Your account has been created successfully'
            context = {'success': successful}
            return render(request, 'tobmag1scrumy/successful.html', context)
    else:
        form = SignUpForm()
        return HttpResponseRedirect(reverse('tobmag1scrumyindex:index'))

def filterArg(request):
    output = ScrumyGoals.objects.filter(goal_name='Learn Django')
    return HttpResponse(output)



def move_goal(request, goal_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    
    # goal = get_object_or_404(ScrumyGoals, pk=goal_id)
    try:
        goal = ScrumyGoals.objects.get(goal_id=goal_id)
    except ObjectDoesNotExist:
        notexist = 'A record with that goal id does not exist'
        context = {'not_exist': notexist}
        return render(request, 'tobmag1scrumy/exception.html')

    if usr_grp == Group.objects.get(name='Developer'): 
        if current_user == goal.user:
            form = DevMoveGoalForm()

            if request.method == 'GET':
                return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

            if request.method == 'POST':
                form = DevMoveGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))

            else:
                form = DevMoveGoalForm()
                return render(request, 'tobmag1scrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})

        if current_user != goal.user:
            notexist = 'A Developer Cannot move other users goals'
            context = {'not_exist': notexist}
            return render(request, 'tobmag1scrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Admin'):
        if current_user == goal.user:
            form = AdminPersonalChangeGoalForm()

            if request.method == 'GET':
                return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = AdminPersonalChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))
            else:
                form = AdminPersonalChangeGoalForm()
                return render(request, 'tobmag1scrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
     
        if current_user != goal.user and goal.goal_status == dailygoal or goal.goal_status == verifygoal:
            form = AdminOthersChangeGoalForm()

            if request.method == 'GET':
                return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = AdminOthersChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))
            else:
                form = AdminOthersChangeGoalForm()
                return render(request, 'tobmag1scrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    
        if current_user != goal.user and goal.goal_status != dailygoal or goal.goal_status != verifygoal:
            notexist = 'Admin Can Only Move other users goals back and forth from Daily Column to Verify Column'
            context = {'not_exist': notexist}
            return render(request, 'tobmag1scrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Owner'):
        form = OwnerChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
                form = OwnerChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))
        else:
            form = OwnerChangeGoalForm()
            return render(request, 'tobmag1scrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    
    
    if usr_grp == Group.objects.get(name='Quality Assurance'):
        if goal.goal_status == verifygoal:
            form = QAVerifyChangegoal()

            if request.method == 'GET':
                return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = QAVerifyChangegoal(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))
            else:
                form = QAVerifyChangegoal()
                return render(request, 'tobmag1scrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

        if goal.goal_status == donegoal:
            form = QADoneChangeGoalForm()
            if request.method == 'GET':
                return render(request, 'tobmag1scrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = QADoneChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('tobmag1scrumy:movegoalsuccess'))

            else:
                form = QADoneChangeGoalForm()
                return render(request, 'tobmag1scrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

        if goal.goal_status != verifygoal or goal.goal_status != donegoal and current_user != goal.user:

            notexist = 'Quality assurance Can Only Move other users goals from Verify Column to Done Column, and from Done Column to other columns'
            context = {'not_exist': notexist}
            return render(request, 'tobmag1scrumy/exception.html', context)


def move_goal_success(request):
    current_user = request.user
    return render(request, 'tobmag1scrumy/movegoalsuccess.html', {'currentuser': current_user})

def error(request):
    current_user = request.user
    return render(request, 'tobmag1scrumy/error.html', {'currentuser': current_user})

def addgoalsuccess(request):
    current_user = request.user
    return render(request, 'tobmag1scrumy/addgoalsuccess.html', {'currentuser': current_user})



# def add_goal(request):
#     goal_id = randint(1000, 10000)  #returns a random number between 1000 and 9999           
 
#     addgoal = ScrumyGoals.objects.create(
#         goal_name ='Keep Learning Django', 
#         goal_id = goal_id, 
#         created_by='Louis', 
#         moved_by = "Louis", 
#         goal_status = GoalStatus.objects.get(pk=1), 
#         user = User.objects.get(pk=1)
#         )
#     return HttpResponse(addgoal, 'Goal Added Successfully!')

def add_goal(request):
    current_user = request.user
    usr_grp = current_user.groups.values_list('name', flat=True).first()
    
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            goal_id = randint(1000, 10000)
            status_name = GoalStatus(pk=1)
            post.created_by = current_user.first_name
            post.moved_by = current_user.first_name
            post.owner = current_user.first_name
            post.goal_id = goal_id
            post.user = current_user
            post.goal_status = status_name
            post.save()
            return HttpResponseRedirect('/tobmag1scrumy/addgoalsuccess/')
    else:
        form = CreateGoalForm()
    return render(request, 'tobmag1scrumy/addgoal.html', {'form': form, 'currentuser': current_user, 'group': usr_grp})


# def home(request):
#     scrumygoal = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
#     output = ', '.join([eachgoal.goal_name for eachgoal in scrumygoal])
#     return HttpResponse(output)

def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    usr_grp = current_user.groups.values_list('name', flat=True).first()
    scrumygoal = ScrumyGoals.objects.get(goal_name='Keep Learning Django')
    user = User.objects.all()
    goalid = ScrumyGoals.objects.get(goal_id=3391)
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    wg = weeklygoal.scrumygoals_set.all()
    dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
    dg = dailygoal.scrumygoals_set.all()
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    vg = verifygoal.scrumygoals_set.all()
    donegoal = GoalStatus.objects.get(status_name="Done Goal")
    gd = donegoal.scrumygoals_set.all()

    context = {'user': user, 'goalid': goalid, 'weeklygoal': wg, 'dailygoal': dg, 'verifygoal': vg,
                       'donegoal': gd, 'scrumygoal': scrumygoal, 'currentuser': current_user, 'group': usr_grp }
    return render(request, 'tobmag1scrumy/home.html', context)