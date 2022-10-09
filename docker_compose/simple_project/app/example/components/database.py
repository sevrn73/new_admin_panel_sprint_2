import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
        'OPTIONS': {'options': '-c search_path=public,content'},
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
