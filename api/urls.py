from django.urls import path

from api import views


urlpatterns = [
    path('centers/', views.centers),
    path('ussd/', views.ussd),
    path('dropoff/', views.dropoff),
    path('users/', views.users),
    path('locations/', views.get_locations),
]
