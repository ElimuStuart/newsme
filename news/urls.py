from django.urls import path
from .views import scrape, news

app_name = "news"

urlpatterns = [
    path("news/", news, name='news'),
    path("scrape/", scrape, name="scrape"),
]