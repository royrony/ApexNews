from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.models import AbstractUser
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    fields = ('user', 'title', 'category', 'pic', 'content', 'tags', 'date_created', 'moderated')
    list_display = ('title', 'content', 'date_created', 'moderated')
    list_filter = ('moderated', 'date_created')
    search_fields = ('title', 'content')  

class StaffAdmin(admin.ModelAdmin):
	list_display = ('user', 'verified')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Staff, StaffAdmin)


