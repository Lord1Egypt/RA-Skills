#!/usr/bin/env python3
"""
video-podcast: Convert videos into a podcast RSS feed hosted on Cloudflare R2.

Supports YouTube, X (Twitter), and any site supported by yt-dlp.

Usage:
  video_podcast.py add <url>                    Download audio and add to feed
  video_podcast.py sync-youtube <playlist_id>   Add new videos from a YouTube playlist
  video_podcast.py feed                         Print the public RSS feed URL
  video_podcast.py list                         List all episodes
  video_podcast.py remove <url_or_guid>         Remove an episode from the feed
  video_podcast.py setup                        Interactive first-time configuration

Required env vars (in ~/.openclaw/.env):
  VIDPOD_R2_ACCESS_KEY     Cloudflare R2 API token access key
  VIDPOD_R2_SECRET         Cloudflare R2 API token secret
  VIDPOD_R2_ENDPOINT       R2 endpoint URL (https://<account_id>.r2.cloudflarestorage.com)
  VIDPOD_R2_BUCKET         R2 bucket name (e.g. podcast-feed)
  VIDPOD_PUBLIC_BASE       Public r2.dev URL (https://pub-<hash>.r2.dev)

Optional:
  VIDPOD_FEED_TITLE        Podcast title (default: "My Video Podcast")
  VIDPOD_FEED_AUTHOR       Podcast author name (default: "Video Podcast")
"""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

ENV_FILE   = Path.home() / ".openclaw" / ".env"
STATE_FILE = Path.home() / ".openclaw" / "video-podcast-state.json"

REQUIRED_ENV = [
    "VIDPOD_R2_ACCESS_KEY",
    "VIDPOD_R2_SECRET",
    "VIDPOD_R2_ENDPOINT",
    "VIDPOD_R2_BUCKET",
    "VIDPOD_PUBLIC_BASE",
]

# ── Env helpers ────────────────────────────────────────────────────────────────

def load_env():
    """Load ~/.openclaw/.env into os.environ."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def require_env(key: str) -> str:
    v = os.environ.get(key)
    if not v:
        sys.exit(
            f"ERROR: {key} is not set.\n"
            f"Run: video_podcast.py setup\n"
            f"Or add it manually to ~/.openclaw/.env"
        )
    return v


def get_config() -> dict:
    """Return all config values, reading env as needed."""
    load_env()
    return {
        "access_key":  require_env("VIDPOD_R2_ACCESS_KEY"),
        "secret":      require_env("VIDPOD_R2_SECRET"),
        "endpoint":    require_env("VIDPOD_R2_ENDPOINT"),
        "bucket":      require_env("VIDPOD_R2_BUCKET"),
        "public_base": require_env("VIDPOD_PUBLIC_BASE").rstrip("/"),
        "feed_title":  os.environ.get("VIDPOD_FEED_TITLE", "My Video Podcast"),
        "feed_author": os.environ.get("VIDPOD_FEED_AUTHOR", "Video Podcast"),
    }


# ── State ──────────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"episodes": [], "processed_urls": []}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def url_guid(url: str) -> str:
    """Stable, collision-resistant ID for a URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]


# ── R2 upload ──────────────────────────────────────────────────────────────────

def r2_client(cfg: dict):
    """Return a boto3 S3 client pointed at R2."""
    import boto3
    from botocore.config import Config
    return boto3.client(
        "s3",
        endpoint_url=cfg["endpoint"],
        aws_access_key_id=cfg["access_key"],
        aws_secret_access_key=cfg["secret"],
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def r2_upload_file(cfg: dict, local_path: str, key: str,
                   content_type: str, cache_control: str) -> str:
    """Upload a local file to R2. Returns public URL."""
    client = r2_client(cfg)
    client.upload_file(
        local_path,
        cfg["bucket"],
        key,
        ExtraArgs={
            "ContentType": content_type,
            "CacheControl": cache_control,
        },
    )
    return f"{cfg['public_base']}/{key}"


def r2_upload_text(cfg: dict, content: str, key: str,
                   content_type: str, cache_control: str) -> str:
    """Upload a string directly to R2. Returns public URL."""
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False,
                                     mode="w", encoding="utf-8") as f:
        f.write(content)
        tmp = f.name
    try:
        return r2_upload_file(cfg, tmp, key, content_type, cache_control)
    finally:
        os.unlink(tmp)


# ── yt-dlp helpers ─────────────────────────────────────────────────────────────

def download_audio(url: str, out_dir: str) -> dict:
    """
    Download audio from any yt-dlp-supported URL.
    Returns metadata dict including filepath, title, duration, thumbnail.
    Raises SystemExit on failure.
    """
    try:
        import yt_dlp
    except ImportError:
        sys.exit(
            "ERROR: yt-dlp not installed.\n"
            "Run: pip3 install yt-dlp"
        )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "5",  # VBR ~130kbps — good quality, reasonable size
        }],
        "quiet": False,
        "no_warnings": False,
    }

    # Use browser cookies if available — helps with YouTube's SABR enforcement
    # and age-restricted content. Reads from Safari; does not store or transmit cookies.
    cookie_browser = os.environ.get("VIDPOD_COOKIE_BROWSER", "safari")
    if cookie_browser and cookie_browser.lower() != "none":
        ydl_opts["cookiesfrombrowser"] = (cookie_browser,)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except yt_dlp.utils.DownloadError as e:
            sys.exit(f"ERROR: Could not download {url}\n{e}")

    video_id = info.get("id") or url_guid(url)
    mp3_path = os.path.join(out_dir, f"{video_id}.mp3")

    if not os.path.exists(mp3_path):
        # Find any file matching the video_id (yt-dlp naming can vary)
        matches = list(Path(out_dir).glob(f"{video_id}*"))
        if matches:
            mp3_path = str(matches[0])
        else:
            sys.exit(f"ERROR: Audio file not found after download in {out_dir}")

    return {
        "filepath":    mp3_path,
        "title":       info.get("title", "Untitled"),
        "duration":    info.get("duration", 0),
        "thumbnail":   info.get("thumbnail", ""),
        "description": info.get("description", ""),
        "uploader":    info.get("uploader", ""),
        "video_id":    video_id,
        "webpage_url": info.get("webpage_url", url),
    }


def get_playlist_video_ids(playlist_id: str) -> list:
    """List video IDs in a YouTube playlist without downloading."""
    try:
        import yt_dlp
    except ImportError:
        sys.exit("ERROR: yt-dlp not installed. Run: pip3 install yt-dlp")

    ydl_opts = {"extract_flat": True, "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(
                f"https://www.youtube.com/playlist?list={playlist_id}",
                download=False,
            )
        except yt_dlp.utils.DownloadError as e:
            sys.exit(f"ERROR: Could not fetch playlist {playlist_id}\n{e}")

    return [e["id"] for e in info.get("entries", []) if e and e.get("id")]


# ── RSS feed ───────────────────────────────────────────────────────────────────

def build_rss(cfg: dict, episodes: list) -> str:
    """Build a valid podcast RSS XML string."""
    ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")

    feed_url   = f"{cfg['public_base']}/feed.xml"
    cover_url  = f"{cfg['public_base']}/cover.jpg"
    feed_title = cfg["feed_title"]

    rss = ET.Element("rss", {"version": "2.0"})
    rss.set("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    rss.set("xmlns:atom",   "http://www.w3.org/2005/Atom")

    ch = ET.SubElement(rss, "channel")
    ET.SubElement(ch, "title").text       = feed_title
    ET.SubElement(ch, "description").text = f"Auto-generated podcast feed from bookmarked videos"
    ET.SubElement(ch, "language").text    = "en"
    ET.SubElement(ch, "link").text        = feed_url

    atom_link = ET.SubElement(ch, "atom:link")
    atom_link.set("href", feed_url)
    atom_link.set("rel",  "self")
    atom_link.set("type", "application/rss+xml")

    ET.SubElement(ch, "itunes:author").text   = cfg["feed_author"]
    ET.SubElement(ch, "itunes:explicit").text = "no"

    # Feed-level cover art (required by Apple Podcasts and most apps)
    ch_img = ET.SubElement(ch, "image")
    ET.SubElement(ch_img, "url").text   = cover_url
    ET.SubElement(ch_img, "title").text = feed_title
    ET.SubElement(ch_img, "link").text  = feed_url
    itunes_img = ET.SubElement(ch, "itunes:image")
    itunes_img.set("href", cover_url)

    # Episodes — newest first
    for ep in reversed(episodes):
        item = ET.SubElement(ch, "item")
        ET.SubElement(item, "title").text                       = ep["title"]
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = ep["guid"]
        ET.SubElement(item, "pubDate").text                     = ep.get("pub_date", "")
        ET.SubElement(item, "description").text                 = ep.get("description", "")

        enc = ET.SubElement(item, "enclosure")
        enc.set("url",    ep["audio_url"])
        enc.set("length", str(ep.get("file_size", 0)))
        enc.set("type",   "audio/mpeg")

        dur = int(ep.get("duration", 0))
        if dur:
            mins, secs = divmod(dur, 60)
            hours, mins = divmod(mins, 60)
            dur_str = f"{hours}:{mins:02d}:{secs:02d}" if hours else f"{mins}:{secs:02d}"
            ET.SubElement(item, "itunes:duration").text = dur_str

        ET.SubElement(item, "itunes:author").text = ep.get("uploader", cfg["feed_author"])

        if ep.get("thumbnail"):
            ep_img = ET.SubElement(item, "itunes:image")
            ep_img.set("href", ep["thumbnail"])

        if ep.get("source_url"):
            ET.SubElement(item, "link").text = ep["source_url"]

    ET.indent(rss, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(rss, encoding="unicode")


def upload_feed(cfg: dict, episodes: list) -> str:
    """Build and upload feed.xml to R2. Returns public feed URL."""
    xml = build_rss(cfg, episodes)
    r2_upload_text(cfg, xml, "feed.xml", "application/rss+xml", "no-cache, no-store")
    return f"{cfg['public_base']}/feed.xml"


# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_setup():
    """Interactive first-time configuration."""
    print("video-podcast setup\n")
    print("You'll need a Cloudflare account with R2 enabled.")
    print("See: https://developers.cloudflare.com/r2/get-started/\n")

    fields = {
        "VIDPOD_R2_ACCESS_KEY":  "R2 Access Key ID",
        "VIDPOD_R2_SECRET":      "R2 Secret Access Key",
        "VIDPOD_R2_ENDPOINT":    "R2 Endpoint URL  (https://<account_id>.r2.cloudflarestorage.com)",
        "VIDPOD_R2_BUCKET":      "R2 Bucket name   (e.g. podcast-feed)",
        "VIDPOD_PUBLIC_BASE":    "R2 Public URL    (https://pub-<hash>.r2.dev)",
    }

    # Read existing env file
    existing = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                existing[k.strip()] = v.strip()

    new_values = {}
    for key, label in fields.items():
        current = existing.get(key, "")
        display = f" [{current}]" if current else ""
        val = input(f"{label}{display}: ").strip()
        new_values[key] = val if val else current

    # Write back
    lines = []
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                k = stripped.partition("=")[0].strip()
                if k in new_values:
                    continue  # Will be replaced below
            lines.append(line)

    lines.append("\n# video-podcast")
    for k, v in new_values.items():
        if v:
            lines.append(f"{k}={v}")

    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    ENV_FILE.write_text("\n".join(lines) + "\n")
    print("\n✅ Config saved to ~/.openclaw/.env")
    print("\nNext: verify ffmpeg is installed:")
    print("  brew install ffmpeg   (macOS)")
    print("  sudo apt install ffmpeg  (Linux)")


def cmd_add(url: str):
    cfg   = get_config()
    state = load_state()

    guid = url_guid(url)
    if guid in state.get("processed_urls", []):
        print(f"Already in feed — skipping: {url}")
        return

    print(f"Downloading audio from: {url}")
    with tempfile.TemporaryDirectory() as tmp_dir:
        info      = download_audio(url, tmp_dir)
        filepath  = info["filepath"]
        file_size = os.path.getsize(filepath)
        filename  = f"{guid}.mp3"

        print(f"Uploading {filename} ({file_size // 1024} KB) to R2…")
        audio_url = r2_upload_file(
            cfg, filepath, filename,
            "audio/mpeg", "public, max-age=604800",
        )

    # Truncate description to 500 chars to keep feed.xml manageable
    description = (info.get("description") or "")[:500]
    if len(info.get("description") or "") > 500:
        description += "…"

    episode = {
        "guid":        guid,
        "title":       info["title"],
        "description": description,
        "uploader":    info.get("uploader", ""),
        "duration":    info.get("duration", 0),
        "thumbnail":   info.get("thumbnail", ""),
        "audio_url":   audio_url,
        "file_size":   file_size,
        "source_url":  info.get("webpage_url", url),
        "pub_date":    datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"),
    }

    state.setdefault("episodes", []).append(episode)
    state.setdefault("processed_urls", []).append(guid)
    save_state(state)

    print("Updating RSS feed…")
    feed_url = upload_feed(cfg, state["episodes"])

    print(f"\n✅ Added: {info['title']}")
    print(f"🎙️  Feed:  {feed_url}")


def cmd_sync_youtube(playlist_id: str):
    cfg     = get_config()
    state   = load_state()
    seen    = set(state.get("processed_urls", []))

    print(f"Fetching playlist: {playlist_id}")
    video_ids = get_playlist_video_ids(playlist_id)
    print(f"Found {len(video_ids)} videos in playlist")

    added = 0
    for vid_id in video_ids:
        url  = f"https://www.youtube.com/watch?v={vid_id}"
        guid = url_guid(url)
        if guid in seen:
            print(f"  skip (already in feed): {vid_id}")
            continue
        print(f"  adding: {vid_id}")
        cmd_add(url)
        state = load_state()  # Reload after each add
        seen  = set(state.get("processed_urls", []))
        added += 1
        time.sleep(1)  # Rate limiting courtesy

    print(f"\nSync complete — {added} new episode(s) added.")


def cmd_feed():
    cfg = get_config()
    print(f"{cfg['public_base']}/feed.xml")


def cmd_list():
    state    = load_state()
    episodes = state.get("episodes", [])
    if not episodes:
        print("No episodes yet. Use: video_podcast.py add <url>")
        return
    print(f"{'#':<4} {'Title':<52} {'Duration':<10} {'Added'}")
    print("─" * 90)
    for i, ep in enumerate(episodes, 1):
        dur  = int(ep.get("duration", 0))
        m, s = divmod(dur, 60)
        h, m = divmod(m, 60)
        dur_str  = f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"
        date_str = ep.get("pub_date", "")[:16]
        title    = ep["title"][:50]
        print(f"{i:<4} {title:<52} {dur_str:<10} {date_str}")


def cmd_remove(identifier: str):
    state    = load_state()
    episodes = state.get("episodes", [])
    guid     = url_guid(identifier) if identifier.startswith("http") else identifier
    before   = len(episodes)

    state["episodes"]       = [e for e in episodes if e.get("guid") != guid]
    state["processed_urls"] = [u for u in state.get("processed_urls", []) if u != guid]

    if len(state["episodes"]) == before:
        print(f"Episode not found: {identifier}")
        return

    save_state(state)
    cfg = get_config()
    print("Updating RSS feed…")
    upload_feed(cfg, state["episodes"])
    print(f"✅ Removed episode {guid}")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="video_podcast.py",
        description="video-podcast — turn bookmarked videos into a podcast feed",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("setup", help="Interactive first-time setup")

    p = sub.add_parser("add", help="Add a video URL to the podcast feed")
    p.add_argument("url", help="Video URL (YouTube, X/Twitter, or any yt-dlp source)")

    p = sub.add_parser("sync-youtube", help="Sync new videos from a YouTube playlist")
    p.add_argument("playlist_id", help="YouTube playlist ID (the part after list=)")

    sub.add_parser("sync-x", help="Placeholder — use 'add <url>' for individual X videos")
    sub.add_parser("feed",   help="Print the RSS feed URL")
    sub.add_parser("list",   help="List all episodes in the feed")

    p = sub.add_parser("remove", help="Remove an episode by source URL or GUID")
    p.add_argument("identifier", help="Source URL or episode GUID")

    args = parser.parse_args()

    dispatch = {
        "setup":         cmd_setup,
        "feed":          cmd_feed,
        "list":          cmd_list,
        "sync-x":        lambda: print(
            "sync-x is not yet automated. Use 'add <url>' for individual X/Twitter URLs."
        ),
    }

    if args.cmd in dispatch:
        dispatch[args.cmd]()
    elif args.cmd == "add":
        cmd_add(args.url)
    elif args.cmd == "sync-youtube":
        cmd_sync_youtube(args.playlist_id)
    elif args.cmd == "remove":
        cmd_remove(args.identifier)


if __name__ == "__main__":
    main()
