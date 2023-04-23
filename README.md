# QDownload

# Description 描述:
Quick downloader for debian-based linux systems.
专为基于Debian的Linux系统打造的快速下载器。

Using python3.
使用python3搭建。

Requirements: requests, tqdm, multitasking, urllib3, retry
依赖模块：requests，tqdm，multitasking, urllib3, retry

# Program runtime 运行环境:
基于Debian的Linux系统，并安装了python3.7或以上版本。


# Usage 使用方法:
python QDownload.py (or 或) 
python3 QDownload.py

# Type 类型：
1. Quick-Download: General download.
快速下载：即正常下载

2. Block-Download: Using multitasking to download block-by-block.
分块下载：利用multitasking进行多线程下载

3. Github-Download: Using GHProxy (https://ghproxy.com/).
GITHUB加速下载：使用Ghproxy工具(https://ghproxy.com/)

4. AndroidFileHost-Download: Using script to hit download links.
AndroidFileHost下载：利用爬虫获取afh文件链接（速度较慢，可以获取链接后用分块下载加速）
