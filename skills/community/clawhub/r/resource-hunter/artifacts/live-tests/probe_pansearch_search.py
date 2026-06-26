from __future__ import annotations

import ssl
import urllib.request

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
URLS = [
    "https://www.pansearch.me/search?q=Attack%20on%20Titan",
    "https://www.pansearch.me/api/search?q=Attack%20on%20Titan",
    "https://www.pansearch.me/api?keyword=Attack%20on%20Titan",
    "https://www.pansearch.me/?q=Attack%20on%20Titan",
]

for url in URLS:
    print("URL", url)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        text = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
        print(text[:5000])
    except Exception as exc:
        print(type(exc).__name__, exc)
    print("====")
