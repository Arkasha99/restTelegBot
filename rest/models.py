from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Token(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    chat_id = models.BigIntegerField(blank=True)


class Message(models.Model):
    user = models.ForeignKey(User, verbose_name='Автор сообщения', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    time = models.DateTimeField(blank=True)
