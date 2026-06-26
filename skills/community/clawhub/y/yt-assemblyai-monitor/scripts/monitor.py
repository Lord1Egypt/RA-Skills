#!/usr/bin/env python3
"""YouTube channel monitor + AssemblyAI transcription. Pure requests, zero extra dependencies."""

import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests required. pip3 install requests")
    sys.exit(1)

# --- Paths ---
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
CHANNELS_FILE = DATA_DIR / "channels.json"
PROCESSED_FILE = DATA_DIR / "processed.json"
SUMMARIES_DIR = DATA_DIR / "summaries"
CONFIG_FILE = DATA_DIR / "config.json"

API_BASE = "https://api.assemblyai.com/v2"
POLL_INTERVAL = 15
MAX_WAIT = 600

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)


# --- Config ---
def get_api_key():
    key = os.environ.get("ASSEMBLYAI_API_KEY")
    if key:
        return key
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("api_key")
    print("ERROR: No API key. Set ASSEMBLYAI_API_KEY or create data/config.json")
    sys.exit(1)


# --- File helpers ---
def load_json(path, default=None):
    if path.exists():
        return json.loads(path.read_text())
    return default if default is not None else []


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


# --- YouTube innertube API (pure requests) ---
def _get_innertube_context(video_url):
    """Fetch YouTube page and extract innertube context."""
    resp = requests.get(video_url, headers={"User-Agent": UA}, timeout=20)
    if resp.status_code != 200:
        print(f"  ERROR: YouTube returned HTTP {resp.status_code}")
        return None, None

    m = re.search(r"ytcfg\.set\(({.*?})\);", resp.text, re.DOTALL)
    if not m:
        print("  ERROR: Cannot find innertube config")
        return None, None

    try:
        config = json.loads(m.group(1))
        ctx = config.get("INNERTUBE_CONTEXT")
        key = config.get("INNERTUBE_API_KEY", "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8")
        return ctx, key
    except json.JSONDecodeError:
        return None, None


def extract_audio_url(video_url):
    """Extract direct audio URL from YouTube using innertube API."""
    video_id = _parse_video_id(video_url)
    if not video_id:
        return None

    ctx, key = _get_innertube_context(video_url)
    if not ctx:
        return None

    body = {"videoId": video_id, "context": ctx}
    resp = requests.post(
        f"https://www.youtube.com/youtubei/v1/player?key={key}",
        json=body,
        headers={
            "User-Agent": UA,
            "Origin": "https://www.youtube.com",
            "Referer": f"https://www.youtube.com/watch?v={video_id}",
        },
        timeout=15,
    )

    data = resp.json()
    status = data.get("playabilityStatus", {}).get("status")
    if status != "OK":
        reason = data.get("playabilityStatus", {}).get("reason", "unknown")
        print(f"  ERROR: Video {status}: {reason}")
        return None

    formats = data.get("streamingData", {}).get("adaptiveFormats", [])
    audio = [f for f in formats if f.get("mimeType", "").startswith("audio/")]
    if not audio:
        print("  ERROR: No audio formats found")
        return None

    audio.sort(key=lambda f: f.get("bitrate", 0), reverse=True)
    best = audio[0]

    if best.get("url"):
        return best["url"]

    if best.get("signatureCipher"):
        print("  WARNING: Audio uses signatureCipher, may not work without decryption")
        pairs = {}
        for pair in best["signatureCipher"].split("&"):
            k, v = pair.split("=", 1)
            pairs[k] = requests.utils.unquote(v)
        return pairs.get("url")

    return None


def get_channel_videos(channel_url, limit=5):
    """Get recent video IDs from a YouTube channel page."""
    resp = requests.get(channel_url, headers={"User-Agent": UA}, timeout=20)
    if resp.status_code != 200:
        print(f"  ERROR: Channel HTTP {resp.status_code}")
        return []

    ids = list(dict.fromkeys(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', resp.text)))
    title_pat = re.compile(r'"title":\s*\{[^}]*"runs":\s*\[\s*\{[^}]*"text":\s*"([^"]+)"')
    titles = title_pat.findall(resp.text)

    videos = []
    for i, vid in enumerate(ids[:limit]):
        videos.append({
            "id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": titles[i] if i < len(titles) else "",
            "date": "unknown",
        })
    return videos


def _parse_video_id(url):
    if "youtube.com/watch" in url:
        m = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
        return m.group(1) if m else None
    elif "youtu.be/" in url:
        m = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
        return m.group(1) if m else None
    return None


def get_channel_info(channel_url):
    m = re.search(r"@([^/]+)", channel_url)
    if m:
        return m.group(1)
    return channel_url.split("/")[-1]


# --- AssemblyAI API ---
def submit_transcription(api_key, audio_url):
    headers = {
        "authorization": api_key,
        "content-type": "application/json",
    }
    payload = {
        "audio_url": audio_url,
        "speech_models": ["universal-3-pro"],
        "speaker_labels": True,
        "summarization": True,
        "summary_type": "paragraph",
        "summary_model": "conversational",
    }
    resp = requests.post(f"{API_BASE}/transcript", json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"  ERROR submit: {resp.status_code} {resp.text[:200]}")
        return None
    return resp.json()["id"]


def poll_transcription(api_key, tid):
    headers = {"authorization": api_key}
    start = time.time()
    while time.time() - start < MAX_WAIT:
        resp = requests.get(f"{API_BASE}/transcript/{tid}", headers=headers, timeout=30)
        data = resp.json()
        st = data.get("status")
        if st == "completed":
            return data
        elif st == "error":
            print(f"  Transcription error: {data.get('error', 'unknown')}")
            return None
        print(f"  Status: {st}...")
        time.sleep(POLL_INTERVAL)
    print("  Timeout")
    return None


def transcribe_video(api_key, video_url):
    """Extract audio URL + submit to AssemblyAI + poll result."""
    if "youtube.com" in video_url or "youtu.be" in video_url:
        print(f"Extracting audio URL...")
        audio_url = extract_audio_url(video_url)
        if not audio_url:
            return None
        print(f"  Got audio URL ({len(audio_url)} chars)")
    else:
        audio_url = video_url

    print(f"Submitting...")
    tid = submit_transcription(api_key, audio_url)
    if not tid:
        return None
    print(f"  ID: {tid}")
    return poll_transcription(api_key, tid)


# --- Channel management ---
def add_channel(url, alias=None):
    channels = load_json(CHANNELS_FILE, [])
    for ch in channels:
        if ch.get("url") == url:
            print(f"Already exists: {ch.get('alias', 'unnamed')}")
            return
    if not alias:
        alias = get_channel_info(url)
    channels.append({"url": url, "alias": alias or url, "added": time.strftime("%Y-%m-%d")})
    save_json(CHANNELS_FILE, channels)
    print(f"Added: {alias} ({url})")


def remove_channel(alias):
    channels = load_json(CHANNELS_FILE, [])
    new = [ch for ch in channels if ch.get("alias") != alias and ch.get("url") != alias]
    if len(new) == len(channels):
        print(f"Not found: {alias}")
        return
    save_json(CHANNELS_FILE, new)
    print(f"Removed: {alias}")


def list_channels():
    channels = load_json(CHANNELS_FILE, [])
    if not channels:
        print("No channels.")
        return
    for i, ch in enumerate(channels, 1):
        print(f"  {i}. {ch.get('alias', '?')} — {ch.get('url')}")


# --- Main ---
def check_channels(api_key, limit=2):
    channels = load_json(CHANNELS_FILE, [])
    if not channels:
        print("No channels. Use 'add' first.")
        return []

    processed = set(load_json(PROCESSED_FILE, []))
    results = []

    for ch in channels:
        alias = ch.get("alias", "?")
        url = ch.get("url")
        print(f"\n📺 {alias}")
        videos = get_channel_videos(url, limit)
        new = [v for v in videos if v["id"] not in processed]
        if not new:
            print("  No new videos.")
            continue

        print(f"  {len(new)} new video(s)")
        for v in new:
            print(f"\n  🎬 {v['title']} ({v['date']})")
            result = transcribe_video(api_key, v["url"])
            if result:
                save_data = {
                    "video_id": v["id"],
                    "title": v["title"],
                    "url": v["url"],
                    "text": result.get("text", ""),
                    "summary": result.get("summary", ""),
                    "confidence": result.get("confidence", 0),
                    "utterances": (result.get("utterances") or [])[:50],
                }
                SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
                save_json(SUMMARIES_DIR / f"{v['id']}.json", save_data)
                processed.add(v["id"])
                save_json(PROCESSED_FILE, sorted(processed))
                results.append(save_data)
                print(f"  ✅ Confidence: {result.get('confidence', 'N/A')}")
                summary = result.get("summary", "")
                if summary:
                    print(f"  📝 {summary[:500]}")
            else:
                print(f"  ❌ Failed")

    print(f"\n{'='*50}")
    print(f"Transcribed: {len(results)}")
    return results


def now_transcribe(api_key, url):
    vid = _parse_video_id(url) or "unknown"
    result = transcribe_video(api_key, url)
    if result:
        save_data = {
            "video_id": vid,
            "url": url,
            "text": result.get("text", ""),
            "summary": result.get("summary", ""),
            "confidence": result.get("confidence", 0),
        }
        SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
        save_json(SUMMARIES_DIR / f"{vid}.json", save_data)
        print(f"\n✅ Done!")
        print(f"📝 {result.get('summary', 'No summary')[:500]}")
    else:
        print("❌ Failed")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 monitor.py check [count]")
        print("  python3 monitor.py add <url> [alias]")
        print("  python3 monitor.py remove <alias>")
        print("  python3 monitor.py list")
        print("  python3 monitor.py now <url>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        api_key = get_api_key()
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        check_channels(api_key, limit)
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: add <channel_url> [alias]")
            sys.exit(1)
        add_channel(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("Usage: remove <alias>")
            sys.exit(1)
        remove_channel(sys.argv[2])
    elif cmd == "list":
        list_channels()
    elif cmd == "now":
        if len(sys.argv) < 3:
            print("Usage: now <video_url>")
            sys.exit(1)
        api_key = get_api_key()
        now_transcribe(api_key, sys.argv[2])
    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
