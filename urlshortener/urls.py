from django.contrib import admin
from django.urls import path
from Account.views import *
from URL.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('generate/', generate, name='generate'),
    path('dashboard/',dashboard, name='dashboard'),
    path('dash/<str:query>/',go, name='go'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('signup', signup, name='signup'),
    path('token', token, name='token'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error/',error, name='error'),
    path('forget/',forget, name='forget'),   
    path('change_password/<auth_token>', change_password, name='change_password'),
    path('dash/',dash, name='dash'),   
]   


