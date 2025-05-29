from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("landing/", views.landing, name="landing"),
    path("drop/", views.drop, name='drop'),
    path("skydive_path/", views.skydive_path, name='skydive_path'),
    path("reset_path/", views.reset_path, name='reset_path'),
]