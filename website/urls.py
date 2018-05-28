"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from newsapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^login/',login,name='login'),
    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/viewer/', AudienceSignUpView.as_view(), name='audience_signup'),
    path('accounts/signup/staff/', StaffSignUpView.as_view(), name='staff_signup'),
    path('personalised_feed/', ArticleListView.as_view(), name='article_list'),
    path('interests/', AudienceInterestsView.as_view(), name='audience_interests'),
    url(r'^$',index,name='index'),
    url(r'^news/new/$',article_new, name='article_new'),
    url(r'^delete/(\d+)/$',delete,name='delete'),
    url(r'^search/$',search,name='search'),
    url(r'^(?P<category>[^\.]+)/(?P<slug>[^\.]+).html',detail,name='detail'),
    url(r'^edit/(\d+)/$',edit,name='edit'),
    #url(r'^register/$',register,name='register'),
    #url(r'^auth_check/$',auth_view,name='check'),
    url(r'^logged_in/$',loggedin,name='loggedin'),
    #url(r'^invalid/$',invalid),
    #url(r'^logout/$',logout),
    url(r'^profile/$',profile,name='profile'),
    url(r'^password/$',password,name='password'),
    url(r'^news/$',article,name='article'),
    url(r'^profile/(?P<usr>[-\w]+)/$',profiledisp,name='profiledisp'),
    url(r'^articles/(?P<usr>[-\w]+)/$',postbyuser,name='postbyuser'),
    url(r'^about/$',about,name='about'),
    url(r'^contact/$',contact,name='contact'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^category/(?P<category_slug>[-\w]+)/$',categorywise, name='list_of_news_by_category'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
