# !/usr/lib/python3
from __future__ import annotations
import datetime, os
import webbrowser as wbs
def logWrite(text, status):
    t = str(datetime.datetime.now())
    logName = "Log-" + t + ".txt"
    if os.path.isfile(logName):
        log = open(logName, "w")
        log.close()
    with open(logName, "a") as l:
        t = str(datetime.datetime.now())
        l.write("[" + status + "] " + t + " " + text)
        l.close()
logWrite("QDownload initiates.", "INFO")
logWrite("Imported modules: __future__, webbrowser, os, datetime", "INFO")
try:
    from tqdm import tqdm
    logWrite("Imported Module: tqdm", "INFO")
except ModuleNotFoundError:
    logWrite("Module not found: tqdm", "ERROR")
    c = input("[USER REQUEST] QDownload 需要tqdm模块以继续，是否安装(y/n)? ")
    logWrite("Requesting to install tqdm.", "USER REQUEST")
    if c == "y":
        logWrite("Request agreed.", "INFO")
        logWrite("Installing tqdm...", "INFO")
        os.system("pip install tqdm")
        os.system("pip3 install tqdm")
        import tqdm
        logWrite("Imported Module: tqdm", "INFO")
    else:
        logWrite("Request refused, exiting...", "INFO")
        exit()
try:
    import requests
    logWrite("Imported Module: requests", "INFO")
except ModuleNotFoundError:
    logWrite("Module not found: requests", "ERROR")
    c = input("[USER REQUEST] QDownload 需要requests模块以继续，是否安装(y/n)? ")
    logWrite("Requesting to install requests.", "USER REQUEST")
    if c == "y":
        logWrite("Request agreed.", "INFO")
        os.system("pip install requests")
        os.system("pip3 install requests")
        import requests
        logWrite("Imported Module: requests", "INFO")
    else:
        logWrite("Request refused, exiting...", "INFO")
        exit()
try:
    import multitasking
    logWrite("Imported Module: multitasking", "INFO")
except ModuleNotFoundError:
    logWrite("Module not found: multitasking", "ERROR")
    c = input("[USER REQUEST] QDownload 需要multitasking模块以继续，是否安装(y/n)? ")
    logWrite("Requesting to install multitasking.", "USER REQUEST")
    if c == "y":
        logWrite("Request agreed.", "INFO")
        os.system("pip install multitasking")
        os.system("pip3 install multitasking")
        import multitasking
        logWrite("Imported Module: multitasking", "INFO")
    else:
        logWrite("Request refused, exiting...", "INFO")
        exit()
import signal
try:
    from retry import retry
    logWrite("Imported Module: retry", "INFO")
except ModuleNotFoundError:
    logWrite("Module not found: retry", "ERROR")
    c = input("[USER REQUEST] QDownload 需要retry模块以继续，是否安装(y/n)? ")
    logWrite("Requesting to install retry.", "USER REQUEST")
    if c == "y":
        logWrite("Request agreed.", "INFO")
        os.system("pip install multitasking")
        os.system("pip3 install multitasking")
        import retry
        logWrite("Imported Module: retry", "INFO")
    else:
        logWrite("Request refused, exiting...", "INFO")
        exit()
try:
    import urllib
    logWrite("Imported Module: urllib3", "INFO")
except ModuleNotFoundError:
    logWrite("Module not found: urllib3", "ERROR")
    c = input("[USER REQUEST] QDownload 需要urllib3模块以继续，是否安装(y/n)? ")
    logWrite("Requesting to install urllib3.", "USER REQUEST")
    if c == "y":
        logWrite("Request agreed.", "INFO")
        os.system("pip install urllib3")
        os.system("pip3 install urllib3")
        import urllib
        logWrite("Imported Module: urllib3", "INFO")
    else:
        logWrite("Request refused, exiting...", "INFO")
        exit()
print("[INFO] 该版本是一个预览版本，意味着有某写功能没有完成/仍在调试，请用户积极反馈bug（在设置中可以反馈）")
print("[INFO] QDownload v1.2.1-pre1 正在初始化...")
print("[INFO] 正在准备下载引擎...")
print("[INFO] 准备完毕的引擎:\n (1) 正常下载\n (2) 分块下载\n (3) GITHUB加速下载\n (4) ANDROID-FILE-HOST文件下载\n")
print("[INFO] QDownload v1.2 新功能：输入5进入设置\n")
signal.signal(signal.SIGINT, multitasking.killall)
try:
    h = save("HEADERS.QDownload.conf", "r")
except:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
else:
    headers = {"User-Agent": h}
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
            raise ValueError('[ERROR] 该文件无法分块下载.')
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
    print(f'[INFO] 分块数量：{len(parts)}')
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
        print('[INFO] 下载 %s%%  %s/%s' % (downloaded, a * b, c))
def save(filepath, typ="r", text = None, encoding = "utf-8", errors = "ignore"):
    with open(filepath, typ, encoding = encoding, errors = errors) as file:
        if typ == "r":
            return file.read()
        elif typ == "w":
            file.write(text)
        elif typ == "a":
            file.write(text)
if "__main__" == __name__:
    while True:
        choice = int(input("[USER REQUEST] 请选择下载引擎（输入0退出）: "))
        if choice == 1:
            url = input("[USER REQUEST] 请输入文件下载链接: ")
            user = os.getlogin()
            filename = url[url.rindex('/') + 1:]
            print('文件名： ' + filename)
            downloaded = '0'
            path = '/home/{0}/QDownloads/'.format(user)
            if not os.path.exists(path):
                os.mkdir(path)
            response = urllib.request.urlretrieve(url, path + filename, download_listener)
        if choice == 2:
            url = input("[USER REQUEST] 请输入文件下载链接： ")
            user = os.getlogin()
            filename = url[url.rindex('/') + 1:]
            print('文件名： ' + filename)
            downloaded = '0'
            path = '/home/{0}/QDownloads/'.format(user)
            if not os.path.exists(path):
                os.mkdir(path)
            download(url, filename)
        if choice == 3:
            url = input("[USER REQUEST] 请输入文件下载链接（非git仓库地址）： ")
            url = "https://ghproxy.com/" + url
            user = os.getlogin()
            filename = url[url.rindex('/') + 1:]
            print('文件名： ' + filename)
            downloaded = '0'
            path = '/home/{0}/QDownloads/'.format(user)
            if not os.path.exists(path):
                os.mkdir(path)
            response = urllib.request.urlretrieve(url, path + filename, download_listener)
        if choice == 4:
            fid = input("[USER REQUEST] 请输入FID码（afh的链接以fid=xxxxxxxxxxxxxxxxxxxxxx结尾，把fid=后面的内容输入即可）： ")
            data = {'submit':'submit', 'action':'getdownloadmirrors', 'fid':fid}
            headers_afh = {'Content-Type':'application/x-www-form-urlencoded'}
            ret = requests.post(url = 'https://androidfilehost.com/libs/otf/mirrors.otf.php', data = data, headers = headers)
            content = ret.json()
            ret = requests.post(url = 'https://androidfilehost.com/libs/otf/mirrors.otf.php', data = data, headers = headers_afh)
            content = ret.json()
            if len(content['MIRRORS']) < 1:
                print('[ERROR] 没有可用的下载链接.')
                exit()
            flag = True
            for i in content['MIRRORS']:
                print(f"[INFO] 服务器名称: {i['name']}")
                print(f"[INFO] 下载地址: {i['url']}\r\n")
            if flag:
                c = input("[USER REQUEST] 是否下载下载该文件？ (y/n): ")
                if c == "y":
                    user = os.getlogin()
                    url = content["MIRRORS"][0]["url"]
                    print(url)
                    filename = url[url.rindex('/') + 1:]
                    print('文件名： ' + filename)
                    downloaded = '0'
                    path = '/home/{0}/QDownloads/'.format(user)
                    if not os.path.exists(path):
                        os.mkdir(path)
                    response = urllib.request.urlretrieve(url, path + filename, download_listener)
        if choice == 5:
            print("[INFO] 设置:\n (1) 下载Headers设置\n (2) 反馈bug\n")
            cc = int(input("[USER REQUEST] 请选择: "))
            if cc == 1:
                userheader = input("[USER REQUEST] 请输入headers的user-agent部分字段: ")
                headers["User-Agent"] = userheader
                print("[INFO] 修改已保存！")
                save("HEADER.QDownload.conf", "w", userheader)
            if cc == 2:
                wbs.open("https://github.com/dsz1714/qdownload/issues")
                print("[INFO] 程序正在将您导向bug反馈页面...")
        if choice == 0:
            break
                    
        




