from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_editor = models.BooleanField(default=False)
    is_viewer = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='imgs/')

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Headline = models.CharField(max_length=300)
    image = models.ImageField(upload_to='imgs/')
    Body = models.TextField()
    publishing_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Headline


class Rating(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(5)])  # Ratings from 0 to 4
    comment = models.TextField()
