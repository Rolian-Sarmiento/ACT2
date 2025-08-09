from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from .models import Tweet

def hello_world(request):
    error_message = None

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")

        # Check for blacklisted words from settings.py
        if any(bad_word.lower() in content.lower() for bad_word in getattr(settings, "BLACKLISTED_WORDS", [])):
            error_message = "Your tweet contains inappropriate words!"
        elif content or image:
            tweet = Tweet(content=content, created_at=timezone.now())
            if image:
                tweet.image = image
            tweet.save()
            return redirect("hello_world")

    # Get all tweets ordered by newest first
    tweets = Tweet.objects.all().order_by("-created_at")

    return render(
        request,
        "base.html",
        {
            "tweets": tweets,
            "error_message": error_message
        }
    )
