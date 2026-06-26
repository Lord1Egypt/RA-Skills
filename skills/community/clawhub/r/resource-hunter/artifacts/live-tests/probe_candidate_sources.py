import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

QUERY = "The Merry Widow 1952"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TIMEOUT = 15

CANDIDATES = [
    {"name": "quark.so", "category": "pan", "url": f"https://quark.so/search?q={urllib.parse.quote(QUERY)}"},
    {"name": "lanzoux.com", "category": "pan", "url": "https://www.lanzoux.com/"},
    {"name": "lanzoui.com", "category": "pan", "url": "https://www.lanzoui.com/"},
    {"name": "znds.com", "category": "community", "url": f"https://www.znds.com/so/{urllib.parse.quote(QUERY)}"},
    {"name": "dmhy.org", "category": "anime", "url": f"https://dmhy.org/topics/list?keyword={urllib.parse.quote(QUERY)}"},
    {"name": "torrentgalaxy.to", "category": "torrent", "url": f"https://torrentgalaxy.to/torrents.php?search={urllib.parse.quote(QUERY)}"},
    {"name": "limetorrents.pro", "category": "torrent", "url": f"https://www.limetorrents.pro/search/all/{urllib.parse.quote(QUERY)}/"},
    {"name": "torlock2.com", "category": "torrent", "url": f"https://www.torlock2.com/all/torrents/{urllib.parse.quote(QUERY)}.html"},
    {"name": "solidtorrents.to", "category": "torrent", "url": f"https://solidtorrents.to/search?q={urllib.parse.quote(QUERY)}"},
    {"name": "torrentdownloads.pro", "category": "torrent", "url": f"https://www.torrentdownloads.pro/search/?search={urllib.parse.quote(QUERY)}"},
    {"name": "animetosho.org", "category": "anime", "url": f"https://animetosho.org/search?q={urllib.parse.quote(QUERY)}"},
    {"name": "ext.to", "category": "torrent", "url": f"https://ext.to/search/?q={urllib.parse.quote(QUERY)}"},
    {"name": "zooqle.com", "category": "torrent", "url": f"https://zooqle.com/search?q={urllib.parse.quote(QUERY)}"},
    {"name": "bing", "category": "index", "url": f"https://www.bing.com/search?q={urllib.parse.quote(QUERY + ' magnet OR pan')}"},
    {"name": "brave", "category": "index", "url": f"https://search.brave.com/search?q={urllib.parse.quote(QUERY + ' magnet OR pan')}"},
    {"name": "yandex", "category": "index", "url": f"https://yandex.com/search/?text={urllib.parse.quote(QUERY + ' magnet OR pan')}"},
    {"name": "searx.be", "category": "index", "url": f"https://searx.be/search?q={urllib.parse.quote(QUERY + ' magnet OR pan')}"},
    {"name": "btdig.com", "category": "torrent", "url": f"https://btdig.com/search?query={urllib.parse.quote(QUERY)}"},
    {"name": "btso.pw", "category": "torrent", "url": f"https://btso.pw/search/{urllib.parse.quote(QUERY)}"},
]


def title_of(html_text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html_text, re.I | re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def markers_of(html_text: str) -> list[str]:
    lowered = html_text.lower()
    markers = []
    checks = {
        "magnet": "magnet:?xt=urn:btih:",
        "torrent": "torrent",
        "search": "search",
        "login": "login",
        "captcha": "captcha",
        "cloudflare": "cloudflare",
        "results": "result",
        "forum": "forum",
        "pan": "网盘",
    }
    for key, needle in checks.items():
        if needle in lowered:
            markers.append(key)
    return markers


def probe(item: dict) -> dict:
    url = item["url"]
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT, context=ssl.create_default_context()) as response:
            body = response.read().decode("utf-8", errors="replace")
            elapsed = int((time.time() - started) * 1000)
            return {
                **item,
                "ok": True,
                "status": getattr(response, "status", 200),
                "final_url": response.geturl(),
                "content_type": response.headers.get_content_type(),
                "title": title_of(body),
                "markers": markers_of(body),
                "body_preview": body[:500],
                "elapsed_ms": elapsed,
                "content_length": len(body),
            }
    except Exception as exc:
        elapsed = int((time.time() - started) * 1000)
        return {
            **item,
            "ok": False,
            "error": str(exc),
            "elapsed_ms": elapsed,
        }


def main() -> int:
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(probe, item): item for item in CANDIDATES}
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item["name"])
    output = {
        "query": QUERY,
        "probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": results,
    }
    out_path = Path("skills/resource-hunter/artifacts/live-tests/candidate-source-probe.json")
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
