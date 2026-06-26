#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a replay evaluation report.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    lines = [
        "# Skill Forge Replay Report",
        "",
        f"- skill: {payload.get('skill')}",
        f"- cases_run: {payload.get('cases_run')}",
        f"- score: {payload.get('score', payload.get('candidate_score'))}",
        f"- passed: {payload.get('passed')}",
        f"- details_hidden: {payload.get('details_hidden', True)}",
    ]
    if "improvement" in payload:
        lines.append(f"- improvement: {payload['improvement']}")
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {"status": "ok", "output": str(output)}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
