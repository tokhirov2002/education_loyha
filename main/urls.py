from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('teachers/', views.teachers, name='teachers'),
    path('teacher/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('branches/', views.branches, name='branches'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    
    # Foydalanuvchi paneli
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autentifikatsiya
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
