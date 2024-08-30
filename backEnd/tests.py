from django.test import TestCase
from .models import Property, Tenant, Rental
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import io
from contextlib import redirect_stdout

class PropertyModelTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='apartment',
            number_of_units=10,
            rental_cost=1200.00
        )

    def test_property_str(self):
        self.assertEqual(str(self.property), 'Test Property')


class TenantModelTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='apartment',
            number_of_units=10,
            rental_cost=1200.00
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            contact_details='tenant@test.com',
            property=self.property,
            section_occupy='Section A'
        )

    def test_tenant_str(self):
        self.assertEqual(str(self.tenant), 'Test Tenant')

    def test_send_payment_reminder(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.tenant.send_payment_reminder()
        
        self.assertIn("Email sent to Test Tenant", buffer.getvalue())


class RentalModelTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='apartment',
            number_of_units=10,
            rental_cost=1200.00
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            contact_details='tenant@test.com',
            property=self.property,
            section_occupy='Section A'
        )
        self.rental = Rental.objects.create(
            tenant=self.tenant,
            payment_amount=1200.00,
            is_settled=False
        )

    def test_rental_str(self):
        self.assertEqual(str(self.rental), 'Payment of 1200.00 by Test Tenant')


User = get_user_model()

class PropertyViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='apartment',
            number_of_units=10,
            rental_cost=1200.00
        )

    def test_list_properties(self):
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_property(self):
        data = {
            'name': 'New Property',
            'address': '456 New St',
            'property_type': 'house',
            'number_of_units': 5,
            'rental_cost': 1500.00
        }
        response = self.client.post(reverse('property-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SendReminderViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='apartment',
            number_of_units=10,
            rental_cost=1200.00
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            contact_details='tenant@test.com',
            property=self.property,
            section_occupy='Section A'
        )

    def test_send_reminder(self):
        response = self.client.post(reverse('send_reminder', kwargs={'tenant_id': self.tenant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Payment reminder sent to Test Tenant', response.content.decode())