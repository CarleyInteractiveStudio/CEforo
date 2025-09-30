from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Category, Thread, Post, PostImage
from .forms import ThreadForm, PostForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def home(request):
    recent_threads = Thread.objects.order_by('-created_at')[:15]
    context = {'recent_threads': recent_threads}
    return render(request, 'forum/home.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'category': category
    }
    return render(request, 'forum/category_detail.html', context)

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = thread.posts.order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        form = PostForm(request.POST, request.FILES)
        if thread.thread_type == 'DEBATE':
            form.fields.pop('post_type', None)

        if form.is_valid():
            images = request.FILES.getlist('images')
            if len(images) > 4:
                form.add_error('images', 'No puedes subir más de 4 imágenes.')
            else:
                post = form.save(commit=False)
                post.thread = thread
                post.created_by = request.user
                if thread.thread_type == 'DEBATE':
                    post.post_type = None
                post.save()

                for image in images:
                    PostImage.objects.create(post=post, image=image)

                return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = PostForm()
        if thread.thread_type == 'DEBATE':
            form.fields.pop('post_type', None)

    context = {
        'thread': thread,
        'posts': posts,
        'form': form
    }
    return render(request, 'forum/thread_detail.html', context)

@login_required
def create_thread(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST, request.FILES)

        post_form.fields.pop('post_type', None)

        if thread_form.is_valid() and post_form.is_valid():
            images = request.FILES.getlist('images')
            if len(images) > 4:
                post_form.add_error('images', 'No puedes subir más de 4 imágenes.')
            else:
                thread = thread_form.save(commit=False)
                thread.category = category
                thread.created_by = request.user
                thread.save()

                post = post_form.save(commit=False)
                post.thread = thread
                post.created_by = request.user
                post.post_type = None
                post.save()

                for image in images:
                    PostImage.objects.create(post=post, image=image)

                return redirect(thread.get_absolute_url())
    else:
        thread_form = ThreadForm()
        post_form = PostForm()
        post_form.fields.pop('post_type', None)

    context = {
        'category': category,
        'thread_form': thread_form,
        'post_form': post_form
    }
    return render(request, 'forum/create_thread.html', context)