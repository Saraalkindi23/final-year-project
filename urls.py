# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('login/', views.login_view, name='login'),# Maps the root URL to the 'home' view
     path('fridge/', views.fridge_prediction, name='fridge_prediction'),
    path('garage/', views.garage_predict, name='garage_predict'),
    path('gps/', views.gps_predict, name='gps_predict'),
    path('light/', views.light_prediction, name='light_prediction'),
    path('fridge/', views.fridge, name='fridge'),
    path('garage/', views.garage, name='garage'),
    path('light/', views.light, name='light'),
    path('gps/', views.gps, name='gps'),
    path('iot/', views.iot, name='iot'),
]
