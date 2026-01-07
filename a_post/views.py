from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Tag
from .forms import PostCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug = tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    categories = Tag.objects.all()
    context = {
        'posts': posts,
        'categories':categories,   
        'tag':tag,
    }
    return render(request, 'a_post/home.html',context)

@login_required
def post_create_view(request):
    if request.method =='POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostCreateForm()
    context = {
        'form': form
    }   
    return render(request, 'a_post/post_create.html',context)

@login_required
def post_delete_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post delted successfully.')
        return redirect('home')
    context = {
        'post':post,
    }
    return render(request, 'a_post/post_delete.html', context)

@login_required
def post_edit_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostCreateForm(instance=post)
    context = {
        'post':post,
        'form':form,
    }
    return render(request, 'a_post/post_edit.html',context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    return render(request, 'a_post/post_page.html',{'post':post})