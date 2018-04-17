from __future__ import unicode_literals
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


'''
class Postform(forms.Form):
    title=forms.CharField(max_length=50,widget=forms.
                          TextInput(attrs={'placeholder':'Title'}))
    content=forms.CharField(widget=forms.
Textarea(attrs=
         {'placeholder':'Comment','rows':4,'cols':30,'style':'resize:none'}))
    
'''
#here no need to define all the fields
class ArticleForm(forms.ModelForm):
    title=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'id':'textinput', 'name':'textinput', 'type':'text', 'placeholder':'Enter the title'}))
    content=forms.CharField(widget=CKEditorUploadingWidget(attrs={'class':'form-control', 'id':'textarea', 'name':'textarea'}))
    pic=models.ImageField()
    class Meta:
        model=Article
        fields=['title','content','pic','category','tags'] 
        #fields='__all__'
"""class Regforms(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(),
    max_length=30,required=True)
    email=forms.CharField(widget=forms.EmailInput(),
    max_length=30,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),
    max_length=30,required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(),
    label="Confirm your password", max_length=30,required=True)
    class Meta:
        model=User
        fields=['username','email','password','confirm_password']

    def clean(self):
        cleaned_data = super(Regforms, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )"""

class AudienceSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_audience = True
        user.save()
        audience = Audience.objects.create(user=user)
        audience.interests.add(*self.cleaned_data.get('interests'))
        return user

class StaffSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            staff = Staff.objects.create(user=user)
        return user

class AudienceInterestsForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class MyProfile(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput
                             (),
                             max_length=30,
                             required=True)
    
    last_name=forms.CharField(widget=forms.TextInput
                             (),
                             max_length=30,
                             required=True)

    email=forms.CharField(widget=forms.EmailInput
                             (),
                             max_length=30,
                             required=True)
    bio=forms.CharField(widget=forms.TextInput
                             (),
                             max_length=100,
                             required=True)
    profilepic=forms.FileField(required=True)
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','profilepic','bio']
        

class Password(forms.ModelForm):
    old_password=forms.CharField(widget=forms.PasswordInput
                             (),
                             max_length=30,
                             label="Old password",
                             required=True)
    new_password=forms.CharField(widget=forms.PasswordInput
                             (),
                             max_length=30,
                             label="New password",
                             required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput
                             (),
                             max_length=30,
                             label="Confirm new password",
                             required=True)

    
        
    class Meta:
        model=User
        fields=['old_password','new_password','confirm_password']

class CommentForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput
                             (),
                             max_length=30,
                             required=True)
    body=forms.CharField(widget=forms.Textarea
                             (),
                             max_length=300,
                             required=True)
    class Meta:
        model = Comment
        fields = ('name', 'body')        