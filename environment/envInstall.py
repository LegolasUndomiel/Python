# coding=utf-8
# gcc g++ build-essential perl make cmake code xmake
# texlive openmpi cuda blender OpenGL OpenCV OpenMP
# anaconda matplotlib numpy cupy sympy manimGL
# WebGL
import os
import threading
import subprocess
import requests
from tqdm import tqdm


def download(url, path):
    fName = url.split('/')[-1]
    fPath = os.path.join(path, fName)
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    bar = tqdm(desc=fName, total=total, unit='iB', unit_scale=True, unit_divisor=1024, leave=False)
    with open(fPath, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    bar.close()
    file.close()


def parallel(urls, path):
    threads = []
    for url in urls:
        t = threading.Thread(target=download, args=(url, path))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('\r', end='')
    for url in urls:
        print('Done: \t%-40s %4s' % (url.split('/')[-1], '下载成功'))


def fontsInstall():
    path = 'fonts'
    urls = ['https://github.com/ryanoasis/nerd-fonts/releases/latest/download/0xProto.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/AnonymousPro.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Arimo.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/AurulentSansMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/BitstreamVeraSansMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/CascadiaCode.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/CodeNewRoman.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/CommitMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Go-Mono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Noto.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/RobotoMono.tar.xz',
            'https://github.com/laishulu/Sarasa-Term-SC-Nerd/releases/latest/download/sarasa-term-sc-nerd.ttf.tar.gz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/SpaceMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Tinos.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Ubuntu.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/UbuntuMono.tar.xz',
            'https://github.com/ryanoasis/nerd-fonts/releases/latest/download/UbuntuSans.tar.xz']

    if not os.path.exists(path):
        os.makedirs(path)

    print('-'*90)
    print('Fonts Downloading...')
    print('-'*90)

    parallel(urls, path)

    print('-'*90)
    print('Fonts Installing...')
    print('-'*90)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.tar.xz') or file.endswith('.tar.gz'):
                dName = file.split('.')[0]
                dPath = os.path.join(root, dName)
                if not os.path.exists(dPath):
                    os.makedirs(dPath)

                p = subprocess.Popen('tar -xf %s -C %s' %(os.path.join(root, file), dPath), shell=True)
                p.wait()
                if not p.returncode:
                    print('Done: \t%-40s %4s' % (dName, '安装成功'))


if __name__ == '__main__':
    fontsInstall()
