from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortURLSerializer
import random, string
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def redirect_view(request, short_code):
    obj = get_object_or_404(ShortURL, short_code=short_code)
    return redirect(obj.original_url)
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

class ShortenURL(APIView):
    def post(self, request):
        original_url = request.data.get('original_url')
        # Ensure the URL starts with http:// or https://
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url
        short_code = generate_short_code()
        short_url = ShortURL.objects.create(original_url=original_url, short_code=short_code)
        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RedirectURL(APIView):
    def get(self, request, short_code):
        try:
            url = ShortURL.objects.get(short_code=short_code)
            # Ensure the original_url is a valid absolute URL
            if not url.original_url.startswith(('http://', 'https://')):
                return Response({'error': 'Invalid URL'}, status=400)
            return redirect(url.original_url)
        except ShortURL.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
