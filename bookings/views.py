from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Resource, Booking, Queue
from .serializers import ResourceSerializer, BookingSerializer, QueueSerializer
from .services import check_availability, add_to_queue
from django.utils.decorators import method_decorator


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('user', 'resource')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, pk=request.data['resource'])
        start_time = request.data['start_time']
        end_time = request.data['end_time']

        if check_availability(resource, start_time, end_time):
            return super().create(request, *args, **kwargs)
        else:
            add_to_queue(request.user, resource, start_time, end_time)
            return Response({"detail": "Resource is fully booked. You have been added to the queue."},
                            status=status.HTTP_202_ACCEPTED)


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all().select_related('user', 'resource')
    serializer_class = QueueSerializer
