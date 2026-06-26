#!/usr/bin/env python3
"""
YouTube / Bilibili Summarizer - Universal Video Summarization Tool

Usage:
  youtube-summarizer --url "https://youtube.com/watch?v=VIDEO_ID"
  youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx"
  youtube-summarizer --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
  youtube-summarizer --config channels.json --daily --output /tmp/youtube_summary.json
"""

import os
import sys
import json
import glob
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
from pathlib import Path

# Default config
DEFAULT_MIN_DURATION = 300  # 5 minutes (filter Shorts)
DEFAULT_HOURS_LOOKBACK = 24
DEFAULT_MAX_VIDEOS_PER_CHANNEL = 5
DEFAULT_OUTPUT = "/tmp/youtube_summary.json"
DEFAULT_WHISPER_MODEL = "small"
DEFAULT_FRAME_INTERVAL = 30  # seconds

# ─────────────────────────────────────────────
# Config loader
# ─────────────────────────────────────────────

def load_settings() -> dict:
    """Load settings from config/settings.json (relative to this script's skill root)."""
    skill_root = Path(__file__).parent.parent
    config_path = skill_root / "config" / "settings.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


SETTINGS = load_settings()


def resolve_mode(args_mode: str | None) -> str:
    """Resolve effective mode: CLI arg > env var > config file > default (ai-review)."""
    if args_mode:
        return args_mode
    env_mode = os.environ.get("SUMMARY_MODE")
    if env_mode:
        return env_mode
    return SETTINGS.get("default_mode", "ai-review")

SUMMARY_PROMPT_TEMPLATE = """You are a professional content analyst. Please generate an in-depth, practical summary (at least 300 words) for the following video transcript.

Video Title: {title}
Channel: {channel}
Duration: {duration}
Transcript: {transcript}

Please output strictly in the following format (no preamble):

### 🎯 Core Problem/Innovation
- Summarize in one sentence what problem the video addresses
- What novel perspectives or technical breakthroughs are presented

### 💡 Key Arguments (detailed, 2-3 sentences each)
1. **Argument 1**: Detailed explanation with specific data, examples, or evidence
2. **Argument 2**: ...
3. **Argument 3**: ...

### 🛠️ Practical Steps (if applicable)
1. Step 1: Specific instructions
2. Step 2: ...

### 💰 Value & Application
- Who would benefit from this content
- How to apply it to real work/life situations

### ⚠️ Considerations
- Risks, limitations, and important notes"""


# ─────────────────────────────────────────────
# Platform detection
# ─────────────────────────────────────────────

def detect_platform(url: str) -> str:
    """Detect video platform from URL."""
    if 'bilibili.com' in url or 'b23.tv' in url:
        return 'bilibili'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    else:
        return 'unknown'


# ─────────────────────────────────────────────
# Bilibili helpers
# ─────────────────────────────────────────────

def extract_bilibili_id(url: str) -> str:
    """Extract BV number from Bilibili URL (follows b23.tv short links)."""
    import re
    if 'b23.tv' in url:
        try:
            import requests
            r = requests.head(url, allow_redirects=True, timeout=10)
            url = r.url
        except Exception:
            pass
    match = re.search(r'BV[\w]+', url)
    return match.group(0) if match else "unknown"


def select_key_frames(frame_files: list, target_count: int = 10, oversample_ratio: float = 1.5) -> list:
    """按固定规则从所有帧中选择关键帧

    规则：
    - 如果总帧数 <= actual_count + 3，全部使用
    - 否则均匀选取 actual_count 张（包含首帧和末帧）
    - actual_count = round(target_count * oversample_ratio)，多选留余量
    """
    total = len(frame_files)
    actual_count = min(round(target_count * oversample_ratio), total)

    if total <= actual_count + 3:
        return frame_files

    indices = [0]
    step = (total - 1) / (actual_count - 1)
    for i in range(1, actual_count - 1):
        indices.append(round(i * step))
    indices.append(total - 1)

    indices = sorted(set(indices))
    return [frame_files[i] for i in indices]


def process_bilibili_video(
    url: str,
    output_dir: str = "/tmp",
    whisper_model: str = DEFAULT_WHISPER_MODEL,
    frame_interval: int = DEFAULT_FRAME_INTERVAL,
    skip_frames: bool = False,
    max_frames: int = 10,
) -> Dict:
    """
    Process a Bilibili video:
      1. Download video via yt-dlp (Chrome cookies bypass 412)
      2. Extract audio with ffmpeg
      3. Transcribe with faster-whisper
      4. Extract keyframes with ffmpeg (optional)
    Returns a dict with paths and transcript text.
    """
    video_id = extract_bilibili_id(url)
    video_path = os.path.join(output_dir, f"bili_{video_id}.mp4")
    audio_path = os.path.join(output_dir, f"bili_{video_id}_audio.mp3")
    frames_dir = os.path.join(output_dir, f"bili_{video_id}_frames")
    transcript_path = os.path.join(output_dir, f"bili_{video_id}_transcript.txt")

    print(f"🎬 Bilibili: {video_id}", file=sys.stderr)

    # Step 1: Download video
    print("  📥 Downloading video...", file=sys.stderr)
    download_cmd = [
        "yt-dlp",
        "--cookies-from-browser", "chrome",
        "--no-check-certificates",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "--merge-output-format", "mp4",
        "-o", video_path,
        url,
    ]
    subprocess.run(download_cmd, check=True, timeout=300)

    # Step 2: Extract audio
    print("  🎵 Extracting audio...", file=sys.stderr)
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        audio_path,
    ], check=True, timeout=120, capture_output=True)

    # Step 3: Whisper transcription
    print(f"  🗣️  Transcribing (whisper {whisper_model})...", file=sys.stderr)
    from faster_whisper import WhisperModel
    model = WhisperModel(whisper_model, device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(audio_path, language="zh")

    segments_list = list(segments_iter)
    transcript_lines = [f"[{s.start:.1f}-{s.end:.1f}] {s.text}" for s in segments_list]
    transcript_with_timestamps = "\n".join(transcript_lines)
    transcript_plain = " ".join(s.text for s in segments_list)

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_with_timestamps)
    print(f"  ✅ Transcript: {len(transcript_plain)} chars", file=sys.stderr)

    # Step 4: Extract keyframes
    frame_files = []
    if not skip_frames:
        print(f"  🖼️  Extracting keyframes (every {frame_interval}s)...", file=sys.stderr)
        os.makedirs(frames_dir, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"fps=1/{frame_interval}", "-q:v", "2",
            os.path.join(frames_dir, "frame_%03d.jpg"),
        ], check=True, timeout=120, capture_output=True)
        frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
        print(f"  ✅ Keyframes: {len(frame_files)}", file=sys.stderr)

    # Select key frames
    FRAME_TIME_OFFSET = int(os.environ.get("FRAME_TIME_OFFSET", "5"))
    selected_frames = select_key_frames(frame_files, max_frames) if frame_files else []
    frame_time_map = []
    for frame_path in selected_frames:
        frame_num = int(os.path.basename(frame_path).split('_')[1].split('.')[0])
        time_sec = (frame_num - 1) * frame_interval + FRAME_TIME_OFFSET  # +偏移避开转场
        frame_time_map.append({
            "file": os.path.basename(frame_path),
            "time_sec": time_sec
        })

    return {
        "video_id": video_id,
        "platform": "bilibili",
        "video_path": video_path,
        "audio_path": audio_path,
        "transcript_path": transcript_path,
        "transcript": transcript_plain,
        "transcript_with_timestamps": transcript_with_timestamps,
        "frame_files": frame_files,
        "frame_count": len(frame_files),
        "selected_frames": selected_frames,
        "selected_frame_count": len(selected_frames),
        "frame_interval": frame_interval,
        "frame_time_map": frame_time_map,
    }


# ─────────────────────────────────────────────
# YouTube helpers (unchanged)
# ─────────────────────────────────────────────

def get_channel_videos(channel_id: str, hours: int, max_videos: int) -> List[Dict]:
    """Get recent videos from a YouTube channel using yt-dlp"""
    videos = []

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
    """Get video transcript using multiple methods to avoid rate limiting"""
    transcript = _get_transcript_innertube_proxy(video_id)
    if transcript:
        return transcript
    transcript = _get_transcript_ytapi(video_id)
    if transcript:
        return transcript
    return None


def _parse_caption_xml(xml_text: str) -> List[str]:
    import xml.etree.ElementTree as ET
    import html as html_mod

    try:
        root = ET.fromstring(xml_text)
        texts = []

        for p in root.findall('.//p'):
            words = []
            for s in p.findall('s'):
                if s.text:
                    words.append(html_mod.unescape(s.text.strip()))
            if words:
                texts.append(' '.join(words))
            elif p.text:
                texts.append(html_mod.unescape(p.text.strip()))

        if not texts:
            for elem in root.findall('.//text'):
                if elem.text:
                    texts.append(html_mod.unescape(elem.text.strip()))

        return texts
    except Exception:
        return []


def _download_caption(url: str) -> Optional[str]:
    try:
        import requests
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and r.text.strip():
            return r.text
    except Exception:
        pass
    return None


def _get_transcript_innertube_proxy(video_id: str) -> Optional[str]:
    try:
        import innertube

        client = innertube.InnerTube('ANDROID')
        data = client.player(video_id=video_id)

        if 'captions' not in data:
            return None

        caps = data['captions']['playerCaptionsTracklistRenderer']['captionTracks']
        if not caps:
            return None

        cap_url = None
        for prefer in ['en', 'zh-Hans', 'zh']:
            for c in caps:
                if c.get('languageCode') == prefer:
                    cap_url = c['baseUrl']
                    break
            if cap_url:
                break
        if not cap_url:
            cap_url = caps[0]['baseUrl']

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
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=["zh-Hans", "zh-Hant", "en"])
        transcript = " ".join([item.text if hasattr(item, 'text') else item["text"] for item in fetched])
        return transcript if len(transcript) > 50 else None

    except Exception:
        return None


# ─────────────────────────────────────────────
# LLM helpers (shared)
# ─────────────────────────────────────────────

def get_copilot_session_token(gh_token: str) -> Optional[str]:
    try:
        import requests
        r = requests.get(
            "https://api.github.com/copilot_internal/v2/token",
            headers={
                "Authorization": f"token {gh_token}",
                "Editor-Version": "vscode/1.95.0",
                "User-Agent": "GitHubCopilotChat/0.20.0"
            },
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get("token")
        print(f"⚠️ Failed to get Copilot token: {r.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ Copilot auth error: {e}", file=sys.stderr)
    return None


def _call_llm(api_url: str, api_key: str, model: str, prompt: str) -> Optional[str]:
    try:
        import requests
        headers = {
            "Content-Type": "application/json",
            "Editor-Version": "vscode/1.95.0",
            "User-Agent": "GitHubCopilotChat/0.20.0"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        response = requests.post(
            api_url,
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        print(f"⚠️ LLM API error: {response.status_code} {response.text[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ LLM call error: {e}", file=sys.stderr)
    return None


def generate_summary(title: str, channel: str, duration: str, transcript: str) -> Optional[str]:
    """Generate summary using LLM API (multi-backend fallback chain)."""
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        title=title,
        channel=channel,
        duration=duration,
        transcript=transcript[:8000]
    )

    env_url = os.environ.get("LLM_API_URL")
    env_key = os.environ.get("LLM_API_KEY")
    env_model = os.environ.get("LLM_MODEL", "gpt-4o-mini")

    if env_url and env_key:
        print(f"  🔑 Using LLM_API_URL env var: {env_url}", file=sys.stderr)
        result = _call_llm(env_url, env_key, env_model, prompt)
        if result:
            return result

    oc_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN")
    if oc_token:
        api_url = env_url or "http://localhost:18789/v1/chat/completions"
        print(f"  🔑 Using OPENCLAW_GATEWAY_TOKEN → {api_url}", file=sys.stderr)
        result = _call_llm(api_url, oc_token, env_model, prompt)
        if result:
            return result

    gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if gh_token:
        print("  🔑 Trying GitHub Copilot API...", file=sys.stderr)
        copilot_token = get_copilot_session_token(gh_token)
        if copilot_token:
            copilot_model = os.environ.get("LLM_MODEL", "claude-haiku-4.5")
            result = _call_llm(
                "https://api.githubcopilot.com/chat/completions",
                copilot_token,
                copilot_model,
                prompt
            )
            if result:
                return result

    poll_key = os.environ.get("POLLINATIONS_API_KEY")
    if poll_key:
        print("  🔑 Trying Pollinations API (with key)...", file=sys.stderr)
        result = _call_llm(
            "https://gen.pollinations.ai/v1/chat/completions",
            poll_key,
            "openai",
            prompt
        )
        if result:
            return result

    print("  🌐 Trying Pollinations free anonymous call...", file=sys.stderr)
    result = _call_llm(
        "https://gen.pollinations.ai/v1/chat/completions",
        "",
        "openai",
        prompt
    )
    if result:
        return result

    print("⚠️ All LLM backends failed. No summary generated.", file=sys.stderr)
    return None


# ─────────────────────────────────────────────
# YouTube video processing
# ─────────────────────────────────────────────

def process_video(video_id: str, title: str = None, channel: str = None) -> Dict:
    """Process a single YouTube video: get details, transcript, and summary"""
    print(f"📹 Processing: {video_id}")

    details = get_video_details(video_id)
    if not details:
        return {
            "video_id": video_id,
            "title": title or "Unknown",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "error": "Failed to fetch video details"
        }

    transcript = get_transcript(video_id)
    has_transcript = transcript is not None

    result = {
        "video_id": video_id,
        "title": title or "Unknown",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "platform": "youtube",
        "channel": channel or "Unknown",
        "duration": details["duration"],
        "published": details["published"],
        "has_transcript": has_transcript,
        "metadata": {
            "view_count": details.get("view_count", 0),
            "like_count": details.get("like_count", 0),
        }
    }

    if has_transcript:
        print(f"  ✅ Transcript: {len(transcript)} chars")
        summary = generate_summary(title, channel, details["duration"], transcript)
        result["summary"] = summary or "⚠️ 摘要生成失败\n\n视频有字幕但 LLM 调用失败。"
        if summary:
            print(f"  ✅ Summary: {len(summary)} chars")
    else:
        result["summary"] = f"📺 **需观看获取详细内容**\n\n视频暂无字幕，无法生成详细摘要。\n\n基于标题推测：{title}"
        print(f"  ⚠️ No transcript available")

    return result


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="YouTube / Bilibili Summarizer")
    parser.add_argument("--url", help="Single video URL (YouTube or Bilibili)")
    parser.add_argument("--channel", help="YouTube channel ID or handle")
    parser.add_argument("--config", help="Config file path (JSON)")
    parser.add_argument("--daily", action="store_true", help="Daily batch mode (requires --config)")
    parser.add_argument("--hours", type=int, default=DEFAULT_HOURS_LOOKBACK, help="Hours to look back")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON file")

    # Mode selection
    parser.add_argument("--mode",
                        choices=["text-only", "auto-insert", "ai-review"],
                        default=None,
                        help="Output mode: text-only / auto-insert / ai-review (overrides config & env)")

    # Bilibili-specific options
    parser.add_argument("--no-frames", action="store_true",
                        help="Skip keyframe extraction (Bilibili) — same as --mode text-only")
    parser.add_argument("--whisper-model",
                        default=os.environ.get("WHISPER_MODEL", SETTINGS.get("whisper_model", DEFAULT_WHISPER_MODEL)),
                        help="Whisper model size for Bilibili (default: small)")
    parser.add_argument("--frame-interval", type=int,
                        default=int(os.environ.get("FRAME_INTERVAL", SETTINGS.get("frame_interval", DEFAULT_FRAME_INTERVAL))),
                        help="Keyframe extraction interval in seconds (default: 30)")
    parser.add_argument("--max-frames", type=int,
                        default=int(os.environ.get("MAX_FRAMES", SETTINGS.get("max_frames", 15))),
                        help="Max keyframes to select (default: 15)")

    args = parser.parse_args()

    # Resolve effective mode
    effective_mode = resolve_mode(args.mode)
    # --no-frames is equivalent to text-only
    if args.no_frames:
        effective_mode = "text-only"
    skip_frames = (effective_mode == "text-only")

    print(f"🎨 图文模式: {effective_mode}", file=sys.stderr)

    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": [],
        "stats": {
            "total_videos": 0,
            "with_transcript": 0,
            "without_transcript": 0,
        }
    }

    # Mode 1: Single video (YouTube or Bilibili)
    if args.url:
        platform = detect_platform(args.url)

        if platform == 'bilibili':
            output_dir = str(Path(args.output).parent) if args.output != DEFAULT_OUTPUT else "/tmp"
            try:
                bili_result = process_bilibili_video(
                    args.url,
                    output_dir=output_dir,
                    whisper_model=args.whisper_model,
                    frame_interval=args.frame_interval,
                    skip_frames=skip_frames,
                    max_frames=args.max_frames,
                )
                summary = generate_summary(
                    title=bili_result.get("title", "B站视频"),
                    channel="Bilibili",
                    duration="unknown",
                    transcript=bili_result["transcript"],
                )
                result = {
                    "video_id": bili_result["video_id"],
                    "title": bili_result.get("title", "B站视频"),
                    "url": args.url,
                    "platform": "bilibili",
                    "mode": effective_mode,
                    "has_transcript": bool(bili_result["transcript"]),
                    "transcript_path": bili_result["transcript_path"],
                    "frame_files": bili_result["frame_files"],
                    "frame_count": bili_result["frame_count"],
                    "selected_frames": bili_result["selected_frames"],
                    "selected_frame_count": bili_result["selected_frame_count"],
                    "frame_interval": bili_result["frame_interval"],
                    "frame_time_map": bili_result["frame_time_map"],
                    "summary": summary or "摘要生成失败",
                }
                if effective_mode == "ai-review":
                    result["ai_review_hint"] = "⚠️ ai-review 模式：agent 需基于文章结构对帧进行审图（补帧/删帧/替换），再出图文版。"
                results["items"].append(result)
                results["stats"]["total_videos"] = 1
                results["stats"]["with_transcript"] = 1
            except Exception as e:
                print(f"❌ Bilibili processing failed: {e}", file=sys.stderr)
                results["items"].append({
                    "url": args.url,
                    "platform": "bilibili",
                    "error": str(e),
                })
                results["stats"]["total_videos"] = 1
                results["stats"]["without_transcript"] = 1

        elif platform == 'youtube':
            video_id = args.url.split("v=")[-1].split("&")[0]
            if "youtu.be/" in args.url:
                video_id = args.url.split("youtu.be/")[-1].split("?")[0]
            result = process_video(video_id)
            results["items"].append(result)
            results["stats"]["total_videos"] = 1
            if result.get("has_transcript"):
                results["stats"]["with_transcript"] = 1
            else:
                results["stats"]["without_transcript"] = 1

        else:
            print(f"❌ Unsupported URL platform: {args.url}", file=sys.stderr)
            sys.exit(1)

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

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Output written to: {output_path}")
    print(f"📊 Stats: {results['stats']}")


if __name__ == "__main__":
    main()
