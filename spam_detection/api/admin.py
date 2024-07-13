from django.contrib import admin
from .models import Contact, UserContactMap, UserProfile

admin.site.register(Contact) 
admin.site.register(UserProfile)
admin.site.register(UserContactMap)
