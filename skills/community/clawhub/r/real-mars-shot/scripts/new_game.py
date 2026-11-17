#!/usr/bin/env python3
"""Create a Real Mars Shot save. Prints the opening brief and the public state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rms.present import opening_brief, summary_lines
from rms.state import new_state, public_view, save_game


def main() -> None:
    parser = argparse.ArgumentParser(description="Start a Real Mars Shot campaign")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--language", choices=["zh", "en"], default="zh")
    parser.add_argument("--director", default="")
    parser.add_argument("--program", default="")
    parser.add_argument("--seed", type=int, default=20260101)
    parser.add_argument("--difficulty", choices=["realistic", "hard"], default="realistic")
    parser.add_argument("--tts", choices=["on", "off"], default="on")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--no-save", action="store_true")
    args = parser.parse_args()
    state = new_state(
        user_id=args.user_id,
        language=args.language,
        director=args.director,
        program=args.program,
        seed=args.seed,
        difficulty=args.difficulty,
        tts=args.tts == "on",
    )
    saved = None if args.no_save else save_game(state, backup=False)
    payload = {
        "success": True,
        "save": saved,
        "opening": opening_brief(state),
        "summary_lines": summary_lines(state),
        "state": public_view(state),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
