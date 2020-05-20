__author__ = 'faculty'


from pizza import models

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "removes all model data"

    def handle(self, *args, **options):
        models.Pizza.objects.all().delete()
        models.Crust.objects.all().delete()
        models.Sauce.objects.all().delete()
        models.Topping.objects.all().delete()
        models.Invoice.objects.all().delete()
        models.Customer.objects.all().delete()
