from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from blog.models import Article
admin.autodiscover()

from blog.views import (IndexView,DetailViews,CategoryListView,TagListView)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',IndexView.as_view(template_name='index.html')),
    url(r'^detail/(?P<slug>.*)$',DetailViews.as_view(model=Article,template_name='detail.html')),
    url(r'^category/(?P<alias>.*)/$',CategoryListView.as_view(template_name='index.html')),
    url(r'^tag/(?P<tag>.*)/$',TagListView.as_view(template_name='index.html')),
)
urlpatterns += staticfiles_urlpatterns()
