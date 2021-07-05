from django.contrib import admin

# Register your models here.
from rest.models import Token, Message

admin.site.register(Token)
admin.site.register(Message)
