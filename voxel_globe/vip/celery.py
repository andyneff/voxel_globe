from __future__ import absolute_import

import os
from os import environ as env

from celery import Celery

from django.conf import settings

#Thanks ask https://groups.google.com/forum/#!msg/celery-users/QTCf6T4QnUE/z7nvZUuS-NUJ
import logging
from celery import signals
@signals.worker_process_init.connect
def configure_pool_process_loglevel(**kwargs):
  logging.getLogger().setLevel(getattr(logging, 
                                       env['VIP_CELERY_WORKER_LOG_LEVEL']))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env['VIP_DJANGO_SETTINGS_MODULE'])
#Really set by common.bat...

try:
  import boxm2_register
  boxm2_register.smart_register = True
  #This need to me imported before other boxm2 because of how it's designed
  #This should take care of all boxm2 calls in Django and celery alike
except ImportError:
  print "Cannot load boxm2_register... This should ONLY happen when building"
  print "voxel_globe for the first time, and probably only during initialize"
  print "database. YOU SHOULD NOT BE SEEING THIS FREQUENTLY!!!"

#app = Celery('voxel_globe') #???
#app = Celery(env['VIP_CELERY_APP']);
app = Celery('voxel_globe.vip');

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
