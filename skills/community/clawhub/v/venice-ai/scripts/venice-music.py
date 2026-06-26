#!/usr/bin/env python3
"""Generate music via Venice AI Audio API (queue-based async, similar to video)."""

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Import shared utilities
sys.path.insert(0, str(Path(__file__).parent))
from venice_common import (
    require_api_key,
    list_models,
    print_models,
    print_media_line,
    default_out_dir,
    USER_AGENT,
)

DEFAULT_MODEL = "elevenlabs-music"


def get_music_quote(
    api_key: str,
    model: str,
    duration_seconds: int | None = None,
) -> dict:
    """Get a price quote for music generation."""
    url = "https://api.venice.ai/api/v1/audio/quote"

    payload: dict = {"model": model}
    if duration_seconds is not None:
        payload["duration_seconds"] = duration_seconds

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def queue_music(
    api_key: str,
    model: str,
    prompt: str,
    lyrics_prompt: str | None = None,
    duration_seconds: int | None = None,
    force_instrumental: bool = False,
    voice: str | None = None,
    language_code: str | None = None,
) -> dict:
    """Queue a music generation request."""
    url = "https://api.venice.ai/api/v1/audio/queue"

    payload: dict = {
        "model": model,
        "prompt": prompt,
    }

    if lyrics_prompt:
        payload["lyrics_prompt"] = lyrics_prompt
    if duration_seconds is not None:
        payload["duration_seconds"] = duration_seconds
    if force_instrumental:
        payload["force_instrumental"] = True
    if voice:
        payload["voice"] = voice
    if language_code:
        payload["language_code"] = language_code

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def retrieve_music(
    api_key: str,
    queue_id: str,
    delete_on_completion: bool = True,
) -> tuple[str, bytes | None, dict]:
    """
    Check music generation status and retrieve if complete.
    Returns (status, audio_bytes or None, timing_info).
    """
    url = "https://api.venice.ai/api/v1/audio/retrieve"

    payload = {
        "queue_id": queue_id,
        "delete_media_on_completion": delete_on_completion,
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content_type = resp.headers.get("Content-Type", "")

            if "audio/" in content_type or "application/octet-stream" in content_type:
                # Audio is ready
                return "COMPLETED", resp.read(), {}

            data = json.loads(resp.read().decode("utf-8"))
            status = data.get("status", "UNKNOWN")
            timing_info = {
                "average_execution_time": data.get("average_execution_time"),
                "execution_duration": data.get("execution_duration"),
            }
            return status, None, timing_info

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "NOT_FOUND", None, {}
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def complete_music(api_key: str, queue_id: str) -> bool:
    """
    Mark music as completed and delete from server storage.
    Use after downloading with --no-delete.
    """
    url = "https://api.venice.ai/api/v1/audio/complete"

    payload = {"queue_id": queue_id}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("success", False)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate music via Venice AI Audio API (queue-based async generation).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get price quote
  python3 venice-music.py --quote --model elevenlabs-music --duration 60

  # Generate instrumental music
  python3 venice-music.py --prompt "epic orchestral battle theme" --instrumental

  # Generate music with lyrics
  python3 venice-music.py --prompt "upbeat pop song" --lyrics "verse 1: walking down the street..."

  # Generate and save to specific dir
  python3 venice-music.py --prompt "ambient piano" --duration 30 --out-dir ./music

  # Clean up server-side media
  python3 venice-music.py --complete QUEUE_ID
""",
    )

    ap.add_argument("--prompt", help="Music description (style, mood, genre, instruments)")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Model ID (default: {DEFAULT_MODEL})")
    ap.add_argument("--duration", type=int, metavar="SECONDS",
                    help="Duration in seconds (model-dependent)")
    ap.add_argument("--lyrics", dest="lyrics_prompt",
                    help="Optional lyrics for lyric-capable models")
    ap.add_argument("--instrumental", action="store_true", dest="force_instrumental",
                    help="Generate instrumental (no vocals)")
    ap.add_argument("--voice", help="Voice selection for vocal tracks")
    ap.add_argument("--language", dest="language_code",
                    help="Language code (e.g., en, es, fr, de)")
    ap.add_argument("--out-dir", help="Output directory (default: auto-generated)")
    ap.add_argument("--output", "-o", help="Output filename (default: auto-generated .mp3)")
    ap.add_argument("--poll-interval", type=int, default=10,
                    help="Status check interval in seconds (default: 10)")
    ap.add_argument("--timeout", type=int, default=300,
                    help="Max wait time in seconds (default: 300)")
    ap.add_argument("--no-delete", action="store_true",
                    help="Don't delete server media after download")
    ap.add_argument("--complete", metavar="QUEUE_ID",
                    help="Mark a previously downloaded track as complete (cleanup)")
    ap.add_argument("--quote", action="store_true",
                    help="Show price estimate and exit (no generation)")
    ap.add_argument("--list-models", action="store_true",
                    help="List available audio models and exit")
    args = ap.parse_args()

    api_key = require_api_key()

    # Handle --complete (cleanup)
    if args.complete:
        try:
            success = complete_music(api_key, args.complete)
            if success:
                print(f"Track {args.complete} cleaned up successfully")
                return 0
            else:
                print(f"Failed to clean up track {args.complete}", file=sys.stderr)
                return 1
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Handle --list-models
    if args.list_models:
        try:
            models = list_models(api_key, "audio")
            print_models(models)
            return 0
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Handle --quote
    if args.quote:
        try:
            quote = get_music_quote(
                api_key=api_key,
                model=args.model,
                duration_seconds=args.duration,
            )
            price = quote.get("quote", 0)
            print(f"\nMusic Generation Price Quote")
            print(f"  Model: {args.model}")
            if args.duration:
                print(f"  Duration: {args.duration}s")
            print(f"\n  Estimated cost: ${price:.4f} USD")
            return 0
        except RuntimeError as e:
            print(f"Error getting quote: {e}", file=sys.stderr)
            return 1

    # Require prompt for generation
    if not args.prompt:
        print("Error: --prompt is required for music generation", file=sys.stderr)
        print("       Use --quote to get a price estimate, or --list-models to see models", file=sys.stderr)
        return 2

    # Queue music generation
    print(f"Queuing music generation...", flush=True)
    print(f"  Model: {args.model}")
    print(f"  Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    if args.lyrics_prompt:
        print(f"  Lyrics: {args.lyrics_prompt[:60]}{'...' if len(args.lyrics_prompt) > 60 else ''}")
    if args.duration:
        print(f"  Duration: {args.duration}s")
    if args.force_instrumental:
        print(f"  Mode: instrumental")
    if args.voice:
        print(f"  Voice: {args.voice}")
    if args.language_code:
        print(f"  Language: {args.language_code}")

    try:
        queue_result = queue_music(
            api_key=api_key,
            model=args.model,
            prompt=args.prompt,
            lyrics_prompt=args.lyrics_prompt,
            duration_seconds=args.duration,
            force_instrumental=args.force_instrumental,
            voice=args.voice,
            language_code=args.language_code,
        )
    except RuntimeError as e:
        print(f"\nError queuing music: {e}", file=sys.stderr)
        return 1

    queue_id = queue_result.get("queue_id")
    if not queue_id:
        print(f"Error: No queue_id in response: {queue_result}", file=sys.stderr)
        return 1

    print(f"\nQueued successfully!")
    print(f"  Queue ID: {queue_id}")

    # Poll for completion
    print(f"\nWaiting for music generation (polling every {args.poll_interval}s, timeout {args.timeout}s)...")

    start_time = time.time()
    last_status = None
    last_timing_shown = None

    while True:
        elapsed = time.time() - start_time
        if elapsed > args.timeout:
            print(f"\nTimeout after {args.timeout}s", file=sys.stderr)
            print(f"Queue ID for later: {queue_id}", file=sys.stderr)
            return 1

        try:
            status, audio_data, timing_info = retrieve_music(
                api_key=api_key,
                queue_id=queue_id,
                delete_on_completion=not args.no_delete,
            )
        except RuntimeError as e:
            print(f"\nError retrieving music: {e}", file=sys.stderr)
            return 1

        # Build status message
        timing_str = ""
        avg_time = timing_info.get("average_execution_time")
        exec_dur = timing_info.get("execution_duration")
        if avg_time and exec_dur:
            progress_pct = min(100, int((exec_dur / avg_time) * 100))
            timing_str = f" ({exec_dur // 1000}s / ~{avg_time // 1000}s avg, ~{progress_pct}%)"
        elif exec_dur:
            timing_str = f" ({exec_dur // 1000}s elapsed)"

        status_msg = f"{status}{timing_str}"
        if status != last_status or timing_str != last_timing_shown:
            print(f"  [{int(elapsed)}s] Status: {status_msg}")
            last_status = status
            last_timing_shown = timing_str

        if status == "COMPLETED" and audio_data:
            # Determine output path
            if args.output:
                out_path = Path(args.output).expanduser()
            else:
                out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir("venice-music")
                out_dir.mkdir(parents=True, exist_ok=True)
                timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
                out_path = out_dir / f"music-{timestamp}.mp3"

            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(audio_data)

            # Save metadata
            metadata = {
                "queue_id": queue_id,
                "model": args.model,
                "prompt": args.prompt,
                "lyrics_prompt": args.lyrics_prompt,
                "duration_seconds": args.duration,
                "force_instrumental": args.force_instrumental,
                "voice": args.voice,
                "language_code": args.language_code,
                "generated_at": dt.datetime.now().isoformat(),
            }
            (out_path.parent / f"{out_path.stem}-metadata.json").write_text(
                json.dumps(metadata, indent=2), encoding="utf-8"
            )

            print(f"\nMusic saved: {out_path.as_posix()}")
            print(f"Size: {len(audio_data) / 1024:.1f}KB")
            print_media_line(out_path)
            return 0

        if status == "NOT_FOUND":
            print(f"\nError: Track not found (may have expired)", file=sys.stderr)
            return 1

        if status in ("FAILED", "ERROR", "CANCELLED"):
            print(f"\nMusic generation failed: {status}", file=sys.stderr)
            return 1

        if status not in ("PROCESSING", "QUEUED", "PENDING"):
            print(f"\nUnexpected status: {status}", file=sys.stderr)

        time.sleep(args.poll_interval)


if __name__ == "__main__":
    raise SystemExit(main())
