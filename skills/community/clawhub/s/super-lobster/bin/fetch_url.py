#!/usr/bin/env python3
import argparse
import json
import sys
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--timeout', type=int, default=20)
args = parser.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
}
resp = requests.get(args.url, headers=headers, timeout=args.timeout)
resp.raise_for_status()
content_type = resp.headers.get('content-type', '')
out = {
    'url': resp.url,
    'status_code': resp.status_code,
    'content_type': content_type,
    'encoding': resp.encoding,
}
if 'html' in content_type:
    soup = BeautifulSoup(resp.text, 'lxml')
    title = soup.title.get_text(' ', strip=True) if soup.title else None
    text = soup.get_text('
', strip=True)
    out['title'] = title
    out['text_preview'] = text[:4000]
    out['html_preview'] = resp.text[:4000]
else:
    out['body_preview'] = resp.text[:4000]
json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
print()
