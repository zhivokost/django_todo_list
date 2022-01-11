from django.contrib import admin
from .models import Todos


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('date_create',)

# Register your models here.
admin.site.register(Todos, TodoAdmin)
