from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ResourceViewSet, BookingViewSet, QueueViewSet

router = DefaultRouter()
router.register(r'resources', ResourceViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'queues', QueueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
