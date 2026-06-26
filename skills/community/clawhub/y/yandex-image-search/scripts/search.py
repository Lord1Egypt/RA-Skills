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
import random
from pathlib import Path
from datetime import datetime, timezone

# Auto-activate sibling venv
_venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv")
if os.path.exists(_venv):
    for d in os.listdir(os.path.join(_venv, "lib")):
        sp = os.path.join(_venv, "lib", d, "site-packages")
        if os.path.exists(sp):
            sys.path.insert(0, sp)
            break

from PicImageSearch import Bing, GoogleLens, Yandex
from PicImageSearch.utils import parse_html, read_file

ENGINES = {"yandex": Yandex, "google": GoogleLens, "bing": Bing}
RETRY_ATTEMPTS = {"yandex": 5, "google": 1, "bing": 1}
RETRY_DELAY_SECONDS = 1.5
YANDEX_BASE_URLS = ("https://yandex.com", "https://yandex.ru")


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


def has_usable_results(results: list[dict]) -> bool:
    return any(item.get("url") for item in results if not item.get("error"))


def all_results_are_errors(results: list[dict]) -> bool:
    return bool(results) and all(item.get("error") for item in results)


def extract_html_title(html: str) -> str:
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1 or end <= start + 7:
        return ""
    return html[start + 7 : end].strip()


def save_debug_html(prefix: str, base_url: str, html: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    host = base_url.replace("https://", "").replace("http://", "").replace("/", "_")
    out = f"/tmp/{prefix}-{host}-{ts}.html"
    Path(out).write_text(html, encoding="utf-8")
    return out


def parse_yandex_sites_from_data_state(data_state: str) -> list[dict]:
    try:
        data = json.loads(str(data_state))
    except Exception:
        return []

    sites = (
        data.get("initialState", {}).get("cbirSites", {}).get("sites")
        or data.get("cbirSites", {}).get("sites")
        or data.get("sites")
        or []
    )

    parsed = []
    for site in sites:
        if not isinstance(site, dict):
            continue
        url = site.get("url") or ""
        if not url:
            continue
        thumb = site.get("thumb", {}) if isinstance(site.get("thumb"), dict) else {}
        thumb_url = thumb.get("url") or ""
        if thumb_url.startswith("//"):
            thumb_url = f"https:{thumb_url}"
        original = (
            site.get("originalImage", {})
            if isinstance(site.get("originalImage"), dict)
            else {}
        )
        width = original.get("width")
        height = original.get("height")
        size = f"{width}x{height}" if width and height else ""
        parsed.append(
            {
                "title": site.get("title") or "",
                "url": url,
                "thumbnail": thumb_url,
                "source_engine": "yandex",
                "source": site.get("domain") or "",
                "content": site.get("description") or "",
                "size": size,
                "recovered_from_diagnostics": True,
            }
        )
    return parsed


def recover_yandex_results_from_html(html: str) -> list[dict]:
    pq = parse_html(html)
    selectors = [
        'div.Root[id^="ImagesApp-"]',
        'div[id^="ImagesApp-"][data-state]',
        'div[id^="ImagesApp-"]',
    ]
    for selector in selectors:
        node = pq.find(selector)
        if not len(node):
            continue
        data_state = node.attr("data-state")
        if not data_state:
            continue
        recovered = parse_yandex_sites_from_data_state(data_state)
        if recovered:
            return recovered
    return []


async def collect_yandex_diagnostics(input_path: str) -> tuple[list[dict], list[dict]]:
    diagnostics = []
    recovered_results = []
    local = is_local_file(input_path)
    for base_url in YANDEX_BASE_URLS:
        try:
            engine = Yandex(base_url=base_url)
            params = {"rpt": "imageview", "cbir_page": "sites"}
            if local:
                resp = await engine._send_request(
                    method="post",
                    params=params,
                    data={"prg": 1},
                    files={"upfile": read_file(input_path)},
                )
            else:
                resp = await engine._send_request(
                    method="get", params={**params, "url": input_path}
                )

            html = resp.text
            pq = parse_html(html)
            strict_node = pq.find('div.Root[id^="ImagesApp-"]')
            loose_node = pq.find('div[id^="ImagesApp-"]')
            recovered = recover_yandex_results_from_html(html)
            if recovered and not recovered_results:
                recovered_results = recovered
            html_path = save_debug_html("openclaw-yandex-debug", base_url, html)
            diagnostics.append(
                {
                    "base_url": base_url,
                    "status_code": resp.status_code,
                    "final_url": str(resp.url),
                    "title": extract_html_title(html),
                    "has_imagesapp": "ImagesApp-" in html,
                    "has_data_state": "data-state=" in html,
                    "strict_selector_count": len(strict_node),
                    "loose_selector_count": len(loose_node),
                    "strict_selector_has_data_state": bool(
                        strict_node.attr("data-state")
                    )
                    if len(strict_node)
                    else False,
                    "loose_selector_has_data_state": bool(loose_node.attr("data-state"))
                    if len(loose_node)
                    else False,
                    "recovered_result_count": len(recovered),
                    "recovered_preview": recovered[:3],
                    "has_captcha_marker": any(
                        marker in html.lower()
                        for marker in (
                            "smartcaptcha",
                            "are you not a robot",
                            "not a robot",
                            "captcha",
                        )
                    ),
                    "debug_html_path": html_path,
                }
            )
        except Exception as e:
            diagnostics.append(
                {
                    "base_url": base_url,
                    "diagnostic_error": str(e),
                }
            )
    return diagnostics, recovered_results


async def search_engine(cls, input_path: str, name: str) -> list[dict]:
    attempts = RETRY_ATTEMPTS.get(name, 1)
    last_error = None
    attempt_log = []

    for attempt in range(1, attempts + 1):
        yandex_base_url = None
        try:
            if name == "yandex":
                yandex_base_url = YANDEX_BASE_URLS[
                    (attempt - 1) % len(YANDEX_BASE_URLS)
                ]
                engine = cls(base_url=yandex_base_url)
            else:
                engine = cls()
            if is_local_file(input_path):
                resp = await engine.search(file=input_path)
            else:
                resp = await engine.search(url=input_path)
            if name == "yandex":
                attempt_log.append(
                    {
                        "attempt": attempt,
                        "base_url": yandex_base_url,
                        "ok": True,
                        "result_count": len(resp.raw) if resp and resp.raw else 0,
                    }
                )
            return parse_results(resp, name)
        except Exception as e:
            last_error = e
            if name == "yandex":
                attempt_log.append(
                    {
                        "attempt": attempt,
                        "base_url": yandex_base_url,
                        "ok": False,
                        "error": str(e),
                    }
                )
            if attempt < attempts:
                jitter = random.uniform(0.8, 1.2)
                await asyncio.sleep(RETRY_DELAY_SECONDS * attempt * jitter)

    if name == "yandex":
        diagnostics, recovered_results = await collect_yandex_diagnostics(input_path)
        if recovered_results:
            return recovered_results
        return [
            {
                "error": f"[{name}] {last_error}",
                "source_engine": name,
                "attempt_log": attempt_log,
                "diagnostics": diagnostics,
            }
        ]

    return [{"error": f"[{name}] {last_error}", "source_engine": name}]


async def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"error": "Usage: search.py <image_url_or_path> [engine] [limit]"}
            )
        )
        sys.exit(1)

    input_path = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else "yandex"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    local = is_local_file(input_path)
    exit_code = 0

    if engine == "all":
        yandex_results = (await search_engine(ENGINES["yandex"], input_path, "yandex"))[
            :limit
        ]
        all_results = {"yandex": yandex_results}
        skipped_engines = []

        if has_usable_results(yandex_results):
            for name in ("google", "bing"):
                all_results[name] = []
                skipped_engines.append(name)
        else:
            tasks = {
                name: search_engine(ENGINES[name], input_path, name)
                for name in ("google", "bing")
            }
            for name, task in tasks.items():
                all_results[name] = (await task)[:limit]

        usable_engines = [
            name for name, results in all_results.items() if has_usable_results(results)
        ]
        failed_engines = [
            name
            for name, results in all_results.items()
            if all_results_are_errors(results)
        ]
        empty_engines = [
            name
            for name, results in all_results.items()
            if not results and not has_usable_results(results)
        ]
        if failed_engines and not usable_engines:
            exit_code = 2
        output = {
            "status": 200 if exit_code == 0 else 502,
            "query": input_path,
            "is_local_file": local,
            "execution_strategy": "yandex-first-fallback",
            "usable_engines": usable_engines,
            "failed_engines": failed_engines,
            "empty_engines": empty_engines,
            "skipped_engines": skipped_engines,
            "engines": {
                k: {"count": len(v), "results": v} for k, v in all_results.items()
            },
        }
    elif engine in ENGINES:
        results = await search_engine(ENGINES[engine], input_path, engine)
        if all_results_are_errors(results):
            exit_code = 2
        output = {
            "status": 200 if exit_code == 0 else 502,
            "query": input_path,
            "is_local_file": local,
            "engine": engine,
            "has_usable_results": has_usable_results(results),
            "total_found": len(results),
            "results": results[:limit],
        }
    else:
        exit_code = 1
        output = {
            "error": f"Unknown engine: {engine}. Available: {', '.join(ENGINES)}, all"
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
