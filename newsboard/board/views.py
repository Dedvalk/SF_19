import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView

from .forms import PostForm, ReplyForm
from .models import Post, Reply, OneTimeCode
from .filters import PostFilter


JUST_EMAIL = os.getenv('JUST_EMAIL')
JUST_ANOTHER_EMAIL = os.getenv('JUST_ANOTHER_EMAIL')
LOCAL_HOST = os.getenv('LOCALHOST')


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        queryset = Reply.objects.filter(post__author=self.request.user)
        context['filterset'] = PostFilter(self.request.GET, queryset, request=self.request.user)
        return context


class PostsList(ListView):

    model = Post
    ordering = '-creation_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context

class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):

        post = form.save(commit=False)
        post.author_id = self.request.user.pk
        post.save()
        response = super().form_valid(form)
        return response


class ReplyCreate(CreateView):

    form_class = ReplyForm
    model = Reply
    template_name = 'reply_create.html'

    def form_valid(self, form):

        reply = form.save(commit=False)
        reply.post = Post.objects.get(id=self.kwargs.get('pk'))
        reply.user = self.request.user
        reply.save()

        html_content = render_to_string('new_reply.html',
                                        {
                                            'post': reply.post,
                                            'url': f'{LOCAL_HOST}/newsboard/index',
                                            'author': reply.post.author,
                                            'user': reply.user,
                                            'content': reply.content
                                        })

        msg = EmailMultiAlternatives(
            subject=f'Отклик на ваше объявление {reply.post.title}',
            body='',
            from_email=JUST_ANOTHER_EMAIL,
            to=[reply.post.author.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response = super().form_valid(form)
        return response


class PostDelete(DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class ReplyDelete(DeleteView):

    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('home')

class ReplyAccept(DetailView):

    model = Reply
    template_name = 'reply_accept.html'
    context_object_name = 'reply_accept'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        reply = context['reply_accept']
        html_content = render_to_string('reply_acception.html',
                                        {
                                            'post': reply.post,
                                            'url': f'{LOCAL_HOST}/newsboard/index',
                                            'author': reply.post.author,
                                            'user': reply.user,
                                            'content': reply.content
                                        })

        msg = EmailMultiAlternatives(
            subject=f'Ваш отклик принят!',
            body='',
            from_email=JUST_ANOTHER_EMAIL,
            to=[reply.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return context


class ConfirmRegistrationView(CreateView):

    model = OneTimeCode
    context_object_name = 'confirm_registration'

    def post(self, request, *args, **kwargs):

        if 'code' in request.POST:
            code = OneTimeCode.objects.filter(code=request.POST['code'])
            if code.count() > 0:
                user = User.objects.filter(id=code[0].user_id)
                if user.exists:
                    user.update(is_active=True)
                    code.delete()
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('account_login')
