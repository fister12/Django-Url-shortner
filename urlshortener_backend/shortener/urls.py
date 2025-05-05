from django.urls import path
from .views import ShortenURL, RedirectURL

urlpatterns = [
    path('shorten/', ShortenURL.as_view()),
    path('<str:short_code>/', RedirectURL.as_view()),
]