import urllib.request
import sys
import io

# 强制 stdout 为 UTF-8，解决 Windows 控制台 GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

if len(sys.argv) < 2:
    print("Usage: python fetch_url.py <url>")
    sys.exit(1)

url = sys.argv[1]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=10)
content = resp.read().decode('utf-8', errors='ignore')
print(content)
