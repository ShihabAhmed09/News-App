from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Category
import requests

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"


def news(request):
    categories = Category.objects.all()

    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search == 'top':
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format('us', 1, settings.API_KEY)
    else:
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search, 'popularity', page,
                                                                                          settings.API_KEY)

    news = requests.get(url=url)
    data = news.json()

    if data['status'] != 'ok':
        return HttpResponse('<h1>Request Failed</h1>')

    data = data['articles']

    context = {
        'categories': categories,
        'success': True,
        'data': [],
        'search': search
    }

    for i in data:
        context['data'].append({
            'source': i['source']['name'],
            'author': i['author'],
            'title': i['title'],
            'description': '' if i['description'] is None else i['description'],
            'url': i['url'],
            'image': temp_img if i['urlToImage'] is None else i['urlToImage'],
            'publishedAt': i['publishedAt'],
        })

    return render(request, 'news_app/news_home.html', context)


def load_content(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)

        if search is None or search == 'top':
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format('us', page,
                                                                                             settings.API_KEY)
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search, 'popularity',
                                                                                              page, settings.API_KEY)

        news = requests.get(url=url)
        data = news.json()

        if data['status'] != 'ok':
            return JsonResponse({"success": False})

        data = data['articles']

        context = {
            'success': True,
            'data': [],
            'search': search
        }

        for i in data:
            context['data'].append({
                'source': i['source']['name'],
                'author': i['author'],
                'title': i['title'],
                'description': '' if i['description'] is None else i['description'],
                'url': i['url'],
                'image': temp_img if i['urlToImage'] is None else i['urlToImage'],
                'publishedAt': i['publishedAt'],
            })

        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success": False})
