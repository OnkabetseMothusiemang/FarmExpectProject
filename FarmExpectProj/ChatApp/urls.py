
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),  # Render the main page with chatbox
    path('chatBot/', views.chatBot, name='chatBot'),
    path('generate_image/',views.generate_image,name="generate_image"),
]

