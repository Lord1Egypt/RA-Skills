#!/usr/bin/env python3
import argparse
import json
import sys
import requests
import trafilatura

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--timeout', type=int, default=20)
args = parser.parse_args()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
}
resp = requests.get(args.url, headers=headers, timeout=args.timeout)
resp.raise_for_status()
html = resp.text
text = trafilatura.extract(html, url=resp.url, include_links=True, include_images=False, favor_precision=True) or ''
result = {
    'url': resp.url,
    'status_code': resp.status_code,
    'title': trafilatura.extract_metadata(html, default_url=resp.url).title if trafilatura.extract_metadata(html, default_url=resp.url) else None,
    'text': text,
}
json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
print()
