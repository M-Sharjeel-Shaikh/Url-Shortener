from tkinter import CASCADE
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.
class url_user(models.Model):
    original_url = models.URLField(default=False)
    short_url = models.CharField(blank=False, max_length=8)
    visit = models.IntegerField(default=0)
    user = models.ForeignKey(User ,on_delete= models.CASCADE)