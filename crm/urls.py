"""
URL configuration for the CRM app.

Namespace all URLs under ``crm`` to avoid collisions with other apps.
Each path maps to a class‑based view for listing or editing the
corresponding model.
"""

from __future__ import annotations

from django.urls import path
from django.views.generic import RedirectView

from .views import (
    CarCreateView,
    CarListView,
    CarUpdateView,
    CustomerCreateView,
    CustomerListView,
    CustomerUpdateView,
    ReservationCreateView,
    ReservationListView,
    ReservationUpdateView,
    PublicReservationView,
)

from django.views.generic import TemplateView


app_name = 'crm'

urlpatterns = [
    # Default CRM root -> vehicles list
    path('', RedirectView.as_view(pattern_name='crm:car_list', permanent=False)),
    # Cars
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/add/', CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit/', CarUpdateView.as_view(), name='car_edit'),
    # Customers
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', CustomerCreateView.as_view(), name='customer_add'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    # Reservations
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/add/', ReservationCreateView.as_view(), name='reservation_add'),
    path('reservations/<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation_edit'),
    # Public reservation form and success page
    path('public/reserve/', PublicReservationView.as_view(), name='public_reservation'),
    path('public/reserve/success/',
         TemplateView.as_view(template_name='crm/public_reservation_success.html'),
         name='public_reservation_success'),
]
