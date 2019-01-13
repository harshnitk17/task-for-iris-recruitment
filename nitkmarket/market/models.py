from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=5000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    mobile=models.IntegerField(default=888888888,blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class item(models.Model):
    user_id=models.IntegerField(blank=True,null=True)
    price=models.CharField(max_length=100,blank=True)
    description=models.TextField(max_length=5000,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    type=models.CharField(max_length=10,blank=True)
    tag=models.CharField(max_length=1000,blank=True)
    title=models.CharField(max_length=1000,blank=True)
    imagefile= models.FileField(upload_to='images/', null=True, verbose_name="")
    status=models.TextField(max_length=50,default="notsold")
