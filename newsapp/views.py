from django.shortcuts import *
from django.http import *
from .models import *
from .forms import *
from django.views.decorators.http import require_GET
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

#OR

def index(request):
    data=Article.objects.filter(Q(moderated=True)).order_by('-date_created')
    trend=Article.objects.filter(Q(moderated=True)).order_by('-hits')
    national=Article.objects.filter(Q(moderated=True)).filter(category__name='National').order_by('-date_created')
    international=Article.objects.filter(Q(moderated=True)).filter(category__name='Interational').order_by('-date_created')
    sports=Article.objects.filter(Q(moderated=True)).filter(category__name='Sports').order_by('-date_created')
    technology=Article.objects.filter(Q(moderated=True)).filter(category__name='Technology').order_by('-date_created')
    movies=Article.objects.filter(Q(moderated=True)).filter(category__name='Movies').order_by('-date_created')
    lifestyle=Article.objects.filter(Q(moderated=True)).filter(category__name='Lifestyle').order_by('-date_created')
    business=Article.objects.filter(Q(moderated=True)).filter(category__name='Business').order_by('-date_created')
    science=Article.objects.filter(Q(moderated=True)).filter(category__name='Science').order_by('-date_created')
    return render(request,'index.html',{'data': data,'trend': trend, 'national':national,'international':international,'sports':sports,'technology':technology,'movies':movies,'lifestyle':lifestyle,'business':business,'science':science})

def delete(request,pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return HttpResponseRedirect('/article/')

def search(request):
    if request.method=='POST':
        squery=request.POST['search_box']
        if squery:
            data=Article.objects.filter(Q(title__icontains=squery)|Q(content__icontains=squery)|Q(user__username__exact=squery))#i=ignorecase and Q means query
            paginator = Paginator(data, 5) # 3 articles in each page
            page = request.GET.get('page')
            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                articles = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                articles = paginator.page(paginator.num_pages)
            if data:
                return render(request,'search.html',{'page': page,'articles': articles})
            else:
                return render(request,'search.html',{'msg':'No Matching Search Result'})
        else:
            return HttpResponseRedirect('/')

def detail(request,category,slug):
    article = get_object_or_404(Article,slug=slug)
    article.hits+=1
    article.save()
    similar_posts = article.tags.similar_objects()[:3]
        # List of active comments for this article
    comments = article.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
            return HttpResponseRedirect(new_comment.article.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request, 'detail.html', {'article': get_object_or_404(Article, slug=slug),'similar_posts': similar_posts,'comments': comments,
'comment_form': comment_form})


def edit(request,pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method=='POST':
        form=ArticleForm(request.POST,request.FILES,instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user=request.user
            article.save()
            form.save_m2m()
            form.save()
            return HttpResponseRedirect('/article/')
    else:
        form=ArticleForm(instance=article)
    return render(request,'edit.html',{'form':form})

def register(request):
    if request.method=='POST':
        #form=UserCreationForm(request.POST)   #built in form
        form=Regforms(request.POST)   #user created form
        #built in form usercreationform and table is user
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            profile.profilepic='pic/def.png'
            
            User.objects.create_user(username=form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/login/')
    else:
        #form=UserCreationForm()
        form=Regforms()
    return render(request,'register.html',{'form':form})
@login_required
def profile(request):
    user=request.user
    if request.method=='POST':
        #form=UserCreationForm(request.POST)   #built in form
        form=MyProfile(request.POST,request.FILES)   #user created form
        #built in form usercreationform and table is user
        if form.is_valid():
            user.first_name=form.cleaned_data.get('first_name')
            user.last_name=form.cleaned_data.get('last_name')
            user.profile.bio=form.cleaned_data.get('bio')
            user.email=form.cleaned_data.get('email')
            user.profile.profilepic=form.cleaned_data['profilepic']
            user.save()
            return redirect('/profiledisp/')
    else:
        form=MyProfile(instance=user,initial={
            'bio':user.profile.bio,
            'profilepic':user.profile.profilepic
            })
    return render(request,'profile.html',{'form':form})

def password(request):
    user=request.user
    if request.method=='POST':
        form =Password(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            return redirect('login')
    else:
        form=Password()
    return render(request,'password.html',{'form':form})
        

def login(request):
    return render(request,'login.html')

def auth_view(request):
    uname=request.POST['uname']
    passw=request.POST['passw']
    user=auth.authenticate(username=uname,password=passw)
    if not request.POST.get('remember', None):
            request.session.set_expiry(0)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/logged_in/')
    else:
        return HttpResponseRedirect('/invalid/')

def loggedin(request):
    if request.user.is_authenticated:
        user=request.user
        if user.profile.flag is 0:
            user.profile.flag=1
            user.profile.save()
            return HttpResponseRedirect('/profile/')
        else:
            return HttpResponseRedirect('/profiledisp/')
    else:
        return HttpResponse('Page not Found....!')

def invalid(request):
    return render(request,'invalid.html')
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    
def article(request):
    data=Article.objects.filter(Q(moderated=True)).order_by('-date_created')
    trend=Article.objects.filter(Q(moderated=True)).order_by('-hits')
    national=Article.objects.filter(Q(moderated=True)).filter(category__name='National').order_by('-date_created')
    international=Article.objects.filter(Q(moderated=True)).filter(category__name='International').order_by('-date_created')
    sports=Article.objects.filter(Q(moderated=True)).filter(category__name='Sports').order_by('-date_created')
    technology=Article.objects.filter(Q(moderated=True)).filter(category__name='Technology').order_by('-date_created')
    movies=Article.objects.filter(Q(moderated=True)).filter(category__name='Movies').order_by('-date_created')
    lifestyle=Article.objects.filter(Q(moderated=True)).filter(category__name='Lifestyle').order_by('-date_created')
    business=Article.objects.filter(Q(moderated=True)).filter(category__name='Business').order_by('-date_created')
    science=Article.objects.filter(Q(moderated=True)).filter(category__name='Science').order_by('-date_created')
    return render(request,'index.html',{'data': data,'trend': trend, 'national':national,'international':international,'sports':sports,'technology':technology,'movies':movies,'lifestyle':lifestyle,'business':business,'science':science})
    

@login_required()
def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user=request.user
            article.save()
            form.save_m2m()
            return redirect('detail', article.category.slug, article.slug)
    else:
        form = ArticleForm()
    return render(request, 'post_edit.html', {'form': form})
@login_required
def profiledisp(request):
    return render(request,'profiledisp.html')

def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
@login_required
def postbyuser(request):
    return render(request,'postbyuser.html')

def categorywise(request,category_slug=None):
    data=Article.objects.filter(Q(moderated=True)).order_by('-date_created')
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = data.filter(category=category)
        paginator = Paginator(data, 10) # 3 articles in each page
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            articles = paginator.page(paginator.num_pages)
        return render(request,'categorywiselist.html',{'page': page,'articles': articles,'category':category})