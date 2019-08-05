from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'tobmag1scrumy'

# create url patterns here
urlpatterns = [
    path('', views.index, name = 'index'),

    path('filter/', views.filterArg, name = 'filterArg'),

    path('movegoal/<int:goal_id>/', views.move_goal, name = "movegoal"),

    path('addgoal/', views.add_goal, name='addgoal'),
    
    path('home/', views.home, name='home'),

    path('addgoalsuccess/', views.addgoalsuccess, name = 'addgoalsuccess'),

    path('movegoalsuccess/', views.move_goal_success, name = 'movegoalsuccess'),

    path('accounts/', include('django.contrib.auth.urls')),

]