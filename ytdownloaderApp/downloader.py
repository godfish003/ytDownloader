from pytube import YouTube
import sys
import ffmpeg
import os 
import subprocess

class Downloader(YouTube):

    def con(self, link):
        self.link = YouTube(link)
        self.hq = []

    def stream_objects(self):
        self.best = self.link.streams.filter(file_extension='mp4')
        q = [self.hq.append(x) for x in self.best.all()]
        self.best_vid_itag = str(self.best.all()[1]).split()[1].split('\"')[1]
        self.best_audio_itag = str(self.best.all()[-1]).split()[1].split('\"')[1]

    def downloader(self):
        vid = self.link.streams.get_by_itag(self.best_vid_itag)
        aud = self.link.streams.get_by_itag(self.best_audio_itag)
        print('Donwloading Video file...\n')
        vid.download('ytdownloaderApp/vids',filename='video.mp4')
        print('Video file downloaded... Now Trying download Audio file..\n')
        aud.download('ytdownloaderApp/vids',filename='audio.mp4')
        print('Audio file downloaded... Now Trying to merge audio and video files...\n')

    def merger(self):
        lin = str(self.link.title).rstrip()
        lin2 = ('ytdownloaderApp/vids/'+lin+'.mp4')
        subprocess.run(f'ffmpeg -i ytdownloaderApp/vids/video.mp4 -i ytdownloaderApp/vids/audio.mp4 -c copy "{lin2}"', shell=True)
        os.remove('ytdownloaderApp/vids/video.mp4')
        os.remove('ytdownloaderApp/vids/audio.mp4')
        print('Done....\n')

def dwl(lnk):
    a = Downloader(link = lnk)
    a.stream_objects()
    a.downloader()
    a.merger()