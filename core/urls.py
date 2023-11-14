from django.urls import path
from . import views
urlpatterns = [
    path('place', views.get_data),
    path('uploadcsv', views.FileUploadView.as_view())
]