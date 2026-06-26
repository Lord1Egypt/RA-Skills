#!/usr/bin/env python3
import argparse
import collections
import json
import sys
from urllib.parse import urljoin, urldefrag, urlparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--limit', type=int, default=10)
parser.add_argument('--timeout', type=int, default=15)
args = parser.parse_args()

start = args.url
start_host = urlparse(start).netloc
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'}
seen = set()
queue = collections.deque([start])
results = []

while queue and len(results) < args.limit:
    url = queue.popleft()
    if url in seen:
        continue
    seen.add(url)
    try:
        resp = requests.get(url, headers=headers, timeout=args.timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        title = soup.title.get_text(' ', strip=True) if soup.title else None
        links = []
        for a in soup.select('a[href]'):
            href = a.get('href')
            full = urldefrag(urljoin(resp.url, href))[0]
            if urlparse(full).scheme not in ('http', 'https'):
                continue
            if urlparse(full).netloc != start_host:
                continue
            links.append(full)
        links = list(dict.fromkeys(links))
        results.append({'url': resp.url, 'title': title, 'links': links[:50]})
        for link in links:
            if link not in seen and len(seen) + len(queue) < args.limit * 5:
                queue.append(link)
    except Exception as e:
        results.append({'url': url, 'error': str(e)})

json.dump({'start_url': start, 'results': results}, sys.stdout, ensure_ascii=False, indent=2)
print()
