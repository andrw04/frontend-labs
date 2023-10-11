import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Review, Category, Doctor, Service, Client, Schedule, Appointment
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate', 'text')
        widgets = {
            'rate': forms.Select(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }


class ScheduleCreateForm(forms.ModelForm):
    date_and_time = forms.DateTimeField(label="Дата и время",
                                         widget=forms.DateTimeInput(attrs={'class':'form-control',
                                                                           'type':'datetime-local'}))
    class Meta:
        model = Schedule
        fields = ('doctor', 'date_and_time')
        widgets = {
            'doctor': forms.Select(attrs={'class':'form-control'}),
            #'date_and_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class ServiceCreateForm(forms.ModelForm):
    name = forms.CharField(label="Название услуги", widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label="Категория услуг", widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label="Цена", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ('name', 'description', 'category', 'price')


class AppoinmentCreateForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),
                                     widget=forms.Select(attrs={'class':'form-control'}),
                                     label="Врач")
    scheduled_slot = forms.ModelChoiceField(queryset=Schedule.objects.all().filter(is_available=True, date_and_time__gt=timezone.now()),
                                             widget=forms.Select(attrs={'class':'form-control'}),
                                             label="Выбрать время")
    class Meta:
        model = Appointment
        fields = ('doctor', 'scheduled_slot')
        widgets = {
            'doctor': forms.Select(attrs={'class':'form-control'}),
        }


phone_regex = RegexValidator(
    regex=r'\+375\d{9}$',
    message="Номер телефона должен быть в формате +375XXXXXXX"
)

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError(_("Вы должны быть старше 18 лет."), code='invalid_age')


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    birth_date = forms.DateField(label="Дата рождения",
                                 validators=[validate_age],
                                 widget=forms.DateInput(attrs={'class':'form-control',
                                                               'placeholder':'YYYY-MM-DD'}))
    
    phone = forms.CharField(label="Номер телефона",
                            validators=[phone_regex],
                            max_length=13,
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder':'+37529XXXXXXX'}))

    class Meta(UserCreationForm):
        model = Doctor
        fields = (
            'last_name',
            'first_name',
            'father_name',
            'email',
            'phone',
            'category',
            'job_title',
            'birth_date',
            'photo')
        
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = Doctor
        fields = (
            'last_name',
            'first_name',
            'father_name',
            'email',
            'category',
            'job_title',
            'birth_date',
            'photo',
            )
        
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Почта',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = Doctor
        fields = ('username','password')


class CustomServiceUpdateForm(forms.ModelForm):
    name = forms.CharField(label="Название", widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория",
                                      widget=forms.Select(attrs={'class':'form-control'}))
    #category = forms.ChoiceField(label="Категория услуг", widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.FloatField(label="Цена", widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Service
        fields = ['name','description', 'category', 'price']

        # widgets = {
        #     'category': forms.Select(attrs={'class':'form-control'}),
        # }


class ClientInfoForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя",
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Фамилия",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    father_name = forms.CharField(label="Отчество",
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label="Дата рождения",
                                 validators=[validate_age],
                                 widget=forms.DateInput(attrs={'class':'form-control',
                                                               'placeholder':'YYYY-MM-DD'}))
    phone = forms.CharField(label="Номер телефона",
                            validators=[phone_regex],
                            max_length=13,
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder': '+375XXXXXXX'}))

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'father_name', 'birth_date', 'phone')

