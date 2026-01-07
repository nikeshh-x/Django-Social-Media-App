from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=500)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts') 
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.FileField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.name