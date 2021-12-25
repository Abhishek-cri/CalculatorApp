from django.db import models
from django.contrib.auth.models import User
# Create your models here


class Student(models.Model):
    Expression = models.CharField(max_length=30)
    User = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    result=models.FloatField()
    profile_pic=models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.result

