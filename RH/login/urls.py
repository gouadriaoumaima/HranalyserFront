
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('register/', views.Register, name='Register'),
    

]