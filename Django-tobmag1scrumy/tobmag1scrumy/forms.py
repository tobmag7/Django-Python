from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import GoalStatus, ScrumyGoals 

# Create your forms here

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']

class AddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'goal_status']

class MoveGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']

class DevMoveGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class OwnerChangeGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']

class AdminOthersChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])
    
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QADoneChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QAPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QAVerifyChangegoal(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:2][::-1]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QAChangeGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status', 'user']