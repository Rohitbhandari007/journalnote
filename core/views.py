from django.http import Http404
from django.views import View
from django.views.generic.edit import CreateView
from .models import Journal, Post
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import OrderFilter


# class PostListView(LoginRequiredMixin, ListView):
#     model = Post
#     template_name = 'core/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_created']

class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = request.user.my_post.all()
        context = {"posts": posts}
        return render(request, 'core/home.html', context)


class CreatePost(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'details']

    # This method will get the user and make it author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = '/'
    template_name = 'core/journal_form.html'


class PostDetails(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.author == request.user:
            context = {"post": post, "id": id}
            return render(request, 'core/journal_detail.html', context)
        else:
            raise Http404


def register(request):
    if request.method == "GET":
        return render(
            request, "core/register.html",
            {"form": CustomUserCreationForm}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('User Created')

            login(request, user)
            return redirect(reverse("home"))


def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.all().filter(title=search)
        return render(request, 'core/search_results.html', {'post': post, 'search': search})


def adsearch(request):

    posts = Post.objects.filter(author=request.user)
    filters = OrderFilter(request.GET, queryset=posts)
    posts = filters.qs
    title = request.GET.get('title')
    startdate = request.GET.get('start_date')
    enddate = request.GET.get('end_date')

    context = {
        'posts': posts,
        'filters': filters,
        'title': title,
        'startdate': startdate,
        'enddate': enddate
    }

    return render(request, 'core/adsearch.html', context)
