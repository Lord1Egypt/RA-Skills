#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    raise SystemExit(
        "Missing Playwright. Run `python scripts/bootstrap_env.py` first."
    ) from exc

from pipeline_common import USER_AGENT, find_browser_executable, sanitize_captured_headers


def _looks_like_audio(url: str, content_type: str = "") -> bool:
    lowered = url.lower()
    ctype = content_type.lower()
    return (
        "media-audio" in lowered
        or "/audio" in lowered
        or "audio/" in ctype
        or "mime_type=audio" in lowered
    )


def _looks_like_video(url: str, content_type: str = "") -> bool:
    lowered = url.lower()
    ctype = content_type.lower()
    return (
        "media-video" in lowered
        or ".mp4" in lowered
        or ".m3u8" in lowered
        or "video/" in ctype
        or "mime_type=video" in lowered
    )


def _is_relevant(url: str) -> bool:
    lowered = url.lower()
    return (
        "toutiaovod.com" in lowered
        or "toutiao.com" in lowered
        or ".mp4" in lowered
        or ".m3u8" in lowered
        or "media-audio" in lowered
        or "media-video" in lowered
    )


def extract_media_info(url: str, wait_seconds: int = 12) -> dict[str, object]:
    browser_executable = find_browser_executable()
    audio_candidates: dict[str, dict[str, object]] = {}
    video_candidates: dict[str, dict[str, object]] = {}

    def collect(
        candidate_url: str,
        content_type: str = "",
        headers: dict[str, str] | None = None,
    ) -> None:
        if not _is_relevant(candidate_url):
            return
        candidate = {
            "url": candidate_url,
            "content_type": content_type or None,
            "headers": sanitize_captured_headers(headers),
        }
        if _looks_like_audio(candidate_url, content_type):
            audio_candidates.setdefault(candidate_url, candidate)
        elif _looks_like_video(candidate_url, content_type):
            video_candidates.setdefault(candidate_url, candidate)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=browser_executable)
        page = browser.new_page(user_agent=USER_AGENT)
        page.on("request", lambda request: collect(request.url, headers=getattr(request, "headers", None)))
        page.on(
            "response",
            lambda response: collect(
                response.url,
                (response.headers or {}).get("content-type", ""),
                headers=getattr(response.request, "headers", None),
            ),
        )
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        time.sleep(wait_seconds)
        title = page.title()
        final_url = page.url
        browser.close()

    audio_list = list(audio_candidates.values())
    video_list = list(video_candidates.values())
    best_audio = audio_list[0] if audio_list else None
    best_video = video_list[0] if video_list else None

    return {
        "source_url": url,
        "final_url": final_url,
        "title": title,
        "audio_urls": [str(item["url"]) for item in audio_list],
        "video_urls": [str(item["url"]) for item in video_list],
        "audio_candidates": audio_list,
        "video_candidates": video_list,
        "best_audio_url": best_audio["url"] if best_audio else None,
        "best_video_url": best_video["url"] if best_video else None,
        "best_audio_headers": best_audio["headers"] if best_audio else None,
        "best_video_headers": best_video["headers"] if best_video else None,
        "best_audio": best_audio,
        "best_video": best_video,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract audio/video URLs from a Toutiao video page.")
    parser.add_argument("url", help="Toutiao page URL")
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
