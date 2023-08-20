from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.detail, name="detail"),
    path("add", views.add, name="add"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
]
