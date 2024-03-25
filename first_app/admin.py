from .models import Category, News, Rating
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)


admin.site.register(Category)


class AdminNews(admin.ModelAdmin):
    list_display = ('Headline', 'category')


admin.site.register(News, AdminNews)


class Adminrating(admin.ModelAdmin):
    list_display = ('news', 'rating', 'comment')


admin.site.register(Rating, Adminrating)
