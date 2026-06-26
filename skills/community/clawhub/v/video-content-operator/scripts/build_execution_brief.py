#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description="Build execution brief from video-content-operator output")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    payload = load_json(args.input)
    next_action = payload.get("next_action", {})
    handoff = next_action.get("handoff") or {}

    brief = {
        "goal": handoff.get("goal"),
        "source_material": handoff.get("source_material", []),
        "platform": handoff.get("platform"),
        "duration": handoff.get("duration"),
        "style_or_prompt": handoff.get("style_or_prompt"),
        "must_preserve": handoff.get("must_preserve", []),
    }

    print(json.dumps(brief, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
