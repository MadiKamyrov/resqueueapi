from datetime import timedelta
from django.core.cache import cache

from .models import Booking, Queue


def check_availability(resource, start_time, end_time):
    cache_key = f"availability_{resource.id}_{start_time}_{end_time}"
    availability = cache.get(cache_key)

    if availability is None:
        bookings_exist = Booking.objects.filter(
            resource=resource,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exists()

        availability = not bookings_exist or Booking.objects.filter(
            resource=resource,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).count() < resource.max_slots

        cache.set(cache_key, availability, timeout=300)

    return availability


def add_to_queue(user, resource, start_time, end_time):
    last_position = Queue.objects.filter(resource=resource).count() + 1
    queue = Queue.objects.create(
        user=user,
        resource=resource,
        created_at=start_time,
        position=last_position,
        status="waiting",
    )
    return queue


def process_queue(resource):
    next_in_queue = Queue.objects.filter(resource=resource, status="waiting").order_by('position').first()

    if next_in_queue:
        next_in_queue.status = "notified"
        next_in_queue.save()

        Booking.objects.create(
            user=next_in_queue.user,
            resource=resource,
            start_time=next_in_queue.created_at,
            end_time=next_in_queue.created_at + timedelta(hours=1)
        )
