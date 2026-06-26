#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    raise SystemExit(
        "Missing Playwright. Run `python scripts/bootstrap_env.py` first."
    ) from exc

from pipeline_common import (
    AUDIO_SUFFIXES,
    STREAM_SUFFIXES,
    USER_AGENT,
    VIDEO_SUFFIXES,
    classify_media_url,
    find_browser_executable,
    is_probable_media_url,
    sanitize_captured_headers,
)


def _candidate_score(
    url: str,
    *,
    kind: str,
    content_type: str = "",
    headers: dict[str, str] | None = None,
) -> int:
    lowered = url.lower()
    ctype = content_type.lower()
    suffix = Path(urlparse(url).path).suffix.lower()
    score = 200 if kind == "audio" else 100

    if suffix in AUDIO_SUFFIXES | VIDEO_SUFFIXES:
        score += 60
    elif suffix in STREAM_SUFFIXES:
        score += 30

    if ctype.startswith("audio/") or ctype.startswith("video/"):
        score += 40

    if "media-audio" in lowered or "media-video" in lowered:
        score += 30

    if any(token in lowered for token in ("playurl", "playlist", "manifest", "stream")):
        score += 15

    if headers:
        score += 5 * len(headers)

    return score


def _upsert_candidate(
    store: dict[str, dict[str, object]],
    candidate_url: str,
    *,
    content_type: str = "",
    headers: dict[str, str] | None = None,
) -> None:
    if not candidate_url.startswith(("http://", "https://")):
        return
    if not is_probable_media_url(candidate_url, content_type):
        return

    kind = classify_media_url(candidate_url, content_type)
    if kind is None:
        return

    clean_headers = sanitize_captured_headers(headers)
    candidate = {
        "url": candidate_url,
        "kind": kind,
        "content_type": content_type or None,
        "headers": clean_headers,
        "score": _candidate_score(
            candidate_url,
            kind=kind,
            content_type=content_type,
            headers=clean_headers,
        ),
    }

    existing = store.get(candidate_url)
    if existing is None:
        store[candidate_url] = candidate
        return

    if candidate["score"] > existing.get("score", 0):
        store[candidate_url] = candidate
        return

    if candidate["content_type"] and not existing.get("content_type"):
        existing["content_type"] = candidate["content_type"]

    merged_headers = dict(existing.get("headers") or {})
    merged_headers.update(clean_headers)
    existing["headers"] = merged_headers


def _trigger_page_media(page) -> None:
    try:
        page.evaluate(
            """
            () => {
              for (const video of document.querySelectorAll("video")) {
                video.muted = true;
                const promise = video.play();
                if (promise && promise.catch) {
                  promise.catch(() => {});
                }
              }
            }
            """
        )
    except Exception:
        pass

    selectors = [
        "video",
        "[aria-label*='play' i]",
        "[aria-label*='播放']",
        "[title*='play' i]",
        "[title*='播放']",
        "[class*='play']",
        "[id*='play']",
    ]

    for selector in selectors:
        try:
            locator = page.locator(selector).first
            locator.click(timeout=1500)
            page.wait_for_timeout(800)
        except PlaywrightTimeoutError:
            continue
        except Exception:
            continue


def extract_media_info(url: str, wait_seconds: int = 12) -> dict[str, object]:
    browser_executable = find_browser_executable()
    candidates: dict[str, dict[str, object]] = {}

    def collect(candidate_url: str, *, content_type: str = "", headers: dict[str, str] | None = None) -> None:
        _upsert_candidate(
            candidates,
            candidate_url,
            content_type=content_type,
            headers=headers,
        )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=browser_executable)
        page = browser.new_page(user_agent=USER_AGENT)
        page.on(
            "request",
            lambda request: collect(
                request.url,
                headers=getattr(request, "headers", None),
            ),
        )
        page.on(
            "response",
            lambda response: collect(
                response.url,
                content_type=(response.headers or {}).get("content-type", ""),
                headers=getattr(response.request, "headers", None),
            ),
        )
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(1500)
        _trigger_page_media(page)
        time.sleep(wait_seconds)
        title = page.title()
        final_url = page.url
        browser.close()

    audio_candidates = sorted(
        (item for item in candidates.values() if item["kind"] == "audio"),
        key=lambda item: (-int(item["score"]), str(item["url"])),
    )
    video_candidates = sorted(
        (item for item in candidates.values() if item["kind"] == "video"),
        key=lambda item: (-int(item["score"]), str(item["url"])),
    )

    best_audio = audio_candidates[0] if audio_candidates else None
    best_video = video_candidates[0] if video_candidates else None

    return {
        "source_url": url,
        "final_url": final_url,
        "title": title,
        "audio_urls": [str(item["url"]) for item in audio_candidates],
        "video_urls": [str(item["url"]) for item in video_candidates],
        "audio_candidates": audio_candidates,
        "video_candidates": video_candidates,
        "best_audio_url": best_audio["url"] if best_audio else None,
        "best_video_url": best_video["url"] if best_video else None,
        "best_audio_headers": best_audio["headers"] if best_audio else None,
        "best_video_headers": best_video["headers"] if best_video else None,
        "best_audio": best_audio,
        "best_video": best_video,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract audio/video URLs and common headers from a generic web page."
    )
    parser.add_argument("url", help="Web page URL")
    parser.add_argument("--wait-seconds", type=int, default=12, help="Extra wait time after page load")
    parser.add_argument("--output-json", help="Optional output JSON path")
    args = parser.parse_args()

    info = extract_media_info(args.url, wait_seconds=args.wait_seconds)
    rendered = json.dumps(info, ensure_ascii=False, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(rendered + "\n", encoding="utf-8")
        print(f"Saved media info to: {Path(args.output_json).resolve()}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
