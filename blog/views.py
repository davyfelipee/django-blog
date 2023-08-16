from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from blog.models import Post # Acrescentar

def index(request):
    # return HttpResponse('Olá Django - index')
    return render(request, 'index.html', {'titulo': 'Últimos Artigos'})

def ola(request): # Modificar
    # return HttpResponse('Olá django')
    posts = Post.objects.all() # recupera todos os posts do banco de dados
    context = {'posts_list': posts } # cria um dicionário com os dado
    return render(request, 'posts.html', context) # renderiza o template e passa o contexto