from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

RUN_SCRIPT = Path(__file__).with_name("run.py")


def _parse_payload(text: str) -> Dict[str, Any] | None:
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _run_command(args: List[str]) -> Dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(RUN_SCRIPT), *args, "--json"],
        capture_output=True,
        text=True,
    )
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    payload = _parse_payload(stdout)
    if payload is not None:
        return payload
    if result.returncode != 0:
        raise RuntimeError(stderr or stdout or f"run.py exited with code {result.returncode}")
    raise RuntimeError(f"run.py did not return valid JSON: {stdout}")


def _base_args(parsed: argparse.Namespace) -> List[str]:
    args: List[str] = []
    if parsed.text:
        args.append(parsed.text)
    if parsed.input_file:
        args.extend(["--input-file", parsed.input_file])
    if parsed.project_id:
        args.extend(["--project-id", parsed.project_id])
    if parsed.language:
        args.extend(["--language", parsed.language])
    if parsed.shots is not None:
        args.extend(["--shots", str(parsed.shots)])
    if parsed.output_file:
        args.extend(["--output-file", parsed.output_file])
    if parsed.reference_image_source:
        args.extend(["--reference-image-source", parsed.reference_image_source])
    if parsed.debug_video_prompt:
        args.append("--debug-video-prompt")
    if parsed.no_render:
        args.append("--no-render")
    if parsed.no_subtitle:
        args.append("--no-subtitle")
    if parsed.no_upload:
        args.append("--no-upload")
    if parsed.allow_partial:
        args.append("--allow-partial")
    return args


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent wrapper for reelonce-skill")
    parser.add_argument("text", nargs="?", help="故事文本")
    parser.add_argument("--input-file")
    parser.add_argument("--project-id", default="")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--shots", type=int, default=None)
    parser.add_argument("--output-file", default="final_video.mp4")
    parser.add_argument("--reference-image-source", choices=("shot", "asset"), default="shot")
    parser.add_argument("--debug-video-prompt", action="store_true")
    parser.add_argument("--no-render", action="store_true")
    parser.add_argument("--no-subtitle", action="store_true")
    parser.add_argument("--no-upload", action="store_true")
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    try:
        payload = _run_command(_base_args(args))
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

    print(json.dumps(payload, ensure_ascii=False))
    raise SystemExit(0 if payload.get("status") == "done" else 1)


if __name__ == "__main__":
    main()
