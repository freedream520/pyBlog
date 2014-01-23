#coding:utf-8
from django.db import models
from datetime import datetime


# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=32, verbose_name=u'名字')
	create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
	update_time = models.DateTimeField(u'修改时间', auto_now=True)

#暂时未加入用户模块	
class User(models.Model):
	name = models.CharField(max_length=64, verbose_name=u'用户名')

class Category(models.Model):
	name = models.CharField(max_length=64, verbose_name=u'名称')
	is_nav = models.BooleanField(default=False, verbose_name=u'是否在导航显示')
	turn = models.IntegerField(default=0, verbose_name=u'排序')
	status = models.IntegerField(default=1, verbose_name=u'状态')

class Article(models.Model):
	title = models.CharField(max_length=128, verbose_name=u'标题')
	alias = models.CharField(max_length=128, verbose_name=u'别名')
	author = models.ForeignKey(User, verbose_name=u'作者')
	summary = models.TextField(verbose_name=u'摘要,html格式')
	content = models.TextField(verbose_name=u'文章正文,html格式')

	hits = models.IntegerField(default=1, verbose_name=u'点击量')

	category = models.ForeignKey(Category, verbose_name=u'类别')
	tags = models.CharField(max_length=64, verbose_name=u'标签',help_text=u'用英文逗号分割')
	
	is_recommend = models.BooleanField(max_length=1, default=False, verbose_name=u'是否推荐')
	is_top = models.BooleanField(max_length=1, default=False, verbose_name=u'置顶')
	status = models.IntegerField(default=1, verbose_name=u'状态')

	issue_time = models.DateTimeField(default=datetime.now, verbose_name=u'发布时间')
	
	create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
	update_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)

	def tags_list(self):
		return self.tags.split(',')
	@classmethod
	def get_new_list(self,num):
		return self.objects.values('title','alias').filter(status=1).order_by('-create_time')[:num]
	@classmethod
	def get_hot_list(self,num):
		return self.objects.values('title','alias').filter(status=1,is_recommend=True).order_by('-hits')[:num]





