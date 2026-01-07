from django import forms
from django.forms import ModelForm
from .models import Post

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created_at']
        labels = {
            'title': 'Title',
            'image': 'Image URL',
            'body': 'Caption',
            'tags': 'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write your caption here...',
            'class': 'font1 text-4xl'
        }),
            'tags': forms.CheckboxSelectMultiple(),
    }