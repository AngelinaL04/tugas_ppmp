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

    @transaction.atomic
    def perform_update(self, serializer):
        # Ambil reservasi sebelum diupdate
        reservation = self.get_object()
        old_room = reservation.room

        # Ambil data kamar baru dari request
        new_room_id = serializer.validated_data['room'].id
        new_room = Room.objects.get(id=new_room_id)

        # Jika kamar lama berbeda dengan kamar baru
        if old_room.id != new_room.id:
            # Ubah kamar lama menjadi available
            old_room.status = 'available'
            old_room.save()

        # Ubah kamar baru menjadi unavailable jika masih available
        if new_room.status == 'available':
            new_room.status = 'unavailable'
            new_room.save()
        else:
            raise ValueError("The new room is already unavailable.")

        # Simpan perubahan reservasi
        serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            # Lanjutkan untuk memproses request update
            return super().update(request, *args, **kwargs)
        except ValueError as e:
            # Jika terjadi error (misal room baru sudah tidak tersedia), kembalikan error
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

