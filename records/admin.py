from django.contrib import admin
from .models import Record
# Register your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')  # Display relevant fields in the list view
    search_fields = ('first_name', 'last_name', 'email')  # Allow searching by first name, last name, and email
    list_filter = ('created_at', 'city', 'state')  # Filter records by creation date, city, and state
    ordering = ('-created_at',)  # Order records by created date in descending order

admin.site.register(Record, RecordAdmin)