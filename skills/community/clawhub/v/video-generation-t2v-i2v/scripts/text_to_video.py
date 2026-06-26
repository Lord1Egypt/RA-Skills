#!/usr/bin/env python3
"""AI Video generation from text prompts using inference.sh API."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _load_env_file(path: Path) -> None:
    """Load environment variables from .env file."""
    if not path.exists() or not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def _load_default_envs(env_file: str) -> None:
    """Load default environment files."""
    if env_file:
        _load_env_file(Path(env_file).expanduser())
        return
    skill_root = Path(__file__).resolve().parent.parent
    _load_env_file(skill_root / ".env")
    _load_env_file(Path.cwd() / ".env")


def _build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate AI video from text prompt using inference.sh CLI."
    )
    parser.add_argument("--prompt", required=True, help="Video description in English.")
    parser.add_argument("--model", default="veo-3.1",
                       help="Model name (veo-3.1, veo-3, seedance-1.5-pro, wan-2.5, grok-imagine-video, omnihuman).")
    parser.add_argument("--duration", type=int, default=5, help="Video duration in seconds (default 5).")
    parser.add_argument("--width", type=int, default=1280, help="Video width (default 1280).")
    parser.add_argument("--height", type=int, default=720, help="Video height (default 720).")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second (default 24).")
    parser.add_argument("--save-dir", default="", help="Directory for saved videos (default: ./outputs/videos).")
    parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds.")
    parser.add_argument("--env-file", default="", help="Optional .env file path.")
    parser.add_argument("--dry-run", action="store_true", help="Print request and exit.")
    return parser


def _resolve_save_dir(cli_value: str) -> Path:
    """Resolve output directory."""
    if cli_value.strip():
        return Path(cli_value).expanduser()
    return Path.cwd() / "outputs" / "videos"


def generate_video_from_text(prompt: str, model: str = "veo-3.1", duration: int = 5,
                              width: int = 1280, height: int = 720, fps: int = 24,
                              save_dir: Path = None, timeout: int = 600, dry_run: bool = False) -> dict:
    """Generate video from text prompt using inference.sh CLI.

    Args:
        prompt: Video description in English
        model: Model name
        duration: Video duration in seconds
        width: Video width
        height: Video height
        fps: Frames per second
        save_dir: Output directory
        timeout: Request timeout in seconds
        dry_run: Print request and exit

    Returns:
        Generation result dictionary
    """
    if save_dir is None:
        save_dir = Path.cwd() / "outputs" / "videos"

    save_dir.mkdir(parents=True, exist_ok=True)

    # Build inference.sh command
    cmd = [
        "inference.sh",
        "video",
        "generate",
        "--model", model,
        "--prompt", prompt,
        "--duration", str(duration),
        "--width", str(width),
        "--height", str(height),
        "--fps", str(fps),
        "--output", str(save_dir),
    ]

    if dry_run:
        print(json.dumps({
            "ok": True,
            "command": " ".join(cmd),
            "prompt": prompt,
            "model": model,
            "duration": duration,
        }, ensure_ascii=False, indent=2))
        return {"ok": True, "dry_run": True}

    # Execute command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=timeout
    )

    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown error"
        return {
            "ok": False,
            "error": "Video generation failed",
            "detail": error_msg
        }

    # Parse output to find video file path
    # inference.sh typically outputs the generated file path
    output_lines = result.stdout.strip().split('\n')
    video_file = None

    for line in output_lines:
        line = line.strip()
        if line.endswith('.mp4') and Path(line).exists():
            video_file = Path(line)
            break

    # If no explicit path found, look in save_dir
    if video_file is None:
        video_files = list(save_dir.glob("*.mp4"))
        if video_files:
            # Get the most recently created file
            video_file = max(video_files, key=lambda p: p.stat().st_mtime)

    if video_file:
        return {
            "ok": True,
            "downloaded_files": [str(video_file.resolve())]
        }
    else:
        return {
            "ok": False,
            "error": "Video generation completed but output file not found",
            "stdout": result.stdout
        }


def main() -> int:
    """Main entry point."""
    args = _build_parser().parse_args()
    _load_default_envs(args.env_file)

    save_dir = _resolve_save_dir(args.save_dir)

    result = generate_video_from_text(
        prompt=args.prompt,
        model=args.model,
        duration=args.duration,
        width=args.width,
        height=args.height,
        fps=args.fps,
        save_dir=save_dir,
        timeout=args.timeout,
        dry_run=args.dry_run
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
