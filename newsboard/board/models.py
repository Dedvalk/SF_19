from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from ckeditor.fields import RichTextField
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

CATEGORIES = (
    ('tanks', 'Танки'),
    ('heals', 'Хилы'),
    ('DD', 'ДД'),
    ('dealers', 'Торговцы'),
    ('guildmasters', 'Гилдмастеры'),
    ('questgivers', 'Квестгиверы'),
    ('smiths', 'Кузнецы'),
    ('tanners', 'Кожевники'),
    ('potionmakers', 'Зельевары'),
    ('spellmasters', 'Мастера заклинаний')
)


class Post(models.Model):

    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, verbose_name='Категория')


    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reply', verbose_name='Объявление')
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('posts')


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class OneTimeCode(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(default=timezone.localtime(timezone.now()) + timedelta(minutes=1))

    def __str__(self):
        return f'{self.code}'