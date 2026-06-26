#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_cache(path: Path | None) -> set[int]:
    if not path or not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {int(item["id"]) for item in data if str(item.get("zh", "")).strip()}


def cue_id(cue: dict[str, object], fallback: int) -> int:
    return int(cue.get("id", fallback))


def make_batches(items: list[dict[str, object]], batch_size: int, max_chars: int) -> list[list[dict[str, object]]]:
    batches: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    current_chars = 0
    for item in items:
        item_chars = len(str(item.get("en", "")))
        if current and (len(current) >= batch_size or current_chars + item_chars > max_chars):
            batches.append(current)
            current = []
            current_chars = 0
        current.append(item)
        current_chars += item_chars
    if current:
        batches.append(current)
    return batches


def main() -> int:
    parser = argparse.ArgumentParser(description="Create numbered subtitle batches for agent-model translation.")
    parser.add_argument("cue_json", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--cache", type=Path, help="Existing translation cache JSON")
    parser.add_argument("--batch-size", type=int, default=80)
    parser.add_argument("--max-chars", type=int, default=6000, help="Maximum English characters per batch")
    args = parser.parse_args()

    cues = json.loads(args.cue_json.read_text(encoding="utf-8"))
    completed = load_cache(args.cache)
    pending = [
        {"id": cue_id(cue, index + 1), "en": cue["en"]}
        for index, cue in enumerate(cues)
        if cue_id(cue, index + 1) not in completed
    ]
    if not pending:
        print("PASS: no pending subtitles")
        return 0

    args.out_dir.mkdir(parents=True, exist_ok=True)
    batches = make_batches(pending, args.batch_size, args.max_chars)
    for batch_index, batch in enumerate(batches):
        payload = {
            "instruction": (
                "Translate these English video subtitles into natural Simplified Chinese. "
                "Keep every id, return JSON only as an array of {id, zh}. "
                "Use concise on-screen wording. Preserve product names such as Codex, ChatGPT, "
                "Claude, Claude Code, GitHub, OpenAI, Chronicle, Computer Use, MCP."
            ),
            "items": batch,
        }
        output = args.out_dir / f"batch-{batch_index + 1:03d}.json"
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {output}")
    print(f"PASS: wrote {len(batches)} batch file(s), {len(pending)} pending cue(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
