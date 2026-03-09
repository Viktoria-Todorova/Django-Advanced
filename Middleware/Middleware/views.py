from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.core.signing import Signer, BadSignature
from django.shortcuts import redirect, render
from django.utils.timezone import now


def choose_language(request):
    if request.method == 'POST':
        selected_language = request.POST.get('language','').lower()

        if selected_language in settings.SUPPORTED_LANGUAGES:
            request.session['language'] = selected_language

        return redirect('home')

    current_language= request.session.get('language','')
    return render(request,'choose_language.html',
                  {'current_language':current_language,
                   'supported_languages':settings.SUPPORTED_LANGUAGES})

def home_page(request):
    GREETING_MESSAGES={
        'en': 'Hello! How are you today?',
        "de":'Hallo! Wie geht es Ihnen heute?',
        "bg": "Здравей как си днес"
    }

    current_language = request.session.get('language','en')
    greeting_messages = GREETING_MESSAGES[current_language]
    return render(request,'home.html',
                  {'current_language':current_language,
                   'greeting_messages':greeting_messages})

def session_expiry(request):
    error_message = ''
    if request.method == 'POST':
        expiry_value = request.POST.get('expiry_seconds', 0)
        try:
            expiry_seconds = int(expiry_value)
            if expiry_seconds <= 0:
                raise ValueError
        except ValueError:
            error_message = 'Enter a positive number of seconds.'
        else:
            request.session.set_expiry(expiry_seconds)

            return redirect('session_expiry')

    return render(request,
                  'session_expiry.html',
                  {'remaining_seconds':  request.session.get_expiry_age(),
                   'error_message': error_message})

def clear_session(request):
    request.session.pop('language', None)
    return redirect('home')

def flush_session(request):
    request.session.flush()
    return redirect('home')

def read_theme_cookie(request):
    return render(
        request,
        'read_theme.html',
        {
            'theme_value': request.COOKIES.get('theme'),
        }
    )

def set_theme_cookie(request):
    response = redirect('read_theme_cookie')
    response.set_cookie(
        key='theme',
        value='dark',
        expires=now() + timedelta(hours=1),
        secure= True, #send this only over https
        httponly=True,
    )
    return response

def read_signed_cookie(request):
    role_cookie = request.COOKIES.get('role','')
    signature_valid = False
    signer = Signer()
    try:
        verified_value = signer.unsign(role_cookie)
        signature_valid = True
    except (BadSignature, TypeError):
        verified_value = 'Invalid or missing signature'

    return render(
        request,
        'read_signed_cookie.html',
        {
            'signature_valid': signature_valid,
            'verified_value': verified_value,
        }
    )

def set_signed_cookie(request):
    signer = Signer()
    signed_value = signer.sign('user')
    response = redirect('read_signed_cookie')
    response.set_cookie(
        key='role',
        value=signed_value,
    )
    return response