from ast import Return
from pyexpat.errors import messages
from urllib import response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import FileResponse
from django.shortcuts import render
import pathlib
import os
import mimetypes
from pytube import YouTube

from .forms import videoForm
from .downloader import download_vid



def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = videoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            urlv = form.cleaned_data['videoLnk']
            url = urlv
            yt = YouTube(url)
            video = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
            try:
                video.first().download('ytdownloaderApp/vids')

                print("Download complete for: ", yt.title)
            except Exception as e:
                print("Download failed due to: ", e)
            download(request, yt.title)
            return HttpResponseRedirect('/thanks/'+yt.title)
            
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = videoForm()

    return render(request, 'index.html', {'form': form})

def thx(request, id):
    return render(request, 'thx.html', {"id": id})

def error(request):
    return render(request, 'error.html')

def download(request, id):
# Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    # Define text file name
    filename = id + '.mp4'
    # Define the full file path
    filepath = BASE_DIR + '/ytdownloaderApp/vids/' + filename
    print(filepath)
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

def downloading(request):
    return render(request, 'downloading.html')
    