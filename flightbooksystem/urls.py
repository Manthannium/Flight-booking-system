from django.contrib import admin
from django.urls import path

from flightbooksystem.views import home
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('signin',views.signin,name="signin"),
    path('signup-new',views.signup,name="signup-new"),
    path('signout-new',views.signout,name="signout"),
    path('roomallo',views.seat_data,name="seat_data"),
    path('invoice',views.invoice,name="invoice"),
]