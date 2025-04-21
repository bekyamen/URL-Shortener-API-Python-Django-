from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ShortURL
from .serializers import ShortURLSerializer, ShortURLCreateSerializer
from django.utils import timezone

class ShortenURLView(generics.CreateAPIView):
    serializer_class = ShortURLCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = serializer.save()
        response_serializer = ShortURLSerializer(short_url)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


from django.core.cache import cache

class RedirectView(generics.GenericAPIView):
    def get(self, request, short_code, *args, **kwargs):
        cache_key = f'short_url_{short_code}'
        short_url = cache.get(cache_key)
        
        if not short_url:
            short_url = get_object_or_404(ShortURL, short_code=short_code)
            cache.set(cache_key, short_url, timeout=60*60)  # Cache for 1 hour
            
        if short_url.is_expired():
            return Response(status=status.HTTP_410_GONE)
            
        short_url.visits += 1
        short_url.save()
        return redirect(short_url.original_url)



class StatsView(generics.RetrieveAPIView):
    serializer_class = ShortURLSerializer
    queryset = ShortURL.objects.all()
    lookup_field = 'short_code'
    lookup_url_kwarg = 'short_code'