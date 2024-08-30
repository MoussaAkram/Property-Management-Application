# Property Management Application

The goal is to create a simple property management application that can handle properties of various sizes. The app should enable property managers to add new properties, manage tenants, and monitor rent payments.

For this we using [Django](https://www.djangoproject.com/) to create this application.

For explaien our application we decide to structured around three chapters.


## Container of files

Our code is Django project called HomeAssignment that contains a single app called backEnd.
 - backEnd/urls.py, where the URL configuration for this app is defined.
 - backEnd/models.py, where we define our models(User,Property,Tenant,Rental)
 - backEnd/serializers.py it's allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON
 - backEnd/views.py contains views that are associated with routes.The `PropertyViewSet` using for creates a new property and get a list of properties. The `TenantViewSet` using for adding, modifying, and removing tenants from properties. The `PaymentViewSet` using to enter information about payments made by each tenant.The `send_reminder_view` using for send notifications for due payments.



## How to run application

First start with download requirements.txt with :
```bash
pip3 install -r requirements.txt 
```

after run following command : 
```bash
python manage.py makemigrations backEnd

python manage.py migrate

```

and add super user to use for test application with :
```bash
python manage.py createsuperuser
```

then you can run :
```bash
python manage.py runserver
```
## API documentation 

First, navigate to [Swagger](http://127.0.0.1:8000/swagger/).

You need to authenticate and obtain your JWT access token from `/api/token/`. You also can refresh the token with `/api/token/refresh/`.

All endpoints require authentication using JSON Web Tokens (JWT). You need to include the token in the Authorization header of your requests: `Bearer <your_token>`.

- `GET /api/properties`/, retrieve a list of all properties.
- `POST /api/properties/`, create a new property.
- `GET /api/tenants/`, retrieve a list of all tenants.
- `GET /api/tenants/{id}/`, retrieve a specific tenant by their id.
- `POST /api/tenants/`, create a new tenant.
- `PUT /api/tenants/`, update a tenant.
- `DELETE /api/tenants/`, delete a tenant.
- `POST /send-reminder/{tenant_id}/`, Send a payment reminder to a tenant via email.
- `POST /api/payments/`, enter information about payments.
