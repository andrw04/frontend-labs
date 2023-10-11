from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about),
    path("contacts/", views.ContactListView.as_view()),
    path("faq/", views.QuestionListView.as_view()),
    path("privacy-policy/", views.privacy_policy),
    path("promo/", views.promo),
    path("vacancy/", views.VacancyListView.as_view()),

    path("news/", views.NewsListView.as_view()),
    path("news/<int:pk>/",views.NewsDetailView.as_view()),

    path("review/", views.ReviewListView.as_view(), name='reviews'),
    path("review/create/", views.create_review),


    path('category/', views.CategoryListView.as_view(), name='category'),
    path("service/<int:pk>/", views.ServiceListView.as_view()),
    path("service/create/", views.ServiceCreateView.as_view(), name='add-service'),
    path("service/update/<int:pk>/",views.ServiceUpdateView.as_view(), name='update-service'),
    path("service/delete/<int:pk>/", views.ServiceDeleteView.as_view(), name='delete-service'),

    # login registration
    path("register/", views.SignUpView.as_view()),
    path("login/", views.SignInView.as_view(), name='login'),
    path("logout/", views.logout_user, name='logout'),

    # orders
    path("order/", views.view_order, name='order'),
    path("order/add/<int:pk>", views.add_to_order, name='add-to-order'),
    path("order/delete/<int:pk>", views.delete_from_order, name='delete-from-order'),
    path("order/create/", views.create_order, name='create-order'),

    path("order-list/", views.OrderListView.as_view(), name='order-list'),
    path("order/details/<int:pk>", views.OrderDetailView.as_view(), name='order-detail'),
    path("order/details/delete/<int:pk>", views.DeleteOrderView.as_view(), name='delete-order'),

    path("schedule/", views.ScheduleListView.as_view(), name='schedule'),
    path("schedule/create/", views.ScheduleCreateView.as_view(), name='create-schedule'),

    path("appointment/create/<int:order_id>", views.create_appointment, name='create-appointment'),
    path("appointment/details/<int:schedule_id>", views.appointment_detail, name='appointment-detail'),
]
