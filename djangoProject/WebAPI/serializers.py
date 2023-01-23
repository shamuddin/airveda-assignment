from rest_framework import serializers
from WebAPI.models import Device, TemperatureReading, HumidityReading


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'uid', 'name')


class TemperatureReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = ('id', 'device', 'temperature', 'timestamp')


class HumidityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityReading
        fields = ('id', 'device', 'humidity', 'timestamp')
