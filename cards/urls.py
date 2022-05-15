from django.urls import path
from .views import cards_view, add_card_view, delete_card, edit_card

urlpatterns = [
    path("", cards_view, name="cards"),
    path("add/", add_card_view, name="add"),
    path("delete/<int:pk>", delete_card, name="delete"),
    path("edit/<int:pk>", edit_card, name="edit"),
]
