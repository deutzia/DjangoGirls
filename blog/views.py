from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.date = timezone.now()
			comment.commented_post = post
			comment.save()
			comment.published=False
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	comments = Comment.objects.filter(commented_post=post, published=True)
	return render(request, 'blog/post_detail.html', {'post': post, 'commentform': form, 'comments': comments})

def new_post(request):
	if request.method == 'POST':
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

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post.author = request.user
			post.edited_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def accept_comments(request):
	if request.method == 'POST':
		print(request.POST)
		for key in request.POST:
			if key.startswith('comment'):
				comment = Comment.objects.get(pk=int(key.lstrip('comment')))
				comment.published = True
				comment.save()
		return redirect('post_list')
	new_comments = Comment.objects.filter(published=False).order_by('date')
	return render(request, 'blog/accept_comments.html', {'comments': new_comments})
