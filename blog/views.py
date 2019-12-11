from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
#     return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect

class PostNew(FormView):
    form_class = PostForm
    success_url = reverse_lazy('post_new')
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        self.success_url = reverse_lazy('post_detail', kwargs={'pk': post.pk})
        return HttpResponseRedirect(self.get_success_url())


class PostList(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
#     return render(request, 'blog/post_list.html', {'posts': posts})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})