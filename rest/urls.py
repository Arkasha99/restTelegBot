from django.urls import path, include
from rest import views

urlpatterns = [
    path('telegram/', views.TelegramView.as_view()),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('create_token/', views.generate_token, name='generate_token'),
    path('send_message/', views.send_msg, name='send_msg'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('', views.index, name='index'),
]
