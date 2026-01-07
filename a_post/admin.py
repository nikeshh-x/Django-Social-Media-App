from django.contrib import admin
from .models import Post,Tag
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Post)

admin.site.register(Tag,TagAdmin)