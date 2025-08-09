from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

class Tweet(models.Model):
    # allow anonymous posts by making user optional
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    image = models.ImageField(upload_to='tweet_images/', blank=True, null=True)  # NEW field
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Use BLACKLISTED_WORDS from settings (fallback to empty list)
        for word in getattr(settings, "BLACKLISTED_WORDS", []):
            if word.lower() in (self.content or "").lower():
                raise ValidationError(f"The word '{word}' is inappropriate.")

    def __str__(self):
        return self.content[:50] + ("..." if len(self.content) > 50 else "")
