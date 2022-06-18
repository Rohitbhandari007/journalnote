from turtle import title
from warnings import filters
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Journal, Post
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import OrderFilter
from django.contrib import messages


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'core/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_created']


class CreatePost(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'details']

    # This method will get the user and make it author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = '/'
    template_name = 'core/journal_form.html'


class PostDetails(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'core/journal_detail.html'
    context_object_name = 'post'


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

    posts = Post.objects.all()
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
