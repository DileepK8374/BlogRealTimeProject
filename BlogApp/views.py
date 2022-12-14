from django.shortcuts import render,get_object_or_404
from BlogApp.models import Post
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home_page_view(request):
    return render(request,'BlogApp/home.html')

@login_required
def Login_Page(request):
    return render(request,'BlogApp/post_detail.html');


def logout_view(request):
    return render(request, 'BlogApp/logout.html')
'''

# Create your views here.

#post-list-view with paginator-codes...
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from BlogApp.models import Post
# Create your views here.




#from django.core.mail import send_mail
#print(send_mail('Hello', 'Very imp msg....','kdileep8374@gmail.com',['kdileep1240@gmail.com','dileepk1240@gmail.com']))


#post-list-view with paginator-codes...
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from BlogApp.models import Post
from taggit.models import Tag

# Create your views here.
def post_list_view(request,tag_slug=None):
    print("post_list_view with paginator")
    post_list=Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,2)            #no.of.pages(20/2-rec=>10-pages)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'BlogApp/post_list.html',{"post_list":post_list,'tag':tag})

    # comment form-view


from BlogApp.models import Comment
from BlogApp.forms import CommentForm
from django.db.models import Count
def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'BlogApp/post_detail.html', {"post": post, 'form': form, 'comments': comments, 'csubmit': csubmit,'similar_posts': similar_posts})

#views for email
from django.core.mail import send_mail
from BlogApp.forms import EmailSendForm
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id, status='published')
    sent=False
    form=EmailSendForm()
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],	post.title)
            message="Read Post At: \n{}\n\n{} 'Comments:\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject, message, 'kdileep1240@gmail.com', [cd['to']]) #use[]
            sent=True;
    else:
        form=EmailSendForm()
    return render(request,'BlogApp/sharebymail.html', {'post':post,'form':form,'sent':sent})


from BlogApp.forms import SignUpForm
from django.http import HttpResponseRedirect
def signup_view(request):
    formobj=SignUpForm()
    if request.method=="POST":
        formobj=SignUpForm(request.POST)
        user=formobj.save()
        user.set_password(user.password)
        user.save()
        return HttpResponseRedirect('/accounts/login/')
    return render(request, 'BlogApp/signup.html', {'formobj':formobj})


from django.contrib.auth.decorators import login_required
@login_required
def Blog_view(request):
    return render(request,'registration/login.html');

def Logout_view(request):
    request.session.clear()
    return render(request,'BlogApp/logout.html')




#Listview with pagination
from django.views.generic import ListView
class PostListView(ListView):
    model=Post
    paginate_by=1

'''
from django.views.generic import DetailView
class StudentDetailView(DetailView):
    model = Post;
'''
'''    
from django.views.generic import CreateView
class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
'''
from django.views.generic import UpdateView
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title','slug','author','body','publish','status','tags')

from django.urls import reverse_lazy
from django.views.generic import DeleteView
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('thanks')
from django.http import HttpResponseRedirect
from BlogApp.forms import AddForm
from BlogApp.models import Post
def CreatePost(request):
    #form = AddForm()
    print('hello')
    if request.method == 'POST':
        form = AddForm(request.POST,request.FILES)
        if form.is_valid():
            print('dk')
            Post = form.save(commit=True)
            return HttpResponseRedirect('/thanks/')
    else:
        form = AddForm()
    return render(request,'BlogApp/postmain.html',{'form':form})

def Thanks(request):
    return render(request,'BlogApp/thankyou.html')
def Homepage(request):
    return render(request,'BlogApp/Homepage.html')


def Success(request):
    return  render(request,'BlogApp/success.html')