#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

from search_first_image import main as _unused  # noqa: F401
import search_first_image as sfi

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


def guess_ext(url: str, content_type: str | None) -> str:
    if content_type:
        ct = content_type.lower()
        if "jpeg" in ct or "jpg" in ct:
            return ".jpg"
        if "png" in ct:
            return ".png"
        if "gif" in ct:
            return ".gif"
        if "webp" in ct:
            return ".webp"
    m = re.search(r"\.([a-zA-Z0-9]{2,5})(?:$|\?)", url)
    if m:
        ext = "." + m.group(1).lower()
        if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def download(url: str, query: str) -> tuple[str, int, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.bing.com/"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type")
    ext = guess_ext(url, content_type)
    safe = re.sub(r"[^\w\-\u4e00-\u9fff]+", "_", query).strip("_") or "image"
    out_dir = Path("/home/mumu/clawd/tmp/search-image")
    out_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=f"{safe}_", suffix=ext, dir=out_dir)
    os.close(fd)
    with open(tmp_path, "wb") as f:
        f.write(data)
    return tmp_path, len(data), content_type


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fetch_first_image.py <query>", file=sys.stderr)
        return 1
    query = " ".join(sys.argv[1:]).strip()
    result = {"query": query}
    search = {
        "query": query,
        "engines": [],
        "first_image": None,
    }
    for fn in (sfi.bing_search, sfi.baidu_search):
        try:
            search["engines"].append(fn(query))
        except Exception as e:
            name = fn.__name__.replace("_search", "")
            search["engines"].append({"engine": name, "ok": False, "error": str(e), "results": []})
    for engine in search["engines"]:
        results = engine.get("results") or []
        if results:
            search["first_image"] = {"engine": engine["engine"], **results[0]}
            break
    result["search"] = search
    first = search.get("first_image")
    if not first:
        result["ok"] = False
        result["reason"] = "no-image-found"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    try:
        path, size, content_type = download(first["image_url"], query)
        result["ok"] = True
        result["image_url"] = first["image_url"]
        result["engine"] = first["engine"]
        result["path"] = path
        result["size"] = size
        result["content_type"] = content_type
    except Exception as e:
        result["ok"] = False
        result["reason"] = "download-failed"
        result["image_url"] = first["image_url"]
        result["engine"] = first["engine"]
        result["error"] = str(e)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
