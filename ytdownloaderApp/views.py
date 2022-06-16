from asyncio import exceptions
from pyexpat.errors import messages
import re
import random
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from wsgiref.util import FileWrapper
from django.shortcuts import render
import os
from pytube import YouTube
import subprocess

from .forms import videoForm




def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = videoForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['videoLnk']
            format = form.cleaned_data['type']
            yt=YouTube(link)
            vid_id=str(random.randrange(1000000,9999999))
            try:
                download_server(yt, vid_id, format)
            except Exception as e:
                print("Download failed due to: ", e)
            
            return HttpResponseRedirect('/thanks/'+vid_id+'/'+format)
    else:
        form = videoForm()

    return render(request, 'index.html', {'form': form})

def thx(request, id, format):
    return render(request, 'thx.html', {"id": id, "format": format})

def error(request, e):
    return render(request, 'error.html', {"e" : e})

def download_client(request, id, format):
# Define Django project base directory
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)
        # Define text file name
        reg = re.search("[0-9]{7}", id)
        if not reg:
            return error(request, 'bad file')
        filename = id + '.' + str(format)
        if format=='mp3':
            filename = 'aud' + filename
        # Define the full file path
        filepath = BASE_DIR + '/ytdownloaderApp/vids/' + filename
        print(filepath)
        # Open the file for reading content

        file = FileWrapper(open(filepath, 'rb'))
        # Set the return value of the HttpResponse
        if format=='mp4':
            response = HttpResponse(file, content_type='video/mp4')
        if format=='mp3':
            response = HttpResponse(file, content_type='audio/mp3')
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    except Exception as e :
        error(request, e)



def download_server(yt, vid_id, format):
        yt.hq = []
        yt.best = yt.streams.filter(file_extension='mp4')
        q = [yt.hq.append(x) for x in yt.best.all()]
        yt.best_vid_itag = str(yt.best.all()[1]).split()[1].split('\"')[1]
        yt.best_audio_itag = str(yt.best.all()[-1]).split()[1].split('\"')[1]
        vid = yt.streams.get_by_itag(yt.best_vid_itag)
        aud = yt.streams.get_by_itag(yt.best_audio_itag)
        lin = ('ytdownloaderApp/vids/'+vid_id+'.mp4')
        aud_name = ('aud'+vid_id+'.'+format)
        aud.download('ytdownloaderApp/vids',filename=aud_name)
        if format=='mp4':
            vid.download('ytdownloaderApp/vids',filename='vid'+vid_id+'.mp4')
            subprocess.run(f'ffmpeg -i ytdownloaderApp/vids/vid{vid_id}.mp4 -i ytdownloaderApp/vids/{aud_name} -c copy "{lin}"', shell=True)
            os.remove('ytdownloaderApp/vids/vid'+vid_id+'.mp4')
            os.remove('ytdownloaderApp/vids/'+aud_name)

def downloading(request):
    return render(request, 'downloading.html')