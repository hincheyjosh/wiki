from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/create", views.create, name="create"),
    path("wiki/randompage", views.randompage, name="randompage"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search")
]
