from django.db import models

# Create your models here.
class Post(models.Model):
    body_text = models.TextField('Texto Principal')
    pub_date = models.DateTimeField('Data Publicação')
    categoria = models.CharField(
        'Categoria',
        max_length=15,
        choices=[
            ('noticias', 'Notícias'),
            ('como_fazer', 'Como Fazer'),
            ('review', 'Review'),
        ],
        default=None,
        null=True
    )

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): # herda o model User base padrão do Django
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)
    cpf = models.CharField("CPF", max_length=11, null=True, blank=True)