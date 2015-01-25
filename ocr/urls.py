from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt   

from ocr import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^convertImage/$', csrf_exempt(views.index), name='Ocr')
]
