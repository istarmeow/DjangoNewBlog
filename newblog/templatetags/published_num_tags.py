from django import template

register = template.Library()

from ..models import Article


@register.simple_tag
def total_post_num(category_id):
    return Article.objects.filter(status='p', category__id=category_id).count()


@register.simple_tag
def year_mont_post_num(year, month):
    return Article.objects.filter(status='p', publish_time__year=year, publish_time__month=month).count()