from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'taskapp'

urlpatterns = [
    # Authentication view
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Staff Panel
    path('', StaffHomeView.as_view(), name='staffhome'),
    path('task/<int:pk>/detail/',
         StaffTaskDetailView.as_view(), name='stafftaskdetail'),
    path('task/<int:pk>/update/',
         StaffTaskUpdateView.as_view(), name="stafftaskupdate"),
    # Admin Panel

    path('adminhome/', AdminHomeView.as_view(), name='adminhome'),
    # Staff Management
    path('register/', AdminStaffRegisterView.as_view(),
         name='adminstaffregister'),
    # Task Management
    path('admin/task/create/', AdminTaskCreateView.as_view(),
         name='admintaskcreate'),
    path('admin/task/<int:pk>/detail/',
         AdminTaskDetailView.as_view(), name='admintaskdetail'),
    path('admin/task/<int:pk>/update/',
         AdminTaskUpdateView.as_view(), name='admintaskupdate'),
    path('admin/task/<int:pk>/delete/',
         AdminTaskDeleteView.as_view(), name='admintaskdelete')



]
