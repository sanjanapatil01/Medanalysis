
from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('', views.index,name='index'),
    path('register/',views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('prediction/',views.prediction,name='prediction'),
    path('cvdform/',views.cvdform,name='cvdform'),
    path('diabaticform/',views.diabaticform,name='diabaticform'),
    path('cvd/',views.cvd,name='cvd'),
    path('diabatic/',views.diabatic,name='diabatic'),

]

