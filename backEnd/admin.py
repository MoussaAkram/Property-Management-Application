from django.contrib import admin
from .models import User, Property, Tenant, Rental
# Register your models here.

admin.site.register(User)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(Rental)
