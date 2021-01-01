from django.contrib import admin
from searchApp.models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'ProductName', 'Price', 'Url', 'ImageUrl']