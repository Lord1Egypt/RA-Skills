#!/usr/bin/env python3
"""
Reverse Image Search — find image source and visually similar images.
Usage: search.py <image_url_or_path> [engine] [limit]
Engines: yandex (default), google, bing, all
"""
import sys
import json
import asyncio
import os
from pathlib import Path

# Auto-activate sibling venv
_venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv")
if os.path.exists(_venv):
    for d in os.listdir(os.path.join(_venv, "lib")):
        sp = os.path.join(_venv, "lib", d, "site-packages")
        if os.path.exists(sp):
            sys.path.insert(0, sp)
            break

from PicImageSearch import Google, Bing, Yandex

ENGINES = {"yandex": Yandex, "google": Google, "bing": Bing}


def is_local_file(path: str) -> bool:
    if path.startswith(("http://", "https://", "ftp://")):
        return False
    return Path(path).exists()


def parse_results(resp, engine_name: str) -> list[dict]:
    results = []
    if not (resp and resp.raw):
        return results
    for item in resp.raw:
        r = {
            "title": getattr(item, "title", "") or "",
            "url": getattr(item, "url", "") or "",
            "thumbnail": getattr(item, "thumbnail", "") or "",
            "source_engine": engine_name,
        }
        for attr in ("similarity", "size", "source", "content"):
            val = getattr(item, attr, None)
            if val:
                r[attr] = str(val)[:300]
        if r["url"]:
            results.append(r)
    return results


async def search_engine(cls, input_path: str, name: str) -> list[dict]:
    try:
        engine = cls()
        if is_local_file(input_path):
            resp = await engine.search(file=input_path)
        else:
            resp = await engine.search(url=input_path)
        return parse_results(resp, name)
    except Exception as e:
        return [{"error": f"[{name}] {e}", "source_engine": name}]


async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: search.py <image_url_or_path> [engine] [limit]"}))
        sys.exit(1)

    input_path = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else "yandex"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    local = is_local_file(input_path)

    if engine == "all":
        tasks = {name: search_engine(cls, input_path, name) for name, cls in ENGINES.items()}
        all_results = {name: (await task)[:limit] for name, task in tasks.items()}
        output = {
            "status": 200,
            "query": input_path,
            "is_local_file": local,
            "engines": {k: {"count": len(v), "results": v} for k, v in all_results.items()},
        }
    elif engine in ENGINES:
        results = await search_engine(ENGINES[engine], input_path, engine)
        output = {
            "status": 200,
            "query": input_path,
            "is_local_file": local,
            "engine": engine,
            "total_found": len(results),
            "results": results[:limit],
        }
    else:
        output = {"error": f"Unknown engine: {engine}. Available: {', '.join(ENGINES)}, all"}

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
