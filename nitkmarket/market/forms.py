from django.forms import ModelForm
from market.models import Profile,item
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db import models


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address','birth_date','mobile')

class ImageForm(forms.ModelForm):
    class Meta:
        model= item
        labels = {
        "title": "Title of advertisement ",
        "description":"Description of your product",
        "price":"Maximum asking price       ",
        "imagefile":"Upload an image of your product",
        "type":"Rent or Sell??        ",
        "tag":"Some keywords associated with the product",
    }
        fields= ('title','description','price','imagefile','type','tag' )

class query(forms.Form):
    keyword=forms.CharField(max_length=100)
