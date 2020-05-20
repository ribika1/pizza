

from pizza import models

from django.core.management.base import BaseCommand
from os.path import split, join
import sqlite3


class Command(BaseCommand):
    help = "adds sample entities to the application"

    def load1(self):
        this_dir = split(__file__)[0]
        abs_path = join(this_dir, "pizza-190807A.sqlite")
        with sqlite3.connect(abs_path) as conn:
            crs = conn.cursor()

            self.stdout.write("Customer")
            cmd = "select * from Customer"
            crs.execute(cmd)
            for row in crs:
                cust = models.Customer(
                    customerId=row[0],
                    firstName=row[1],
                    lastName=row[2],
                    email=row[3]
                )
                cust.save()

            self.stdout.write("Crust")
            cmd = "select * from crust"
            crs.execute(cmd)
            for row in crs:
                topping = models.Crust(
                    crustId=row[0],
                    name=row[1],
                    price=row[2]
                )
                topping.save()

            self.stdout.write("Sauce")
            cmd = "select * from sauce"
            crs.execute(cmd)
            for row in crs:
                topping = models.Sauce(
                    sauceId=row[0],
                    name=row[1],
                    price=row[2]
                )
                topping.save()

            self.stdout.write("Topping")
            cmd = "select * from topping"
            crs.execute(cmd)
            for row in crs:
                topping = models.Topping(
                    toppingId=row[0],
                    name=row[1],
                    price=row[2]
                )
                topping.save()

            self.stdout.write("Invoice")
            cmd = "select * from invoice"
            crs.execute(cmd)
            for row in crs:
                invoice = models.Invoice(
                    invoiceId=row[0],
                    customer=models.Customer.objects.get(pk=row[1]),
                    date=row[2]
                )
                invoice.save()

            self.stdout.write("Pizza")
            cmd = "select * from pizza"
            crs.execute(cmd)
            for row in crs:
                pizza = models.Pizza(
                    pizzaId=row[0],
                    crust=models.Crust.objects.get(pk=row[1]),
                    sauce=models.Sauce.objects.get(pk=row[2]),
                    discount=row[3],
                    invoice=models.Invoice.objects.get(pk=row[4])
                )
                pizza.save()

            self.stdout.write("Link toppings to pizzas")
            cmd = "select * from pizzaTopping"
            crs.execute(cmd)
            for row in crs:
                topping = models.Topping.objects.get(pk=row[1])
                pizza = models.Pizza.objects.get(pk=row[0])
                pizza.toppings.add(topping)
                # pizza.save()
            for p in models.Pizza.objects.all():
                p.save()
                # self.stdout.write(p.toppings.all())

    def handle(self, *args, **options):
        self.load1()
