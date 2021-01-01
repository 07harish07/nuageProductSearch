from django.urls import path
from searchApp import views

appname = 'search'
urlpatterns = [
    path('', views.product_list, name='product'),
]