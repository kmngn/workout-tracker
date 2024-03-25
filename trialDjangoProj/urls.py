"""
URL configuration for trialDjangoProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from trial import views

urlpatterns = [
    path('', views.view_all_sessions, name='view_all_sessions'),
    path('view/<int:session_id>', views.view_session, name='view_session'),
    path('log-session/', views.log_session, name='log_session'),
    path('update-session/<int:session_id>', views.update_session, name='update_session'),
    path('add-exercise/<int:session_id>', views.add_exercise, name='add_exercise'),
    path('add-sets/<int:exercise_id>', views.add_sets, name='add_sets'),
    path('delete-exercise/<int:exercise_id>', views.exercise_del, name='exercise_del'),
    path('delete-session/<int:session_id>', views.session_del, name='session_del'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
