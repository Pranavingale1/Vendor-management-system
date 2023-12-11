# your_app/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Vendor
from datetime import datetime, timedelta

class VendorManagementSystemTestCase(TestCase):
    def setUp(self):
        # Create a sample vendor for testing
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test_vendor@example.com',
            'address': '123 Test Street',
            'vendor_code': 'V001',
            'on_time_delivery_rate': 90.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 2.5,
            'fulfillment_rate': 95.0,
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_vendor_crud_operations(self):
        # Test creating a new vendor
        new_vendor_data = {
            'name': 'New Vendor',
            'contact_details': 'new_vendor@example.com',
            'address': '456 New Street',
            'vendor_code': 'V002',
            'on_time_delivery_rate': 85.0,
            'quality_rating_avg': 4.0,
            'average_response_time': 3.0,
            'fulfillment_rate': 92.0,
        }
        response = self.client.post(reverse('vendor-list-create'), new_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving the new vendor
        new_vendor_id = response.data['id']
        response = self.client.get(reverse('vendor-retrieve-update-delete', args=[new_vendor_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test updating the new vendor
        updated_vendor_data = {
            'name': 'Updated Vendor',
            'contact_details': 'updated_vendor@example.com',
            'address': '789 Updated Street',
        }
        response = self.client.put(reverse('vendor-retrieve-update-delete', args=[new_vendor_id]), updated_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_vendor_data['name'])

        # Test deleting the new vendor
        response = self.client.delete(reverse('vendor-retrieve-update-delete', args=[new_vendor_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_purchase_order_crud_operations(self):
        # Test creating a new purchase order
        po_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': datetime.now().isoformat(),
            'delivery_date': (datetime.now() + timedelta(days=10)).isoformat(),
            'items': [{'item_name': 'Item1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending',
            'quality_rating': 4.0,
            'issue_date': datetime.now().isoformat(),
            'acknowledgment_date': (datetime.now() + timedelta(hours=2)).isoformat(),
        }
        response = self.client.post(reverse('purchase-order-list-create'), po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving the new purchase order
        new_po_id = response.data['id']
        response = self.client.get(reverse('purchase-order-retrieve-update-delete', args=[new_po_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test updating the new purchase order
        updated_po_data = {
            'status': 'completed',
            'quality_rating': 4.5,
        }
        response = self.client.put(reverse('purchase-order-retrieve-update-delete', args=[new_po_id]), updated_po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], updated_po_data['status'])

        # Test deleting the new purchase order
        response = self.client.delete(reverse('purchase-order-retrieve-update-delete', args=[new_po_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_historical_performance_crud_operations(self):
        # Test creating a new historical performance record
        historical_performance_data = {
            'vendor': self.vendor.id,
            'date': datetime.now().isoformat(),
            'on_time_delivery_rate': 90.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 2.5,
            'fulfillment_rate': 95.0,
        }
        response = self.client.post(reverse('historical-performance-list-create'), historical_performance_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieving the new historical performance record
        new_historical_performance_id = response.data['id']
        response = self.client.get(reverse('historical-performance-retrieve-update-delete', args=[new_historical_performance_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test updating the new historical performance record
        updated_historical_performance_data = {
            'on_time_delivery_rate': 92.0,
            'quality_rating_avg': 4.8,
            'average_response_time': 2.2,
            'fulfillment_rate': 96.0,
        }
        response = self.client.put(reverse('historical-performance-retrieve-update-delete', args=[new_historical_performance_id]), updated_historical_performance_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], updated_historical_performance_data['on_time_delivery_rate'])

        # Test deleting the new historical performance record
        response = self.client.delete(reverse('historical-performance-retrieve-update-delete', args=[new_historical_performance_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
