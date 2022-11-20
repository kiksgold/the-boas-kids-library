from django.contrib import admin
from .models import Book
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'slug', 'uploaded_on')
    search_fields = ['title', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'author', 'uploaded_on')
