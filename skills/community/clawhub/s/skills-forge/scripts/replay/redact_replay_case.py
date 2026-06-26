#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from replay_common import load_jsonl, redact_text, write_json


def redact_value(value):
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Redact replay case JSON or JSONL.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    if input_path.suffix == ".jsonl":
        rows = [redact_value(row) for row in load_jsonl(input_path)]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
        count = len(rows)
    else:
        payload = redact_value(json.loads(input_path.read_text(encoding="utf-8")))
        write_json(output_path, payload)
        count = 1
    result = {"status": "ok", "cases_redacted": count, "output": str(output_path)}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
