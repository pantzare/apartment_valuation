from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('', views.post_new, name='post_new'),
    path('valuation/', views.valuation, name='valuation')
]