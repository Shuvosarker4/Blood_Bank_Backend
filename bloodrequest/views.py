from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import BloodRequest, DonationAcceptance
from .serializers import BloodRequestSerializer, DonationAcceptanceSerializer

class BloodRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BloodRequest.objects.all()
        return BloodRequest.objects.filter(status='open')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DonationAcceptanceViewSet(viewsets.ModelViewSet):
    serializer_class = DonationAcceptanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DonationAcceptance.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        request_obj = serializer.validated_data['request']
        if request_obj.status != 'open':
            raise ValidationError("This request is not open.")
        serializer.save(donor=self.request.user)
