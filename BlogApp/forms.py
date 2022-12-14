from django import forms
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)



#model-based-form for comments
from django import forms
from BlogApp.models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
       model=Comment
       fields=('name','email','body')

from django import forms;
from django.contrib.auth.models import User
class SignUpForm(forms.ModelForm):
    class Meta:
        model=User		#it is mysql-db model-table(for auth_app_db)
        fields=['username', 'password','email','first_name','last_name'];


from django import forms
from BlogApp.models import Post
class AddForm(forms.ModelForm):
    class Meta:
       model=Post
       fields=('title','slug','author','body','publish','status','tags')