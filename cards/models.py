from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="card's title", max_length=100)
    body = models.TextField(verbose_name="card's body", max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        return super(Cards, self).save(*args, **kwargs)
