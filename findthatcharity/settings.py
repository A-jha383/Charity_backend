"""
Django settings for findthatcharity project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import dj_database_url
import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()


if os.environ.get("SENTRY_DSN"):
    environment = "production"
    if os.environ.get("DEBUG", "true").lower().startswith("t"):
        environment = "development"
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        environment=environment,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.05,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = "Find that Charity"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "true").lower().startswith("t")

ALLOWED_HOSTS = (
    os.environ.get("ALLOWED_HOSTS").split(";")
    if os.environ.get("ALLOWED_HOSTS")
    else []
)

GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS")

# Application definition

INSTALLED_APPS = [
    "ftc.apps.FtcConfig",
    "charity.apps.CharityConfig",
    "reconcile.apps.ReconcileConfig",
    "addtocsv.apps.AddtocsvConfig",
    "geo.apps.GeoConfig",
    "other_data.apps.OtherDataConfig",
    "api.apps.ApiConfig",
    "django_elasticsearch_dsl",
    "django.contrib.postgres",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "prettyjson",
    "django_better_admin_arrayfield",
    "django_filters",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "findthatcharity.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [(os.path.join(BASE_DIR, "jinja2"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "findthatcharity.jinja2.environment",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "findthatcharity.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(),
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Caching in database

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "findthatcharity_cache",
    }
}

# Elasticsearch

ELASTICSEARCH_DSL = {
    "default": {"hosts": os.environ.get("ELASTICSEARCH_URL")},
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} [{name}] {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

CORS_ALLOW_ALL_ORIGINS = True

IGNORE_DOMAINS = (
    "gmail.com",
    "hotmail.com",
    "btinternet.com",
    "hotmail.co.uk",
    "yahoo.co.uk",
    "outlook.com",
    "aol.com",
    "btconnect.com",
    "yahoo.com",
    "googlemail.com",
    "ntlworld.com",
    "talktalk.net",
    "sky.com",
    "live.co.uk",
    "ntlworld.com",
    "tiscali.co.uk",
    "icloud.com",
    "btopenworld.com",
    "blueyonder.co.uk",
    "virginmedia.com",
    "nhs.net",
    "me.com",
    "msn.com",
    "talk21.com",
    "aol.co.uk",
    "mail.com",
    "live.com",
    "virgin.net",
    "ymail.com",
    "mac.com",
    "waitrose.com",
    "gmail.co.uk",
)
