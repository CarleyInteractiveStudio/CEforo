from .models import Category

def categories_processor(request):
    """
    Este procesador de contexto hace que la lista de todas las categorías
    esté disponible en todas las plantillas.
    """
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}