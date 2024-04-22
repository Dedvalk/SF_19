from django.contrib import admin
from .models import Post, Reply, OneTimeCode


from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class PostAdminForm(forms.ModelForm):

    content = forms.CharField(label="Содержание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(OneTimeCode)


