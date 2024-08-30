from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Property, Tenant, Rental
from .serializers import PropertySerializer, TenantSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PropertyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['address', 'property_type', 'rental_cost']
    ordering_fields = ['rental_cost']

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

class PaymentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rental.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_reminder_view(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    tenant.send_payment_reminder()
    return JsonResponse({"message": f"Payment reminder sent to {tenant.name}"})

