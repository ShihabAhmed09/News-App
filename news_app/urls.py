from django.urls import path
from . import views

app_name = 'news_app'
urlpatterns = [
    path('', views.news, name='news_home'),
    path('next/', views.load_content, name='load-content'),
]
