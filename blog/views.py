from django.shortcuts import render,  get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic import DetailView, ListView, TemplateView
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from blog.models import Post # Acrescentar
from django.template.loader import render_to_string
from django.core.mail import send_email
from django.conf import settings

def index(request):
    # return HttpResponse('Olá Django - index')
    return render(request, 'index.html', {'titulo': 'Últimos Artigos'})
def ola(request): # Modificar
    # return HttpResponse('Olá django')
    posts = Post.objects.all() # recupera todos os posts do banco de dados
    context = {'posts_list': posts } # cria um dicionário com os dado
    return render(request, 'posts.html', context) # renderiza o template e passa o contexto
def post_show(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/detail.html', {'post': post})
class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'
def get_all_posts(request):
    posts = list(Post.objects.values('pk', 'body_text', 'pub_date'))
    data = {'success': True, 'posts': posts}
    json_data = json.dumps(data, indent=1, cls=DjangoJSONEncoder)
    response = HttpResponse(json_data, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*' # requisição de qualquer origem
    return response
def get_post(request, post_id):
    post = Post.objects.filter(
        pk=post_id
    ).values(
        'pk', 'body_text', 'pub_date'
    ).first()
    data = {'success': True, 'post': post}
    status = 200
    if post is None:
        data = {'success': False, 'error': 'Post ID não existe.'}
        status=404
    response = HttpResponse(
        json.dumps(data, indent=1, cls=DjangoJSONEncoder),
        content_type="application/json",
        status=status
    )
    response['Access-Control-Allow-Origin'] = '*' # requisição de qualquer origem
    return response
class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ('body_text', )
    success_url = reverse_lazy('posts_list')
    # success_url = reverse_lazy('posts_list')
    success_url = reverse_lazy('posts_all') # modifiquei para ir direto no template da aula do dia 20/09

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        body_text = data.get('body_text')
        if body_text is None:
            data = {'success': False, 'error': 'Texto do post inválido.'}
            status = 400 # Bad Request => erro do client
        else:
            post = Post(body_text=body_text)
            post.save()
            post_data = Post.objects.filter(
                pk=post.id
            ).values(
                'pk', 'body_text', 'pub_date'
            ).first()
        data = {'success': True, 'post': post_data}
        status = 201 # Created
    response = HttpResponse(
        json.dumps(data, indent=1, cls=DjangoJSONEncoder),
        content_type="application/json",
        status=status
    )

    response['Access-Control-Allow-Origin'] = '*'

    return response
    return response

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'

class SobreTemplateView(TemplateView):
    template_name = 'post/sobre.html'

    return super(PostDeleteView, self).form_valid(form)



def post_send(request, post_id):
    post = get_object_or_404 (Post, pk-post_id)
    post_url = reverse_lazy('post_detail', args=[post_id])
    try:
        email = request.POST.get('email')
        if len(email) < 5:
            raise ValueError('E-mail inválido')

    link = f'{request._current_scheme_host}{post_url}'
    template = "post/post_send"
    text_message = render_to_string(f"{template}.txt", {'post_link': link})
    html_message = render_to_string(f"{template}.html", {'post_link': link})
    send_mail(
        subject="Este assunto pode te interessar!", 
        message=text_message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[email],
        html_message=html_message,
        )
        messages, success(
            request, 'Postagem compartilhada com sucesso."
        )
    except ValueError as error:
        messages.error(request, error)
    except:
        messages.error(
            request, 'Erro ao enviar a mensagem
        )

    return redirect(post_url)