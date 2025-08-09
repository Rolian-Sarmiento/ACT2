from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "created_at")
    readonly_fields = ("created_at",)
