from __future__ import annotations

import re
import ssl
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
TARGETS = {
    "torlock": "https://www.torlock2.com/all/torrents/Attack%20on%20Titan.html",
    "limetorrents": "https://www.limetorrents.pro/search/all/Attack%20on%20Titan/",
}

for name, url in TARGETS.items():
    req = urllib.request.Request(url, headers=HEADERS)
    body = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
    out = Path(f"skills/resource-hunter/artifacts/live-tests/{name}-attack-on-titan.html")
    out.write_text(body, encoding="utf-8")
    print(f"saved {name} -> {out}")
    if name == "limetorrents":
        match = re.search(r"window\.location\.replace\('(.*?)'\)", body)
        print("redirect:", match.group(1) if match else "none")
