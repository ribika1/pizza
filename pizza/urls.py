"""a06_django_pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from pizza import views

urlpatterns = [
    path('', views.build_pizza, name='build_pizza'),
    path('price_pizza', views.price_pizza, name="price_pizza"),
    path('add_to_tab', views.add_to_tab, name="add_to_tab"),
    # path('show_tab', views.show_tab, name='show_tab'),
    path('show_tab', views.show_tab, name='show_tab'),
    path('remove_from_tab', views.remove_from_tab, name='remove_from_tab'),
    path('edit_pizza', views.edit_pizza, name='edit_pizza'),
    path('save_edits', views.save_edits, name='save_edits'),
    path('checkout', views.checkout, name='checkout'),
    path('complete_sale', views.complete_sale, name='complete_sale'),
    path('thank_you', views.thank_you, name='thank_you'),
    path('select_user', views.select_user, name='select_user'),
    path('list_invoices', views.list_invoices, name='list_invoices'),
    path('invoice_details', views.invoice_details, name='invoice_details'),
    path('big_spenders', views.big_spenders, name='big_spenders'),
]



