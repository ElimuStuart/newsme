from django.conf import settings
import os
import math
import shutil

from django.shortcuts import render, redirect, reverse
from django.utils import timezone

from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()

from .models import NewsArticle, UserProfile
from datetime import datetime, timedelta

def news(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    now = timezone.now()
    time_difference = now - user_p.last_scrape
    time_difference_in_hours = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_difference_in_hours

    if time_difference_in_hours <= 24:
        hide_me = True
    else:
        hide_me = False

    news_articles = NewsArticle.objects.all()
    context = {
        'news_articles': news_articles,
        'hide_me': hide_me,
        'next_scrape': math.ceil(next_scrape),
        'time_difference_in_hours': math.ceil(time_difference_in_hours),


    }
    return render(request, 'index.html', context)

def scrape(request):
    # print(datetime.now())
    user_p = UserProfile.objects.filter(user=request.user).first()
    user_p.last_scrape = timezone.now()
    user_p.save()

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"}
    url = 'https://www.monitor.co.ug/'

    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")
    

    top_headline = soup.find('section', class_='main-home')
    posts = top_headline.find_all('div', class_='story-teaser')

    for post in posts:
        title = post.a.text
        image = url+post.img['src']
        post_url = url+post.a['href']
        summary = post.p.text

        media_root = settings.MEDIA_ROOT
        if not image.startswith(("data:image", "javascript")):
            local_filename = image.split("/")[-1].split("?")[0]
            r = session.get(image, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)

        news_article = NewsArticle()
        news_article.title = title
        news_article.url = post_url
        news_article.image = local_filename
        news_article.summary = summary

        news_article.save()

        # print(title)    
        # print(url+image)
        # print(url+post_url)
        # print()

    return redirect(reverse('news:news'))
