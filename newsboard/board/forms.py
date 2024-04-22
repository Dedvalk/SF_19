import os
import random
from string import hexdigits

from ckeditor.fields import RichTextFormField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.core.mail import send_mail

from .models import Post, Reply, OneTimeCode


JUST_ANOTHER_EMAIL = os.getenv('JUST_ANOTHER_EMAIL')


class PostForm(forms.ModelForm):

    content = forms.CharField(label='Содержание', widget=CKEditorUploadingWidget())

    class Meta:
       model = Post
       fields = [
           'title',
           'category',
           'content'

       ]


class ReplyForm(forms.ModelForm):

    content = forms.CharField()
    class Meta:
       model = Reply
       fields = [
           'content'
       ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        return cleaned_data


class CustomSignupForm(SignupForm):

    def save(self, request):

        user = super(CustomSignupForm, self).save(request)
        user.is_active = False
        one_time_code = OneTimeCode.objects.create(user=user, code=''.join(random.sample(hexdigits, 8)))
        user.save()
        send_mail(
            subject='Код активации',
            message=f'Код активации для пользователя {user}: {one_time_code}',
            from_email=JUST_ANOTHER_EMAIL,
            recipient_list=[user.email],
        )
        return user
