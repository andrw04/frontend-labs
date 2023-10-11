from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .managers import CustomUserManager
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=80)
    image = models.ImageField(upload_to=r'users/%Y/%m/%d', null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.name + " - " + str(self.price) + "$"



class Doctor(AbstractUser):
    username = models.CharField(blank=True, unique=False, max_length=255)

    first_name = models.CharField("Имя",max_length=20, null=True)
    last_name = models.CharField("Фамилия",max_length=20, null=True)
    father_name = models.CharField("Отчество",max_length=20, null=True)

    email = models.CharField("Почта", max_length=150, null=True, unique=True)
    phone = models.CharField("Номер телефона", max_length=15, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", null=True)

    job_title = models.CharField("Должность", max_length=80, null=True)

    birth_date = models.DateField("Дата рождения", null=True)
    photo = models.ImageField("Фото", upload_to=r'users/%Y/%m/%d', null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"Доктор {self.first_name} {self.last_name}"


class Room(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return 'Номер кабинета: ' + str(self.number)

class Client(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    father_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.date_and_time}"
    

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField(default=10)
    scheduled_slot = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Посещение для {self.order.client} с {self.doctor} в {self.scheduled_slot.date_and_time}"
    

RATE_CHOICES = (
    (1, "Очень плохо"),
    (2, "Плохо"),
    (3, "Нормально"),
    (4, "Хорошо"),
    (5, "Очень хорошо"),
)

class Review(models.Model):
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATE_CHOICES)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.rate}"


class Question(models.Model):
    question = models.CharField(max_length=150)
    answer = models.TextField()
    date = models.DateField(auto_now_add=True)


class News(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    summary = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(upload_to=r'users/%Y/%m/%d')


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата')
    location = models.CharField(max_length=50, verbose_name='Местоположение')
    published_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

