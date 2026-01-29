"""
URL configuration for gamboa_project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    # Public home page for the car rental business.
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # CRM app URLs under '/crm/'.
    path('crm/', include('crm.urls')),
    # Contrato page
    path('contrato/', TemplateView.as_view(template_name='contract.html'), name='contract'),
    # Django admin interface.
    path('admin/', admin.site.urls),
]
