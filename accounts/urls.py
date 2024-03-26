from django.contrib import admin
from django.urls import path
from . import views

  
urlpatterns = [
     path("",views.home, name="home"),
     path("product/",views.products,name="product"),
     path("customer/<str:pk>/",views.customers, name="customer" ),
     path("orderform/",views.createorder,name="xyz"), 
     path("updateform/<str:pk>",views.updateorder,name="pqr"),
     path("delete/<str:pk>",views.deleteorder,name="abc"),
     path("register/",views.register,name="r"),
     path("register/<int:flag>",views.register,name="r"),
     path("login/",views.logins,name="l"),
     path("logout/",views.logoutuser,name="o"),
     path("user/",views.users, name="userz" ),
]  