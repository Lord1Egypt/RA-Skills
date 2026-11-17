#!/usr/bin/env python3
"""Write an SVG scene card for the current save. Host image tools may also use image_prompt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.present import decorate, image_prompt
from rms.state import load_game
from rms.viz import scene_card_svg, write


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Real Mars Shot scene card")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    loaded = load_game(args.user_id)
    if not loaded.get("exists"):
        print(json.dumps({"ok": False, "error": "no save"}))
        sys.exit(2)
    payload = decorate(loaded["data"], {"action": "scene"})
    path = write(Path(args.out), scene_card_svg(loaded["data"], payload))
    print(json.dumps({"ok": True, "path": path, "image_prompt": image_prompt(loaded["data"], payload)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
