from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Thread(models.Model):
    THREAD_TYPE_CHOICES = [
        ('DEBATE', 'Debate'),
        ('AYUDA', 'Petición de Ayuda'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    thread_type = models.CharField(
        max_length=10,
        choices=THREAD_TYPE_CHOICES,
        default='DEBATE'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_detail', kwargs={'thread_id': self.pk})

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('DEBATE', 'Debatir'),
        ('SOLUCION', 'Ofrecer Solución'),
        ('PROBLEMA', 'Tengo el mismo problema'),
    ]

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    content = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        blank=True, # El campo es opcional
        null=True
    )

    def __str__(self):
        return f"Post by {self.created_by.username} in {self.thread.title}"

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for post {self.post.id}"