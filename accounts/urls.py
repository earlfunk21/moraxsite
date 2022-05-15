from django.urls import path
from .views import LoginView, RegisterView, logout_view

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("", LoginView.as_view(), name="login")
]
