from __future__ import annotations

import json
import re
import ssl
import urllib.parse
import urllib.request

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
QUERIES = [
    "进击的巨人",
    "三体",
    "周杰伦",
    "奥本海默",
    "流浪地球",
]
NEXT_DATA_RE = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")


def inspect_pansearch(query: str) -> None:
    url = "https://www.pansearch.me/search?" + urllib.parse.urlencode({"q": query})
    text = fetch(url)
    match = NEXT_DATA_RE.search(text)
    print("PANSEARCH", query)
    if not match:
        print("NO_NEXT_DATA")
        print("====")
        return
    data = json.loads(match.group(1))
    payload = data.get("props", {}).get("pageProps", {}).get("data", {})
    print("TOTAL", payload.get("total"), "TIME", payload.get("time"))
    for item in payload.get("data", [])[:10]:
        print(item)
    print("====")


def inspect_dalipan(query: str) -> None:
    candidates = [
        "https://www.dalipan.com/search?" + urllib.parse.urlencode({"keyword": query}),
        "https://www.dalipan.com/search?" + urllib.parse.urlencode({"q": query}),
        "https://www.dalipan.com/s/" + urllib.parse.quote(query),
    ]
    print("DALIPAN", query)
    for url in candidates:
        try:
            text = fetch(url)
        except Exception as exc:
            print("URL", url, type(exc).__name__, exc)
            continue
        match = NEXT_DATA_RE.search(text)
        print("URL", url, "HAS_NEXT_DATA", bool(match), "HAS_QUERY", query in text)
        print(text[:1200])
        if match:
            try:
                data = json.loads(match.group(1))
                print("NEXT_KEYS", list(data.keys())[:10])
            except Exception as exc:
                print("NEXT_JSON_ERROR", exc)
        print("---")
    print("====")


for query in QUERIES:
    inspect_pansearch(query)

for query in QUERIES[:2]:
    inspect_dalipan(query)
