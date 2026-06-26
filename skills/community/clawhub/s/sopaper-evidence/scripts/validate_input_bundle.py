#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


SCHEMAS = {
    "source-note": ["## Title", "## Source", "Verification status:", "## Why it matters", "## Key facts", "## Limits"],
    "claims": ["- Claim:", "Claim type:", "Current status:"],
    "result-artifact": ["## Artifact", "Artifact type:", "Path:", "Metric:", "Provenance:"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a structured Sopaper Evidence input file against a lightweight schema."
    )
    parser.add_argument("schema", choices=sorted(SCHEMAS.keys()))
    parser.add_argument("file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        print(f"Missing input: {path}", file=sys.stderr)
        return 1

    if args.schema == "result-artifact" and path.suffix.lower() in {".csv", ".tsv", ".json"}:
        if validate_result_artifact_file(path):
            print("ok")
            return 0
        print("invalid")
        print("- missing: parseable structured result content")
        return 1

    text = path.read_text(encoding="utf-8")
    missing = [item for item in SCHEMAS[args.schema] if item not in text]
    if missing:
        print("invalid")
        for item in missing:
            print(f"- missing: {item}")
        return 1

    print("ok")
    return 0


def validate_result_artifact_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            rows = list(reader)
        if len(rows) < 2:
            return False
        header = [cell.strip().lower() for cell in rows[0]]
        required_signal = any(
            any(token in cell for token in ["metric", "benchmark", "baseline", "task", "score", "success", "accuracy"])
            for cell in header
        )
        return required_signal
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            keys = {str(key).lower() for key in payload.keys()}
            if "results" in keys and isinstance(payload.get("results"), list) and payload["results"]:
                return True
            return any(token in keys for token in ["metric", "benchmark", "baseline", "task", "results"])
        if isinstance(payload, list) and payload:
            first = payload[0]
            if isinstance(first, dict):
                keys = {str(key).lower() for key in first.keys()}
                return any(token in keys for token in ["metric", "benchmark", "baseline", "task", "score", "success_rate"])
        return False
    return False


if __name__ == "__main__":
    raise SystemExit(main())
