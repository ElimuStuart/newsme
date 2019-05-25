from django.contrib import admin

from .models import NewsArticle, UserProfile

admin.site.register(NewsArticle)
admin.site.register(UserProfile)