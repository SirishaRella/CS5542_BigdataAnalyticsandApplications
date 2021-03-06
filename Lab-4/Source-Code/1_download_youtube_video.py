from pytube import YouTube
import os


def download_video(video_url, file_name):
    yt = YouTube(video_url)

    YouTube(video_url).streams.first().download('test_data//video', file_name)

    file_path = 'test_data/youtube_captions/' + file_name + '.txt'
    en_caption = yt.captions.get_by_language_code('en')
    en_caption_convert_to_srt = (en_caption.generate_srt_captions())
    text_file = open(file_path, "w")
    text_file.write(en_caption_convert_to_srt)
    text_file.close()


video_url = "https://youtu.be/ElqbG-xfsdg"
file_name = "1"
download_video(video_url, file_name)
