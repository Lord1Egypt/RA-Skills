#!/usr/bin/env python3
"""Optional narration audio via the edge-tts CLI. Missing edge-tts is a skip, not a failed turn."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.state import load_game


def main() -> None:
    parser = argparse.ArgumentParser(description="Narrate a Real Mars Shot turn with edge-tts")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    loaded = load_game(args.user_id)
    if not loaded.get("exists"):
        print(json.dumps({"success": False, "generated": False, "error": "no save"}))
        sys.exit(2)
    state = loaded["data"]
    tts = state.get("tts", {})
    if not tts.get("enabled", True):
        print(json.dumps({"success": True, "generated": False, "reason": "tts_disabled"}))
        return
    if shutil.which("edge-tts") is None:
        print(json.dumps({
            "success": True,
            "generated": False,
            "reason": "edge_tts_missing",
            "hint": "Install the edge-tts CLI to enable narration. The turn is still valid without audio.",
        }, ensure_ascii=False))
        return
    language = state.get("language", "zh")
    voice = tts.get("voices", {}).get(language, "zh-CN-XiaoxiaoNeural" if language == "zh" else "en-US-AriaNeural")
    out = Path(args.out) if args.out else Path.home() / ".realmarsshot" / "tts" / f"{args.user_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = args.text.strip()[:4000]
    proc = subprocess.run(
        ["edge-tts", "--voice", voice, "--text", text, "--write-media", str(out)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or not out.exists():
        print(json.dumps({
            "success": False,
            "generated": False,
            "error": (proc.stderr or proc.stdout or "edge-tts failed").strip()[:500],
        }, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps({"success": True, "generated": True, "path": str(out), "voice": voice, "language": language}, ensure_ascii=False))


if __name__ == "__main__":
    main()
