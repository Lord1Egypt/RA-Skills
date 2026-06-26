from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request
from itertools import islice

HEADERS = {"User-Agent": "Mozilla/5.0"}
QUERIES = [
    "site:www.znds.com/tv- 阿里云盘",
    "site:www.znds.com/tv- 夸克 网盘",
    "site:www.znds.com/tv- 影视 下载",
    "site:www.znds.com/tv- 网盘 分享",
]
BING_RE = re.compile(r'<li class="b_algo".*?<h2><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S | re.I)
THREAD_PAT = re.compile(r"https?://www\.znds\.com/tv-\d+-\d+-\d+\.html")
RESOURCE_PAT = re.compile(r"https?://[^\s\"'<>]+|magnet:\?[^\s\"'<>]+", re.I)
PASS_PAT = re.compile(r"(?:提取码|访问码|密码)[:：]?\s*([A-Za-z0-9]{3,8})")

for query in QUERIES:
    print("QUERY", query)
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers=HEADERS)
    text = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    hits = BING_RE.findall(text)
    thread_urls: list[str] = []
    for href, title in hits:
        href = html.unescape(href)
        title = re.sub(r"<[^>]+>", " ", html.unescape(title)).strip()
        m = THREAD_PAT.search(href)
        if m:
            thread_urls.append(m.group(0))
            print("THREAD", m.group(0), "TITLE", title)
    if not thread_urls:
        print("NO THREADS")
        print("====")
        continue
    for thread_url in islice(thread_urls, 0, 3):
        print("FETCH", thread_url)
        req = urllib.request.Request(thread_url, headers=HEADERS)
        body = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        resources = RESOURCE_PAT.findall(body)
        resources = [item for item in resources if any(sig in item for sig in ("pan.", "drive", "aliyun", "quark", "lanzou", "baidu", "magnet:?", "115.com", "alipan"))]
        passes = PASS_PAT.findall(body)
        print("RESOURCE_COUNT", len(resources))
        for item in resources[:10]:
            print("RES", item)
        print("PASSWORDS", passes[:10])
        print("---")
    print("====")
