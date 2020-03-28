"""
Django settings for tdxStock project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ

root = environ.Path(__file__) - 2  # two folder back (/a/b/c/ - 2 = /a/)
env = environ.Env(DEBUG=(bool, False), )
env.read_env(root('.env'))  # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=True)

SQL_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'option',
    'account',
    'wiki',
    'basedata',

    # Debug toolbar + extensions
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'django_filters',
    'corsheaders',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tdxStock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'option.context_processors.options_processor',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'tdxStock.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

_default_db_conf = env.db()
_default_db_conf.update({
    # Tell Django to build the test database with the 'utf8mb4' character set
    'TEST': {
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_unicode_ci',
    }
})

DATABASES = {
    'default': _default_db_conf,
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
public_root = root.path('public/')

MEDIA_ROOT = public_root('media')
MEDIA_URL = '/media/'

STATIC_ROOT = public_root('static')
STATIC_URL = '/static/'

# 配置静态文件搜索路径
STATICFILES_DIRS = (
    ('css', public_root('static/css')),
    ('js', public_root('static/js')),
    ('img', public_root('static/img')),
)

# 允许使用用户名或密码登录
AUTHENTICATION_BACKENDS = ['account.user_login_backend.EmailOrUsernameModelBackend']

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# 分页
PAGINATE_BY = 25

# Email:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True

EMAIL_HOST = env('MAIL_HOST', default='localhost')
EMAIL_PORT = env('MAIL_PORT', default=1025)
EMAIL_HOST_USER = env('MAIL_USERNAME', default='')
EMAIL_HOST_PASSWORD = env('MAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('MAIL_FROM', default='webmaster@tdxstock.com')
SERVER_EMAIL = env('MAIL_NAME', default='tdxStock')

# 设置 debug=false 未处理异常邮件通知
ADMINS = [('yang', 'wnh3yang@gmail.com')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'log_file'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(module)s] %(message)s',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': root('storage/logs/txdStock.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'txdStock': {
            'handlers': ['log_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

IDENTICON_FOREGROUND = ['#000000', '#0000CC', '#0099CC', '#33CC33', '#33FFFF', '#6666FF',
                        '#66FF00', '#CC33CC', '#FF0033', '#FF6666', '#FFFF66', '#99CC66']

SITE_NAME = 'TdxStock'
SITE_DESCRIPTION = '大巧无工,重剑无锋.'

# bootstrap颜色样式
BOOTSTRAP_COLOR_TYPES = [
    'default', 'primary', 'success', 'info', 'warning', 'danger'
]

# =============
# Debug Toolbar
# =============

INTERNAL_IPS = ['127.0.0.1', '::1']

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 10,
    'SEARCH_PARAM': 'q',  # default search
}

# 重点，设置信任站点
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1',
    'http://localhost',
    'http://127.0.0.1:8081',
    'http://localhost:8081',
)
CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作。
