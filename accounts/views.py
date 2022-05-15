from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


class RegisterView(View):
    title = "Register Page"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.success(request, "You are already logged in")
            return redirect(reverse_lazy("cards"))
        return super().dispatch(request, *args, **kwargs)

    @property
    def get_context_data(self) -> dict:
        context = {}
        context["title"] = self.title
        return context

    def get(self, request):
        return render(request, "accounts/register.html", self.get_context_data)

    def post(self, request):
        username = self.request.POST.get("username")
        password1 = self.request.POST.get("password1")
        password2 = self.request.POST.get("password2")
        if User.objects.filter(username=username).first():
            messages.error(request, "Username already in use")
            return redirect(reverse_lazy("register"))
        elif password1 != password2:
            messages.error(request, "Password mismatch")
            return redirect(reverse_lazy("register"))
        else:
            user = User.objects.create(username=username)
            user.set_password(password1)
            user.save()
            return redirect(reverse_lazy("login"))


class LoginView(View):
    title = "Login Page"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.success(request, "You are already logged in")
            return redirect(reverse_lazy("cards"))
        return super().dispatch(request, *args, **kwargs)

    @property
    def get_context_data(self) -> dict:
        context = {}
        context["title"] = self.title
        return context

    def get(self, request):
        return render(request, "accounts/login.html", self.get_context_data)

    def post(self, request):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect(reverse_lazy("cards"))
        else:
            messages.error(request, "Invalid username or password")
            return redirect(reverse_lazy("login"))


@login_required(redirect_field_name="login")
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect(reverse_lazy("login"))
