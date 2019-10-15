from django.contrib import admin
from django.apps import apps
from .models import *
# Register your models here.

admin.site.register(Lga)
admin.site.register(Agentname)
admin.site.register(AnnouncedLgaResults)
admin.site.register(AnnouncedPuResults)
admin.site.register(AnnouncedStateResults)
admin.site.register(AnnouncedWardResults)
admin.site.register(PollingUnit)
admin.site.register(Party)