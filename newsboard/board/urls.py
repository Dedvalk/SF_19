from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from .views import PostsList, PostDetail, IndexView, PostCreate, ReplyCreate, PostDelete, ReplyAccept, \
   ReplyDelete, ConfirmRegistrationView

urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('index/', IndexView.as_view(), name='home'),
   path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('post/create', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/reply', ReplyCreate.as_view(), name='post_reply'),
   path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('reply/<int:pk>/delete', ReplyDelete.as_view(), name='reply_delete'),
   path('reply/<int:pk>/accept', ReplyAccept.as_view(), name='reply_accept'),
   path('confirm/', ConfirmRegistrationView.as_view(), name='confirm_registration')

]
