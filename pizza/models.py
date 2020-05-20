from django.db import models
# from django.db.models import Sum


class Topping(models.Model):
    toppingId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return "Topping[%d  %s   %.2f]" % (self.toppingId, self.name, float(self.price))


class Crust(models.Model):
    crustId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)


class Sauce(models.Model):
    sauceId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)


class Customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def total_invoices(self):
        return sum([inv.amount() for inv in self.invoice_set.all()])


class Invoice(models.Model):
    invoiceId = models.AutoField(primary_key=True)
    customer = models.ForeignKey("Customer", models.PROTECT)
    date = models.DateTimeField()

    def amount(self):
        return sum([pz.cost() for pz in self.pizza_set.all()])


class Pizza(models.Model):
    pizzaId = models.AutoField(primary_key=True)
    crust = models.ForeignKey("Crust", models.PROTECT)
    sauce = models.ForeignKey("Sauce", models.PROTECT)
    discount = models.FloatField()
    invoice = models.ForeignKey("Invoice", models.PROTECT)
    toppings = models.ManyToManyField("Topping")

    def cost(self):
        # base = self.crust.price + self.sauce.price + sum([top.price for top in self.toppings.all()])
        base = self.crust.price + self.sauce.price
        base += self.toppings.all().aggregate(models.Sum('price'))['price__sum']
        base = float(base) * (1.0 - self.discount)
        return base


