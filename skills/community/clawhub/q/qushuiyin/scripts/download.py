#!/usr/bin/env python3
import requests
import sys
import os
import time

APP_ID = '115962'
APP_KEY = '密钥'
API_URL = 'https://qyapi.ipaybuy.cn/api/video'
SERVER_IP = '服务器ip'
VIDEO_DIR = '/www/wwwroot/default/videos'
BASE_URL = f'http://{SERVER_IP}:8899/videos'

def get_no_watermark_url(video_url: str) -> dict:
    headers = {'Content-Type': 'application/json'}
    data = {'appId': APP_ID, 'appKey': APP_KEY, 'url': video_url}
    resp = requests.post(API_URL, headers=headers, json=data, timeout=15)
    resp.raise_for_status()
    return resp.json()

def extract_download_url(result: dict) -> str | None:
    data = result.get('data') or {}
    if isinstance(data, str):
        return data if data.startswith('http') else None
    candidates = [
        data.get('url'), data.get('video_url'), data.get('video'),
        data.get('play_url'), data.get('wm_free_video_url'),
        result.get('url'), result.get('video_url'),
    ]
    for c in candidates:
        if c and isinstance(c, str) and c.startswith('http'):
            return c
    return None

def download_video(download_url: str, output_path: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'}
    resp = requests.get(download_url, stream=True, timeout=60, headers=headers, allow_redirects=True)
    resp.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
    return output_path

def process(video_url: str) -> dict:
    os.makedirs(VIDEO_DIR, exist_ok=True)
    result = get_no_watermark_url(video_url)
    if result.get('code') not in (200, 0):
        return {'success': False, 'error': result.get('msg', '解析失败')}
    dl_url = extract_download_url(result)
    if not dl_url:
        return {'success': False, 'error': f'未找到下载链接，API返回: {result}'}
    filename = f'video_{int(time.time())}.mp4'
    output_path = os.path.join(VIDEO_DIR, filename)
    download_video(dl_url, output_path)
    size = os.path.getsize(output_path)
    public_url = f'{BASE_URL}/{filename}'
    return {'success': True, 'path': output_path, 'size': size, 'public_url': public_url}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('FAIL:未提供链接')
        sys.exit(1)
    res = process(sys.argv[1])
    if res['success']:
        print(f"SUCCESS:{res['public_url']}:{res['size']}")
    else:
        print(f"FAIL:{res['error']}")
        sys.exit(1)
