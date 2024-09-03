from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('manage/', views.manage_registration, name='manage_registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.signup_user, name='signup'),
]
