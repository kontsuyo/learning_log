from django.contrib import admin

from learning_logs.models import Entry
from learning_logs.models import Topic

admin.site.register(Topic)
admin.site.register(Entry)
