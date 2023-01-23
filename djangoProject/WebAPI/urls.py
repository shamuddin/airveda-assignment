from django.urls import path
from WebAPI.views import list_devices, retrieve_device, device_readings, create_device, delete_device, device_graph

urlpatterns = [
   path('devices-create/', create_device, name='create-device'),
   path('devices-delete/<str:uid>/', delete_device, name='delete-device'),
   path('devices-retrive/<str:uid>/', retrieve_device, name='retrieve-device'),
   path('devices-list/', list_devices, name='list-devices'),
   path('devices-details/<str:device_uid>/readings/<str:parameter>/', device_readings, name='device-readings'),
   path('devices-graph/', device_graph, name='device-graph'),
]
