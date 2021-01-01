from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
import requests
import json
from django.http import HttpResponseRedirect
from searchApp.models import Product
from threading import Thread
from django.core.paginator import Paginator


def shopclues_product(search):
    shopclues_URL = f"http://api.shopclues.com/api/v11/search?q={search}&z=1&key=d12121c70dda5edfgd1df6633fdb36c0&page=1"
    product_data = requests.get(shopclues_URL)      

    product_json_data = product_data.json()
    total_page = int(product_json_data["products_count"])//int(product_json_data["items_per_page"])

    for page in range(1,total_page):
        payload = {
            "q": search,
            "z": 1,
            "key": "d12121c70dda5edfgd1df6633fdb36c0",
            "page": page
        }
        URL2 = "http://api.shopclues.com/api/v11/search"
        product_data = requests.get(URL2, params=payload)
        product_json_data = product_data.json()

        product = product_json_data["products"]
        for i in range(int(product_json_data["items_per_page"])):
            product_name = product[i]["product"]
            product_url = product[i]["product_url"]
            product_image = product[i]["image_url"]
            product_price = product[i]["price"]

            productdata, created = Product.objects.update_or_create(ProductName = product_name, Price = product_price, defaults={'ProductName': product_name, 'Url': product_url,'ImageUrl': product_image, 'Price': product_price})

    return created

def paytm_product(search):
    paytm_URL = f"https://search.paytm.com/v2/search?userQuery={search}&page_count=1&items_per_page=30"
    product_data = requests.get(paytm_URL)
    
    product_json_data = product_data.json()

    for page in range(1,101):
        payload = {
            "userQuery": search,
            "page_count": page,
            "items_per_page": 30
        }
        URL2 = "https://search.paytm.com/v2/search"
        product_data = requests.get(URL2, params=payload)
        product_json_data = product_data.json()

        product = product_json_data["grid_layout"]
        for i in range(30):
            product_name = product[i]["name"]
            product_url = product[i]["newurl"]
            product_image = product[i]["image_url"]
            product_price = product[i]["actual_price"]

            productdata, created = Product.objects.update_or_create(ProductName = product_name, Price = product_price, defaults={'ProductName': product_name, 'Url': product_url,'ImageUrl': product_image, 'Price': product_price})
    return created



def product_list(request):
    if request.GET:
        searchfield = request.GET.get('searchfield')
        print("searchfield-----------------", searchfield)
                
        if not Product.objects.filter(ProductName__icontains=searchfield).exists() :
            t1 = Thread(target=shopclues_product, args=(searchfield, ))
            t2 = Thread(target=paytm_product, args=(searchfield, ))
            t1.start()
            t1.join()
            t2.start()
            t2.join()
        product_detail = Product.objects.filter(ProductName__icontains=searchfield).order_by('id')
        paginator = Paginator(product_detail, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "search.html", {"products": page_obj, "search":searchfield})
    return render(request, "search.html")


