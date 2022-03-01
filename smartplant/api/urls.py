from django.urls import path
from .views import Test, Devices, Minutes, Range, CreateDevice

urlpatterns = [
    path('test/', Test.as_view()),
    path('devices/all', Devices.as_view()),
    path('minutes/<int:minutes>/<str:dev_eui>', Minutes.as_view()),
    path('range/<int:start_timestamp>/<int:stop_timestamp>/<str:dev_eui>', Range.as_view()),
    path('create/device', CreateDevice.as_view())
]