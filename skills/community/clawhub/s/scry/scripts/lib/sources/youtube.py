"""YouTube source for SCRY skill (via yt-dlp).

Searches YouTube and fetches auto-generated transcripts for top results.
"""

import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from ..source_base import Source, SourceMeta
from .. import query

# Max words to keep from each transcript
TRANSCRIPT_MAX_WORDS = 500

TRANSCRIPT_LIMITS = {
    "quick": 3,
    "default": 5,
    "deep": 8,
}


def _log(msg: str):
    import sys
    sys.stderr.write(f"[YouTube] {msg}\n")
    sys.stderr.flush()


def _clean_vtt(raw: str) -> str:
    """Clean VTT subtitle content into plain text."""
    lines = []
    seen = set()
    for line in raw.splitlines():
        line = line.strip()
        # Skip VTT headers, timestamps, and blank lines
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if re.match(r'^\d+$', line):
            continue
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if not clean:
            continue
        # Deduplicate consecutive identical lines (VTT repeats)
        if clean not in seen:
            lines.append(clean)
            seen.add(clean)
            # Reset seen periodically to allow natural repetition
            if len(seen) > 50:
                seen.clear()

    return re.sub(r'\s+', ' ', ' '.join(lines)).strip()


def _fetch_transcript(video_id: str, temp_dir: str) -> Optional[str]:
    """Fetch auto-generated transcript for a YouTube video."""
    output_template = os.path.join(temp_dir, f"{video_id}")
    cmd = [
        "yt-dlp",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--sub-format", "vtt",
        "--skip-download",
        "--no-warnings",
        "-o", output_template,
        f"https://www.youtube.com/watch?v={video_id}",
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None

    # Find the subtitle file
    for ext in [".en.vtt", ".en-orig.vtt", ".vtt"]:
        sub_path = output_template + ext
        if os.path.isfile(sub_path):
            try:
                with open(sub_path, "r", encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                return None

            transcript = _clean_vtt(raw)
            words = transcript.split()
            if len(words) > TRANSCRIPT_MAX_WORDS:
                transcript = ' '.join(words[:TRANSCRIPT_MAX_WORDS]) + '...'
            return transcript if transcript else None

    return None


def _fetch_transcripts_parallel(video_ids: List[str], max_workers: int = 5) -> Dict[str, Optional[str]]:
    """Fetch transcripts for multiple videos in parallel."""
    if not video_ids:
        return {}

    _log(f"Fetching transcripts for {len(video_ids)} videos")
    results = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_fetch_transcript, vid, temp_dir): vid
                for vid in video_ids
            }
            for future in as_completed(futures):
                vid = futures[future]
                try:
                    results[vid] = future.result()
                except Exception:
                    results[vid] = None

    got = sum(1 for v in results.values() if v)
    _log(f"Got transcripts for {got}/{len(video_ids)} videos")
    return results


class YouTubeSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="youtube",
            display_name="YouTube",
            tier=2,
            emoji="\U0001f534",
            id_prefix="YT",
            has_engagement=True,
            requires_keys=[],
            requires_bins=["yt-dlp"],
            domains=["general"],
        )

    def is_available(self, config):
        return config.get("_has_ytdlp", False)

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        count = min(dc["max_results"], 20)
        # Full metadata mode (no --flat-playlist) to get likes/comments.
        # This is slower, so use longer timeout.
        yt_timeout = max(dc["timeout"], 120)
        cmd = [
            "yt-dlp",
            f"ytsearch{count}:{core}",
            "--dump-json",
            "--no-download",
            "--no-warnings",
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=yt_timeout,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return []

        if result.returncode != 0:
            return []

        items = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                video = json.loads(line)
            except json.JSONDecodeError:
                continue

            title = video.get("title", "")
            if not title:
                continue

            video_id = video.get("id", "")
            item_url = video.get("url") or video.get("webpage_url") or ""
            if not item_url and video_id:
                item_url = f"https://www.youtube.com/watch?v={video_id}"

            item_date = None
            upload_date = video.get("upload_date", "")
            if upload_date and len(upload_date) == 8:
                try:
                    item_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                except (IndexError, ValueError):
                    pass

            author = video.get("channel", "") or video.get("uploader", "")
            description = video.get("description", "") or ""

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{title} {description[:200]}"),
                "engagement": {
                    "views": video.get("view_count", 0),
                    "likes": video.get("like_count", 0),
                    "num_comments": video.get("comment_count", 0),
                },
                "author": author,
                "snippet": description[:300] if description else "",
                "source_id": video_id,
                "_video_id": video_id,
            })

        return items

    def enrich(self, items, depth, config):
        """Fetch transcripts for top videos."""
        limit = TRANSCRIPT_LIMITS.get(depth, TRANSCRIPT_LIMITS["default"])

        # Sort by view count to prioritize popular videos for transcripts
        sorted_items = sorted(items, key=lambda x: (x.get("engagement") or {}).get("views", 0), reverse=True)
        top_ids = [item["_video_id"] for item in sorted_items[:limit] if item.get("_video_id")]

        if not top_ids:
            return items

        transcripts = _fetch_transcripts_parallel(top_ids)

        for item in items:
            vid = item.get("_video_id", "")
            transcript = transcripts.get(vid)
            if transcript:
                item["snippet"] = transcript
            # Clean up internal field
            item.pop("_video_id", None)

        return items


def get_source():
    return YouTubeSource()
