from django.urls import path,re_path
from . import views
from directory.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('login_req', TemplateView.as_view(template_name="login.html"), name='login'),
    path('home',LoginView.as_view(),name="home"),
    path('add_teacher', views.add_teacher, name='add_teacher'),
    path('bulk_upload', TemplateView.as_view(template_name="bulk_upload.html"), name='bulk_upload'),
    path('add_teacher_bulk', TeachersBulkUpload.as_view(), name='add_teacher_bulk'),
    path('', TeachersListView.as_view(),name='teachers_list'),
    re_path(r'^teacher-detail/(?P<pk>[0-9]+)/$',TeacherDetailView.as_view(), name='teacher_details'),
    path('logout', views.logout_view, name="logout_view"),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
