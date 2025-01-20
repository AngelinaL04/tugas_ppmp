from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = router.urls
