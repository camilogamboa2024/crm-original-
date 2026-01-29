"""
Views for the CRM application.

This module defines list and create/update views for the primary
models. Using Django’s generic class‑based views simplifies CRUD
operations and enforces consistency across pages.
"""

from __future__ import annotations

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.shortcuts import redirect, render


from .models import Car, Customer, Reservation
from .forms import CarForm, CustomerForm, ReservationForm, PublicReservationForm


class CarListView(ListView):
    model = Car
    template_name = 'crm/car_list.html'
    context_object_name = 'cars'


class CarCreateView(SuccessMessageMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'crm/car_form.html'
    success_url = reverse_lazy('crm:car_list')
    success_message = 'Vehículo agregado correctamente.'


class CarUpdateView(SuccessMessageMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'crm/car_form.html'
    success_url = reverse_lazy('crm:car_list')
    success_message = 'Vehículo actualizado correctamente.'


class CustomerListView(ListView):
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('crm:customer_list')
    success_message = 'Cliente agregado correctamente.'


class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('crm:customer_list')
    success_message = 'Cliente actualizado correctamente.'


class ReservationListView(ListView):
    model = Reservation
    template_name = 'crm/reservation_list.html'
    context_object_name = 'reservations'


class ReservationCreateView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'crm/reservation_form.html'
    success_url = reverse_lazy('crm:reservation_list')
    success_message = 'Reserva registrada correctamente.'


class ReservationUpdateView(SuccessMessageMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'crm/reservation_form.html'
    success_url = reverse_lazy('crm:reservation_list')
    success_message = 'Reserva actualizada correctamente.'


class PublicReservationView(FormView):
    """Public view to allow visitors to request a reservation."""

    template_name = 'crm/public_reservation_form.html'
    form_class = PublicReservationForm
    success_url = reverse_lazy('crm:public_reservation_success')

    def form_valid(self, form):
        car = form.cleaned_data['car']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        # Check date ordering
        if end_date < start_date:
            form.add_error('end_date', 'La fecha de fin no puede ser anterior a la de inicio.')
            return self.form_invalid(form)
        # Check if there are overlapping reservations for this car
        conflict = Reservation.objects.filter(
            car=car,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()
        if conflict:
            form.add_error('car', 'Lo sentimos, este vehículo no está disponible en las fechas seleccionadas.')
            return self.form_invalid(form)

        # Create or retrieve the customer
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        customer, _ = Customer.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone},
        )
        # Update existing customer details if necessary
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.save()

        # Create the reservation
        reservation = Reservation.objects.create(
            customer=customer,
            car=car,
            start_date=start_date,
            end_date=end_date,
            status='booked',
        )
        # Nota: no cambiamos el estado del vehículo aquí.
        # La disponibilidad se determina por las reservas existentes.
        # Si quieres manejar estados (Disponible/Reservado/En uso), es mejor
        # hacerlo desde el CRM o con una regla basada en fechas.

        # You could send email or WhatsApp notifications here

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide price for selected car if selected; used via JS or template
        return context