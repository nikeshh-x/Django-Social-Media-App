from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, CommentCreateForm, ReplyCreateForm
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
    commentForm = CommentCreateForm()
    replyForm = ReplyCreateForm()
    context = {
        'post':post,
        'commentForm':commentForm,
        'replyForm':replyForm,
    }
    return render(request, 'a_post/post_page.html',context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    return redirect('post',post.id)

@login_required
def comment_delete_view(request,pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Comment delted successfully.')
        return redirect('post', post.parent_post.id)
    context = {
        'comment':post,
    }
    return render(request, 'a_post/comment_delete.html', context)

def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
    return redirect('post',comment.parent_post.id)

@login_required
def reply_delete_view(request,pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply delted successfully.')
        return redirect('post', reply.parent_comment.parent_post.id)
    context = {
        'reply':reply,
    }
    return render(request, 'a_post/reply_delete.html', context)

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.author != request.user:
        post.likes.add(request.user)
        return redirect('post', post.id)
