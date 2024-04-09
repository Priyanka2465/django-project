"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('index/',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('changepass/',views.changepass,name='changepass'),
    path('profile/',views.profile,name='profile'),
    path('forgotpass/',views.forgotpass,name='forgotpass'),
    path('otp/',views.otp,name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('addevent/',views.addevent,name='addevent'),
    path('viewevent/',views.viewevent,name='viewevent'),
    path('editevent/<int:pk>',views.editevent,name='editevent'),
    path('deleteevent/<int:pk>',views.deleteevent,name='deleteevent'),
    path('shows-events/',views.shows_events,name='shows-events'),
    path('event-details/<int:pk>',views.event_details,name='event-details'),
    path('bookevent/<int:pk>',views.bookevent,name='bookevent'),
    path('myevent/',views.myevent,name='myevent'),
    path('checkout/<int:pk>',views.checkout,name='checkout'),
    path('create-checkout-session/',views.create_checkout_session,name='payment'),

]
