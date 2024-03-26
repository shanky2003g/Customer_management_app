from django.forms import ModelForm
#from django import forms
from .models import *

class orderForm(ModelForm):
    #a=forms.CharField(label="value1")
    class Meta:
        model=order
        fields='__all__' 