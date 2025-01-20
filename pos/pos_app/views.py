from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import transaction  # Import transaksi
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @transaction.atomic  # Pastikan kedua proses ini berjalan dalam satu transaksi
    def perform_create(self, serializer):
        # Ambil objek room berdasarkan id yang diterima dalam request
        room = Room.objects.get(id=serializer.validated_data['room'].id)

        # Cek apakah status room 'available'
        if room.status == 'available':
            # Jika tersedia, update status room menjadi 'unavailable'
            room.status = 'unavailable'
            room.save()

            # Simpan objek Reservation
            serializer.save()
        else:
            # Jika room sudah tidak tersedia, beri error
            raise ValueError("Room is already unavailable")

    def create(self, request, *args, **kwargs):
        try:
            # Lanjutkan untuk memproses request create
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            # Jika terjadi error (misal room sudah tidak tersedia), kembalikan error
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
