from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from autoslug import AutoSlugField

# Create your models here.
class User(AbstractUser):
    is_audience = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    @models.permalink
    def get_absolute_url(self):
        return reverse('list_of_news_by_category', args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    user=models.ForeignKey(User,blank=False,null=False,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title')
    content=RichTextUploadingField()
    pic=models.ImageField(upload_to='pic',null=True,blank=True)
    category = models.ForeignKey(Category, blank=True,on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    hits = models.IntegerField(default=0)
    date_created=models.DateTimeField(default=timezone.now,null=True,blank=True)
    moderated = models.BooleanField(default=False,blank=True)
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('detail', None, { 'category': self.category.slug,'slug': self.slug })


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profilepic = models.FileField(upload_to='pic',null=True,blank=True,default='pic/def.png')
    bio = models.CharField(max_length=100,null=True,blank=True)
    flag = models.IntegerField(default=0)
    
    class Meta:
        db_table='auth_profile'

    def __unicode__(self):
        return self.location

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    #email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.article)


class Audience(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(Category, related_name='interested_audiences')

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verified = models.BooleanField(default=False)