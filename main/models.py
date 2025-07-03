from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Branch(models.Model):
    name = models.CharField(max_length=200, verbose_name="Filial nomi")
    address = models.TextField(verbose_name="Manzil")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.CharField(max_length=100, verbose_name="Ish vaqti")
    latitude = models.FloatField(verbose_name="Kenglik", null=True, blank=True)
    longitude = models.FloatField(verbose_name="Uzunlik", null=True, blank=True)
    image = models.ImageField(upload_to='branches/', verbose_name="Rasm", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Biografiya")
    experience = models.PositiveIntegerField(verbose_name="Tajriba (yil)")
    subject = models.CharField(max_length=200, verbose_name="Fan")
    image = models.ImageField(upload_to='teachers/', verbose_name="Rasm")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
    ]

    name = models.CharField(max_length=200, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")
    duration = models.PositiveIntegerField(verbose_name="Davomiyligi (oy)")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Daraja")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Filial")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    image = models.ImageField(upload_to='courses/', verbose_name="Rasm")
    is_popular = models.BooleanField(default=False, verbose_name="Mashhur kurs")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
        ('completed', 'Yakunlangan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatga olingan vaqt")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Yakunlangan vaqt")

    class Meta:
        verbose_name = "Ro'yxatga olish"
        verbose_name_plural = "Ro'yxatga olishlar"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    image = models.ImageField(upload_to='news/', verbose_name="Rasm")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy yangilik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")

    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
