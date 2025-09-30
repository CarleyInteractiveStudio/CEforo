from django import forms
from .models import Thread, Post

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'thread_type']
        labels = {
            'title': 'Título del Hilo',
            'thread_type': 'Tipo de publicación'
        }
        widgets = {
            'thread_type': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }

class MultipleFileInput(forms.FileInput):
    """
    Un widget personalizado que permite la subida de múltiples archivos.
    """
    allow_multiple_selected = True

class PostForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Añadir imágenes (hasta 4)'
    )

    class Meta:
        model = Post
        fields = ['content', 'post_type']
        labels = {
            'content': 'Tu mensaje',
            'post_type': 'Tipo de respuesta'
        }
        widgets = {
            'post_type': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }