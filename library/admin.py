from django.contrib import admin
from .models import Book
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Book)
