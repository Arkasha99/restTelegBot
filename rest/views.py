import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest.forms import SignUpForm
from rest.models import Token, Message
from restTelegram import settings


class RegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


@csrf_protect
def index(request):
    name = 'Unknown'
    if request.user.is_authenticated:
        name = request.user.first_name
    return render(request, template_name='index.html', context={'name': name})


@login_required
def profile(request, pk):
    if Token.objects.filter(user=request.user):
        token = Token.objects.filter(user=request.user).get()
        messages = Message.objects.filter(user=request.user).order_by('-time')
        return render(request, 'profile.html', {'user': request.user, 'generated_token': token.token,'messages':messages})
    else:
        return render(request, 'profile.html', {'user':request.user})


@login_required()
def send_msg(request):
    if request.method == 'POST':
        msg = request.POST.get('text')
        new_message = Message.objects.create(user=request.user, text=msg, time=datetime.datetime.now())
        new_message.save()
        text = f"{request.user.first_name}, я получил от тебя сообщение: \n" \
               f"{msg}"
        tg_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        chat_id = Token.objects.filter(user=request.user).get().chat_id
        params = {
            'chat_id': chat_id,
            'text': text
        }
        requests.get(tg_url, params=params).json()
        return redirect('index')


@login_required()
def generate_token(request):
    token = get_random_string(32)
    Token.objects.get_or_create(user=request.user, token=token, chat_id=1)
    return redirect('index')


class TelegramView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        if "message" in request.data:
            if request.data["message"]["text"] != '/start':
                msg = request.data["message"]
                chats_id = msg["chat"]["id"]
                token = Token.objects.get(token__exact=request.data["message"]["text"])
                if request.data["message"]["text"] == token.token and token.chat_id != chats_id:
                    token.chat_id = chats_id
                    token.save()
                return Response()
        return Response()
