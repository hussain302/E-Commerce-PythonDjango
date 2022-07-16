from django.shortcuts import render, redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse


def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        subject = request.POST.get('subject', '')
        # print(name)

        contact = Contact(name=name, email=email, message=message, subject=subject)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            order = Orders.objects.filter(order_id=orderId, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')

def productView(request, id):
    # fetch product
    product = Product.objects.filter(id=id)
    # print(product)
    return render(request, 'shop/prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == 'POST':
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address_1 = request.POST.get('address1', '')
        address_2 = request.POST.get('address2', '')
        zip = request.POST.get('zip', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        # print(name)

        order = Orders(name=name,
                       itemsJson=itemsJson,
                       email=email,
                       address_2=address_2,
                       address_1=address_1,
                       state=state,
                       city=city,
                       phone=phone,
                       zip_code=zip,
                       )
        order.save()
        thank = True
        id = order.order_id
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
