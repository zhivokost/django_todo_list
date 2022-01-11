from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todos(models.Model):
    title = models.CharField(max_length = 150)
    memo = models.TextField(blank = True)
    important = models.BooleanField(default = False)
    date_create = models.DateTimeField(auto_now_add = True)
    date_complete = models.DateTimeField(null = True, blank = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)


    def __str__(self):
        return self.title
