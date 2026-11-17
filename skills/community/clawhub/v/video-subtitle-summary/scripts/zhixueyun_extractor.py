#!/usr/bin/env python3
"""ZhiXueYun subtitle extractor — Playwright API route interception approach.

Battle-tested workflow for extracting AI knowledge point summaries and
DOM subtitles from kc.zhixueyun.com course pages.

Usage:
    python zhixueyun_extractor.py <course-url-or-uuid> [--output-dir .temp]
    python zhixueyun_extractor.py "https://kc.zhixueyun.com/#/study/course/detail/7e98894b-..." --output-dir .temp
    python zhixueyun_extractor.py 7e98894b-e1e0-4c12-abce-19cfb353f37c --output-dir .temp

Requires: playwright (pip install playwright && playwright install chromium)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path


def extract_uuid(input_str: str) -> str | None:
    """Extract a UUID from URL or raw string."""
    uuid_match = re.search(
        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        input_str,
        re.IGNORECASE,
    )
    return uuid_match.group(1) if uuid_match else None


def build_course_url(course_uuid: str) -> str:
    return f"https://kc.zhixueyun.com/#/study/course/detail/{course_uuid}"


async def extract_zhixueyun(course_uuid: str, output_dir: str) -> dict:
    """Extract subtitles and knowledge points from a ZhiXueYun course page.

    Launches a non-headless Chromium browser, waits for the user to log in
    manually, then navigates to the course detail page and intercepts API
    responses to capture course metadata, AI knowledge summaries, and DOM
    subtitle text.
    """
    from playwright.async_api import async_playwright

    course_url = build_course_url(course_uuid)
    captured: dict = {}

    async def on_response(response):
        url = response.url
        try:
            if "course-info/front/find-by-ids" in url:
                captured["find_by_ids"] = await response.json()
            elif "course-info/front/find-by-id" in url and "find-by-ids" not in url:
                captured["course_info"] = await response.json()
            elif "guide-study/get-guide-study-info" in url:
                captured["guide_study_info"] = await response.json()
            elif "guide-study/get-guide-record" in url:
                captured["guide_record"] = await response.json()
        except Exception:
            pass

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--autoplay-policy=no-user-gesture-required"],
        )
        context = await browser.new_context()
        page = await context.new_page()
        page.on("response", on_response)

        # Step 1: Navigate to homepage and wait for user login
        print(f"[1/5] Navigating to ZhiXueYun homepage...")
        await page.goto("https://kc.zhixueyun.com/#/home-v")

        print("[2/5] Please log in manually in the browser window.")
        print("      Waiting for login (checking localStorage token)...")
        login_timeout = 300  # 5 minutes
        elapsed = 0
        while elapsed < login_timeout:
            token_raw = await page.evaluate("localStorage.getItem('token')")
            if token_raw and "access_token" in token_raw:
                print("      Login detected!")
                break
            await asyncio.sleep(3)
            elapsed += 3
        else:
            print("      Login timeout (5 min). Exiting.")
            await browser.close()
            return {"error": "Login timeout"}

        # Step 2: If UUID not resolved yet, try to get it from find_by_ids
        if not course_uuid and "find_by_ids" in captured:
            data = captured["find_by_ids"].get("data", [])
            if data and isinstance(data, list):
                course_uuid = data[0].get("id", "")
                print(f"      Resolved course UUID: {course_uuid}")

        if not course_uuid:
            print("      ERROR: Could not resolve course UUID. Exiting.")
            await browser.close()
            return {"error": "Could not resolve course UUID"}

        # Step 3: Navigate to course detail page (triggers key APIs)
        course_url = build_course_url(course_uuid)
        print(f"[3/5] Navigating to course detail page: {course_url}")
        await page.goto(course_url)

        # Step 4: Wait for API responses
        print("[4/5] Waiting for API responses (10 seconds)...")
        await page.wait_for_timeout(10000)

        # Also try scrolling to load any lazy content
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)

        # Step 5: Extract DOM text and video info
        print("[5/5] Extracting DOM subtitles and video info...")
        body_text = await page.evaluate("document.body.innerText")

        videos = await page.evaluate(
            """() => Array.from(document.querySelectorAll('video')).map(v => ({
                src: v.src,
                duration: v.duration,
                tracks: Array.from(v.textTracks || []).map(t => ({
                    kind: t.kind, mode: t.mode, label: t.label
                }))
            }))"""
        )

        # Extract token info (for reference, not stored externally)
        token_raw = await page.evaluate("localStorage.getItem('token')")
        token_info = {}
        if token_raw:
            try:
                token_data = json.loads(token_raw)
                token_info = {
                    "token_type": token_data.get("token_type", ""),
                    "lang": token_data.get("lang", ""),
                    "has_token": bool(token_data.get("access_token")),
                }
            except Exception:
                pass

        await browser.close()

    # Assemble output
    guide_study_data = captured.get("guide_study_info", {}).get("data", [])
    course_info_data = captured.get("course_info", {}).get("data", {})
    guide_record_data = captured.get("guide_record", {}).get("data", {})

    result = {
        "url": course_url,
        "course_uuid": course_uuid,
        "body_text": body_text,
        "videos": videos,
        "guide_study_data": guide_study_data,
        "course_info_data": course_info_data,
        "guide_record_data": guide_record_data,
        "captured_apis": list(captured.keys()),
        "token_info": token_info,
    }

    # Save to output directory
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save full data
    full_path = out_dir / "zhixueyun_full.json"
    full_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"      Full data saved: {full_path}")

    # Save knowledge points separately (primary data source)
    if guide_study_data:
        kp_path = out_dir / "zhixueyun_knowledge_points.json"
        kp_path.write_text(
            json.dumps(guide_study_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"      Knowledge points saved: {kp_path} ({len(guide_study_data)} items)")

    # Print summary
    print("\n=== Extraction Summary ===")
    if course_info_data:
        print(f"  Course: {course_info_data.get('name', 'N/A')}")
        print(f"  Lecturer: {course_info_data.get('lecturer', 'N/A')}")
        total_time = course_info_data.get("courseTime", 0)
        print(f"  Duration: {total_time}s ({total_time // 60}:{total_time % 60:02d})")
    print(f"  Knowledge points: {len(guide_study_data)} items")
    print(f"  Captured APIs: {', '.join(captured.keys())}")
    print(f"  DOM text length: {len(body_text)} chars")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract subtitles from ZhiXueYun course pages using Playwright API interception."
    )
    parser.add_argument(
        "source",
        help="Course URL (e.g. https://kc.zhixueyun.com/#/study/course/detail/{UUID}) or raw UUID",
    )
    parser.add_argument(
        "--output-dir",
        default=".temp",
        help="Directory for extracted data (default: .temp)",
    )
    args = parser.parse_args()

    course_uuid = extract_uuid(args.source)
    if not course_uuid:
        print(f"ERROR: Could not extract UUID from: {args.source}")
        return 1

    try:
        asyncio.run(extract_zhixueyun(course_uuid, args.output_dir))
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
