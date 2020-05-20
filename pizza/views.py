from django.shortcuts import render, redirect
from pizza.models import Crust, Sauce, Topping, Pizza, Customer, Invoice
from django.views.decorators.http import require_http_methods
from datetime import datetime


@require_http_methods(['GET'])
def build_pizza(request, messages=None):
    """
    Creates and displays the build pizza page.
    :param messages: Not used
    """
    if not messages:
        messages = []
    context = {
        'crusts': Crust.objects.all(),
        'sauces': Sauce.objects.all(),
        't_regular': Topping.objects.filter(price__lt=2),
        # regular toppings are less than $2
        #CHANGE MADE
        't_premium': Topping.objects.filter(price__gte=2),
        # premium toppings are $2 or more
        'messages': messages,
    }
    return render(request, 'pizza/build_a_pizza.html', context)


@require_http_methods(['GET'])
def price_pizza(request):
    try:
        # Get the data from the Build Pizza page, all id's
        crust_id = request.GET['crust']
        #CHANGE MADE
        sauce_id = request.GET['sauce']
        topping_ids = request.GET.getlist('topping')
        # get the corresponding arguments
        crust = Crust.objects.get(pk=crust_id)
        sauce = Sauce.objects.get(pk=sauce_id)
        toppings = Topping.objects.filter(pk__in=topping_ids)
        toppings_price = sum([tp.price for tp in toppings])
        # create and save the 'built' variable in the session
        request.session['built'] = (crust.crustId, sauce.sauceId,
                                    [t.toppingId for t in toppings])
        context = {
            'crust': crust,
            'sauce': sauce,
            'toppings': toppings,
            'total': crust.price + sauce.price + toppings_price,
        }
        return render(request, 'pizza/price_pizza.html', context)
    except KeyError:
        return render(request, "pizza/error.html",
                                   {'error_list': ['missing information']})
    except Crust.DoesNotExist:
        return render(request, "pizza/error.html",
                                   {'error_list': ['invalid crust id %s' % (crust_id,)]})
    except Sauce.DoesNotExist:
        return render(request, "pizza/error.html",
                                   {'error_list': ['invalid sauce id %s' % (sauce_id,)]})



#  this is not a view function, it is a utility function used in a couple of the view functions.
def built_to_objects(built):
    """"
        Convert the 'built' information to a similarly organized
        collection of objects.

        built is a list of crustId, sauceId, and a list of toppingId's

        return a crust object, a sauce object, and a list of topping objects
    """
    rtblt = [Crust.objects.get(pk=built[0]), Sauce.objects.get(pk=built[1])]
    toppings = [Topping.objects.get(pk=t) for t in built[2]]
    rtblt.append(toppings)
    toppings_price = sum([tp.price for tp in toppings])
    rtblt.append(rtblt[0].price+rtblt[1].price+toppings_price)
    return rtblt



@require_http_methods(['POST'])
def add_to_tab(request):
    # get the pizza built by the user
    built = request.session.get('built')
    if not built:
        return build_pizza(request, messages=["No pizza built yet, build one here"])
    else:
        # Get the value of the 'tab' session variable
        # The 'get' method returns an empty list, the second argument, if `built` is not defined
        tabb = request.session.get('tab', [])
        #CHANGE MADE (ADDED CODE BELOW)
        tabb.append(built)
        # add the new pizza information to the list
        # assign the new value back to the `tab` variable in the session
        request.session['tab'] = tabb
        # empty the `built` session variable
        request.session['built'] = []
        return redirect("show_tab")


@require_http_methods(['GET'])
def show_tab(request):
    # get the tab session variable
    tab = request.session.get('tab', [])
    # get the corresponding objects (crusts, sauces, and toppings)
    tab_obj = [built_to_objects(t) for t in tab]
    #CHANGE MADE
    grand_total = sum([t[3] for t in tab_obj])
    return render(request, "pizza/show_tab.html",
                  {'tab': tab_obj, 'grand_total': grand_total})


@require_http_methods(['POST'])
def remove_from_tab(request):
    tab = request.session.get('tab', [])
    try:
        # the show tab page sends the index of the pizza to remove
        index = request.POST['pizza_index']
        index = int(index)
    except ValueError:
        return render(request, "pizza/error.html",
                  {'error_list': ['Invalid pizza choice']})
    if 0 <= index < len(tab):
        # delete the selected pizza from the local copy of `tab`
        del tab[int(index)]
        #CHANGE MADE
        request.session['tab']=tab
        return redirect("show_tab")
    else:
        return render(request, "pizza/error.html",
                      {'error_list': ['Invalid pizza choice']})


@require_http_methods(['GET'])
def edit_pizza(request):
    tab = request.session.get('tab', [])
    try:
        # the show tab page sends the index, in the `tab` variable, of the pizza to edit
        #CHANGE MADE
        index = request.GET['pizza_index']
        index = int(index)
    except ValueError:
        return render(request, "pizza/error.html",
                      {'error_list': ['Invalid pizza choice']})
    if 0 <= index < len(tab):
        # get the id's describing the pizza from the `tab` variable
        # This will be used in the template to determine dynamically which
        # check boxes and which radio buttons should be checked.
        pizza_descriptor = tab[index]
        context = {
            'crusts': Crust.objects.all(),
            'sauces': Sauce.objects.all(),
            't_regular': Topping.objects.filter(price__lt=2),
            't_premium': Topping.objects.filter(price__gte=2),
            'pizza_descriptor': pizza_descriptor,
            'index': index,
        }
        return render(request, "pizza/edit_pizza.html", context)
    else:
        return render(request, "pizza/error.html",
                      {'error_list': ['Invalid pizza choice']})


@require_http_methods(['POST'])
def save_edits(request):
    try:
        # this page is much like the Price Pizza page
        # the information is sent in the HTTP request
        crust_id = int(request.POST['crust'])
        sauce_id = int(request.POST['sauce'])
        tab_index = int(request.POST['index'])
        topping_ids = [int(t) for t in request.POST.getlist('topping')]
        # get the current 'tab' from session
        tab = request.session.get('tab', [])
        # replace the edited pizza in the local copy of `tab`
        tab[tab_index] = (crust_id, sauce_id, topping_ids)
        # replace the `tab` variable with the new value
        request.session['tab'] = tab
        #CHANGE MADE
        return redirect("show_tab")
    except KeyError:
        return render(request, "pizza/error.html",
                                   {'error_list': ['missing information']})
    except Crust.DoesNotExist:
        return render(request, "pizza/error.html",
                                   {'error_list': ['invalid crust id %s' % (crust_id,)]})
    except Sauce.DoesNotExist:
        return render(request, "pizza/error.html",
                                   {'error_list': ['invalid sauce id %s' % (sauce_id,)]})


@require_http_methods(['GET'])
def checkout(request):
    customers = Customer.objects.all().order_by("lastName")

    tab = request.session.get('tab', [])
    tab_obj = [built_to_objects(t) for t in tab]
    grand_total = sum([t[3] for t in tab_obj])

    context = {
        #CHANGE MADE
        'customers': customers,
        'tab': tab_obj,
        'grand_total': grand_total
    }
    return render(request, "pizza/checkout.html", context)


@require_http_methods(['POST'])
def complete_sale(request):
    # get the `tab` from session
    # this will be used as the basis for building an invoice
    tab = request.session.get('tab', [])

    if tab:

        try:
            customer_id = int(request.POST['customer_id'])
        except:
            return render(request, "pizza/error.html",
                          {'error_list': ['invalid customer id']})

        # create an invoice object with the customer spacified on the Checkout page
        #    and the current time
        invoice = Invoice(customer_id=customer_id, date=datetime.now())
        # Persist the object, that is, save in the database
        invoice.save()

        # for each pizza in the tab, create a Pizza object
        for pizza in tab:
            # we can create a Pizza object specify the id's for crust and sauce rather
            #     than providing objects
            # Notice that we provide the invoice to the Pizza, so the connection between
            #    the two is made here
            pz = Pizza(crust_id=pizza[0], sauce_id=pizza[1],
                       discount=0, invoice=invoice)
            # Persist the pizza object
            pz.save()
            # for each topping, add it to the pizza
            for topping_id in pizza[2]:
                # Looks like we have to add topping objects, we can't use the id's directly
                pz.toppings.add(Topping.objects.get(toppingId=topping_id))
            pz.save()
        request.session['tab'] = []
        return redirect("thank_you")

    else:
        return render(request, 'pizza/error.html',
                  {'error_list': ['You have not ordered any pizzas yet!']})


@require_http_methods(['GET'])
def thank_you(request):
    return render(request, 'pizza/thank_you.html')


@require_http_methods(['GET'])
def select_user(request):
    context = {
        'customers':    Customer.objects.all().order_by('lastName')
    }
    return render(request, 'pizza/select_user.html', context)


@require_http_methods(['GET'])
def list_invoices(request):
    try:
        customer_id = int(request.GET['customer_id'])
        customer = Customer.objects.get(pk=customer_id)
        invoices = customer.invoice_set.all()
        context = {
            'customer': customer,
            # 'invoices': invoices,
        }
        return render(request, 'pizza/show_invoices.html', context)
    except Exception as exc:
        return render(request, 'pizza/error.html',
                      {'error_list': ['Invalid customer choice', str(exc)]})


@require_http_methods(['GET'])
def invoice_details(request):
    try:
        invoice_id = int(request.GET['invoice_id'])
        invoice = Invoice.objects.get(pk=invoice_id)
        context = {
            'invoice': invoice,
        }
        return render(request, 'pizza/invoice_details.html', context)
    except Exception as exc:
        return render(request, 'pizza/error.html',
                      {'error_list': ['Invalid invoice choice', str(exc)]})


@require_http_methods(['GET'])
def big_spenders(request):
    customers = sorted(Customer.objects.all(), key=lambda c: -c.total_invoices())
    context = {
        'customers': customers
    }
    return render(request, 'pizza/big_spenders.html', context)
