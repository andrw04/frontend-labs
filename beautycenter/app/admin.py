from django.contrib import admin
from .models import Service, Category, Room, Schedule, Client, Question, News, Doctor, Appointment, Order, Review, Vacancy

# Register your models here.
@admin.register(Service)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price']


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']

@admin.register(News)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ['id','title']

@admin.register(Doctor)
class DoctorModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name']

admin.site.register(Room)
admin.site.register(Appointment)
admin.site.register(Schedule)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Vacancy)
