#!/usr/bin/env python3
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import List, Dict, Any

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, "ignore")


def bing_search(query: str, limit: int = 5) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://www.bing.com/images/search?q={encoded}"
    html_text = fetch(url)
    matches = re.findall(r'murl&quot;:&quot;(.*?)&quot;', html_text)
    results = []
    seen = set()
    for m in matches:
        img = html.unescape(m)
        if not img.startswith("http"):
            continue
        if img in seen:
            continue
        seen.add(img)
        results.append({"image_url": img})
        if len(results) >= limit:
            break
    return {
        "engine": "bing",
        "search_url": url,
        "ok": bool(results),
        "results": results,
        "count": len(results),
    }


def baidu_search(query: str, limit: int = 5) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded}"
    html_text = fetch(url)
    low = html_text.lower()
    if "百度安全验证" in html_text or "security" in low and "verify" in low:
        return {
            "engine": "baidu",
            "search_url": url,
            "ok": False,
            "blocked": True,
            "reason": "baidu-security-check",
            "results": [],
            "count": 0,
        }

    patterns = [
        r'"thumbURL":"(.*?)"',
        r'"middleURL":"(.*?)"',
        r'"objURL":"(.*?)"',
    ]
    results = []
    seen = set()
    for pat in patterns:
        for m in re.findall(pat, html_text):
            img = html.unescape(m).replace('\\/', '/')
            if not img.startswith("http"):
                continue
            if img in seen:
                continue
            seen.add(img)
            results.append({"image_url": img})
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break
    return {
        "engine": "baidu",
        "search_url": url,
        "ok": bool(results),
        "blocked": False,
        "results": results,
        "count": len(results),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: search_first_image.py <query>", file=sys.stderr)
        return 1
    query = " ".join(sys.argv[1:]).strip()
    out: Dict[str, Any] = {"query": query}

    engines: List[Dict[str, Any]] = []
    for fn in (bing_search, baidu_search):
        try:
            engines.append(fn(query))
        except Exception as e:
            name = fn.__name__.replace("_search", "")
            encoded = urllib.parse.quote(query, safe="")
            fallback_url = (
                f"https://www.bing.com/images/search?q={encoded}"
                if name == "bing"
                else f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded}"
            )
            engines.append({
                "engine": name,
                "search_url": fallback_url,
                "ok": False,
                "error": str(e),
                "results": [],
                "count": 0,
            })

    out["engines"] = engines
    out["first_image"] = None
    for engine in engines:
        results = engine.get("results") or []
        if results:
            out["first_image"] = {
                "engine": engine["engine"],
                **results[0],
            }
            break
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
