#!/usr/bin/env python3
"""YouTube Transcript Fetcher, transcript extraction tool."""

import re
import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone
from typing import Optional, List, Dict
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Default config
DEFAULT_MIN_DURATION = 300  # 5 minutes (filter Shorts)
DEFAULT_HOURS_LOOKBACK = 24
DEFAULT_MAX_VIDEOS_PER_CHANNEL = 5
DEFAULT_OUTPUT = "/tmp/youtube_transcript_fetcher.json"


def get_channel_videos(channel_id: str, hours: int, max_videos: int) -> List[Dict]:
    """Get recent videos from a YouTube channel using yt-dlp"""
    videos = []
    
    # Build channel URL
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
            print(f"⚠️ yt-dlp error for {channel_id}: {result.stderr[:100]}", file=sys.stderr)
            return []
        
        data = json.loads(result.stdout)
        entries = data.get("entries", [])
        
        for entry in entries:
            if not entry:
                continue
            
            video_id = entry.get("id")
            if not video_id:
                continue
            
            # Filter Shorts by duration
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
        
    except Exception as e:
        print(f"⚠️ Error fetching channel {channel_id}: {e}", file=sys.stderr)
    
    return videos


def get_video_details(video_id: str) -> Optional[Dict]:
    """Get detailed video metadata using yt-dlp"""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--no-warnings",
                "-j",
                "--no-download",
                f"https://www.youtube.com/watch?v={video_id}",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout)
        duration = data.get("duration", 0)
        
        return {
            "duration_seconds": duration,
            "duration": f"{duration // 60}:{duration % 60:02d}",
            "description": data.get("description", "")[:1000],
            "published": data.get("upload_date", ""),
            "view_count": data.get("view_count", 0),
            "like_count": data.get("like_count", 0),
        }
        
    except Exception:
        return None


def get_transcript(video_id: str) -> Optional[str]:
    """Get video transcript using multiple methods."""
    transcript = _get_transcript_innertube_proxy(video_id)
    if transcript:
        return transcript
    
    # Method 2: youtube-transcript-api (fallback, may be rate limited)
    transcript = _get_transcript_ytapi(video_id)
    if transcript:
        return transcript
    
    return None


def _parse_caption_xml(xml_text: str) -> List[str]:
    """Parse YouTube caption XML (supports multiple formats)"""
    import xml.etree.ElementTree as ET
    import html as html_mod
    
    try:
        root = ET.fromstring(xml_text)
        texts = []
        
        # Try <p> tags first (format 3 and format 2)
        for p in root.findall('.//p'):
            # Check for <s> child tags (format 3: word-level)
            words = []
            for s in p.findall('s'):
                if s.text:
                    words.append(html_mod.unescape(s.text.strip()))
            if words:
                texts.append(' '.join(words))
            elif p.text:  # format 2: direct text
                texts.append(html_mod.unescape(p.text.strip()))
        
        # If no <p> found, try <text> tags (format 1)
        if not texts:
            for elem in root.findall('.//text'):
                if elem.text:
                    texts.append(html_mod.unescape(elem.text.strip()))
        
        return texts
    except Exception:
        return []


def _download_caption(url: str) -> Optional[str]:
    """Download caption content directly from YouTube."""
    import requests

    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and r.text.strip():
            return r.text
    except Exception:
        pass
    
    return None


def _extract_innertube_api_key(html_text: str) -> Optional[str]:
    match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html_text)
    return match.group(1) if match else None


def _fetch_video_page(video_id: str) -> Optional[str]:
    import requests

    try:
        response = requests.get(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36"
            },
            timeout=15,
        )
        if response.status_code == 200 and response.text:
            return response.text
    except Exception:
        pass
    return None


def _fetch_caption_tracks_with_clients(video_id: str, api_key: str) -> List[Dict]:
    import requests

    url = f"https://www.youtube.com/youtubei/v1/player?key={api_key}"
    client_attempts = [
        {
            "name": "ANDROID",
            "user_agent": "com.google.android.youtube/21.02.35 (Linux; U; Android 11) gzip",
            "client": {
                "hl": "en",
                "gl": "US",
                "clientName": "ANDROID",
                "clientVersion": "21.02.35",
                "androidSdkVersion": 30,
                "osName": "Android",
                "osVersion": "11",
                "platform": "MOBILE",
            },
        },
        {
            "name": "WEB",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
            "client": {
                "hl": "en",
                "gl": "US",
                "clientName": "WEB",
                "clientVersion": "2.20240619.06.00",
            },
        },
        {
            "name": "TVHTML5_SIMPLY_EMBEDDED_PLAYER",
            "user_agent": "Mozilla/5.0 (Chromecast; Android TV 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.99 Safari/537.36",
            "client": {
                "hl": "en",
                "gl": "US",
                "clientName": "TVHTML5_SIMPLY_EMBEDDED_PLAYER",
                "clientVersion": "2.0",
                "clientScreen": "EMBED",
                "platform": "TV",
                "deviceMake": "Google",
                "deviceModel": "Chromecast",
                "osName": "Android",
                "osVersion": "10",
            },
        },
        {
            "name": "IOS",
            "user_agent": "com.google.ios.youtube/19.09.3 (iPhone; CPU iPhone OS 17_5 like Mac OS X)",
            "client": {
                "hl": "en",
                "gl": "US",
                "clientName": "IOS",
                "clientVersion": "19.09.3",
                "deviceMake": "Apple",
                "deviceModel": "iPhone16,2",
                "osName": "iOS",
                "osVersion": "17.5",
            },
        },
    ]

    for attempt in client_attempts:
        try:
            response = requests.post(
                url,
                headers={
                    "User-Agent": attempt["user_agent"],
                    "Content-Type": "application/json",
                },
                json={
                    "videoId": video_id,
                    "context": {"client": attempt["client"]},
                    "contentCheckOk": True,
                    "racyCheckOk": True,
                },
                timeout=15,
            )
            if response.status_code != 200:
                continue
            data = response.json()
            captions = data.get("captions")
            if not captions:
                continue
            tracks = captions.get("playerCaptionsTracklistRenderer", {}).get("captionTracks") or []
            if tracks:
                return [{**track, "fetchUserAgent": attempt["user_agent"]} for track in tracks]
        except Exception:
            continue
    return []


def _pick_caption_track(tracks: List[Dict]) -> Optional[Dict]:
    if not tracks:
        return None
    for prefer in ["en", "zh-Hans", "zh-Hant", "zh"]:
        for track in tracks:
            code = track.get("languageCode")
            if code == prefer:
                return track
    return tracks[0]


def _get_transcript_innertube_proxy(video_id: str) -> Optional[str]:
    """Method 1: watch-page scrape + InnerTube multi-client fallback + caption XML"""
    try:
        video_page_html = _fetch_video_page(video_id)
        if not video_page_html:
            return None

        api_key = _extract_innertube_api_key(video_page_html)
        if not api_key:
            return None

        caption_tracks = _fetch_caption_tracks_with_clients(video_id, api_key)
        selected_track = _pick_caption_track(caption_tracks)
        if not selected_track:
            return None

        cap_url = selected_track.get('baseUrl')
        if not cap_url:
            return None

        xml_text = _download_caption(cap_url)
        if not xml_text:
            return None
        
        texts = _parse_caption_xml(xml_text)
        if not texts:
            return None
        
        result = ' '.join(texts).strip()
        return result if len(result) > 50 else None
        
    except Exception:
        return None


def _get_transcript_ytapi(video_id: str) -> Optional[str]:
    """Method 2 (fallback): youtube-transcript-api direct connection"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=["zh-Hans", "zh-Hant", "en"])
        transcript = " ".join([item["text"] for item in fetched])
        return transcript if len(transcript) > 50 else None
        
    except Exception:
        return None


def extract_video_id(url_or_id: str) -> Optional[str]:
    """Extract a YouTube video ID from a video URL or raw ID."""
    value = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host in {"youtu.be", "www.youtu.be"}:
        candidate = path.split("/")[0] if path else ""
        return candidate if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate) else None

    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
        query_id = parse_qs(parsed.query).get("v", [None])[0]
        if query_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", query_id):
            return query_id

        parts = [part for part in path.split("/") if part]
        if len(parts) >= 2 and parts[0] in {"shorts", "embed", "live", "watch"}:
            candidate = parts[1] if parts[0] != "watch" else None
            if candidate and re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
                return candidate

    return None


def process_video(video_id: str, title: str = None, channel: str = None) -> Dict:
    """Process a single video and return transcript-oriented JSON."""
    print(f"📹 Processing: {video_id}")
    
    # Get video details
    details = get_video_details(video_id)
    if not details:
        return {
            "video_id": video_id,
            "title": title or "Unknown",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "error": "Failed to fetch video details"
        }
    
    # Get transcript
    transcript = get_transcript(video_id)
    has_transcript = transcript is not None
    
    result = {
        "video_id": video_id,
        "title": title or "Unknown",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": channel or "Unknown",
        "duration": details["duration"],
        "published": details["published"],
        "has_transcript": has_transcript,
        "metadata": {
            "view_count": details.get("view_count", 0),
            "like_count": details.get("like_count", 0),
        },
        "transcript": transcript if has_transcript else None,
    }
    
    if has_transcript:
        print(f"  ✅ Transcript: {len(transcript)} chars")
    else:
        result["error"] = "No transcript available"
        print(f"  ⚠️ No transcript available")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="YouTube Transcript Fetcher")
    parser.add_argument("--url", help="Single YouTube URL or video ID")
    parser.add_argument("--channel", help="Channel ID or handle")
    parser.add_argument("--config", help="Config file path (JSON)")
    parser.add_argument("--daily", action="store_true", help="Daily batch mode (requires --config)")
    parser.add_argument("--hours", type=int, default=DEFAULT_HOURS_LOOKBACK, help="Hours to look back")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON file")
    
    args = parser.parse_args()
    
    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": [],
        "stats": {
            "total_videos": 0,
            "with_transcript": 0,
            "without_transcript": 0
        }
    }
    
    # Mode 1: Single video
    if args.url:
        video_id = extract_video_id(args.url)
        if not video_id:
            print("⚠️ Could not extract a valid YouTube video ID from --url", file=sys.stderr)
            sys.exit(2)
        result = process_video(video_id)
        results["items"].append(result)
        results["stats"]["total_videos"] = 1
        if result.get("has_transcript"):
            results["stats"]["with_transcript"] = 1
        else:
            results["stats"]["without_transcript"] = 1
    
    # Mode 2: Channel scan
    elif args.channel:
        videos = get_channel_videos(args.channel, args.hours, DEFAULT_MAX_VIDEOS_PER_CHANNEL)
        print(f"📺 Found {len(videos)} videos from channel")
        
        for video in videos:
            result = process_video(video["id"], video["title"], video["channel"])
            results["items"].append(result)
            results["stats"]["total_videos"] += 1
            if result.get("has_transcript"):
                results["stats"]["with_transcript"] += 1
            else:
                results["stats"]["without_transcript"] += 1
    
    # Mode 3: Daily batch (config file)
    elif args.daily and args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
        
        channels = config.get("channels", [])
        hours = config.get("hours_lookback", args.hours)
        max_videos = config.get("max_videos_per_channel", DEFAULT_MAX_VIDEOS_PER_CHANNEL)
        
        print(f"📺 Processing {len(channels)} channels")
        
        for ch in channels:
            channel_id = ch.get("id") or ch.get("url")
            channel_name = ch.get("name", "Unknown")
            
            print(f"\n🔍 Channel: {channel_name}")
            videos = get_channel_videos(channel_id, hours, max_videos)
            print(f"  Found {len(videos)} videos")
            
            for video in videos:
                result = process_video(video["id"], video["title"], channel_name)
                results["items"].append(result)
                results["stats"]["total_videos"] += 1
                if result.get("has_transcript"):
                    results["stats"]["with_transcript"] += 1
                else:
                    results["stats"]["without_transcript"] += 1
    
    else:
        parser.print_help()
        sys.exit(1)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Output written to: {output_path}")
    print(f"📊 Stats: {results['stats']}")


if __name__ == "__main__":
    main()
