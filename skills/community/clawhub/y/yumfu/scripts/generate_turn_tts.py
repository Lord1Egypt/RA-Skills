#!/usr/bin/env python3
"""
Generate YumFu turn TTS using stable per-save voice settings.

This script:
- resolves the save's current TTS state
- skips generation cleanly if TTS is disabled
- picks a stable voice for the active language
- generates an mp3 with Edge TTS
- prints JSON for the caller to use with message(asVoice=true)

Usage:
  python3 generate_turn_tts.py \
    --user-id 1309815719 \
    --universe game-of-thrones \
    --language en \
    --text "The campfire crackles as snow drifts over the ruined wall..."
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from resolve_tts_voice import resolve, save_path

EDGE_TTS_SCRIPT = Path.home() / "clawd" / "scripts" / "edge-tts-gen.sh"
MEDIA_DIR = Path.home() / ".openclaw" / "media" / "outbound" / "yumfu-tts"


def persist_tts(user_id: str, universe: str, patch: dict) -> None:
    path = save_path(user_id, universe)
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["tts"] = patch["tts"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate YumFu turn TTS")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--universe", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--force-voice")
    parser.add_argument("--tts", choices=["on", "off"])
    args = parser.parse_args()

    result = resolve(
        user_id=args.user_id,
        universe=args.universe,
        language=args.language,
        force_voice=args.force_voice,
        tts=args.tts,
    )

    persist_tts(args.user_id, args.universe, result["save_patch"])

    tts = result["tts"]
    if not tts.get("enabled"):
        print(json.dumps({
            "success": True,
            "generated": False,
            "reason": "tts_disabled",
            "tts": tts,
        }, ensure_ascii=False))
        return

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    output = MEDIA_DIR / f"{args.universe}-user-{args.user_id}-{ts}.mp3"

    cmd = [
        str(EDGE_TTS_SCRIPT),
        args.text,
        str(output),
        tts["current_voice"],
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(json.dumps({
            "success": False,
            "generated": False,
            "error": proc.stderr.strip() or proc.stdout.strip() or f"edge-tts failed ({proc.returncode})",
            "tts": tts,
        }, ensure_ascii=False))
        sys.exit(1)

    if not output.exists():
        print(json.dumps({
            "success": False,
            "generated": False,
            "error": "audio file missing after generation",
            "tts": tts,
        }, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({
        "success": True,
        "generated": True,
        "path": str(output),
        "voice": tts["current_voice"],
        "delivery": tts.get("delivery", "voice-bubble"),
        "language": result["language"],
        "tts": tts,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
