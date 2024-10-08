from django.urls import path, include
from . import views

app_name = "yadisk_interaction"

urlpatterns = [
    path("", views.yandex_disk_view, name="main"),
    path("/download.html", views.download_files, name="download"),
]
