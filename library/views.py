from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from django.http import HttpResponseRedirect
from .forms import ReviewForm


# Create your views here.

from .models import Book, BookInstance


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_visits': num_visits},
    )


class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.all().order_by('-uploaded_on')
    template_name = 'index.html'
    paginate_by = 6


class BookDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Book.objects.filter()
        book = get_object_or_404(queryset, slug=slug)
        reviews = book.reviews.filter(approved=True).order_by('uploaded_on')
        liked = False
        if book.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "reviews": reviews,
                "reviewed": False,
                "liked": liked,
                "review_form": ReviewForm,
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Book.objects.filter()
        book = get_object_or_404(queryset, slug=slug)
        reviews = book.reviews.filter().order_by("-uploaded_on")
        liked = False
        if book.likes.filter(id=self.request.user.id).exists():
            liked = True

        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review = review_form.save(commit=False)
            review.book = book
            review.save()
        else:
            review_form = ReviewForm()

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "reviews": reviews,
                "reviewed": True,
                "review_form": review_form,
                "liked": liked
            },
        )


class BookLike(View): 
    def post(self, request, slug, *args, **kwargs):
        book = get_object_or_404(Book, slug=slug)
        if book.likes.filter(id=request.user.id).exists():
            book.likes.remove(request.user)
        else:
            book.likes.add(request.user)

        return HttpResponseRedirect(reverse('book_detail', args=[slug]))
