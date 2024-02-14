import argparse
import os
import re
import subprocess

from pytube import YouTube


def download_audio(yt: YouTube):
    # 오디오 추출
    print(f"Download [{yt.title}] from YouTube Audio")
    yt.streams \
        .filter(type='audio') \
        .order_by('abr') \
        .desc() \
        .first() \
        .download()
    base_dir = os.path.abspath('.')
    title = re.sub(r'[,|#\'?:]', '', yt.title)
    webm = title + '.webm'
    mp3 = title + '.mp3'
    print(f"Convert [{webm}]\n     to [{mp3}]\n")
    cmd = ['ffmpeg', '-i', webm, '-vn', '-y', mp3]
    subprocess.run(cmd, cwd=base_dir, check=True)
    os.remove(os.path.join(base_dir, webm))


def download_video(yt: YouTube):
    # video 추출
    print(f"Download [{yt.title}] from YouTube Video")
    yt.streams \
        .filter(resolution='1080p', mime_type='video/mp4') \
        .first() \
        .download()


def download(url: str):
    yt = YouTube(url)
    download_audio(yt)
    download_video(yt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest="url", type=str, required=True)
    args = parser.parse_args()

    download(args.url)
