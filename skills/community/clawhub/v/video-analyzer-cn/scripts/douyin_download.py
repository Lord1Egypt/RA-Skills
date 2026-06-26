"""抖音视频下载 - 通过浏览器提取的视频URL下载"""
import urllib.request, sys

def download(video_url, output_path):
    """带Referer下载抖音视频"""
    sys.stdout.reconfigure(encoding='utf-8')
    headers = {
        'Referer': 'https://www.douyin.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(video_url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=60)
    data = resp.read()
    with open(output_path, 'wb') as f:
        f.write(data)
    print(f'Downloaded: {len(data)/1024/1024:.1f} MB -> {output_path}')
    return output_path

if __name__ == '__main__':
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\39535\.openclaw\workspace\tmp\douyin.mp4'
    download(url, output)
