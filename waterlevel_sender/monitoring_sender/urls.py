from django.urls import path
from .views import send_data
from . import views

urlpatterns = [
    path("", views.control_page, name="control_page"),
    path('send/', send_data, name='send_data'),
    path("control/<str:action>/", views.control_script, name="control_script"),
]
