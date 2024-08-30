from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=255, choices=PROPERTY_TYPES)
    number_of_units = models.IntegerField(default=1)
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    property = models.ForeignKey(Property, related_name='tenants', on_delete=models.CASCADE)
    section_occupy = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
    def send_payment_reminder(self):
        print(f"Email sent to {self.name}: 'Your rent is due soon.'")

class Rental(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='payments', on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_settled = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment of {self.payment_amount:.2f} by {self.tenant.name}'