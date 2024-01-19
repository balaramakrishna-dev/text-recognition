from django.urls import path

from . import views

urlpatterns = [
    path("", views.pan_data_extraction, name="pan data extraction"),
    path("aadhar/", views.aadhar_data_extraction, name="aadhar data extraction")
]