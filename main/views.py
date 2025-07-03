from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Teacher, Branch, News, Enrollment, Contact
from .forms import ContactForm, EnrollmentForm


def home(request):
    popular_courses = Course.objects.filter(is_popular=True)[:6]
    featured_teachers = Teacher.objects.all()[:4]
    latest_news = News.objects.filter(is_featured=True)[:3]
    branches = Branch.objects.all()[:3]
    
    context = {
        'popular_courses': popular_courses,
        'featured_teachers': featured_teachers,
        'latest_news': latest_news,
        'branches': branches,
    }
    return render(request, 'main/home.html', context)


def courses(request):
    course_list = Course.objects.all()
    search_query = request.GET.get('search')
    level_filter = request.GET.get('level')
    
    if search_query:
        course_list = course_list.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if level_filter:
        course_list = course_list.filter(level=level_filter)
    
    paginator = Paginator(course_list, 9)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'level_filter': level_filter,
    }
    return render(request, 'main/courses.html', context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user, 
            course=course
        ).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if not is_enrolled:
            Enrollment.objects.create(
                user=request.user,
                course=course
            )
            messages.success(request, "Siz kursga muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('course_detail', pk=pk)
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'main/course_detail.html', context)


def teachers(request):
    teacher_list = Teacher.objects.all()
    search_query = request.GET.get('search')
    
    if search_query:
        teacher_list = teacher_list.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    paginator = Paginator(teacher_list, 8)
    page_number = request.GET.get('page')
    teachers = paginator.get_page(page_number)
    
    context = {
        'teachers': teachers,
        'search_query': search_query,
    }
    return render(request, 'main/teachers.html', context)


def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher_courses = Course.objects.filter(teacher=teacher)
    
    context = {
        'teacher': teacher,
        'teacher_courses': teacher_courses,
    }
    return render(request, 'main/teacher_detail.html', context)


def branches(request):
    branch_list = Branch.objects.all()
    context = {
        'branches': branch_list,
    }
    return render(request, 'main/branches.html', context)


def news(request):
    news_list = News.objects.all()
    search_query = request.GET.get('search')
    
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    context = {
        'news': news,
        'search_query': search_query,
    }
    return render(request, 'main/news.html', context)


def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    latest_news = News.objects.exclude(pk=pk)[:5]
    
    context = {
        'news_item': news_item,
        'latest_news': latest_news,
    }
    return render(request, 'main/news_detail.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    branches = Branch.objects.all()
    context = {
        'form': form,
        'branches': branches,
    }
    return render(request, 'main/contact.html', context)


@login_required
def dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user)
    
    context = {
        'user_enrollments': user_enrollments,
    }
    return render(request, 'main/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)
