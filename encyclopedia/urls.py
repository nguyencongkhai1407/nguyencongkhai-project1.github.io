from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.getTitle, name ="content"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("wiki/new", views.new, name="new"),
    path("wiki/random", views.random, name="random")
    
]
