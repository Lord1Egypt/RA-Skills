#!/usr/bin/env python3
"""video-insight YouTube module: metadata + transcript extraction."""

import json
import subprocess
import sys
from typing import Optional, List, Dict

from utils import (
    extract_youtube_id, progress, load_settings, get_setting, ok_result, err_result
)

SETTINGS = load_settings()


# ──────────────────────────────────────────────
# Metadata
# ──────────────────────────────────────────────

def get_video_details(video_id: str) -> Optional[Dict]:
    """Get detailed video metadata using yt-dlp."""
    retries = int(get_setting("yt_dlp_retries", 3, settings=SETTINGS))
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--no-warnings",
                "-j",
                "--no-download",
                "--retries", str(retries),
                f"https://www.youtube.com/watch?v={video_id}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return None

        data = json.loads(result.stdout)
        duration = data.get("duration", 0)

        return {
            "title": data.get("title", "Unknown"),
            "channel": data.get("channel", data.get("uploader", "Unknown")),
            "duration_seconds": duration,
            "duration_display": f"{duration // 60}:{duration % 60:02d}",
            "description": data.get("description", "")[:1000],
            "published": data.get("upload_date", ""),
            "view_count": data.get("view_count", 0),
            "like_count": data.get("like_count", 0),
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        progress(f"  ⚠️  get_video_details failed: {e}")
        return None


# ──────────────────────────────────────────────
# Transcript: innertube → youtube-transcript-api fallback
# ──────────────────────────────────────────────

def _parse_caption_xml(xml_text: str) -> List[dict]:
    """Parse YouTube caption XML into segments with timestamps."""
    import xml.etree.ElementTree as ET
    import html as html_mod

    segments = []
    try:
        root = ET.fromstring(xml_text)
        # Try <p> format (innertube)
        for p in root.findall(".//p"):
            start_ms = int(p.get("t", 0))
            dur_ms = int(p.get("d", 0))
            words = []
            for s in p.findall("s"):
                if s.text:
                    words.append(html_mod.unescape(s.text.strip()))
            text = " ".join(words) if words else (html_mod.unescape(p.text.strip()) if p.text else "")
            if text:
                segments.append({
                    "start": start_ms / 1000.0,
                    "end": (start_ms + dur_ms) / 1000.0,
                    "text": text,
                })

        # Fallback: <text> format
        if not segments:
            for elem in root.findall(".//text"):
                if elem.text:
                    start = float(elem.get("start", 0))
                    dur = float(elem.get("dur", 0))
                    segments.append({
                        "start": start,
                        "end": start + dur,
                        "text": html_mod.unescape(elem.text.strip()),
                    })
    except Exception:
        pass
    return segments


def _download_caption(url: str) -> Optional[str]:
    try:
        import requests
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and r.text.strip():
            return r.text
    except Exception:
        pass
    return None


def _get_transcript_innertube(video_id: str) -> Optional[List[dict]]:
    """Get transcript via innertube API."""
    try:
        import innertube

        client = innertube.InnerTube("ANDROID")
        data = client.player(video_id=video_id)

        if "captions" not in data:
            return None

        caps = data["captions"]["playerCaptionsTracklistRenderer"]["captionTracks"]
        if not caps:
            return None

        # Pick best caption track
        cap_url = None
        for prefer in ["en", "zh-Hans", "zh", "zh-Hant", "ja", "ko"]:
            for c in caps:
                if c.get("languageCode") == prefer:
                    cap_url = c["baseUrl"]
                    break
            if cap_url:
                break
        if not cap_url:
            cap_url = caps[0]["baseUrl"]

        xml_text = _download_caption(cap_url)
        if not xml_text:
            return None

        segments = _parse_caption_xml(xml_text)
        if not segments:
            return None

        # Minimum length check
        full_text = " ".join(s["text"] for s in segments)
        min_len = int(get_setting("transcript_min_length", 50, settings=SETTINGS))
        return segments if len(full_text) > min_len else None

    except Exception as e:
        progress(f"  ⚠️  innertube failed: {e}")
        return None


def _get_transcript_ytapi(video_id: str) -> Optional[List[dict]]:
    """Get transcript via youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=["zh-Hans", "zh-Hant", "en", "ja", "ko"])

        segments = []
        for item in fetched:
            text = item.text if hasattr(item, "text") else item.get("text", "")
            start = item.start if hasattr(item, "start") else item.get("start", 0)
            duration = item.duration if hasattr(item, "duration") else item.get("duration", 0)
            if text:
                segments.append({
                    "start": float(start),
                    "end": float(start) + float(duration),
                    "text": text,
                })

        full_text = " ".join(s["text"] for s in segments)
        min_len = int(get_setting("transcript_min_length", 50, settings=SETTINGS))
        return segments if len(full_text) > min_len else None

    except Exception as e:
        progress(f"  ⚠️  youtube-transcript-api failed: {e}")
        return None


def get_transcript(video_id: str) -> Optional[List[dict]]:
    """Get video transcript using innertube → ytapi fallback.
    Returns list of {start, end, text} segments.
    """
    progress("  📝 Fetching transcript (innertube)...")
    segments = _get_transcript_innertube(video_id)
    if segments:
        progress(f"  ✅ innertube: {len(segments)} segments")
        return segments

    progress("  📝 Fetching transcript (youtube-transcript-api)...")
    segments = _get_transcript_ytapi(video_id)
    if segments:
        progress(f"  ✅ ytapi: {len(segments)} segments")
        return segments

    return None


# ──────────────────────────────────────────────
# Channel scan
# ──────────────────────────────────────────────

DEFAULT_MIN_DURATION = 300  # 5 minutes — filter Shorts


def get_channel_videos(channel_id: str, hours: int = 24, max_videos: int = 5) -> List[Dict]:
    """Get recent videos from a YouTube channel using yt-dlp."""
    if channel_id.startswith("UC") and len(channel_id) == 24:
        url = f"https://www.youtube.com/channel/{channel_id}/videos"
    elif channel_id.startswith("http"):
        url = channel_id.rstrip("/") + "/videos"
    else:
        url = f"https://www.youtube.com/@{channel_id}/videos"

    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                "--no-warnings",
                "-J",
                "--playlist-end", str(max_videos * 2),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if result.returncode != 0:
            progress(f"⚠️ yt-dlp error for {channel_id}: {result.stderr[:100]}")
            return []

        data = json.loads(result.stdout)
        entries = data.get("entries", [])
        videos = []

        for entry in entries:
            if not entry:
                continue
            video_id = entry.get("id")
            if not video_id:
                continue
            if entry.get("duration") and entry.get("duration") < DEFAULT_MIN_DURATION:
                continue
            videos.append({
                "id": video_id,
                "title": entry.get("title", "Unknown"),
                "channel": entry.get("channel", entry.get("uploader", "Unknown")),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "duration_hint": entry.get("duration"),
            })
            if len(videos) >= max_videos:
                break

        return videos
    except Exception as e:
        progress(f"⚠️ Error fetching channel {channel_id}: {e}")
        return []


# ──────────────────────────────────────────────
# Main YouTube processor
# ──────────────────────────────────────────────

def process_youtube(video_id: str, cache=None, no_cache: bool = False, extract_frames: bool = False) -> dict:
    """Process a YouTube video. Returns unified result dict."""
    progress(f"📹 YouTube: {video_id}")

    # Check cache first
    if cache and not no_cache:
        cached = cache.get("youtube", video_id)
        if cached:
            progress("  ✅ Cache hit")
            return cached

    # Get metadata
    progress("  📋 Fetching metadata...")
    details = get_video_details(video_id)
    if not details:
        return err_result(f"Failed to fetch video details for {video_id}", "METADATA_ERROR")

    # Get transcript
    segments = get_transcript(video_id)
    if not segments:
        return err_result("No transcript available (no captions found)", "NO_TRANSCRIPT")

    transcript_plain = " ".join(s["text"] for s in segments)
    transcript_with_ts = "\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text']}" for s in segments)

    result = {
        "video_id": video_id,
        "platform": "youtube",
        "title": details["title"],
        "channel": details["channel"],
        "duration_seconds": details["duration_seconds"],
        "transcript": transcript_plain,
        "transcript_with_timestamps": transcript_with_ts,
        "frames": [],
        "cached": False,
    }

    # Cache the result
    if cache:
        cache.put("youtube", video_id, result)
        progress("  💾 Cached")

    progress(f"  ✅ Done: {len(transcript_plain)} chars")
    return result
