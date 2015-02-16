#! /usr/bin/env python
# -*- coding:utf8 -*-
from __future__ import unicode_literals


#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
BASEPATH = os.path.abspath(os.path.dirname(__file__))


#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Paris'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('fr', 'FranÃ§ais'),
    ('en', 'English'),
    ('es', 'Spanish'),
)
INSTALLED_APPS = (
    # django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project app
    'authentication',

    # lib / dependences
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_nested',
    'rest_framework_swagger',
    'django_extensions',
)


#==============================================================================
# SECRET KEY
#==============================================================================

SECRET_FILE = os.path.join(BASEPATH, 'secret.txt')

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from random import choice
        import string
        symbols = ''.join((string.ascii_lowercase,
                           string.digits,
                           string.punctuation))
        SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
        secret = open(SECRET_FILE, 'w')
        secret.write(SECRET_KEY)
        secret.close()
    except IOError:
        raise Exception('Please create a %s file with random characters '
                        'to generate your secret key!' % SECRET_FILE)


#==============================================================================
# Auth Backend
#==============================================================================


AUTHENTICATION_BACKENDS = (
    'authentication.auth_backend.EmailOrUsernameModelBackend',
)

#==============================================================================
# Middleware
#==============================================================================

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'authentication.Account'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

#==============================================================================
# Rest Framework
#==============================================================================

REST_FRAMEWORK = {


    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.YAMLRenderer',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.YAMLRenderer'
    )
}


#==============================================================================
# Project URLS and media settings
#==============================================================================

STATIC_URL = '/static/'

#==============================================================================
# Import local settings
#==============================================================================

from config.local_settings import *

