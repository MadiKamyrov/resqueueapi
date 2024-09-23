from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Resource, Booking, Queue

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'max_slots', 'resource_type']

class BookingSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'resource', 'user', 'start_time', 'end_time', 'status']


class QueueSerializer(serializers.ModelSerializer):
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Queue
        fields = ['id', 'resource', 'user', 'created_at', 'position', 'status', 'notified_at', 'expiry_time']