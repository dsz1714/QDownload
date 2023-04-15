from __future__ import annotations
from tqdm import tqdm
import requests
import multitasking
import signal
from retry import retry
import os
print("[INFO] QDownload v1.1 initiates...")
print("[INFO] Preparing download engines...")
print("[INFO] Initited engines:\n (1) NORMAL DOWNLOAD\n (2) CHUNK DOWNLOAD\n (3) GHPROXY\n (4) ANDROID-FILE-HOST\n")
signal.signal(signal.SIGINT, multitasking.killall)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
MB = 1024**2

def split(start: int, end: int, step: int) -> list[tuple[int, int]]:
    parts = [(start, min(start+step, end))
             for start in range(0, end, step)]
    return parts
 
 
def get_file_size(url: str, raise_error: bool = False) -> int:
    response = requests.head(url)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('[ERROR] This file cannot be downloaded via the THREAD engine.')
        return file_size
    return int(file_size)
 
 
def download(url: str, file_name: str, retry_times: int = 3, each_size=16*MB) -> None:
    f = open(file_name, 'wb')
    file_size = get_file_size(url)
 
    @retry(tries=retry_times)
    @multitasking.task
    def start_download(start: int, end: int) -> None:
        _headers = headers.copy()
        _headers['Range'] = f'bytes={start}-{end}'
        response = session.get(url, headers=_headers, stream=True)
        chunk_size = 128
        chunks = []
        for chunk in response.iter_content(chunk_size=chunk_size):
            chunks.append(chunk)
            bar.update(chunk_size)
        f.seek(start)
        for chunk in chunks:
            f.write(chunk)
        del chunks
 
    session = requests.Session()
    each_size = min(each_size, file_size)
 
    parts = split(0, file_size, each_size)
    print(f'[INFO] Chunk counts：{len(parts)}')
    bar = tqdm(total=file_size, desc=f'[INFO] Download file：{file_name}')
    for part in parts:
        start, end = part
        start_download(start, end)
    multitasking.wait_for_tasks()
    f.close()
    bar.close()
def download_listener(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    new_downloaded = '%.1f' % per
    global downloaded
    if new_downloaded != downloaded:
        downloaded = new_downloaded
        print('[INFO] Download %s%%  %s/%s' % (downloaded, a * b, c))
 
if "__main__" == __name__:
    choice = int(input("[USER REQUEST] Please choose a download engine (hit 0 to exit): "))
    if choice == 1:
        url = input("[USER REQUEST] Please type/paste the file's url: ")
        user = os.getlogin()
        filename = url[url.rindex('/') + 1:]
        print('filename = ' + filename)
        downloaded = '0'
        path = '/home/{0}/QDownloads/'.format(user)
        if not os.path.exists(path):
            os.mkdir(path)
        response = urllib.request.urlretrieve(url, path + filename, download_listener)
    if choice == 2:
        url = input("[USER REQUEST] Please type/paste the file's url: ")
        user = os.getlogin()
        filename = url[url.rindex('/') + 1:]
        print('filename = ' + filename)
        downloaded = '0'
        path = '/home/{0}/QDownloads/'.format(user)
        if not os.path.exists(path):
            os.mkdir(path)
        download(url, filename)
    if choice == 3:
        url = input("[USER REQUEST] Please type/paste the file's url (file's url, not git addr.): ")
        url = "https://ghproxy.com/" + url
        user = os.getlogin()
        filename = url[url.rindex('/') + 1:]
        print('filename = ' + filename)
        downloaded = '0'
        path = '/home/{0}/QDownloads/'.format(user)
        if not os.path.exists(path):
            os.mkdir(path)
        response = urllib.request.urlretrieve(url, path + filename, download_listener)
    if choice == 4:
        fid = input("[USER REQUEST] Input fid (afh's file urls always have 'fid=xxxxxxxxx:'s at the ends): ")
        data = {'submit':'submit', 'action':'getdownloadmirrors', 'fid':fid}
        headers_afh = {'Content-Type':'application/x-www-form-urlencoded'}
        ret = requests.post(url = 'https://androidfilehost.com/libs/otf/mirrors.otf.php', data = data, headers = headers)
        content = ret.json()
        ret = requests.post(url = 'https://androidfilehost.com/libs/otf/mirrors.otf.php', data = data, headers = headers_afh)
        content = ret.json()
        if len(content['MIRRORS']) < 1:
            print('[ERROR] No download link available.')
            exit()
        flag = True
        for i in content['MIRRORS']:
            print(f"[INFO] Server name: {i['name']}")
            print(f"[INFO] Download link: {i['url']}\r\n")
        if flag:
            c = input("[USER REQUEST] Do you to download as well? (y/n): ")
            if c == "y":
                user = os.getlogin()
                url = content["MIRRORS"][0]["url"]
                filename = url[url.rindex('/') + 1:]
                print('filename = ' + filename)
                downloaded = '0'
                path = '/home/{0}/QDownloads/'.format(user)
                if not os.path.exists(path):
                    os.mkdir(path)
                response = urllib.request.urlretrieve(url, path + filename, download_listener)
        if choice == 0:
            exit()
