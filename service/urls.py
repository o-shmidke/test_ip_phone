from django.urls import path

from service.views import get_data, control_service, save_permission

urlpatterns = [
    path('', get_data, name='get_data'),
    path('control_service/', control_service, name='control_service'),
    path('save_permission', save_permission, name='save_permission'),
]
