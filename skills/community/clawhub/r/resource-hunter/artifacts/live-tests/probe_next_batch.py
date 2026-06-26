from __future__ import annotations

import ssl
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()
TARGETS = {
    "solidtorrents": "https://solidtorrents.to/",
    "torrentgalaxy": "https://torrentgalaxy.to/",
    "torlock-home": "https://www.torlock2.com/",
    "limetorrents-home": "https://www.limetorrents.pro/",
}

for name, url in TARGETS.items():
    print(f"== {name} ==")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        body = urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")
        path = Path(f"skills/resource-hunter/artifacts/live-tests/{name}.html")
        path.write_text(body, encoding="utf-8")
        print("saved", path)
        print(body[:3000])
    except Exception as exc:
        print(type(exc).__name__, exc)
