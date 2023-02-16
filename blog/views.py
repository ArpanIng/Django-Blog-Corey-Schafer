from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Post


def home(request):
    posts = Post.objects.all()

    context = {
        "posts": posts,
    }
    return render(request, "blog/home.html", context)


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5
    template_name = "blog/home.html"  # or <app_name>/<model>_<viewtype>.html


class UserPostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/user_posts.html"  # or <app_name>/<model>_<viewtype>.html

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.order_by("-date_posted").filter(author=user)


class PostDetailView(generic.DetailView):
    """Individual detail of PostListView"""

    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    context_object_name = "post"
    success_url = "blog:blog-home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {
        "title": "About",
    }
    return render(request, "about.html", context)
