from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from .models import Post,UserProfile
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .form import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm,PostModel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.forms.models import model_to_dict
from time import strptime

# Create your views here.

@login_required()
def feed(request):
    if request.method == 'POST':
        post = Post.objects.create(author = request.user)
        post_form = PostModel(instance=post,data=request.POST,files=request.FILES)
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.save()
            messages.success(request,'Success')
        else:
            messages.error(request,'Error')

    post_form = PostModel()
    posts = Post.objects.all()
    paginator = Paginator(posts,5)
    page = request.GET.get('page')

    try:
        post = paginator.page(page)
        
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        post = paginator.page(1)
    avatars = UserProfile.objects.all()
    return render(request,'feed/post/feed.html',{'page':page,'posts':post,'avatars':avatars,'UserProfile':UserProfile,'post_form':post_form,'this_user':request.user})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username = cd['username'],password = cd['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/feed/')
            else:
                return HttpResponse('User is not active')

        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    return render(request,'feed/post/login.html',{'form':form})


def register(request):
    if request.method=='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect('/feed/login')

    else:
        user_form = UserRegistrationForm()

    return render(request,'feed/post/register.html',{'user_form':user_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/feed/login')



@login_required
def profile(request,user):
    user_info = User.objects.filter(username=request.user)
    user_info2 = User.objects.filter(username=user)
    user_profile = str(user_info) == str(user_info2)
    
    posts = Post.objects.all().filter(author__in=user_info2)
    nickname=user

    paginator = Paginator(posts,5)
    page = request.GET.get('page')

    try:
        post = paginator.page(page)
    
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        post = paginator.page(1)
    try:
        avatar = UserProfile.objects.get(user_id=user_info2[0].id).avatar
    except:
        avatar = None
    this_user = User.objects.get(username = request.user)
    return render(request,'feed/post/profile.html',{'user_info':user_info2,'user_profile':user_profile,'posts':post,'nickname':nickname,'page':page,'avatar':avatar,'this_user':this_user})



@login_required
def profileEdit(request,user):
 
    user_info = User.objects.get(username=request.user)
    user_info2 = User.objects.get(username=user)


    if user_info != user_info2:
        return HttpResponseRedirect('/feed/profile/{}'.format(request.user))


    if request.method == 'POST':
            try:
                avatar = UserProfile.objects.get(user=user_info)
            except:
                UserProfile.objects.create(user=user_info)
            avatar = UserProfile.objects.get(user=user_info)
            user_form = UserEditForm(instance = request.user,data = request.POST)
            profile_form = ProfileEditForm(instance=avatar,data=request.POST,files=request.FILES)

            if user_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request,'Profile updated successfully')

            else:
                messages.error(request,'Error updating your profile')

    else:
        user_form = UserEditForm()
        profile_form  = ProfileEditForm()
    

    return render(request,'feed/post/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})



def postDelete(request,author,publish,result = None):
    user_info = User.objects.get(username=request.user)
    user_info2 = User.objects.get(username=author)

    

    if user_info != user_info2:
        return HttpResponseRedirect('/feed/profile/{}'.format(request.user)) 

    if result == 'success':

        month,other_dates,_,_ = publish.split('.')
        day,year,time = other_dates.replace(' ','').split(',')
        time = time[:-1]
        month = strptime(month,'%b').tm_mon
        user_id = User.objects.get(username=author).id
        posts = Post.objects.filter(author=user_id)


        for post in posts:  
            post_date = str(post.publish).split('.')[0]
            
            post_years,post_time = post_date.split(' ') 
            post_year,post_month,post_day = post_years.split('-')
            post_time,_ = post_time.rsplit(':',1)
            _,post_month = post_month.split('0',1)
            _,post_time= post_time.split('0',1)
            if str(post_year) == str(year) and str(post_month)==str(month) and str(post_day==day) and str(post_time)==str(time):
                post.delete()
            return HttpResponseRedirect('/feed/')

    
    return render(request,'feed/post/delete_post.html',{'pusblish':publish,'author':author})


