from django.db import models
from django.contrib.auth.models import User 
class customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=100, null=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    pic=models.ImageField(null=True,blank=True)
    # def __str__(self):
    #         return self.name
    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return "Unnamed Customer"

    
class tag(models.Model):
    names = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.names    

class product(models.Model):
    CATEGORY = ( 
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor"),
        ("Electronics","Electronics"),
        ("Toys","Toys"),
        ("Stationary","Stationary"),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=100)
    data_created = models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(tag)

    def __str__(self):
        return self.name  
    

class order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),

    )

    customer=models.ForeignKey(customer, null=True, on_delete= models.CASCADE )
    product=models.ForeignKey(product, null=True, on_delete= models.CASCADE )
    data_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)

 