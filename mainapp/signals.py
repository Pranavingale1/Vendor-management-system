from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import Avg, ExpressionWrapper, F, fields
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# To automatically create a token for when a user is created(only for users not vendors)
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Vendor)
def create_vendor_historical_performance(sender, instance, created, **kwargs):
    if created:
        HistoricalPerformance.objects.create(
            vendor=instance,
            date=timezone.now(),
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            avg_response_time=instance.avg_response_time,
            fulfillment_rate=instance.fulfillment_rate,
        )


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_and_historical_performance(sender, instance, **kwargs):
    vendor = instance.vendor

    # Update Vendor parameters
    completed_orders = vendor.purchaseorder_set.filter(status='completed')
    
    vendor.on_time_delivery_rate = completed_orders.count() / vendor.purchaseorder_set.count() * 100
    vendor.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

    avg_response_time_seconds = completed_orders.aggregate(
        AvgDuration=ExpressionWrapper(Avg(F('acknowledgment_date') - F('issue_date')), output_field=fields.DurationField())
    )['AvgDuration']

    if avg_response_time_seconds is not None:
        avg_response_time_hours = avg_response_time_seconds // 3600
        vendor.avg_response_time = avg_response_time_hours.total_seconds() if avg_response_time_hours else 0.0
    else:
        vendor.avg_response_time = 0.0

    vendor.fulfillment_rate = completed_orders.count() / vendor.purchaseorder_set.count() * 100
    vendor.save()

    # Update HistoricalPerformance metrics
    historical_performance, _ = HistoricalPerformance.objects.get_or_create(
        vendor=vendor,
        defaults={
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'avg_response_time': vendor.avg_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
    )

    # Always update the entry if it already exists
    historical_performance.on_time_delivery_rate = vendor.on_time_delivery_rate
    historical_performance.quality_rating_avg = vendor.quality_rating_avg
    historical_performance.avg_response_time = vendor.avg_response_time
    historical_performance.fulfillment_rate = vendor.fulfillment_rate
    historical_performance.save()


@receiver(post_save, sender=PurchaseOrder)
def update_avg_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date and instance.issue_date:
        instance.vendor.update_avg_response_time()