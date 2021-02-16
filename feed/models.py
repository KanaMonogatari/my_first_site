from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField() 
    publish = models.DateTimeField(auto_now_add=True,unique=True)
    updated = models.DateTimeField(auto_now=True)
    image=  models.ImageField(upload_to='images/%Y',blank=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return str(self.author)

    
    def get_absolute_url(self):
        return reverse('feed:image_detail',args=[self.image])



class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    avatar = models.ImageField(upload_to='images/users')
 
    def __str__(self):
        return str(self.user)



