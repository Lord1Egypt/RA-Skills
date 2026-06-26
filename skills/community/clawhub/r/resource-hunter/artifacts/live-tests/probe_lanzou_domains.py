from __future__ import annotations

import ssl
import urllib.request

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
TARGETS = [
    "https://www.lanzoux.com/",
    "https://www.lanzoui.com/",
    "https://www.lanzoub.com/",
    "https://www.lanzout.com/",
    "https://www.ilanzou.com/",
]

for url in TARGETS:
    print("URL", url)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        body = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
        print("OK", len(body), body[:3000])
    except Exception as exc:
        print(type(exc).__name__, exc)
    print("====")
