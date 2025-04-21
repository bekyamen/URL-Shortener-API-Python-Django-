from rest_framework import serializers
from .models import ShortURL
from django.utils import timezone

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'created_at', 'expires_at', 'visits']
        read_only_fields = ['short_code', 'created_at', 'visits']

    def validate_expires_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value

class ShortURLCreateSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='original_url')
    
    class Meta:
        model = ShortURL
        fields = ['url', 'expires_at']