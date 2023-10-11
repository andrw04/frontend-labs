from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Doctor, Category, Service, Review, Question, News, Order, Client, Schedule, Appointment, Vacancy
from django.views import View
from django.urls import reverse_lazy
from .forms import ReviewCreateForm, CustomUserCreationForm, CustomLoginForm, CustomServiceUpdateForm, ClientInfoForm, ServiceCreateForm, ScheduleCreateForm, AppoinmentCreateForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from requests import get
import json
from django.db.models import Count

def index(request):
    # statistics
    slabels = []
    sdata = []
    services_with_order_count = Service.objects.annotate(order_count=Count('order'))
    for service in services_with_order_count:
        slabels.append(service.name)
        sdata.append(service.order_count)

    # first api
    key = '2862bdc96c3f4b79a0bbf519bcb8f1df'
    data = json.loads(get(f'https://api.ipgeolocation.io/ipgeo?apiKey={key}').text)['time_zone']
    result = json.loads(get('https://favqs.com/api/qotd').text)
    context = {
        'author': result.get('quote').get('author'),
        'quote': result.get('quote').get('body'),
        'name': data.get('name'),
        'current_time': data.get('current_time'),
        'labels': slabels,
        'data': sdata,
        'news': News.objects.order_by('-date')[0]
    }

    return render(request, "app/index.html", context)

def about(request):
    return render(request, "app/about.html")

def dictionary(request):
    return render(request, "app/dictionary.html")

def contacts(request):
    return render(request, "app/contacts.html")

def privacy_policy(request):
    return render(request, "app/privacy-policy.html")

def reviews(request):
    return render(request, "app/reviews.html")

def promo(request):
    return render(request, "app/promo.html")


class CategoryBaseView(View):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('categories:all')


class CategoryListView(ListView):
    model = Category


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(is_completed=False)
    

class OrderDetailView(DetailView):
    model = Order


class DeleteOrderView(DeleteView):
    model = Order


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleCreateForm
    success_url = reverse_lazy('schedule')

class ScheduleListView(ListView):
    model = Schedule

    def get_queryset(self):
        user = self.request.user
        current_datetime = timezone.now()
        queryset = super().get_queryset().filter(date_and_time__gt=current_datetime).order_by('date_and_time')
        if user.is_superuser:
            return queryset
        return queryset.filter(doctor_id=user.id)
    


def create_appointment(request, order_id):
    if request.method == "POST":
        form = AppoinmentCreateForm(request.POST)
        if form.is_valid():
            appoinment = form.save(commit=False)
            schedule = appoinment.scheduled_slot
            schedule.is_available = False
            schedule.save()
            order = Order.objects.get(id=order_id)
            order.is_completed = True
            order.save()
            appoinment.order = order
            appoinment.save()
            return redirect('schedule')
    else:
        form = AppoinmentCreateForm()

    return render(request, 'app/appointment_form.html', {'form': form })


def appointment_detail(request, schedule_id):
    obj = Appointment.objects.get(scheduled_slot=schedule_id)
    obj.order.total_price
    return render(request, 'app/appointment_detail.html', {'object': obj, 'total_price': obj.order.total_price})

class AppointmentDetailView(DetailView):
    model = Appointment

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        return super().get(request, *args, **kwargs)


class ServiceListView(ListView):
    model = Service

    def get_queryset(self):
        queryset = super().get_queryset()

        if (self.kwargs.get('pk')):
            category = Category.objects.get(id=self.kwargs.get('pk'))
            queryset = queryset.filter(category=category)
        
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sorting')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

        if sort == 'asc':
                queryset = queryset.order_by('price')

        if sort == 'desc':
                queryset = queryset.order_by('-price')
                
        if sort == 'name':
                queryset = queryset.order_by('name')

        return queryset
    

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceCreateForm
    success_url = reverse_lazy('category')


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = CustomServiceUpdateForm
    success_url = reverse_lazy('category')


class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('category')


class ContactListView(ListView):
    model = Doctor
    template_name = 'app/contact_list.html'

    def get_queryset(self):
        contacts = Doctor.objects.all().filter(is_superuser=0)
        return contacts
        

class ReviewListView(ListView):
    model = Review

    ordering = ['-date']


class QuestionListView(ListView):
    model = Question

@login_required
def create_review(request):
    if request.method == "POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewCreateForm()

    return render(request, 'app/review_form.html', {'form': form })


class NewsListView(ListView):
    model = News


class NewsDetailView(DetailView):
    model = News


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = "/"
    template_name = "app/signup.html"

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('/')
        else:
            return render(request, self.template_name, { 'form': form })
        

class SignInView(LoginView):
    form_class = CustomLoginForm
    template_name = 'app/signin.html'

    def get_success_url(self):
        return reverse_lazy('home') 
    

def logout_user(request):
    logout(request)
    return redirect('login')


def add_to_order(request, pk):
    service = Service.objects.get(id=pk)
    order = request.session.get('order', [])
    order.append(pk)
    request.session['order'] = order

    return redirect('order')


def delete_from_order(request, pk):
    order = request.session.get('order', [])
    order.remove(pk)
    request.session['order'] = order
    request.session.modified = True

    return redirect('order')


def view_order(request):
    order = request.session.get('order', [])
    service_ids = order
    services = Service.objects.filter(id__in=service_ids)

    total_price = sum(service.price for service in services)

    return render(request, 'app/order.html', {'services': services, 'order': order, 'total_price': total_price })


def create_order(request):
    if request.method == "POST":
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            # Создание заказа
            service_ids = request.session.get('order', [])
            services = Service.objects.filter(id__in=service_ids)
            try:
                client = Client.objects.get(**form.cleaned_data)
            except Client.DoesNotExist:
                client = form.save()

            total_price = sum(service.price for service in services)
            order = Order.objects.create(total_price=total_price, client=client)

            order.services.set([service for service in services])

            service_ids.clear()
            request.session['order'] = service_ids

            return redirect('order')
    else:
        form = ClientInfoForm()

    return render(request, 'app/order_form.html', {'form': form })


class VacancyListView(ListView):
    model = Vacancy