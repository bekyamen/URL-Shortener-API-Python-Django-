import random
import string
from django.db import models
from django.utils import timezone

def generate_short_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=6, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    visits = models.PositiveIntegerField(default=0)

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def str(self):
        return f"{self.short_code} -> {self.original_url}"