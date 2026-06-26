#!/usr/bin/env python3
"""
Redacta - re-identification layer.

The inverse of redaction: take text that contains Redacta tokens
([NHS_NUMBER_1], [PATIENT_NAME_1], ...) plus the token map produced during
redaction, and put the original values back. Use this to restore real data into
output that was generated from redacted text - e.g. after passing the
pseudonymised document through another AI tool.

Tokens always end in "]", so "[NAME_1]" never matches inside "[NAME_10]";
plain string replacement is safe and order-independent.

Usage:
    # token map from a file
    python3 reinstate.py redacted.txt --map token_map.json

    # token map on stdin (e.g. piped from redact_structured.py output)
    python3 redact_structured.py letter.txt | python3 reinstate.py redacted.txt --map -

    # read the text from stdin, map from a file
    python3 reinstate.py --map token_map.json < redacted.txt

The map file may be either a bare token map ({"[NHS_NUMBER_1]": "943 476 5919"})
or the full JSON object printed by redact_structured.py (which contains a
"token_map" key). Both are accepted.

Default output is JSON on stdout with two keys:
    text     - the re-identified text
    changed  - whether any token was replaced

Use --text-only to print just the restored text.

Standard library only. No network access; all processing is local.
"""

import argparse
import json
import re
import sys

_TOKEN_RE = re.compile(r"^\[[A-Z_]+_\d+\]$")


def load_token_map(raw):
    """Accept a bare token map or a full redact_structured.py object."""
    data = json.loads(raw)
    if isinstance(data, dict) and "token_map" in data and isinstance(data["token_map"], dict):
        data = data["token_map"]
    if not isinstance(data, dict) or not data:
        raise ValueError("token map is empty or not an object")
    for key, value in data.items():
        if not _TOKEN_RE.match(key) or not isinstance(value, str):
            raise ValueError("not a valid Redacta token map (bad entry: %r)" % key)
    return data


def reinstate(text, token_map):
    """Replace every token with its original value. Returns (text, changed)."""
    out = text
    for token, original in token_map.items():
        if token:
            out = out.replace(token, original)
    return out, out != text


def main():
    ap = argparse.ArgumentParser(
        description="Redacta re-identification layer: restore originals from a token map.")
    ap.add_argument("file", nargs="?",
                    help="redacted input file; reads stdin if omitted")
    ap.add_argument("--map", required=True,
                    help="token map JSON file, or '-' to read it from stdin")
    ap.add_argument("--text-only", action="store_true",
                    help="print only the re-identified text (no JSON)")
    args = ap.parse_args()

    if args.map == "-":
        if args.file is None:
            ap.error("cannot read both text and map from stdin; give a text FILE")
        map_raw = sys.stdin.read()
    else:
        with open(args.map, encoding="utf-8") as fh:
            map_raw = fh.read()

    token_map = load_token_map(map_raw)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    restored, changed = reinstate(text, token_map)

    if args.text_only:
        sys.stdout.write(restored)
        if not restored.endswith("\n"):
            sys.stdout.write("\n")
        return

    json.dump({"text": restored, "changed": changed},
              sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
