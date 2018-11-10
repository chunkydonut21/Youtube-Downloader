import pafy
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat

from .forms import DownloadForm

def download_video(request):
    global context
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        if 'm.' in video_url:
            video_url = video_url.replace(u'm.', u'')

        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
            video_url = 'https://www.youtube.com/watch?v=' + video_id

        if len(video_url.split("=")[-1]) != 11:
            return HttpResponse('Enter correct url.')

        video = pafy.new(video_url)
        stream = video.streams
        video_audio_streams = []
        for s in stream:
            video_audio_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })

        stream_video = video.videostreams
        video_streams = []
        for s in stream_video:
            video_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })

        stream_audio = video.audiostreams
        audio_streams = []
        for s in stream_audio:
            audio_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })

        context = {
            'form': form,
            'title': video.title, 'streams': video_audio_streams,
            'description': video.description, 'likes': video.likes,
            'dislikes': video.dislikes, 'thumb': video.bigthumbhd,
            'duration': video.duration, 'views': video.viewcount,
            'stream_video': video_streams, 'stream_audio': audio_streams
        }

        return render(request, 'home.html', context)

    return render(request, 'home.html', { 'form': form })
