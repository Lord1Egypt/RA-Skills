#!/usr/bin/env python3
"""
Video Results Poller

Poll for video generation results using ShortVideo API.

Usage:
    python3 poll-videos.py --video-ids <id1> <id2> ...
    python3 poll-videos.py --video-ids <id1> --max-attempts 30 --interval 5
"""

import argparse
import json
import os
import sys
import time
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


# Video status constants
STATUS_PENDING = 0
STATUS_PROCESSING = 1
STATUS_COMPLETED = 2
STATUS_FAILED = 3

STATUS_NAMES = {
    STATUS_PENDING: "Pending",
    STATUS_PROCESSING: "Processing",
    STATUS_COMPLETED: "Completed",
    STATUS_FAILED: "Failed"
}


def get_config() -> tuple[str, str]:
    """Get base_url and api_key from environment variables."""
    base_url = os.environ.get("SHORTVIDEO_BASE_URL", "")
    api_key = os.environ.get("SHORTVIDEO_API_KEY", "")

    if not base_url:
        print("Error: SHORTVIDEO_BASE_URL environment variable not set")
        print("Set it with: export SHORTVIDEO_BASE_URL='https://api.shortvideo.ai'")
        sys.exit(1)

    if not api_key:
        print("Error: SHORTVIDEO_API_KEY environment variable not set")
        print("Please visit https://shortvideo.ai to get your API key")
        print("Set it with: export SHORTVIDEO_API_KEY='your-api-key'")
        sys.exit(1)

    return base_url.rstrip("/"), api_key


def fetch_videos(video_ids: list[str]) -> dict[str, Any]:
    """
    Fetch video information by video IDs.

    Args:
        video_ids: List of video IDs

    Returns:
        dict with status and video information
    """
    base_url, api_key = get_config()

    url = f"{base_url}/api/video/fetch?ids={','.join(video_ids)}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        # Check response code
        code = result.get("code", -1)
        if code != 0:
            error_msg = result.get("message", result.get("info", f"Fetch failed with code {code}"))
            return {"status": "error", "error": error_msg, "code": code}

        # Extract data
        data = result.get("data", result)
        return {
            "status": "success",
            "videos": data.get("videos", []),
            "domain": data.get("domain", "")
        }

    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON response"}


def get_video_status_summary(videos: list[dict]) -> tuple[bool, bool, list[str]]:
    """
    Analyze video status.

    Returns:
        tuple: (all_completed, any_failed, status_summary_list)
    """
    all_completed = True
    any_failed = False
    status_summary = []

    for video in videos:
        video_id = video.get("id", "unknown")
        status = video.get("status", STATUS_PENDING)
        status_name = STATUS_NAMES.get(status, f"Unknown({status})")
        status_summary.append(f"{video_id}: {status_name}")

        if status == STATUS_FAILED:
            any_failed = True
        elif status != STATUS_COMPLETED:
            all_completed = False

    return all_completed, any_failed, status_summary


def poll_video_results(video_ids: list[str], max_attempts: int = 60, interval: int = 10) -> dict[str, Any]:
    """
    Poll for video results until completed or max attempts reached.

    Args:
        video_ids: List of video IDs to poll
        max_attempts: Maximum polling attempts (default: 60, ~10 minutes)
        interval: Polling interval in seconds (default: 10)

    Returns:
        dict with polling results
    """
    print(f"Starting to poll for {len(video_ids)} video(s)...")
    print(f"Max attempts: {max_attempts}, Interval: {interval}s")
    print("Video generation typically takes 10-15 minutes. Please wait...")
    print("-" * 60)

    videos = []
    domain = ""

    for attempt in range(1, max_attempts + 1):
        result = fetch_videos(video_ids)

        if result.get("status") != "success":
            print(f"[{attempt}/{max_attempts}] Failed to fetch: {result.get('error')}")
            time.sleep(interval)
            continue

        videos = result.get("videos", [])
        domain = result.get("domain", "")
        if not videos:
            print(f"[{attempt}/{max_attempts}] No videos returned")
            time.sleep(interval)
            continue

        all_completed, any_failed, status_summary = get_video_status_summary(videos)
        print(f"[{attempt}/{max_attempts}] {', '.join(status_summary)}")

        if all_completed:
            print("-" * 60)
            print("All videos completed!")
            return {
                "status": "success",
                "message": "All videos completed",
                "videos": videos,
                "domain": domain,
                "attempts": attempt
            }

        if any_failed:
            failed_videos = [v for v in videos if v.get("status") == STATUS_FAILED]
            print("-" * 60)
            print(f"Some videos failed: {len(failed_videos)}")
            return {
                "status": "partial",
                "message": f"{len(failed_videos)} video(s) failed",
                "videos": videos,
                "domain": domain,
                "failed_videos": failed_videos,
                "attempts": attempt
            }

        time.sleep(interval)

    # Max attempts reached
    print("-" * 60)
    print(f"Max polling attempts ({max_attempts}) reached. Videos still processing.")
    return {
        "status": "timeout",
        "message": f"Polling timed out after {max_attempts} attempts",
        "videos": videos,
        "domain": domain,
        "attempts": max_attempts
    }


def print_video_results(videos: list[dict], domain: str = ""):
    """Pretty print video results with full URLs."""
    print("\n" + "=" * 60)
    print("VIDEO RESULTS")
    print("=" * 60)

    for video in videos:
        video_id = video.get("id", "unknown")
        status = video.get("status", STATUS_PENDING)
        status_name = STATUS_NAMES.get(status, f"Unknown({status})")

        print(f"\nVideo ID: {video_id}")
        print(f"  Status: {status_name}")

        if status == STATUS_COMPLETED:
            duration = video.get("duration", 0)
            width = video.get("width", 0)
            height = video.get("height", 0)
            print(f"  Duration: {duration}s")
            print(f"  Resolution: {width}x{height}")

            specs = video.get("specs", {})
            if specs:
                print("  Files:")
                for quality, spec in specs.items():
                    video_path = spec.get("video", "")
                    cover_path = spec.get("cover", "")
                    size = spec.get("size", 0)
                    size_mb = size / (1024 * 1024) if size else 0

                    # Build full URLs
                    video_url = f"{domain}{video_path}" if domain and video_path else video_path
                    cover_url = f"{domain}{cover_path}" if domain and cover_path else cover_path

                    print(f"    [{quality}]")
                    print(f"      Video: {video_url}")
                    print(f"      Cover: {cover_url}")
                    if size:
                        print(f"      Size: {size_mb:.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Poll for video generation results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic polling
  python3 poll-videos.py --video-ids video_abc123 video_def456

  # Custom polling parameters
  python3 poll-videos.py --video-ids video_abc123 --max-attempts 30 --interval 5

  # Single check (no continuous polling)
  python3 poll-videos.py --video-ids video_abc123 --once

Video Status Codes:
  0 = Pending
  1 = Processing
  2 = Completed
  3 = Failed
        """
    )

    parser.add_argument("--video-ids", nargs="+", required=True,
                        help="Video IDs to poll")
    parser.add_argument("--max-attempts", type=int, default=60,
                        help="Maximum polling attempts (default: 60)")
    parser.add_argument("--interval", type=int, default=10,
                        help="Polling interval in seconds (default: 10)")
    parser.add_argument("--once", action="store_true",
                        help="Check once without continuous polling")
    parser.add_argument("--quiet", action="store_true",
                        help="Only output JSON result")

    args = parser.parse_args()

    if args.once:
        # Single check mode
        result = fetch_videos(args.video_ids)

        if result.get("status") == "success":
            videos = result.get("videos", [])
            domain = result.get("domain", "")
            all_completed, any_failed, status_summary = get_video_status_summary(videos)

            if not args.quiet:
                print(f"Status: {', '.join(status_summary)}")
                if all_completed:
                    print_video_results(videos, domain)

            result["status_summary"] = status_summary

        print(json.dumps(result, indent=2))
        if result.get("status") != "success":
            sys.exit(1)
    else:
        # Continuous polling mode
        result = poll_video_results(args.video_ids, args.max_attempts, args.interval)

        if not args.quiet and result.get("status") == "success":
            print_video_results(result.get("videos", []), result.get("domain", ""))

        print("\n" + json.dumps(result, indent=2))
        if result.get("status") not in ["success", "partial"]:
            sys.exit(1)


if __name__ == "__main__":
    main()