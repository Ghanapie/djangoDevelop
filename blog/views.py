from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import FormView, ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .models import Post

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

class PostDetail(TemplateView):
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=kwargs['pk'])
        return self.render_to_response(context)

# class PostDetail(DetailView):
#     template_name = 'blog/post_detail.html'
#     model = Post
#     context_object_name = 'post'

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         context['data'] = "1112"
#         return self.render_to_response(context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

class PostNew(FormView):
    form_class = PostForm
    success_url = reverse_lazy('post_new')
    template_name = 'blog/post_edit.html'

    def get_success_url(self, pk):
        return str(reverse_lazy('post_detail', kwargs={'pk': pk}))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        # post.published_date = timezone.now()
        post.save()
        return HttpResponseRedirect(self.get_success_url(post.pk))
    
class PostEdit(UpdateView):
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_detail', kwargs={'pk': 1})
    model = Post
    form_class = PostForm

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')