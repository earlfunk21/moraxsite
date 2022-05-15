from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Cards
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def cards_view(request):
    context = {}
    context["cards"] = enumerate(Cards.objects.all().order_by("-created"), 1)
    context["title"] = "Cards Page"
    if not request.user.is_authenticated:
        messages.error(request, "Please logged in")
    return render(request, "cards/cards.html", context)


@login_required(redirect_field_name="login")
def add_card_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        user = request.user
        Cards(user=user, title=title, body=body).save()
        messages.success(request, "Successfully added")
        return redirect("cards")
    return render(request, "cards/add_card.html")


def check_pk(pk):
    try:
        Cards.objects.get(pk=pk)
        return True
    except ObjectDoesNotExist:
        return False


@login_required(redirect_field_name="login")
def delete_card(request, pk):
    if not check_pk(pk):
        messages.error(request, f"Invalid ID {pk}")
    else:
        Cards.objects.get(pk=pk).delete()
        messages.success(request, "Successfully Deleted")
    return redirect("cards")


@login_required(redirect_field_name="login")
def edit_card(request, pk):
    context = {}
    if request.method == "POST" and check_pk(pk):
        card = Cards.objects.get(pk=pk)
        card.title = request.POST.get("title")
        card.body = request.POST.get("body")
        card.save()
        messages.success(request, "Successfully Updated")
        return redirect("cards")
    if not check_pk(pk):
        messages.error(request, f"Invalid ID {pk}")
        return redirect("cards")
    else:
        context["card"] = Cards.objects.get(pk=pk)
    return render(request, "cards/edit_card.html", context)
