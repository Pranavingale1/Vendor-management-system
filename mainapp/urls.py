# urls.py
from django.urls import path
from .views import (VendorListCreateView,
                    VendorRetrieveUpdateDeleteView,
                    PurchaseOrderListCreateView,
                    PurchaseOrderRetrieveUpdateDeleteView,
                    HistoricalPerformanceListCreateView,
                    HistoricalPerformanceRetrieveUpdateDeleteView,
                    AcknowledgePurchaseOrder)

urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    
    path('api/historical_performances/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
    path('api/historical_performances/<int:pk>/', HistoricalPerformanceRetrieveUpdateDeleteView.as_view(), name='historical-performance-retrieve-update-delete'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge_purchase_order'),
]


