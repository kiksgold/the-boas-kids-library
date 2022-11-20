from django.contrib import admin
from .models import Book, Review, BookInstance
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    # Admin Object for Book Model
    list_display = ('title', 'author', 'slug', 'uploaded_on')
    search_fields = ['title', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'author', 'uploaded_on')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Admin Object for Review Model
    list_display = ('name', 'body', 'book', 'uploaded_on')
    list_filter = ('book', 'uploaded_on')
    search_fields = ('name', 'email', 'body')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Admin Object for Book Instance Model
    list_filter = ('status', 'due_back')
    list_display = ('book', 'id', 'status', 'borrower', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )