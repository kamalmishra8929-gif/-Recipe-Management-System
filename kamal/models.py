from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
class Recipe(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True, null=True)
    recipe_name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)