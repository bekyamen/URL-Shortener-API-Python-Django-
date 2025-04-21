from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import ShortURL
from django.utils import timezone
import datetime

class ShortenerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_url = 'https://example.com'
        self.expired_url = ShortURL.objects.create(
            original_url=self.test_url,
            short_code='exp123',
            expires_at=timezone.now() - datetime.timedelta(days=1)
        )

    def test_create_short_url(self):
        url = reverse('shorten')
        data = {'url': self.test_url}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShortURL.objects.count(), 2)

    def test_redirect(self):
        short_url = ShortURL.objects.create(original_url=self.test_url, short_code='test12')
        url = reverse('redirect', args=[short_url.short_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.test_url)

    def test_expired_redirect(self):
        url = reverse('redirect', args=[self.expired_url.short_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

    def test_stats(self):
        short_url = ShortURL.objects.create(original_url=self.test_url, short_code='stats1')
        url = reverse('stats', args=[short_url.short_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.test_url)