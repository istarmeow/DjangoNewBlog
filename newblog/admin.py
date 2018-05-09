from django.contrib import admin
from .models import Tag, Category, Article
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Tag)
admin.site.register(Category)


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # 给content字段添加富文本


admin.site.register(Article, ArticleAdmin)