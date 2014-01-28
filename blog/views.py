#coding:utf-8
from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView
from datetime import datetime
from models import Article,Category,Tag
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from Constant import PageParam,ViewSize

# Create your views here.

class BaseView(object):

	def get_context_data(self,*args,**kwargs):
		context = super(BaseView, self).get_context_data(**kwargs)
		context['tags'] = Tag.objects.all()
		context['new_list'] = Article.get_new_list(ViewSize.NEW_SIZE)
		context['hot_list'] = Article.get_hot_list(ViewSize.HOT_SIZE)
		return context


class IndexView(BaseView,ListView):
	def get(self,request,*args,**kwargs):
		try:
			self.page = int(request.GET.get('page'))
		except TypeError:
			self.page = 1
		except ValueError:
			self.page = 1

		if self.page < 1:
			self.page = 1
		
		return super(IndexView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		return Article.objects.filter(status=1).order_by('-create_time')

	def get_context_data(self,*args,**kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		paginator = Paginator(self.object_list,PageParam.PAGE_SIZE)
		context['articles'] = paginator.page(self.page)
		#分页导航条控制
		if self.page >= PageParam.AFTER_RANGE_NUM:
			page_range = paginator.page_range[self.page-PageParam.AFTER_RANGE_NUM\
				:self.page+PageParam.BEFOR_RANGE_NUM]
		else:
			page_range = paginator.page_range[0:int(self.page)+PageParam.BEFOR_RANGE_NUM]
		context['page_range'] = page_range
		return context


class DetailViews(BaseView,DetailView):
	slug_field = 'alias'
	queryset = Article.objects.all()

	def get(self,request,*args,**kwargs):
		ip = request.META['REMOTE_ADDR']
		print ip;
		alias = self.kwargs.get('slug')
		article = self.queryset.get(alias=alias)
		article.hits+=1
		article.save();
		return super(DetailViews,self).get(request,*args,**kwargs)
	
	def get_context_data(self,**kwargs):
		context = super(DetailViews, self).get_context_data(**kwargs)
		context['article'] = self.get_object();
		return context


class CategoryListView(IndexView):
	def get_queryset(self):
		alias = self.kwargs.get('alias')
		return Article.objects.filter(category=Category.objects.get(name=alias))

	def get_context_data(self,*args,**kwargs):
		return super(CategoryListView, self).get_context_data(**kwargs)


class TagListView(IndexView):
	def get_queryset(self):
		tag = self.kwargs.get('tag')
		return Article.objects.filter(Q(tags__icontains = tag))
	
	def get_context_data(self,*args,**kwargs):
		return super(TagListView, self).get_context_data(**kwargs)

