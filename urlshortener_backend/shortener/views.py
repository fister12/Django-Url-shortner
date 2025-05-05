from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortURLSerializer
import random, string
from django.http import HttpResponseRedirect

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenURL(APIView):
    def post(self, request):
        original_url = request.data.get('original_url')
        short_code = generate_short_code()
        short_url = ShortURL.objects.create(original_url=original_url, short_code=short_code)
        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RedirectURL(APIView):
    def get(self, request, short_code):
        try:
            url = ShortURL.objects.get(short_code=short_code)
            return HttpResponseRedirect(url.original_url)
        except ShortURL.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)