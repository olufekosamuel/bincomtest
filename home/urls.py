from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from .views import *

app_name = "home"

urlpatterns = [
    path('',index,name="index"),
    path('poll/',polling,name="poll"),
    path('lga/',lgalist,name="lga"),
    path('result/<int:id>',result,name="result"),
    path('storeresult/',storeresult,name="sresult"),
    path('lgaresult/<int:id>/<str:party>',lgaresult,name="presult"),
]