from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Device, TemperatureReading, HumidityReading
from .serializers import DeviceSerializer, TemperatureReadingSerializer, HumidityReadingSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def list_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_device(request, uid):
    try:
        device = Device.objects.get(uid=uid)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def retrieve_device(request, uid):
    try:
        device = Device.objects.get(uid=uid)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def device_readings(request, device_uid, parameter):
    start_on = request.query_params.get('start_on')
    end_on = request.query_params.get('end_on')

    if not all([start_on, end_on]):
        return Response({'error': 'start_on and end_on query parameters are required'},
                        status=status.HTTP_400_BAD_REQUEST)
    device = get_object_or_404(Device, uid=device_uid)

    if parameter == 'temperature':
        readings = TemperatureReading.objects.filter(device=device, timestamp__range=[start_on, end_on])
        serializer = TemperatureReadingSerializer(readings, many=True)
    elif parameter == 'humidity':
        readings = HumidityReading.objects.filter(device=device, timestamp__range=[start_on, end_on])
        serializer = HumidityReadingSerializer(readings, many=True)
    else:
        return Response({'error': 'Invalid parameter. Only temperature or humidity are allowed'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


@permission_classes([AllowAny])
def device_graph(request):
    device_uid = request.GET.get('device_uid')
    if not device_uid:
        return render(request, 'error.html', {'error': 'Device Uid is required'})

    device = get_object_or_404(Device, uid=device_uid)

    temperature_readings = TemperatureReading.objects.filter(device=device)
    humidity_readings = HumidityReading.objects.filter(device=device)

    device_data = {
        'labels': [reading.timestamp.strftime("%Y-%m-%d %H:%M") for reading in temperature_readings],
        'datasets': [
            {
                'label': 'Temperature',
                'data': [reading.temperature for reading in temperature_readings],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)'
            },
            {
                'label': 'Humidity',
                'data': [reading.humidity for reading in humidity_readings],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)'
            }
        ]
    }

    return render(request, 'device_graph.html', {'device_data': device_data, 'device_name': device.name})
