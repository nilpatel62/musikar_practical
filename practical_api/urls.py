from django.conf.urls import url
from practical_api import views
from rest_framework import permissions

app_name = 'practical_api'


urlpatterns = [
    url(r'^python/csv/files$', views.ConvertCsvFiles.as_view(), name='ConvertCsvFiles')
]