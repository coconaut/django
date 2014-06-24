from django.conf.urls import patterns, url
from families import views



urlpatterns = patterns('',
url(r'^$', views.fam_reroute, name='family'),
url(r'^(?P<familyname>\w+)/$', views.family, name='family'),
url(r'^(?P<familyname>\w+)/(?P<page>\w+)/$', views.thread_page),
url(r'^(?P<familyname>\w+)/(?P<page>\w+)/(?P<id>\d+)/$', views.fam_board)
)
