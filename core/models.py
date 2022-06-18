from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import Extract


class Journal(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    details = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    details = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_post")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
