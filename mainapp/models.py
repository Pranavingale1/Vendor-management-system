from django.db import models
from datetime import datetime
from django.db.models import ExpressionWrapper, F, fields, Avg

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    avg_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def update_avg_response_time(self):
        completed_orders = self.purchaseorder_set.filter(issue_date__isnull=False)

        avg_response_time_seconds = completed_orders.aggregate(
            AvgDuration=ExpressionWrapper(
                Avg(F('acknowledgment_date') - F('issue_date')),
                output_field=fields.DurationField()
            )
        )['AvgDuration']

        if avg_response_time_seconds is not None:
            avg_response_time_hours = avg_response_time_seconds.total_seconds() // 3600
            self.avg_response_time = avg_response_time_hours if avg_response_time_hours else 0.0
        else:
            self.avg_response_time = 0.0

        self.save()

    def calculate_acknowledgment_date(self):
        # Calculate acknowledgment_date based on your logic
        # For example, you can set it to the current date and time
        from django.utils import timezone
        acknowledgment_date = timezone.now()
        return acknowledgment_date

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    issue_date = models.DateTimeField(null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.vendor.name +" "+ self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    avg_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor.name
    



