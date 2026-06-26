#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "runwayml>=4.0.0",
#   "httpx>=0.27.0",
# ]
# ///
"""
Generate an avatar video from text.

Flow: text -> Runway TTS (audio URL) -> Runway avatar_videos (video URL) -> download .mp4

Usage:
  uv run generate_video.py --text "Hello, how are you?"
  uv run generate_video.py --text "Hi there" --voice "Arjun"
  uv run generate_video.py --text "Hi there" --avatar-id "your-uuid"
  uv run generate_video.py --text "Hi there" --output /tmp/my-video.mp4
  uv run generate_video.py --text "Hi" --voice Maya --vertical   # 9:16 for mobile
  uv run generate_video.py --text "Hi" --voice Maya --square     # 1:1 for Telegram
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


POLL_INTERVAL = 3
POLL_TIMEOUT = 600
DEFAULT_PRESET = "cat-character"
DEFAULT_VOICE = "Maya"
RUNWAY_API_BASE_URL = "https://api.dev.runwayml.com"
API_VERSION = "2024-11-06"
VERTICAL_WIDTH = 1080
VERTICAL_HEIGHT = 1920
SQUARE_SIZE = 1080


def get_config(key: str, default: str | None = None) -> str | None:
    config_path = Path.home() / ".openclaw" / "runway-avatar.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            if key in config:
                return config[key]
        except (json.JSONDecodeError, KeyError):
            pass
    return default


def resolve_api_key(arg_key: str | None) -> str:
    key = arg_key or os.environ.get("RUNWAY_API_SECRET")
    if not key:
        print(
            "Error: No API key. Set RUNWAY_API_SECRET or pass --api-key.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def poll_task(client, task_id: str) -> dict:
    """Poll a Runway task until it reaches a terminal state."""
    start = time.time()
    while time.time() - start < POLL_TIMEOUT:
        task = client.tasks.retrieve(task_id)
        status = task.status
        if status == "SUCCEEDED":
            return task
        if status in ("FAILED", "CANCELED"):
            failure = getattr(task, "failure", None) or "Unknown error"
            print(f"Error: Task {task_id} {status}: {failure}", file=sys.stderr)
            sys.exit(1)
        elapsed = int(time.time() - start)
        print(f"  [{elapsed}s] {status}...")
        time.sleep(POLL_INTERVAL)
    print(f"Error: Task {task_id} timed out after {POLL_TIMEOUT}s.", file=sys.stderr)
    sys.exit(1)


def reencode_vertical_9_16(src: Path, dest: Path) -> None:
    """Scale up to cover 1080x1920, center-crop to exact 9:16. Requires ffmpeg on PATH."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(
            "Error: --vertical requires ffmpeg on PATH. Install ffmpeg or run without --vertical.",
            file=sys.stderr,
        )
        sys.exit(1)
    vf = (
        f"scale={VERTICAL_WIDTH}:{VERTICAL_HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={VERTICAL_WIDTH}:{VERTICAL_HEIGHT}"
    )
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(src),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def reencode_square(src: Path, dest: Path) -> None:
    """Scale and center-crop to 1080x1080 square. Best for Telegram. Requires ffmpeg on PATH."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(
            "Error: --square requires ffmpeg on PATH. Install ffmpeg or run without --square.",
            file=sys.stderr,
        )
        sys.exit(1)
    vf = (
        f"scale={SQUARE_SIZE}:{SQUARE_SIZE}:force_original_aspect_ratio=increase,"
        f"crop={SQUARE_SIZE}:{SQUARE_SIZE}"
    )
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(src),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate an avatar video from text")
    parser.add_argument(
        "--text", "-t", required=True, help="Text for the avatar to speak"
    )
    parser.add_argument(
        "--preset-id",
        help="Runway preset avatar ID (default: game-character; only for fallback)",
    )
    parser.add_argument("--avatar-id", help="Custom avatar ID (overrides --preset-id)")
    parser.add_argument("--voice", "-v", help="TTS voice preset name (default: Maya)")
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: /tmp/runway-avatar-<timestamp>.mp4)",
    )
    parser.add_argument(
        "--vertical",
        action="store_true",
        help=f"Re-encode to {VERTICAL_WIDTH}x{VERTICAL_HEIGHT} (9:16) for mobile (requires ffmpeg)",
    )
    parser.add_argument(
        "--square",
        action="store_true",
        help=f"Re-encode to {SQUARE_SIZE}x{SQUARE_SIZE} (1:1) for Telegram (requires ffmpeg)",
    )
    parser.add_argument("--api-key", "-k", help="Runway API key (overrides env)")
    args = parser.parse_args()

    vertical = args.vertical or os.environ.get(
        "SEND_VIDEO_MESSAGE_VERTICAL", ""
    ).lower() in (
        "1",
        "true",
        "yes",
    )
    square = args.square or os.environ.get(
        "SEND_VIDEO_MESSAGE_SQUARE", ""
    ).lower() in (
        "1",
        "true",
        "yes",
    )
    if vertical and square:
        print("Error: --vertical and --square are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    api_key = resolve_api_key(args.api_key)

    # Precedence: explicit --avatar-id > explicit --preset-id (ignores saved avatar) > saved/env avatar > default preset
    if args.avatar_id:
        avatar_id = args.avatar_id
        preset_id = args.preset_id or os.environ.get(
            "RUNWAY_AVATAR_PRESET", DEFAULT_PRESET
        )
    elif args.preset_id:
        avatar_id = None
        preset_id = args.preset_id
    else:
        avatar_id = os.environ.get("RUNWAY_AVATAR_ID") or get_config("avatar_id")
        preset_id = os.environ.get("RUNWAY_AVATAR_PRESET", DEFAULT_PRESET)
    voice_preset = args.voice or os.environ.get("RUNWAY_VOICE_PRESET", DEFAULT_VOICE)

    from runwayml import RunwayML
    import httpx

    client = RunwayML(api_key=api_key, base_url=RUNWAY_API_BASE_URL)

    text_preview = args.text[:60] + ("..." if len(args.text) > 60 else "")
    needs_reencode = vertical or square
    total_steps = 4 if needs_reencode else 3
    print(f'Generating video: "{text_preview}"')

    print(f"  Step 1/{total_steps}: Text-to-speech (voice: {voice_preset})...")
    tts_task = client.text_to_speech.create(
        model="eleven_multilingual_v2",
        prompt_text=args.text,
        voice={"type": "runway-preset", "preset_id": voice_preset},
    )
    tts_result = poll_task(client, tts_task.id)
    audio_url = tts_result.output[0]

    if avatar_id:
        avatar_config = {"type": "custom", "avatarId": avatar_id}
        label = f"custom ({avatar_id[:8]}...)"
    else:
        avatar_config = {"type": "runway-preset", "presetId": preset_id}
        label = f"preset ({preset_id})"

    print(f"  Step 2/{total_steps}: Avatar video (avatar: {label})...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Runway-Version": API_VERSION,
    }
    body = {
        "model": "gwm1_avatars",
        "avatar": avatar_config,
        "inputAudio": audio_url,
    }

    with httpx.Client(timeout=60) as http:
        resp = http.post(
            f"{RUNWAY_API_BASE_URL}/v1/avatar_videos", headers=headers, json=body
        )
        if resp.status_code >= 400:
            print(
                f"Error: avatar_videos returned {resp.status_code}: {resp.text}",
                file=sys.stderr,
            )
            sys.exit(1)
        video_task_id = resp.json()["id"]

    video_result = poll_task(client, video_task_id)
    video_url = video_result.output[0]

    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_path = Path(f"/tmp/runway-avatar-{timestamp}.mp4")

    print(f"  Step 3/{total_steps}: Downloading video...")
    raw_bytes: bytes
    with httpx.Client(timeout=120, follow_redirects=True) as http:
        dl = http.get(video_url)
        dl.raise_for_status()
        raw_bytes = dl.content

    if needs_reencode:
        if square:
            label = f"{SQUARE_SIZE}x{SQUARE_SIZE} (1:1) for Telegram"
        else:
            label = f"{VERTICAL_WIDTH}x{VERTICAL_HEIGHT} (9:16) for mobile"
        print(f"  Step 4/{total_steps}: Re-encoding to {label}…")
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            tmp_path.write_bytes(raw_bytes)
            if square:
                reencode_square(tmp_path, output_path)
            else:
                reencode_vertical_9_16(tmp_path, output_path)
        finally:
            tmp_path.unlink(missing_ok=True)
    else:
        output_path.write_bytes(raw_bytes)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\nDone! Video saved: {output_path} ({size_mb:.1f} MB)")
    print(f"MEDIA: {output_path}")


if __name__ == "__main__":
    main()
