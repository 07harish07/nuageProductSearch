from django.db import models

# Create your models here.


class Product(models.Model):
    ProductName = models.CharField(max_length=255, default=None,blank=True,null=True)
    Url = models.URLField(default=None)
    ImageUrl = models.URLField(default=None)
    Price = models.DecimalField(max_digits=10, decimal_places=2)