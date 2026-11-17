#!/usr/bin/env python3
"""Validate and normalize Agent-produced user overlay JSON; never prompts or networks."""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from catalog_overlay import (
    OverlayError,
    load_catalog_sections,
    load_json_strict,
    normalize_overlay,
    resolve_catalog_documents,
)

ROOT = Path(__file__).resolve().parents[1]


def _forbidden_output_roots():
    roots = [ROOT]
    if ROOT.parent.name.lower() == "release":
        roots.append(ROOT.parent)
    else:
        release_root = ROOT.parent / "release"
        if release_root.exists():
            roots.append(release_root)
    return tuple(roots)


def _source(value):
    if value == "-":
        return sys.stdin
    return value[1:] if value.startswith("@") else value


def _inside(path, parent):
    try:
        Path(path).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Validate an Agent-produced user catalog overlay", allow_abbrev=False)
    parser.add_argument("input", help="JSON path, @path, or - for stdin")
    parser.add_argument("--output", help="explicit user-owned output path; omitted writes normalized JSON to stdout")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--json", action="store_true", help="machine-readable diagnostic")
    args = parser.parse_args()
    try:
        doc = normalize_overlay(load_json_strict(_source(args.input)))
        sections = load_catalog_sections(ROOT / "data")
        resolve_catalog_documents(sections, [doc], data_dir=ROOT / "data", normalize_names=False)
        if args.output and not args.validate_only:
            if any(_inside(args.output, root) for root in _forbidden_output_roots()):
                raise OverlayError("forbidden_output", "refusing to write inside the installed skill/package", "$.output")
            output = Path(args.output).resolve()
            output.parent.mkdir(parents=False, exist_ok=True)
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, prefix=f".{output.name}.", suffix=".tmp", delete=False) as handle:
                    temp_path = Path(handle.name)
                    handle.write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp_path, output)
            except Exception:
                if temp_path is not None:
                    temp_path.unlink(missing_ok=True)
                raise
        diagnostic = {"ok": True, "currency": doc["currency"], "counts": {k: len(doc[k]) for k in ("quote_patches", "components", "aliases")}, "output": args.output if args.output and not args.validate_only else None}
        if args.json or args.validate_only or args.output:
            print(json.dumps(diagnostic, ensure_ascii=False))
        else:
            print(json.dumps(doc, ensure_ascii=False, indent=2))
        return 0
    except (OverlayError, OSError) as exc:
        error = exc.as_dict() if isinstance(exc, OverlayError) else {"code": "io_error", "path": "$", "message": "file operation failed"}
        print(json.dumps({"ok": False, "errors": [error]}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
