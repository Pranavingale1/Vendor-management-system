from rest_framework import generics, permissions,status
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, AcknowledgePurchaseOrderSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class HistoricalPerformanceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

        # Calculate acknowledgment date
        acknowledgment_date = purchase_order.vendor.calculate_acknowledgment_date()

        # Update acknowledgment date
        purchase_order.acknowledgment_date = acknowledgment_date
        purchase_order.save()

        # Trigger recalculation of average_response_time
        purchase_order.vendor.update_avg_response_time()

        return Response({'success': 'Acknowledgment date updated successfully'}, status=status.HTTP_200_OK)