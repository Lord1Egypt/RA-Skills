from __future__ import annotations

import re
import ssl
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
TARGETS = {
    "pansearch-search-bundle": "https://cdn.pansearch.me/_next/static/chunks/pages/search-9642d6cad95f44ba.js",
    "dalipan-app-bundle": "https://res.hexiaotu.com/sousuo/dalipan/js/app.a1a3a827.js",
}
KEYWORDS = [
    "api",
    "search",
    "axios",
    "fetch(",
    "keyword",
    "query",
    "aliyundrive",
    "quark",
    "baidu",
    "xunlei",
    "/search",
    "/api",
    "https://",
]

for name, url in TARGETS.items():
    req = urllib.request.Request(url, headers=HEADERS)
    text = urllib.request.urlopen(req, timeout=30, context=CTX).read().decode("utf-8", "replace")
    out = Path(f"skills/resource-hunter/artifacts/live-tests/{name}.js")
    out.write_text(text, encoding="utf-8")
    print("saved", out)
    for key in KEYWORDS:
        print(key, text.lower().count(key.lower()))
    print("sample urls")
    urls = sorted(set(re.findall(r"https?://[^\"'`\s)]+|/[A-Za-z0-9_./?=&%-]{3,}", text)))
    for item in urls[:80]:
        print(item)
    print("====")
