from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)

class NewsStory(models.Model):
    category_choices = [
        ('politics', 'Politics'),
        ('entertainment', 'Entertainment'),
        ('sport', 'Sport'),
        ('technology', 'Technology'),
        ('other', 'Other')
    ]
    region_choices = [
        ('uk', 'UK'),
        ('us', 'US'),
        ('eu', 'EU'),
        ('other', 'Other')
    ]
    headline = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=category_choices)
    region = models.CharField(max_length=20, choices=region_choices)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    details = models.CharField(max_length=500)