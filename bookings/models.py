from django.db import models
from django.contrib.auth.models import User

RESOURCE_TYPE = [
    ("room", "Room"),
    ("equipment", "Equipment"),
    ("sport", "Sport"),
]

STATUS_TYPE = [
    ("waiting", "Waiting"),
    ("notified", "Notified"),
]

BOOKING_STATUS = [
    ('active', 'Active'),
    ('queued', 'Queued'),
    ('completed', 'Completed')
]


class Resource(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    max_slots = models.IntegerField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)


class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_TYPE)
    position = models.IntegerField()
    notified_at = models.DateTimeField(null=True, blank=True)
    expiry_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS)

    class Meta:
        indexes = [
            models.Index(fields=['resource', 'start_time', 'end_time']),
        ]
