import re
import urllib.request
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
PAGES = {
    "bing": "https://www.bing.com/search?q=Attack%20on%20Titan%20magnet%20OR%20pan",
    "brave": "https://search.brave.com/search?q=Attack%20on%20Titan%20magnet%20OR%20pan",
}

for name, url in PAGES.items():
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    path = Path(f"skills/resource-hunter/artifacts/live-tests/{name}-attack-on-titan.html")
    path.write_text(html, encoding="utf-8")
    print(f"saved {name} -> {path}")
    print("contains b_algo:", "b_algo" in html)
    print("contains result__title:", "result__title" in html)
    print("contains href=\"http", html.count('href="http'))
    print("contains snippet text count:", html.lower().count("attack on titan"))
    print("first href matches:")
    hits = re.findall(r'href="(https?://[^"]+)"', html)
    for item in hits[:20]:
        print("  ", item)
    print("---")
