#!/usr/bin/env python3
"""Find students who haven't submitted artifacts.

Usage:
    python check.py --manifest <csv> --artifacts <dir> [--match-field code|name|both]

Manifest CSV must have columns: code, name  (case-insensitive header match).
Artifact filenames are matched against student code and/or name (case-insensitive,
substring or exact-stem match).
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path


def load_manifest(path: str) -> list[dict]:
    """Load student manifest CSV. Returns list of {code, name}."""
    students = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Normalize header keys
        for row in reader:
            lower = {k.strip().lower(): v.strip() for k, v in row.items()}
            code = lower.get("code", "")
            name = lower.get("name", "")
            if code or name:
                students.append({"code": code, "name": name})
    return students


def normalize(s: str) -> str:
    """Lowercase, strip whitespace, collapse internal spaces."""
    return re.sub(r"\s+", " ", s.strip().lower())


def build_matchers(students: list[dict], match_field: str):
    """Return list of (student, patterns) where patterns are regex compilable."""
    results = []
    for s in students:
        patterns = []
        code = normalize(s["code"])
        name = normalize(s["name"])

        if match_field in ("code", "both") and code:
            # Match code as whole token (word boundary or separator-adjacent)
            patterns.append(re.compile(re.escape(code), re.IGNORECASE))
        if match_field in ("name", "both") and name:
            # Match full name (spaces may be underscores/dashes in filenames)
            escaped = re.escape(name)
            # Allow spaces in name to match underscores, dashes, or nothing in filename
            flexible = escaped.replace(r"\ ", r"[\s_\-]?")
            patterns.append(re.compile(flexible, re.IGNORECASE))
            # Also try surname only (last token) for short filenames
            parts = name.split()
            if len(parts) > 1:
                surname = re.escape(parts[-1])
                patterns.append(re.compile(rf"(?<![a-zA-Z]){surname}(?![a-zA-Z])", re.IGNORECASE))

        results.append((s, patterns))
    return results


def load_artifact_names(file_path: str) -> list[str]:
    """Load artifact filenames from a text file (one name per line)."""
    names = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                names.append(name)
    return names


def find_artifacts(artifact_path: str) -> list[str]:
    """Return list of filenames from a directory (non-recursive) or a text file.

    If artifact_path is a text file, each non-empty line is treated as an artifact
    filename. If it is a directory, files inside are scanned as before.
    """
    p = Path(artifact_path)
    if p.is_file():
        names = load_artifact_names(str(p))
        if not names:
            print(f"No artifact names found in file: {artifact_path}", file=sys.stderr)
            sys.exit(1)
        return names
    if p.is_dir():
        return [f.name for f in p.iterdir() if f.is_file()]
    print(f"Error: artifact path not found: {artifact_path}", file=sys.stderr)
    sys.exit(1)


def check_submissions(manifest_path: str, artifact_dir: str, match_field: str = "both"):
    students = load_manifest(manifest_path)
    if not students:
        print(f"No students found in manifest: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    artifacts = find_artifacts(artifact_dir)
    if not artifacts:
        print(f"No artifact files found in: {artifact_dir}")
        print(f"All {len(students)} students appear to be missing.")
        return

    matchers = build_matchers(students, match_field)
    submitted = set()
    matched_details = {}

    for fname in artifacts:
        fn = normalize(fname)
        for student, patterns in matchers:
            sid = student["code"] or student["name"]
            if sid in submitted:
                continue
            for pat in patterns:
                if pat.search(fn):
                    submitted.add(sid)
                    matched_details[sid] = fname
                    break

    missing = []
    present = []
    for s in students:
        sid = s["code"] or s["name"]
        if sid in submitted:
            present.append((s, matched_details.get(sid, "?")))
        else:
            missing.append(s)

    # Report
    print(f"=== Submission Check ===")
    print(f"Manifest : {manifest_path}")
    print(f"Artifacts: {artifact_dir}")
    print(f"Total students : {len(students)}")
    print(f"Matched (submitted): {len(present)}")
    print(f"Missing          : {len(missing)}")
    print()

    if missing:
        print("--- MISSING STUDENTS ---")
        for i, s in enumerate(missing, 1):
            print(f"  {i:3d}. [{s['code']}] {s['name']}")
        print()

    if present:
        print("--- SUBMITTED ---")
        for s, fname in present:
            print(f"  [{s['code']}] {s['name']}  ←  {fname}")


def main():
    parser = argparse.ArgumentParser(description="Check student artifact submissions.")
    parser.add_argument("--manifest", required=True, help="Path to class CSV manifest")
    parser.add_argument("--artifacts", required=True, help="Path to artifact folder OR a text file containing artifact filenames (one per line)")
    parser.add_argument("--match-field", choices=["code", "name", "both"], default="both",
                        help="Match against code, name, or both (default: both)")
    args = parser.parse_args()
    check_submissions(args.manifest, args.artifacts, args.match_field)


if __name__ == "__main__":
    main()
