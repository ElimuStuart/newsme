from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_scrape = models.DateTimeField()

    def __str__(self):
        return f'{self.user} - {self.last_scrape}'

class NewsArticle(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField()
    url = models.TextField()
    summary = models.TextField()

    def __str__(self):
        return self.title