from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserDetailsView

app_name = 'users'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/user-details/', UserDetailsView.as_view()),
]