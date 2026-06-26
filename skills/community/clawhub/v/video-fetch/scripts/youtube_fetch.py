#!/usr/bin/env python3
"""
Video content fetcher: YouTube & Bilibili.
Fallback chain: subtitle/transcript API -> STT (ElevenLabs or Whisper) -> description.

Required: requests, youtube-transcript-api
Optional: yt-dlp (for audio STT), openai-whisper + ffmpeg (for local Whisper)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


# ── Utilities ───────────────────────────────────────────────────────────────

def detect_platform(url_or_id):
    if "bilibili.com" in url_or_id or "b23.tv" in url_or_id:
        return "bilibili"
    return "youtube"


def _load_secret(arg):
    """Load secret from argument: raw string or @filepath."""
    if not arg:
        return None
    if arg.startswith("@"):
        path = os.path.expanduser(arg[1:])
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return arg


def _download_audio(video_url, tmpdir, proxy=None, bili_info=None):
    """Download audio with yt-dlp, fallback to Bilibili playurl API. Returns audio file path or None."""
    audio_file = _download_audio_ytdlp(video_url, tmpdir, proxy=proxy)
    if audio_file:
        return audio_file

    # Fallback: Bilibili playurl API (bypasses yt-dlp 412 blocks on VPS/datacenter IPs)
    if bili_info and bili_info.get("bvid") and bili_info.get("cid"):
        return _download_bilibili_audio(bili_info, tmpdir, proxy=proxy)

    return None


def _download_audio_ytdlp(video_url, tmpdir, proxy=None):
    """Download audio with yt-dlp. Returns audio file path or None."""
    if not shutil.which("yt-dlp"):
        print("WARN: yt-dlp not found, cannot download audio", file=sys.stderr)
        return None

    audio_out = os.path.join(tmpdir, "audio.%(ext)s")
    dl_cmd = [
        "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "5",
        "-o", audio_out, "--no-playlist", video_url,
    ]
    if proxy:
        dl_cmd.extend(["--proxy", proxy])

    print("INFO: Downloading audio with yt-dlp...", file=sys.stderr)
    try:
        subprocess.run(dl_cmd, check=True, capture_output=True, text=True, timeout=300)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"WARN: yt-dlp failed: {e}", file=sys.stderr)
        return None

    for f in os.listdir(tmpdir):
        if f.startswith("audio."):
            return os.path.join(tmpdir, f)
    print("WARN: No audio file downloaded", file=sys.stderr)
    return None


def _download_bilibili_audio(bili_info, tmpdir, proxy=None):
    """Download audio via Bilibili playurl API. Returns audio file path or None."""
    import requests

    bvid = bili_info["bvid"]
    cid = bili_info["cid"]
    cookie = bili_info.get("cookie")

    api = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16&fourk=1"
    proxies = {"https": proxy, "http": proxy} if proxy else {}

    print("INFO: Trying Bilibili playurl API for audio...", file=sys.stderr)
    try:
        resp = requests.get(api, proxies=proxies, headers=_bili_headers(cookie), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            print(f"WARN: Bilibili playurl: {data.get('message')}", file=sys.stderr)
            return None

        dash = data.get("data", {}).get("dash")
        if not dash or not dash.get("audio"):
            print("WARN: Bilibili playurl: no DASH audio streams", file=sys.stderr)
            return None

        # Pick highest quality audio stream
        audio_streams = sorted(dash["audio"], key=lambda a: a.get("bandwidth", 0), reverse=True)
        audio_url = audio_streams[0].get("baseUrl") or audio_streams[0].get("base_url")
        if not audio_url:
            return None

        # Download m4s audio
        m4s_path = os.path.join(tmpdir, "audio.m4s")
        print(f"INFO: Downloading audio stream from Bilibili...", file=sys.stderr)
        dl_headers = _bili_headers(cookie)
        dl_headers["Referer"] = f"https://www.bilibili.com/video/{bvid}"
        r = requests.get(audio_url, headers=dl_headers, proxies=proxies, stream=True, timeout=(15, 300))
        r.raise_for_status()
        with open(m4s_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                f.write(chunk)

        # Convert to mp3 with ffmpeg
        mp3_path = os.path.join(tmpdir, "audio.mp3")
        if shutil.which("ffmpeg"):
            print("INFO: Converting to mp3 with ffmpeg...", file=sys.stderr)
            subprocess.run(
                ["ffmpeg", "-i", m4s_path, "-vn", "-acodec", "libmp3lame", "-q:a", "5", mp3_path, "-y"],
                check=True, capture_output=True, timeout=120,
            )
            return mp3_path
        else:
            # No ffmpeg, return m4s directly (ElevenLabs accepts various formats)
            print("INFO: No ffmpeg, using m4s format directly", file=sys.stderr)
            return m4s_path

    except Exception as e:
        print(f"WARN: Bilibili audio download failed: {e}", file=sys.stderr)
        return None


# ── YouTube ─────────────────────────────────────────────────────────────────

def extract_youtube_id(url_or_id):
    patterns = [
        r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return url_or_id


def fetch_youtube_transcript(video_id, proxy=None, languages=None):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("WARN: youtube-transcript-api not installed", file=sys.stderr)
        return None

    langs = languages or ["zh-Hans", "zh-Hant", "zh", "en", "ja", "ko"]
    try:
        if proxy:
            os.environ["HTTP_PROXY"] = proxy
            os.environ["HTTPS_PROXY"] = proxy
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=langs)
        lines = [entry.text for entry in transcript.snippets]
        return "\n".join(lines)
    except Exception as e:
        print(f"WARN: YouTube transcript failed: {e}", file=sys.stderr)
        return None


def fetch_youtube_meta(video_id, proxy=None):
    """Returns (description, title) from YouTube page."""
    import requests

    url = f"https://www.youtube.com/watch?v={video_id}"
    proxies = {"https": proxy, "http": proxy} if proxy else {}
    try:
        resp = requests.get(
            url, proxies=proxies, timeout=30,
            headers={"Accept-Language": "en-US,en;q=0.9,zh;q=0.8"},
        )
        resp.raise_for_status()
        html = resp.text

        title_m = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html)
        title = title_m.group(1) if title_m else None

        og_m = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html)
        og_desc = og_m.group(1) if og_m else ""

        full_desc = None
        player_m = re.search(r'var\s+ytInitialPlayerResponse\s*=\s*(\{.+?\});', html)
        if player_m:
            try:
                pd = json.loads(player_m.group(1))
                full_desc = pd.get("videoDetails", {}).get("shortDescription", "")
            except json.JSONDecodeError:
                pass

        desc = full_desc if full_desc and len(full_desc) > len(og_desc) else og_desc
        for old, new in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                         ("&quot;", '"'), ("&#39;", "'")]:
            desc = desc.replace(old, new)
        return desc, title
    except Exception as e:
        print(f"WARN: YouTube meta failed: {e}", file=sys.stderr)
        return None, None


# ── Bilibili ────────────────────────────────────────────────────────────────

def extract_bilibili_id(url):
    m = re.search(r'(BV[a-zA-Z0-9]{10})', url)
    if m:
        return m.group(1)
    m = re.search(r'av(\d+)', url, re.IGNORECASE)
    if m:
        return f"av{m.group(1)}"
    return None


def resolve_b23(url, proxy=None):
    if "b23.tv" not in url:
        return url
    import requests
    proxies = {"https": proxy, "http": proxy} if proxy else {}
    try:
        resp = requests.head(url, allow_redirects=True, proxies=proxies, timeout=10)
        return resp.url
    except Exception:
        return url


def _bili_headers(cookie=None):
    h = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
    }
    if cookie:
        h["Cookie"] = cookie
    return h


def fetch_bilibili_info(bvid, proxy=None, cookie=None):
    import requests
    if bvid.startswith("av"):
        api = f"https://api.bilibili.com/x/web-interface/view?aid={bvid[2:]}"
    else:
        api = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    proxies = {"https": proxy, "http": proxy} if proxy else {}
    try:
        resp = requests.get(api, proxies=proxies, headers=_bili_headers(cookie), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            print(f"WARN: Bilibili API: {data.get('message')}", file=sys.stderr)
            return None
        d = data["data"]
        return {
            "title": d.get("title"),
            "desc": d.get("desc"),
            "cid": d.get("cid"),
            "bvid": d.get("bvid"),
            "aid": d.get("aid"),
        }
    except Exception as e:
        print(f"WARN: Bilibili info failed: {e}", file=sys.stderr)
        return None


def fetch_bilibili_subtitle(bvid, cid, proxy=None, cookie=None):
    import requests
    api = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
    proxies = {"https": proxy, "http": proxy} if proxy else {}
    try:
        resp = requests.get(api, proxies=proxies, headers=_bili_headers(cookie), timeout=15)
        resp.raise_for_status()
        subtitles = resp.json().get("data", {}).get("subtitle", {}).get("subtitles", [])
        if not subtitles:
            return None
        chosen = None
        for s in subtitles:
            if any(k in s.get("lan", "") for k in ("zh", "cn", "ai-zh")):
                chosen = s
                break
        if not chosen:
            chosen = subtitles[0]
        sub_url = chosen.get("subtitle_url", "")
        if sub_url.startswith("//"):
            sub_url = "https:" + sub_url
        sub_resp = requests.get(sub_url, proxies=proxies, headers=_bili_headers(cookie), timeout=15)
        sub_resp.raise_for_status()
        lines = [item["content"] for item in sub_resp.json().get("body", [])]
        return "\n".join(lines)
    except Exception as e:
        print(f"WARN: Bilibili subtitle failed: {e}", file=sys.stderr)
        return None


# ── STT: ElevenLabs ────────────────────────────────────────────────────────

def fetch_via_elevenlabs(video_url, proxy=None, api_key=None, language=None, bili_info=None):
    """Download audio with yt-dlp, transcribe with ElevenLabs STT API."""
    if not api_key:
        api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("WARN: No ElevenLabs API key (set ELEVENLABS_API_KEY or use --stt-api-key)", file=sys.stderr)
        return None

    import requests

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file = _download_audio(video_url, tmpdir, proxy=proxy, bili_info=bili_info)
        if not audio_file:
            return None

        file_size = os.path.getsize(audio_file)
        print(f"INFO: Uploading to ElevenLabs STT ({file_size / 1024 / 1024:.1f} MB)...", file=sys.stderr)

        data = {"model_id": "scribe_v2"}
        if language:
            data["language_code"] = language

        try:
            with open(audio_file, "rb") as af:
                resp = requests.post(
                    "https://api.elevenlabs.io/v1/speech-to-text",
                    headers={"xi-api-key": api_key},
                    files={"file": (os.path.basename(audio_file), af, "audio/mpeg")},
                    data=data,
                    timeout=600,
                )

            if resp.status_code != 200:
                print(f"WARN: ElevenLabs STT failed ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
                return None

            result = resp.json()
            text = result.get("text", "")
            lang = result.get("language_code", "unknown")
            print(f"INFO: ElevenLabs transcription done (lang={lang}, {len(text)} chars)", file=sys.stderr)
            return text if text.strip() else None
        except Exception as e:
            print(f"WARN: ElevenLabs STT error: {e}", file=sys.stderr)
            return None


# ── STT: Whisper (local) ───────────────────────────────────────────────────

def fetch_via_whisper(video_url, proxy=None, model="base", bili_info=None):
    """Download audio with yt-dlp, transcribe with local Whisper."""
    if not shutil.which("whisper"):
        print("WARN: 'whisper' not found, skipping local Whisper", file=sys.stderr)
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_file = _download_audio(video_url, tmpdir, proxy=proxy, bili_info=bili_info)
        if not audio_file:
            return None

        print(f"INFO: Transcribing with Whisper (model={model})...", file=sys.stderr)
        w_cmd = [
            "whisper", audio_file,
            "--model", model,
            "--output_format", "txt",
            "--output_dir", tmpdir,
        ]
        try:
            result = subprocess.run(w_cmd, check=True, capture_output=True, text=True, timeout=600)
            if result.stdout:
                print(result.stdout[:200], file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"WARN: Whisper failed: {e.stderr[:500] if e.stderr else e}", file=sys.stderr)
            return None
        except subprocess.TimeoutExpired:
            print("WARN: Whisper timed out after 600s", file=sys.stderr)
            return None

        txt_files = [f for f in os.listdir(tmpdir) if f.endswith(".txt")]
        if not txt_files:
            return None
        with open(os.path.join(tmpdir, txt_files[0]), "r", encoding="utf-8") as f:
            return f.read().strip()


# ── STT dispatcher ─────────────────────────────────────────────────────────

def fetch_via_stt(video_url, stt, proxy=None, api_key=None, whisper_model="base", language=None, bili_info=None):
    """Try STT transcription. Returns text or None."""
    if stt == "none":
        return None

    if stt == "elevenlabs":
        text = fetch_via_elevenlabs(video_url, proxy=proxy, api_key=api_key, language=language, bili_info=bili_info)
        if text:
            return text
        # Auto-fallback to Whisper
        print("INFO: ElevenLabs unavailable, trying local Whisper...", file=sys.stderr)
        return fetch_via_whisper(video_url, proxy=proxy, model=whisper_model, bili_info=bili_info)

    if stt == "whisper":
        return fetch_via_whisper(video_url, proxy=proxy, model=whisper_model, bili_info=bili_info)

    return None


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Fetch video content (YouTube & Bilibili)")
    p.add_argument("video", help="Video URL or ID")
    p.add_argument("--proxy", help="Proxy URL (e.g. socks5h://127.0.0.1:1080)")
    p.add_argument("--langs", default="zh-Hans,zh-Hant,zh,en",
                   help="Comma-separated transcript language codes")
    p.add_argument("--output", help="Output file (default: stdout)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--stt", choices=["elevenlabs", "whisper", "none"], default="elevenlabs",
                   help="Speech-to-text engine (default: elevenlabs)")
    p.add_argument("--stt-api-key",
                   help="ElevenLabs API key or @filepath (also reads ELEVENLABS_API_KEY env)")
    p.add_argument("--whisper-model", default="base",
                   help="Whisper model: tiny/base/small/medium/large (default: base)")
    p.add_argument("--platform", choices=["youtube", "bilibili"],
                   help="Force platform (auto-detected by default)")
    p.add_argument("--cookie",
                   help="Bilibili cookie string or @filepath (required for AI subtitles)")
    args = p.parse_args()

    url = args.video
    platform = args.platform or detect_platform(url)
    languages = args.langs.split(",")
    cookie = _load_secret(args.cookie)
    stt_api_key = _load_secret(args.stt_api_key)

    content = None
    source = None
    title = None

    if platform == "bilibili":
        url = resolve_b23(url, proxy=args.proxy)
        bvid = extract_bilibili_id(url)
        if not bvid:
            print("ERROR: Cannot extract Bilibili video ID", file=sys.stderr)
            sys.exit(1)

        info = fetch_bilibili_info(bvid, proxy=args.proxy, cookie=cookie)
        if info:
            title = info.get("title")
            content = fetch_bilibili_subtitle(
                info.get("bvid", bvid), info["cid"], proxy=args.proxy, cookie=cookie
            )
            if content:
                source = "subtitle"

        if not content and args.stt != "none":
            video_url = f"https://www.bilibili.com/video/{bvid}"
            bili_dl_info = {
                "bvid": info.get("bvid", bvid) if info else bvid,
                "cid": info["cid"] if info else None,
                "cookie": cookie,
            } if info else None
            content = fetch_via_stt(
                video_url, args.stt, proxy=args.proxy,
                api_key=stt_api_key, whisper_model=args.whisper_model,
                bili_info=bili_dl_info,
            )
            if content:
                source = f"stt:{args.stt}"

        if not content and info:
            desc = info.get("desc", "")
            if desc and desc.strip() and desc.strip() != "-":
                content = desc
                source = "description"

    else:  # youtube
        video_id = extract_youtube_id(url)

        content = fetch_youtube_transcript(video_id, proxy=args.proxy, languages=languages)
        if content:
            source = "transcript"

        if not content and args.stt != "none":
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            content = fetch_via_stt(
                video_url, args.stt, proxy=args.proxy,
                api_key=stt_api_key, whisper_model=args.whisper_model,
            )
            if content:
                source = f"stt:{args.stt}"

        # Always try to get title; use description as last resort
        desc, title = fetch_youtube_meta(video_id, proxy=args.proxy)
        if not content and desc:
            content = desc
            source = "description"

    if not content:
        print("ERROR: Could not fetch any content for this video", file=sys.stderr)
        sys.exit(1)

    # ── Output ──
    if args.json:
        out = json.dumps({
            "platform": platform,
            "title": title,
            "source": source,
            "content_length": len(content),
            "content": content,
        }, ensure_ascii=False, indent=2)
    else:
        header = f"# {title}\n\n" if title else ""
        notice = ""
        if source == "description":
            notice = ("WARNING: No transcript/subtitles available. "
                      "Content below is from the video description, not a full transcript.\n\n")
        elif source and source.startswith("stt:"):
            engine = source.split(":")[1]
            notice = (f"NOTE: Transcribed from audio via {engine}. "
                      "Minor inaccuracies may exist.\n\n")
        out = f"{header}{notice}{content}"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"OK: {args.output} ({len(content)} chars, source={source})", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
