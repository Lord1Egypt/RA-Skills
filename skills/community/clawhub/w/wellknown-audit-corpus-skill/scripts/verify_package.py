#!/usr/bin/env python3
"""Verify package file checksums before install or support handoff."""
import argparse
import hashlib
import json
import pathlib
import sys

PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[1]


def sha256_path(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_checksums():
    path = PACKAGE_DIR / "checksums.json"
    if not path.exists():
        raise SystemExit(f"missing checksums.json in {PACKAGE_DIR}")
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description="Verify this package against bundled checksums.json.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    checksums = load_checksums()
    failures = []
    verified = []
    for rec in checksums.get("files", []):
        rel = rec["path"]
        path = PACKAGE_DIR / rel
        if not path.exists():
            failures.append({"path": rel, "error": "missing"})
            continue
        actual = sha256_path(path)
        if actual != rec.get("sha256"):
            failures.append({"path": rel, "error": "sha256_mismatch", "expected": rec.get("sha256"), "actual": actual})
        else:
            verified.append(rel)
    result = {"ok": not failures, "slug": checksums.get("slug"), "version": checksums.get("version"), "verified_count": len(verified), "failures": failures}
    if args.json:
        print(json.dumps(result, indent=2))
    elif failures:
        print(f"PACKAGE_VERIFY_FAIL {checksums.get('slug')} failures={len(failures)}")
        for failure in failures:
            print(f"- {failure['path']}: {failure['error']}")
    else:
        print(f"PACKAGE_VERIFY_PASS {checksums.get('slug')} files={len(verified)} version={checksums.get('version')}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
