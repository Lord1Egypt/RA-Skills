#!/usr/bin/env python3
"""Validate a parameterized source index; this does not certify semantic accuracy."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile

def rows(path):
    result = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{number}: expected object")
        result.append(value)
    return result

def validate(directory, source=None, require_complete=False):
    manifest = json.loads((directory / "snapshot-manifest.json").read_text())
    if manifest.get("parse_errors"):
        raise ValueError("manifest has parse errors")
    turns = rows(directory / "turn-index.jsonl")
    thinking = rows(directory / "thinking-coverage.jsonl")
    if len(turns) != manifest["semantic_turns"]:
        raise ValueError("semantic turn count differs")
    if [t.get("turn") for t in turns] != list(range(1, len(turns) + 1)):
        raise ValueError("noncontiguous turn IDs")
    previous_end = 0
    for turn in turns:
        if not previous_end < turn["start_line"] <= turn["end_line"] <= manifest["source_lines"]:
            raise ValueError("invalid or overlapping turn bounds")
        previous_end = turn["end_line"]
        if hashlib.sha256(turn["prompt"].encode()).hexdigest() != turn["prompt_sha256"]:
            raise ValueError("prompt hash differs")
        if "thinking" in turn:
            raise ValueError("private thinking field in turns")
    if len(thinking) != manifest["thinking_blocks"]:
        raise ValueError("thinking coverage count differs")
    for item in thinking:
        if set(item) != {"line", "bytes", "sha256"}:
            raise ValueError("thinking coverage must be metadata only")
        if not 1 <= item["line"] <= manifest["source_lines"]:
            raise ValueError("thinking source line out of bounds")
    incomplete = bool(manifest["unmatched_tool_calls"] or manifest["orphan_tool_results"])
    if require_complete and incomplete:
        raise ValueError("incomplete tool linkage")
    source_verified = False
    # Never silently open a path from an untrusted manifest.
    if source is not None:
        with source.open("rb") as handle:
            raw = handle.read(manifest["source_bytes"])
        if len(raw) != manifest["source_bytes"] or hashlib.sha256(raw).hexdigest() != manifest["source_sha256"]:
            raise ValueError("source snapshot prefix mismatch")
        # Re-index the verified prefix to check the actual evidence, not self-reported counts.
        with tempfile.TemporaryDirectory(prefix="atlas-verify-") as temporary:
            base = Path(temporary)
            snapshot = base / "source.jsonl"
            snapshot.write_bytes(raw)
            fresh = base / "index"
            completed = subprocess.run([sys.executable, str(Path(__file__).with_name("index_claude_session.py")),
                                        "--source", str(snapshot), "--out-dir", str(fresh),
                                        "--snapshot-label", manifest["snapshot_label"]], capture_output=True)
            if completed.returncode:
                raise ValueError("could not re-index verified source")
            for name in ("turn-index.jsonl", "thinking-coverage.jsonl", "source-index.md"):
                if (directory / name).read_bytes() != (fresh / name).read_bytes():
                    raise ValueError("indexed evidence differs from source: " + name)
            recomputed = json.loads((fresh / "snapshot-manifest.json").read_text())
            for key in recomputed:
                if key not in {"source", "generated_at"} and recomputed[key] != manifest.get(key):
                    raise ValueError("manifest differs from source: " + key)
        source_verified = True
    return {"status": "PASS", "source_verified": source_verified,
            "tool_linkage_complete": not incomplete, "semantic_turns": len(turns)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index-dir", required=True, type=Path)
    parser.add_argument("--source", type=Path, help="Explicit source to verify; never read manifest path automatically.")
    parser.add_argument("--require-complete-tools", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.index_dir, args.source, args.require_complete_tools), indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
