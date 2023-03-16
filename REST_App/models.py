from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    marks = models.IntegerField()
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = "Student"


class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary  = models.IntegerField()
    company = models.CharField(max_length= 100)
    is_active = models.BooleanField(default =True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Employees"



#Generating token using signals 

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created =  False , **kwargs):
    print(created)
    if created:
        Token.objects.create(user = instance)
        print(f"Token Generated For {instance}")




