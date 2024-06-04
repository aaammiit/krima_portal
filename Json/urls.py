"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.Home),
    path('admin_home',v.Admin_home),
    path('delete_file/<int:id>',v.Delete),
    path('view_file/<int:id>',v.View_file),
    path('push_to_pm/<int:pid>',v.Push_to_pm),
    path('logout_user',v.Logout_user),


    path('make_pm',v.Make_pm),
    path('pm_login',v.PM_login),
    path('pm_home',v.PM_home),
    path('pm_view_file/<int:id>',v.PM_view_file),
    path('pm_delete_file/<int:id>',v.PM_file_delete),
    path('push/<int:id>',v.Push_to_qc),
    path('download/<int:id>',v.Download_file),


    path('make_qc',v.Make_qc),
    path('qc_login',v.QC_login),
    path('qc_home',v.QC_home),
    path('qc_view_file/<int:id>',v.QC_view_file),
    # path('qc_edit_file/<int:id>',v.QC_edit_file),
    path('qc_edit_data/<int:pid>/<int:did>',v.QC_Edit_data),


    path('make_ed',v.Make_ed),
    path('ed_login',v.ED_login),
    path('ed_home',v.ED_home),
    path('push_to_ed/<int:id>',v.Push_to_Ed),
    path('ed_view/<int:id>',v.ED_view_file),
    path('ed_edit_data/<int:pid>/<int:did>',v.ED_Edit_data),
    path('ed_send/<int:id>',v.ED_send_file),

    path('about_us',v.About,name='about_us'),
   

]
