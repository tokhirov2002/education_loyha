from django.contrib import admin
from .models import Branch, Teacher, Course, Enrollment, News, Contact


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'address']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'experience', 'created_at']
    list_filter = ['subject', 'experience', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'subject']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'price', 'level', 'is_popular', 'start_date']
    list_filter = ['level', 'is_popular', 'branch', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_popular']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['user__username', 'course__name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_featured']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
