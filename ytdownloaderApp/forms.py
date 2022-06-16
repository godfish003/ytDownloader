from unicodedata import name
from django import forms

class videoForm(forms.Form):
    videoLnk = forms.CharField(label='Link', max_length=200)
    formats = (
        ('mp4', 'mp4'),
        ('mp3', 'mp3')
    )
    type = forms.ChoiceField(label='Format', choices=formats)