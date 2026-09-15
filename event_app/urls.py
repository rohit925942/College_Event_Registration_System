from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),   # ye line add karo
    path('events/', views.events, name='events'),
    path('join/<int:event_id>/', views.join_event, name='join_event'),
    path('logout/', views.logout, name='logout'),
    path('my-events/', views.my_events, name='my_events'),
]

