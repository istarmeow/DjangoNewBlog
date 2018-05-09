# DjangoNewBlog
Django写的博客
# Django【学习】个人博客
# --------------------------
# 环境包
```python
pip install django==2.0.5
pip install django-summernote
pip install django-jet
```
# 博客基础功能
开发一个包含如下功能的博客系统：

* 后台文章管理，包括新增、删除和编辑
* 后台分类管理，包括新增、删除和编辑
* 后台标签管理，包括新增、删除和编辑
* 前台列表页展示文章概要信息、发布时间、文章分类、标签、浏览次数
* 前台文章列表页分页展示
* 前台文章列表页点击”阅读全文”显示文章详细内容
* 前台文章详情页每刷新一次浏览次数+1

## 创建环境
```python
C:\Users\Home\OneDrive\PycharmProjects>pip install virtualenv
C:\Users\Home\OneDrive\PycharmProjects>mkdir DjangoNewBlog

C:\Users\Home\OneDrive\PycharmProjects>cd DjangoNewBlog
C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>virtualenv.exe BlogVenv
C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>python -m venv BlogVenv  # python3建议使用
C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>BlogVenv\Scripts\activate

C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>pip list  # 虚拟环境路径变了就不能使用，需要重新创建虚拟环境
Package    Version
---------- -------
pip        10.0.1
setuptools 39.0.1

(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>pip install django
# 创建项目
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>django-admin startproject DjangoNewBlog
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog>cd DjangoNewBlog
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>django-admin startapp newblog

# 创建其他文件夹
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>mkdir static

(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>mkdir templates

(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>mkdir media
```

目录结构
```
C:.
│  db.sqlite3
│  manage.py
│
├─DjangoNewBlog
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │
│  └─__pycache__
│
└─newblog
    │  admin.py
    │  apps.py
    │  models.py
    │  tests.py
    │  views.py
    │  __init__.py
    │
    ├─media
    ├─migrations
    │  │
    │  └─__pycache__
    │
    ├─static
    │  ├─css
    │  │      blog.css
    │  │      font-awesome.min.css
    │  │      grids-responsive-min.css
    │  │      pure-min.css
    │  │
    │  ├─fonts
    │  │      fontawesome-webfont.eot
    │  │      fontawesome-webfont.svg
    │  │      fontawesome-webfont.ttf
    │  │      fontawesome-webfont.woff
    │  │      fontawesome-webfont.woff2
    │  │      FontAwesome.otf
    │  │
    │  ├─image
    │  │      avatar.png
    │  │
    │  └─js
    │          jquery-3.3.1.min.js
    │
    ├─templates
    │
    └─__pycache__
```

### 注册app，修改setting
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'newblog',
]


# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Chongqing'



STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


PAGE_NUM = 3  # 每页显示3篇文章
```

### 应用显示中文
修改newblog应用下 的apps.py
```python
from django.apps import AppConfig


class NewblogConfig(AppConfig):
    name = 'newblog'
    verbose_name = 'LR@个人博客'
```

修改newblog应用下的__init__.py
```python
default_app_config = 'newblog.apps.NewblogConfig'
```

## 创建模型Models
创建模型
```python
from django.db import models
from django.utils.timezone import now


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='标签名称')
    created_time = models.DateTimeField(default=now, verbose_name='创建时间')
    updated_time = models.DateTimeField(default=now, verbose_name='修改时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = '标签名称'  # 后台显示模型名称
        verbose_name_plural = '标签列表'
        db_table = 'tag'  # 数据库表名


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='分类名称')
    created_time = models.DateTimeField(default=now, verbose_name='创建时间')
    updated_time = models.DateTimeField(default=now, verbose_name='修改时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = '分类名称'
        verbose_name_plural = '分类列表'
        db_table = 'category'


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(blank=True, null=True, verbose_name='正文')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p', verbose_name='状态')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    publish_time = models.DateTimeField(blank=True, null=True, default=now, verbose_name='发布时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, verbose_name='所属分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签集合')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time', ]  # 按照发布时间降序，旧的时间在前，也就是新发布的博客放在后面
        verbose_name = '文章'
        verbose_name_plural = '文章列表'
        db_table = 'article'
        get_latest_by = 'created_time'

    def viewed(self):
        """
        更新浏览量
        """
        self.views += 1
        self.save(update_fields=['views'])

    def next_article(self):
        """
        显示下一篇，下一篇的id比当前id大，状态为已发布，发布时间不为空
        :return:
        """
        return Article.objects.filter(id__gt=self.id, status='p', publish_time__isnull=False).last()

    def prev_article(self):
        """
        显示前一篇，前一篇的id比当前id小，状态为已发布，发布时间不为空
        :return:
        """
        return Article.objects.filter(id__lt=self.id, status='p', publish_time__isnull=False).first()

    """
    分析上一篇，下一篇：存入文章，id增大，按照发布时间降序，新的时间在前面：另外应该比较发布时间可能靠谱些，要考虑文章创建好后，晚发布的情况
    id     发布时间
    6       11:00
    4       10:30
    5       10:10（下一篇文章：id比当前id大，排在最后）
    3       10:00（假如当前是这篇文章）
    2       9:20（上一篇文章：id比当前id小，排在最前）
    1       9:00    
    """
```

迁移同步数据库
```
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py makemigrations
Migrations for 'newblog':
  newblog\migrations\0001_initial.py
    - Create model Article
    - Create model Category
    - Create model Tag
    - Add field category to article
    - Add field tags to article

(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py migrate
```

## 后台管理
### 创建管理员
```
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py createsuperuser
Username (leave blank to use 'home'): admin
Email address: admin@admin.com
Password:djangoadmin
Password (again):djagngoadmin
Superuser created successfully.
```

### 注册模型
```python
from django.contrib import admin
from .models import Tag, Category, Article


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article)
```

### 启动服务器测试
```
(BlogVenv) C:\Users\Home\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py runserver
```

在后台添加一些内容。

## 创建视图Views
编辑newblog/views.py
### 博客列表视图 home(request)
```python
from django.shortcuts import render
from .models import Tag, Category, Article
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings


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
    return render(request, 'home.html', {'post_list': post_list})
```

### 博客详情视图 detail(request, id)
```python
def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        tags = post.tags.all()  # 获取文章的所有标签
    except Article.DoseNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post, 'tags': tags})
```

## 配置路由URLs
为不同的URL配置相应的视图函数

```python
from django.contrib import admin
from django.urls import path
from newblog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail')
]
```

## 创建模板Templates
提前准备好静态文件：样式文件和字体文件
### 基础模板 base.html
```html
<!DOCTYPE html>
{% load static %}
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} LR@ Blog {% endblock %}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'css/pure-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/grids-responsive-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/blog.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/font-awesome.min.css' %}"/>
</head>
<body>
<div id="layout" class="pure-g">
    <div class="sidebar pure-u-1 pure-u-md-1-4">
        <div class="header">
            <h1 class="brand-title"><a href="{% url 'home' %}">LR@MS博客</a></h1>
            <h2 class="brand-tagline">NewStarting</h2>
            <nav class="nav">
                <ul class="nav-list">
                    <li class="nav-item">
                        <a class="pure-button" href="#">Github</a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
    <div class="content pure-u-1 pure-u-md-3-4">
        <div>
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>
</body>
</html>
```

### 主页模板 home.html
```html
{% extends 'base.html' %}

{% block content %}
    <div>
        {% for post in post_list %}
            <section class="post">
                <header class="post-header">
                    <h2 class="post_title">
                        <a href="{% url 'detail' post.id %}">{{ post.title }}
                        </a>
                    </h2>
                    <p class="post-meta">
                        发布时间：
                        <a class="post-author" href="#">{{ post.publish_time|date:'Y/m/d' }}</a>
                        &nbsp;&nbsp;
                        分类：
                        <a class="post-category post-category-pure" href="#">{{ post.category }}</a>
                        &nbsp;&nbsp;
                        标签：
                        {% for tag in post.tags.all %}
                            <a class="post-category post-category-pure" href="#">{{ tag }}</a>
                        {% endfor %}
                        &nbsp;&nbsp;
                        浏览次数：
                        {{ post.views }}
                    </p>
                </header>

                <div class="post-description">
                    <p>
                        <!--截取100个字符显示-->
                        {{ post.content|truncatewords_html:100 }}
                    </p>
                </div>

                <div><a class="post-category post-category-design" href="{% url 'detail' post.id %}">阅读全文</a></div>
            </section>
        {% endfor %}
    </div>

    <!--分页显示-->
    <div>
        {% if post_list.object_list and post_list.paginator.num_pages > 1 %}
            <div>
                {% if post_list.has_previous %}
                    <a class="footer" href="?page={{ post_list.previous_page_number }}">
                        <i class="fa fa-angle-left"></i>上一页
                    </a>
                {% endif %}

                {% if post_list.has_next %}

                    <a class="footer" href="?page={{ post_list.next_page_number }}">
                        下一页<i class="fa fa-angle-right"></i>
                    </a>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
```

### 详情模板 post.html
```html
{% extends 'base.html' %}

{% block content %}
    <div>
        <section class="post">
            <header class="post-header">
                <h2 class="post-title">{{ post.title }}</h2>

                <p class="post-meta">
                    发布时间：
                    {{ post.publish_time|date:'Y/m/d H:m:s' }}
                    &nbsp&nbsp
                    分类：
                    <a class="post-category post-category-pure" href="#">{{ post.category }}</a>
                    &nbsp&nbsp
                    标签：
                    {% for tag in post.tags.all %}
                        <a class="post-category post-category-pure" href="#">{{ tag }}</a>
                    {% endfor %}
                    &nbsp;&nbsp;
                    浏览次数：
                    {{ post.views }}
                </p>
            </header>
            <div class="post-description">
                <p>
                    {{ post.content }}
                </p>
            </div>
        </section>
    </div>
{% endblock %}
```

![博客主页](_v_images/_博客主页_1525748481_28955.png)

![博客详情](_v_images/_博客详情_1525748502_12049.png)

# 博客富文本支持
对博客系统进行优化，主要包括:

* 后台发文时正文内容由纯文本输入框改为富文本输入框
* 主页文章列表页显示文章摘要时过滤html标签

## 后台输入框富文本
### 库安装
富文本输入框的实现本文依赖`django-summernote`这个库来实现，首先安装
```python
(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>pip install django-summernote
```

### 添加django_summernote到应用列表
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_summernote',

    'newblog',
]
```

### 迁移同步数据库
执行migrate命令使附件模型生效
```
(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, django_summernote, newblog, sessions
Running migrations:
  Applying django_summernote.0001_initial... OK
  Applying django_summernote.0002_update-help_text... OK
```

需要重启服务器

### settings中添加media支持
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

### 添加到路由URLs
```python
from django.contrib import admin
from django.urls import path
from newblog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### admin添加富文本编辑器
修改admin.py，为Article模型中正文字段添加富文本编辑器

![添加富文本前文章编辑](_v_images/_添加富文本前文章编辑_1525749597_14717.png)

```python
from django.contrib import admin
from .models import Tag, Category, Article
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Tag)
admin.site.register(Category)


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # 给content字段添加富文本


admin.site.register(Article, ArticleAdmin)
```

![后台已添加富文本支持](_v_images/_后台已添加富文本支持_1525750401_16676.png)

至此，登录后台发文时正文输入框已经是富文本输入框了。

## 文章过滤富文本标签
![文章中的html标签](_v_images/_文章中的html标签_1525750522_29035.png)

### home.html过滤html标签
主页文章列表页显示文章摘要时过滤html标签。

修改页面文件home.html

```html
{% extends 'base.html' %}

{% block content %}
    <div>
        {% for post in post_list %}
            <section class="post">
                <header class="post-header">
                    <h2 class="post_title">
                        <a href="{% url 'detail' post.id %}">{{ post.title }}
                        </a>
                    </h2>
                    <p class="post-meta">
                        发布时间：
                        <a class="post-author" href="#">{{ post.publish_time|date:'Y/m/d' }}</a>
                        &nbsp;&nbsp;
                        分类：
                        <a class="post-category post-category-pure" href="#">{{ post.category }}</a>
                        &nbsp;&nbsp;
                        标签：
                        {% for tag in post.tags.all %}
                            <a class="post-category post-category-pure" href="#">{{ tag }}</a>
                        {% endfor %}
                        &nbsp;&nbsp;
                        浏览次数：
                        {{ post.views }}
                    </p>
                </header>

                <div class="post-description">
                    <p>
                        <!--truncatewords_html:100截取100个字符显示-->
                        <!--{{ post.content|truncatewords_html:100 }}-->
                        {#striptags用于过滤正文中所有的HTML标签#}
                        {{ post.content|striptags|truncatewords_html:100 }}
                    </p>
                </div>

                <div><a class="post-category post-category-design" href="{% url 'detail' post.id %}">阅读全文</a></div>
            </section>
        {% endfor %}
    </div>

    <!--分页显示-->
    <div>
        {% if post_list.object_list and post_list.paginator.num_pages > 1 %}
            <div>
                {% if post_list.has_previous %}
                    <a class="footer" href="?page={{ post_list.previous_page_number }}">
                        <i class="fa fa-angle-left"></i>上一页
                    </a>
                {% endif %}

                {% if post_list.has_next %}

                    <a class="footer" href="?page={{ post_list.next_page_number }}">
                        下一页<i class="fa fa-angle-right"></i>
                    </a>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
```

![主页过滤html标签结果](_v_images/_主页过滤html标签_1525750745_12372.png)

`{#striptags用于过滤正文中所有的HTML标签#}`也可以作为注释使用

代码中的`striptags`、`truncatechars`均为Django内置的filter，更多filter信息可以参考: https://docs.djangoproject.com/en/2.0/ref/templates/builtins/

### post.html过滤html标签
```html
{% extends 'base.html' %}

{% block content %}
    <div>
        <section class="post">
            <header class="post-header">
                <h2 class="post-title">{{ post.title }}</h2>

                <p class="post-meta">
                    发布时间：
                    {{ post.publish_time|date:'Y/m/d H:m:s' }}
                    &nbsp&nbsp
                    分类：
                    <a class="post-category post-category-pure" href="#">{{ post.category }}</a>
                    &nbsp&nbsp
                    标签：
                    {% for tag in post.tags.all %}
                        <a class="post-category post-category-pure" href="#">{{ tag }}</a>
                    {% endfor %}
                    &nbsp;&nbsp;
                    浏览次数：
                    {{ post.views }}
                </p>
            </header>
            <div class="post-description">
                <p>
                    {# 富文本过滤html标签，之后显示富文本语言 #}
                    {{ post.content|striptags }}
                </p>
            </div>
        </section>
    </div>
{% endblock %}
```

![详情页过滤html标签](_v_images/_详情页过滤html标_1525751118_7760.png)

# 后台admin页面美化
对博客系统进行优化，主要包括:

* 后台admin页面美化
* 富文本输入框配置优化

配置文件里，这里主要添加了分页参数`PAGE_NUM`，设置单页显示多少篇文章，还有就是添加了后台自定义菜单`JET_SIDE_MENU_ITEMS`参数，这个参数的解释大家可以看下JET的官方文档 http://jet.readthedocs.io/en/latest/config_file.html#custom-menu 里面有详细说明，目前我们用到的就是菜单排序以及后面要用到的后台添加自定义静态页面。

## 后台admin页面美化
### 库安装
```
(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>pip install django-jet
```

### 添加jet到应用列表
修改settings.py，注册应用`jet.dashboard`和`jet`，注意加在`django.contrib.admin`前面，为实现后台主题切换，还得添加`JET_THEMES`参数

```python
INSTALLED_APPS = [
    'jet.dashboard',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_summernote',

    'newblog',
]
```

### 迁移同步数据库
创建`django-jet`所需数据库表
```
(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py migrate jet
Operations to perform:
  Apply all migrations: jet
Running migrations:
  Applying jet.0001_initial... OK
  Applying jet.0002_delete_userdashboardmodule... OK

(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py migrate dashboard
Operations to perform:
  Apply all migrations: dashboard
Running migrations:
  Applying dashboard.0001_initial... OK
```

### 设置django-jet主题
修改settings.py文件，增加以下配置

```python
# django-jet主题
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
```

### 添加到路由URLs
```python
from django.contrib import admin
from django.urls import path
from newblog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 访问后台管理
访问 http://127.0.0.1:8000/admin/

强制刷新

![使用django-jet](_v_images/_使用djangoje_1525754736_18022.png)

## 富文本输入框配置优化
修改settings.py添加如下代码

```python
# 富文本编辑器设置
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # 使用Summernote Air-mode
    'airMode': False,

    # 使用本地HTML标记 (`<b>`, `<i>`, ...) 代替样式属性
    'styleWithSpan': False,

    # 更改编辑器大小
    'width': '80%',
    'height': '480',

    # 自动使用适当的语言设置 (default)
    'lang': 'zh-CN',
}
```

![富文本输入框配置](_v_images/_富文本输入框配置_1525754996_24945.png)

## 设置django-jet显示菜单
修改settings.py文件，增加以下内容

```python
# 是否展开所有菜单
JET_SIDE_MENU_COMPACT = True  # 菜单不是很多时建议为True

JET_SIDE_MENU_ITEMS = [  # A list of application or custom item dicts
    {'label': '内容管理', 'app_label': 'newblog', 'items': [
        {'name': 'category'},
        {'name': 'article'},
        {'name': 'tag'},
    ]},

    {'label': '附件管理', 'app_label': 'django_summernote', 'items': [
        {'label': '附件列表', 'name': 'attachment'},

    ]},

    {'label': '权限管理', 'items': [
        {'name': 'auth.user', 'permissions': ['auth.user']},
        {'name': 'auth.group', 'permissions': ['auth.user']},

    ]},
]
```

![django-jet菜单显示设置](_v_images/_djangojet菜_1525756049_23066.png)

# 前端美化文章搜索
对博客系统进行优化，主要包括:

* 前端界面美化
* 文章列表分页
* 实现文章分类搜索和标签搜索

## 前端界面美化
### base.html增加字体图标和分类列表
增加`font awesome`字体图标，可以在 http://www.fontawesome.com.cn/ 网站上下载`font-awesome.min.css`文件，并将其放到`static/css`目录下，然后在基础模板中引入，页面代码如下：

base.html

```html
<!DOCTYPE html>
{% load static %}
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} LR@ Blog {% endblock %}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'css/pure-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/grids-responsive-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/blog.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/font-awesome.min.css' %}"/>
</head>
<body>
<div id="layout" class="pure-g">
    <div class="sidebar pure-u-1 pure-u-md-1-4">
        <div class="header" style="text-align: center">  <!--美化：设置标题居中-->
            <h1 class="brand-title"><a href="{% url 'home' %}" style="text-decoration: none">LR@MS博客</a></h1>  <!--鼠标移动上去不显示链接下划线-->
            <h2 class="brand-tagline">NewStarting</h2>
            <nav class="nav">

                <ul class="nav-list">
                    <li class="nav-item" >
                        <!--<a class="pure-button" href="#">Github</a>-->
                        <!--显示分类列表-->
                        {% for category in category_list %}
                            <a class="pure-button" href="#" style="text-decoration: none">{{ category }}</a>
                        {% endfor %}
                    </li>
                </ul>
                <br>

                <ul class="nav-list">
                    <li>
                        <a href="#" style="text-decoration: none">
                            <i class="fa fa-weixin" style="font-size: 30px" aria-hidden="true" title="微信公众号"></i>
                        </a>
                        &nbsp;
                        <a href="#" style="text-decoration: none">
                            <i class="fa fa-envelope-o" style="font-size: 30px" aria-hidden="true" title="邮箱"></i>
                        </a>
                        &nbsp;
                        <a href="#" style="text-decoration: none" title="Github">
                            <i class="fa fa-github" style="font-size: 34px" aria-hidden="true"></i>
                        </a>
                        &nbsp;
                    </li>
                </ul>

            </nav>
        </div>
    </div>
    <div class="content pure-u-1 pure-u-md-3-4">
        <div>
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>
</body>
</html>
```

可以用 `<i>` 标签把 Font Awesome 图标放在任意位置，图标的大小可以使用`fa-lg` (33% 递增), `fa-2x`, `fa-3x`, `fa-4x`, `fa-5x`或者直接指定`font-size`。

![左边导航增加分类](_v_images/_左边导航增加分类_1525758976_18357.png)

### 修改主页视图增加分类home(request)
增加category_list参数传递
```python
categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象


def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每一页显示博客数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories})
```

### 主页模板增加字体图标home.html
主页文章列表页也增加Font Awesome 图标，增加文章作者头像，文章之间加入分隔线，还有增加分页，底端上一页和下一页显示在左右方。
```html
{% extends 'base.html' %}

{% load static %}

{% block content %}
    <div>
        {% for post in post_list %}
            <section class="post">
                <header class="post-header">
                    <img width="48" height="48" alt="Tilo Mitra's avatar" class="post-avatar" src='{% static "image/user.png" %}'>
                    <h2 class="post_title">
                        <a href="{% url 'detail' post.id %}" style="text-decoration: none">{{ post.title }}</a>  <!--不显示链接下横线-->
                    </h2>
                    <p class="post-meta">
                        <!--发布时间：-->
                        <i class="fa fa-calendar" aria-hidden="true"></i>
                        <a href="#" style="text-decoration: none">{{ post.publish_time|date:'Y/m/d' }}</a>
                        &nbsp;&nbsp;
                        <!--分类：-->
                        <i class="fa fa-list-alt"></i>
                        <a href="#" style="text-decoration: none">{{ post.category }}</a>
                        &nbsp;&nbsp;
                        <!--标签：-->
                        <i class="fa fa-tags" aria-hidden="true"></i>
                        {% for tag in post.tags.all %}
                            <a href="#" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                        {% endfor %}
                        &nbsp;&nbsp;
                        <!--浏览次数：-->
                        <i class="fa fa-eye" aria-hidden="true"></i>
                        {{ post.views }}次浏览
                    </p>
                </header>

                <div class="post-description">
                    <p>
                        <!--truncatewords_html:100截取100个字符显示-->
                        <!--{{ post.content|truncatewords_html:100 }}-->
                        {#striptags用于过滤正文中所有的HTML标签#}
                        {{ post.content|striptags|truncatewords_html:100 }}
                    </p>
                </div>

                <div><a class="post-category post-category-design" href="{% url 'detail' post.id %}" style="text-decoration: none">阅读全文</a></div>
                <h1 class="content-subhead"></h1>  <!--添加一条分割线-->
            </section>
        {% endfor %}
    </div>

    <!--分页显示-->
    <div>
        {% if post_list.object_list and post_list.paginator.num_pages > 1 %}
            <div>
                <!--上一页和下一页粪便位于底端左右，且鼠标移动上去不显示链接下划线-->
                {% if post_list.has_previous %}
                    <a class="footer" href="?page={{ post_list.previous_page_number }}" style="text-decoration: none; float: left;">
                        <i class="fa fa-angle-left"></i>&nbsp;上一页
                    </a>
                {% endif %}

                {% if post_list.has_next %}

                    <a class="footer" href="?page={{ post_list.next_page_number }}" style="text-decoration: none; float: right;">
                        下一页&nbsp;<i class="fa fa-angle-right"></i>
                    </a>
                {% endif %}
            </div>
        {% endif %}
    </div>
{% endblock %}
```

![主页使用字体图标](_v_images/_主页使用字体图标_1525777653_29670.png)

### 修改详情视图增加分类detail(request, id)
增加分类的参数传递
```python
categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
    except Article.DoseNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post, 'tags': tags, 'category_list': categories})
```

### 详情模板增加字体图标post.html
文章详情页增加Font Awesome 图标、分类和标签搜索，增加显示富文本语言
```html
{% extends 'base.html' %}

{% block content %}
    <div>
        <section class="post">
            <header class="post-header">
                <h2 class="post-title">{{ post.title }}</h2>

                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-clock-o" aria-hidden="true"></i>
                    {{ post.publish_time|date:'Y/m/d H:m:s' }}
                    &nbsp&nbsp
                    <!--分类：-->
                    <i class="fa fa-list-alt"></i>
                    <a href="#" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp&nbsp
                    <!--标签：-->
                    <i class="fa fa-tags" aria-hidden="true"></i>
                    {% for tag in post.tags.all %}
                        <a href="#" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
            </header>
            <div class="post-description">
                <p>
                    {# 支持显示富文本语言 #}
                    {{ post.content|safe }}
                </p>
            </div>
        </section>
    </div>
{% endblock %}
```

![文章详情页增加字体图标](_v_images/_文章详情页增加字体图_1525763661_12717.png)

## 模板分块，使用include
### 列表展示块base_postlist.html
```html
<!--展示博客列表，传递的值为post_list，博客查询集-->
{% load static %}

<div class="blog-post">
    {% for post in post_list %}
        <section class="post">
            <header class="post-header">
                <img width="48" height="48" alt="Tilo Mitra's avatar" class="post-avatar" src='{% static "image/user.png" %}'>
                <h2 class="post_title">
                    <a href="{% url 'detail' post.id %}" style="text-decoration: none">{{ post.title }}</a>  <!--不显示链接下横线-->
                </h2>
                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-calendar" aria-hidden="true"></i>
                    <a href="#" style="text-decoration: none">{{ post.publish_time|date:'Y/m/d' }}</a>
                    &nbsp;&nbsp;
                    分类：
                    <a href="#" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp;&nbsp;
                    标签：
                    {% for tag in post.tags.all %}
                        <a href="#" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
            </header>

            <div class="post-description">
                <p>
                    <!--truncatewords_html:100截取100个字符显示-->
                    <!--{{ post.content|truncatewords_html:100 }}-->
                    {#striptags用于过滤正文中所有的HTML标签#}
                    {{ post.content|striptags|truncatewords_html:100 }}
                </p>
            </div>

            <div><a class="post-category post-category-design" href="{% url 'detail' post.id %}" style="text-decoration: none">阅读全文</a></div>
            <h1 class="content-subhead"></h1>  <!--添加一条分割线-->
        </section>
    {% endfor %}
</div>
```

### 分页显示块base_paginator.html
```html
<!--分页模块，传递的参数为queryset-->
<div>
    {% if queryset.object_list and queryset.paginator.num_pages > 1 %}
        <div>
            <!--上一页和下一页粪便位于底端左右，且鼠标移动上去不显示链接下划线-->
            {% if queryset.has_previous %}
                <a class="footer" href="?page={{ post_list.previous_page_number }}" style="text-decoration: none; float: left;">
                    <i class="fa fa-angle-left"></i>&nbsp;上一页
                </a>
            {% endif %}

            {% if queryset.has_next %}
                <a class="footer" href="?page={{ post_list.next_page_number }}" style="text-decoration: none; float: right;">
                    下一页&nbsp;<i class="fa fa-angle-right"></i>
                </a>
            {% endif %}
        </div>
    {% endif %}
</div>
```

### 修改主页包含块home.html
```html
{% extends 'base.html' %}

{% block content %}
     <!--展示查询列表-->
    {% include 'base_bloglist.html' %}

    <!--分页显示-->
    {% with post_list as queryset %}
        {% include 'base_paginator.html' %}
    {% endwith %}

{% endblock %}
```

## 分类过滤结果
分类搜索结果页、标签搜索结果页和主页文章列表页结构类似，区别在于文章列表页显示的是没有加筛选条件的结果，分类搜索结果页是显示特定分类的文章列表，标签搜索结果页是显示特定标签的文章列表，分类搜索结果页代码如下：
### 分类筛选视图search_category(request, id)
```python
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

    return render(request, 'category.html', {'post_list': post_list, 'category_list': categories, 'category': category})
```

### 分类过滤路由search_category
```python
from django.contrib import admin
from django.urls import path
from newblog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('category/<int:id>/', views.search_category, name='search_category'),  # 分类显示
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 分类筛选模板category.html
```html
{% extends 'base.html' %}

{% block content %}
    <h1 class="content-subhead">分类:&nbsp;<span>{{ category }}</span><br><br></h1>

    <!--展示查询列表-->
    {% include 'base_bloglist.html' %}

    <!--分页显示-->
    {% with post_list as queryset %}
        {% include 'base_paginator.html' %}
    {% endwith %}

{% endblock %}
```

访问 http://127.0.0.1:8000/category/1/ 查看Python分类下的文章

![分类筛选模板](_v_images/_分类筛选模板_1525777764_14467.png)

## 标签过滤结果
标签搜索结果页页面代码如下：
### 标签过滤视图search_tag(request, tag)
```python
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

    return render(request, 'tag.html', {'post_list': post_list, 'category_list': categories, 'tag': tag})
```

### 标签过滤路由search_tag
```python
from django.contrib import admin
from django.urls import path
from newblog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('category/<int:id>/', views.search_category, name='search_category'),  # 分类显示
    path('tags/<str:tag>/', views.search_tag, name='search_tag'),  # 标签显示
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 标签过滤模板tag.html
```html
{% extends 'base.html' %}

{% block content %}
    <h1 class="content-subhead">标签:&nbsp;<span>{{ tag }}</span><br><br></h1>

    <!--展示查询列表-->
    {% include 'base_bloglist.html' %}

    <!--分页显示-->
    {% with post_list as queryset %}
        {% include 'base_paginator.html' %}
    {% endwith %}

{% endblock %}
```

访问 http://127.0.0.1:8000/tags/Web/ 查看标签Web下的结果

![标签过滤模板](_v_images/_标签过滤模板_1525777848_4865.png)

## 补充分类和标签链接
### base.html分类链接
将链接添加的category遍历中
```html
                <ul class="nav-list">
                    <li class="nav-item" >
                        <!--<a class="pure-button" href="#">Github</a>-->
                        <!--显示分类列表-->
                        {% for category in category_list %}
                            <a class="pure-button" href="{% url 'search_category' category.id %}" style="text-decoration: none">{{ category }}</a>
                        {% endfor %}
                    </li>
                </ul>
```

### base_bloglist.html分类和标签链接
增加文章的分类和标签的链接
```html
                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-calendar" aria-hidden="true"></i>
                    <a href="#" style="text-decoration: none">{{ post.publish_time|date:'Y/m/d' }}</a>
                    &nbsp;&nbsp;
                    <!--分类：-->
                    <i class="fa fa-list-alt"></i>
                    <a href="{% url 'search_category' post.category.id %}" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp;&nbsp;
                    <!--标签：-->
                    <i class="fa fa-tags" aria-hidden="true"></i>
                    {% for tag in post.tags.all %}
                        <a href="{% url 'search_tag' tag %}" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
```

### post.html分类和标签链接
详情页的分类和标签增加
```html
                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-clock-o" aria-hidden="true"></i>
                    {{ post.publish_time|date:'Y/m/d H:m:s' }}
                    &nbsp&nbsp
                    <!--分类：-->
                    <i class="fa fa-list-alt"></i>
                    <a href="{% url 'search_category' post.category.id %}" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp&nbsp
                    <!--标签：-->
                    <i class="fa fa-tags" aria-hidden="true"></i>
                    {% for tag in post.tags.all %}
                        <a href="{% url 'search_tag' tag %}" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
```

现在所有分类和标签的链接功能可用。

# 详情页切换和回到顶部
对博客系统进行优化，主要包括:

* 文章详情页内实现上一篇和下一篇文章切换
* 实现点击按钮回到顶部

## 文章详情上下篇切换
### 文章详情视图修改detail(request, id)
修改views.py中的视图函数detail
```python
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
                  })
```

### 文章详情视图模板post.html
修改文章详情页post.html，添加上下篇文章切换页面代码
```html
{% extends 'base.html' %}

{% block content %}
    <div>
        <section class="post">
            <header class="post-header">
                <h2 class="post-title">{{ post.title }}</h2>

                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-clock-o" aria-hidden="true"></i>
                    {{ post.publish_time|date:'Y/m/d H:m:s' }}
                    &nbsp&nbsp
                    <!--分类：-->
                    <i class="fa fa-list-alt"></i>
                    <a href="{% url 'search_category' post.category.id %}" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp&nbsp
                    <!--标签：-->
                    <i class="fa fa-tags" aria-hidden="true"></i>
                    {% for tag in post.tags.all %}
                        <a href="{% url 'search_tag' tag %}" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
            </header>
            <div class="post-description">
                <p>
                    {# 支持显示富文本语言 #}
                    {{ post.content|safe }}
                </p>
            </div>
        </section>
    </div>

    <!--上下篇文章切换-->
    <div>
        {% if prev_post %}
            <a class="footer" href="{% url 'detail' prev_post.id %}" style="text-decoration: none; float: left;">
                <i class="fa fa-angle-left"></i>&nbsp;上一篇 《{{ prev_post.title }}》
            </a>
        {% endif %}
        {% if next_post %}
            <a class="footer" href="{% url 'detail' next_post.id %}" style="text-decoration: none; float: right;">
                《{{ next_post.title }}》 下一篇&nbsp;<i class="fa fa-angle-right"></i>
            </a>
        {% endif %}
    </div>

{% endblock %}
```

![文章详情显示上下篇切换](_v_images/_文章详情显示上下篇切_1525781405_3128.png)

## 实现点击按钮回到顶部
当页面很长时滚动到页面下方，会在右下角一个固定位置出现“返回顶部”的按钮，点一下浏览器滚动条就自动回到顶部，本文实现的这个功能按钮为纯CSS实现，动画效果由Jquery实现；

### 导入jquery
下载jQuery，地址：https://jquery.com/ ，将jquery-3.3.1.min.js文件copy到目录static/js/文件夹下

### 基础模板添加回到顶部按钮base.html
修改基础模板base.html
```html
<!DOCTYPE html>
{% load static %}
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} LR@ Blog {% endblock %}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'css/pure-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/grids-responsive-min.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/blog.css' %}"/>
    <link rel="stylesheet" type="text/css" href="{% static 'css/font-awesome.min.css' %}"/>
</head>
<body>
<div id="layout" class="pure-g">
    <div class="sidebar pure-u-1 pure-u-md-1-4">
        <div class="header" style="text-align: center">  <!--美化：设置标题居中-->
            <h1 class="brand-title"><a href="{% url 'home' %}" style="text-decoration: none">LR@MS博客</a></h1>  <!--鼠标移动上去不显示链接下划线-->
            <h2 class="brand-tagline">NewStarting</h2>
            <nav class="nav">

                <ul class="nav-list">
                    <li class="nav-item" >
                        <!--<a class="pure-button" href="#">Github</a>-->
                        <!--显示分类列表-->
                        {% for category in category_list %}
                            <a class="pure-button" href="{% url 'search_category' category.id %}" style="text-decoration: none">{{ category }}</a>
                        {% endfor %}
                    </li>
                </ul>
                <br>

                <ul class="nav-list">
                    <li>
                        <a href="#" style="text-decoration: none">
                            <i class="fa fa-weixin" style="font-size: 30px" aria-hidden="true" title="微信公众号"></i>
                        </a>
                        &nbsp;
                        <a href="#" style="text-decoration: none">
                            <i class="fa fa-envelope-o" style="font-size: 30px" aria-hidden="true" title="邮箱"></i>
                        </a>
                        &nbsp;
                        <a href="#" style="text-decoration: none" title="Github">
                            <i class="fa fa-github" style="font-size: 34px" aria-hidden="true"></i>
                        </a>
                        &nbsp;
                    </li>
                </ul>

            </nav>
        </div>
    </div>
    <div class="content pure-u-1 pure-u-md-3-4">
        <div>
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>

<!--回到顶部按钮-->
<div class="go-top">
    <div class="arrow"></div>
    <div class="stick"></div>
</div>
<script type="text/javascript" src="{% static 'js/jquery-3.3.1.min.js' %}"></script>
<script>
    $(function () {
        $(window).scroll(function () {
            if ($(window).scrollTop() > 1000)
                $('div.go-top').show();
            else
                $('div.go-top').hide();
        });
        $('div.go-top').click(function () {
            $('html, body').animate({scrollTop: 0}, 500);
        });
    });
</script>

</body>
</html>
```

### 修改css文件blog.css
编辑static/css/blog.css，添加如下样式：
```css
/*回到顶部*/
div.go-top {
    display: none;
    opacity: 0.6;
    z-index: 999999;
    position: fixed;
    bottom: 8%;
    right: 0.3%;
    margin-left: 40px;
    border: 1px solid #47BAC1;
    width: 38px;
    height: 38px;
    background-color: #47BAC1;
    border-radius: 3px;
    cursor: pointer;
}

div.go-top:hover {
    opacity: 1;
    filter: alpha(opacity=100);
}

div.go-top div.arrow {
    position: absolute;
    left: 10px;
    top: -1px;
    width: 0;
    height: 0;
    border: 9px solid transparent;
    border-bottom-color: #FFFFFF;
}

div.go-top div.stick {
    position: absolute;
    left: 15px;
    top: 15px;
    width: 8px;
    height: 14px;
    display: block;
    background-color: #FFFFFF;
    -webkit-border-radius: 1px;
    -moz-border-radius: 1px;
    border-radius: 1px;
}
```

查看效果，添加一篇较长的文章。

![添加返回顶部按钮](_v_images/_添加返回顶部按钮_1525782623_16748.png)


# 实现文章按月归档
对博客系统进行优化，主要包括:

* 页面美化
* 实现文章按月归档

主要还是调样式和字体，包括全局背景色的设置，图标显示，列表页分块，文章标题颜色和字体等等

## 文章按年归档
### 文章按月归档视图archive(request, year, month)
编辑views.py，添加归档视图函数archive
```python
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
                  })
```

### 文章按月归档路由archive
```python
from django.contrib import admin
from django.urls import path
from newblog import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
    path('category/<int:id>/', views.search_category, name='search_category'),  # 分类显示
    path('tags/<str:tag>/', views.search_tag, name='search_tag'),  # 标签显示
    path('archives/<str:year>/<str:month>', views.archive, name='archive'),  # 按月归档
    path('summernote/', include('django_summernote.urls')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 文章按月归档模板archive.html
```html
{% extends 'base.html' %}

{% block content %}
    <h1 class="content-subhead">归档:&nbsp;<span>{{ year_month }}</span><br><br></h1>

    <!--展示查询列表-->
    {% include 'base_bloglist.html' %}

    <!--分页显示-->
    {% with post_list as queryset %}
        {% include 'base_paginator.html' %}
    {% endwith %}

{% endblock %}
```

### 列表页点击日期链接base_bloglist.html
```html
                <p class="post-meta">
                    <!--发布时间：-->
                    <i class="fa fa-calendar" aria-hidden="true"></i>
                    <a href="{% url 'archive' post.publish_time.year post.publish_time.month %}" style="text-decoration: none">{{ post.publish_time|date:'Y/m/d' }}</a>
                    &nbsp;&nbsp;
                    <!--分类：-->
                    <i class="fa fa-list-alt"></i>
                    <a href="{% url 'search_category' post.category.id %}" style="text-decoration: none">{{ post.category }}</a>
                    &nbsp;&nbsp;
                    <!--标签：-->
                    <i class="fa fa-tags" aria-hidden="true"></i>
                    {% for tag in post.tags.all %}
                        <a href="{% url 'search_tag' tag %}" style="text-decoration: none">{{ tag }}</a> {% if not forloop.last %}|{% endif %}
                    {% endfor %}
                    &nbsp;&nbsp;
                    <!--浏览次数：-->
                    <i class="fa fa-eye" aria-hidden="true"></i>
                    {{ post.views }}次浏览
                </p>
```

# 实现文章数量统计
## 分类下的文章统计
### 修改模型Article(models.Model)
创建外键关联
```python
class Article(models.Model):
    # ···
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, related_name='articles', verbose_name='所属分类')
    # ···
```

迁移同步数据库
```
(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py makemigrations
Migrations for 'newblog':
  newblog\migrations\0002_auto_20180509_1315.py
    - Alter field category on article

(BlogVenv) G:\LR@ProjectsSync\OneDrive\PycharmProjects\DjangoNewBlog\DjangoNewBlog>python manage.py migrate
```

### 修改视图返回所有博客数量
使用数据聚合，返回总的博客数量（已发布加草稿），在views.py中修改返回所有分类，并将统计的结果记录到`num_posts`属性中。
```python
# categories = Category.objects.all()  # 获取全部的分类对象
categories = Category.objects.annotate(num_posts=Count('articles')).all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
```

### 创建模板标签返回已发布数量total_post_num(category_id)
在`newblog`应用下创建`templatetags`文件夹，并创建__init__.py文件，接着在该目录下继续创建一个文件并命名为published_num_tags.py，用于返回所有已发布的博客数量
```python
from django import template

register = template.Library()

from ..models import Article


@register.simple_tag
def total_post_num(category_id):
    return Article.objects.filter(status='p', category__id=category_id).count()
```

### 模板中显示上面的数量base.html
修改base.html，添加`{% total_post_num category.id %}`已发布，参数为分类id，{{ category.num_posts }}所有博客
```html
                    <li class="nav-item" >
                        <!--<a class="pure-button" href="#">Github</a>-->
                        <!--显示分类列表-->
                        {% for category in category_list %}
                            <a class="pure-button" href="{% url 'search_category' category.id %}" style="text-decoration: none">{{ category }}({% total_post_num category.id %}/{{ category.num_posts }})</a>
                        {% endfor %}
                    </li>
```

![显示分类数量统计](_v_images/_显示分类数量统计_1525849439_9971.png)

## 按照月份统计
### 修改视图按照月份汇总
**所有**视图中添加`'year_months': year_months`
```python
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
```

### 创建模板标签显示按日期数量year_mont_post_num(year, month)
在published_num_tags.py文件中增加`year_mont_post_num(year, month)`函数，用于统计该日期下已发布博客数量。
```python
from django import template

register = template.Library()

from ..models import Article


@register.simple_tag
def total_post_num(category_id):
    return Article.objects.filter(status='p', category__id=category_id).count()


@register.simple_tag
def year_mont_post_num(year, month):
    return Article.objects.filter(status='p', publish_time__year=year, publish_time__month=month).count()
```

### 修改模板显示归档base.html
修改base.html，增加按照日期统计汇总
```html
                <ul class="nav-list">
                    <li class="nav-item" >
                        <!--<a class="pure-button" href="#">Github</a>-->
                        <!--显示分类列表-->
                        {% for category in category_list %}
                            <a class="pure-button" href="{% url 'search_category' category.id %}" style="text-decoration: none">{{ category }}({% total_post_num category.id %}/{{ category.num_posts }})</a>
                        {% endfor %}
                    </li>
                </ul>
                <br>
                <h3 class="brand-tagline" style="margin: 2%; text-align: left">文章归档(已发布)</h3>
                <ul class="nav-list" style="margin: 2%; text-align: left">
                    {% for ym in year_months %}
                        <li>
                            <a href="{% url 'archive' year=ym.year month=ym.month %}"
                               style="text-decoration: none">{{ ym | date:'Y年m月' }}({% year_mont_post_num ym.year ym.month %})</a>
                        </li>
                    {% empty %}
                        暂无归档！
                    {% endfor %}
                </ul>
```

![博客按日期统计数量](_v_images/_博客按日期统计数量_1525852549_11507.png)

最后诚挚的感谢学习参考网站： http://jinbitou.net/2018/03/06/2644.html
