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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, related_name='articles', verbose_name='所属分类')
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