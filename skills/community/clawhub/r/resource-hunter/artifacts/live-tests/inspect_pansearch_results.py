from __future__ import annotations

import html
import re
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
QUERY = "Attack on Titan"
URL = "https://www.pansearch.me/search?" + urllib.parse.urlencode({"q": QUERY})

req = urllib.request.Request(URL, headers=HEADERS)
text = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
path = Path("skills/resource-hunter/artifacts/live-tests/pansearch-attack-on-titan.html")
path.write_text(text, encoding="utf-8")
print("saved", path)
for token in ["__NEXT_DATA__", "Attack on Titan", "pan.quark.cn", "aliyundrive", "magnet:?", "提取码", "searchData", "result"]:
    print(token, token in text, text.lower().count(token.lower()))

patterns = [
    re.compile(r'href="(https?://[^"]+)"', re.I),
    re.compile(r'magnet:\?[^\s\"\'<>]+', re.I),
]
for pattern in patterns:
    hits = pattern.findall(text)
    print("pattern", pattern.pattern, "count", len(hits))
    for item in hits[:20]:
        if isinstance(item, tuple):
            item = item[0]
        print("HIT", html.unescape(item))
