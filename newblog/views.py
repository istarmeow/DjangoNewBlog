from django.shortcuts import render
from .models import Tag, Category, Article
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings
from django.db.models.aggregates import Count


# categories = Category.objects.all()  # 获取全部的分类对象
categories = Category.objects.annotate(num_posts=Count('articles')).all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
year_months = Article.objects.datetimes('publish_time', 'month', order='DESC')


def home(request):
    posts = Article.objects.filter(status='p')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每一页显示博客数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, 'year_months': year_months})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        next_post = post.next_article()  # 下一篇文章
        prev_post = post.prev_article()  # 上一篇文章
    except Article.DoseNotExist:
        raise Http404
    return render(request, 'post.html',
                  {
                      'post': post,
                      'tags': tags,
                      'category_list': categories,
                      'next_post': next_post,
                      'prev_post': prev_post,
                      'year_months': year_months
                  })


def search_category(request, id):  # 按照分类搜索
    posts = Article.objects.filter(category__id=str(id), status='p')
    category = Category.objects.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每一页显示博客数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'post_list': post_list, 'category_list': categories, 'category': category, 'year_months': year_months})


def search_tag(request, tag):  # 按照标签搜索
    posts = Article.objects.filter(tags__name__contains=str(tag), status='p')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每一页显示博客数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'tag.html', {'post_list': post_list, 'category_list': categories, 'tag': tag, 'year_months': year_months})


def archive(request, year, month):  # 按照月份归档
    posts = Article.objects.filter(publish_time__year=year, publish_time__month=month, status='p').order_by('-publish_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每一页显示博客数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'archive.html',
                  {
                      'post_list': post_list,
                      'category_list': categories,
                      'year_month': year + '年' + month + '月',
                      'year_months': year_months
                  })