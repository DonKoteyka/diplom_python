import os
import time

from celery import Celery, shared_task
from celery.result import AsyncResult
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_pd_diplom.settings')

app = Celery('netology_pd_diplom')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task()
# @shared_task(serializer="pickle")
def debud_celery():
    time.sleep(5)
    print('I am working')