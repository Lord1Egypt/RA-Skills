#!/usr/bin/env python3
"""
merge-pr-context.py — merge per-component PR JSON blobs into pr-context-v0.

Reads newline-separated JSON blobs from stdin (one blob per line, keyed by
the "source" field). Recognises three sources:

    source="fetch-pr"       — PR metadata and diff (required)
    source="fetch-ci"       — CI / check-run status (optional)
    source="fetch-reviews"  — existing review comments (optional)

Merges them into a single pr-context-v0 envelope written to stdout.

Usage (pipe-through):
    { scripts/fetch-pr.sh "$PR"; scripts/fetch-ci.sh "$PR"; \\
      scripts/fetch-reviews.sh "$PR"; } | scripts/merge-pr-context.py

Lobster workflow stdin template:
    "$fetch_pr.stdout\\n$fetch_ci.stdout\\n$fetch_reviews.stdout"

Exit codes:
    0 — success (pr blob present; ci/reviews optional)
    1 — partial — pr blob present but optional blobs missing
    2 — error — no valid blobs, or required pr blob absent

Environment:
    MERGE_DEBUG=1 — print skipped/unrecognised lines and sources to stderr
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone


_DEBUG = bool(os.environ.get("MERGE_DEBUG"))


def _parse_stdin() -> dict[str, dict]:
    """Return {source: blob} for all recognised sources read from stdin.

    When MERGE_DEBUG=1 is set in the environment, lines that are skipped
    (empty, null, unrecognised JSON, unknown source) are printed to stderr
    with a brief explanation, which aids troubleshooting pipeline issues.
    """
    blobs: dict[str, dict] = {}
    for lineno, line in enumerate(sys.stdin, 1):
        raw = line.strip()
        if not raw or raw in ("{}", "null"):
            if _DEBUG and raw:
                print(f"[MERGE_DEBUG] line {lineno}: skipped trivial blob: {raw!r}",
                      file=sys.stderr)
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            if _DEBUG:
                preview = raw[:120] + ("..." if len(raw) > 120 else "")
                print(f"[MERGE_DEBUG] line {lineno}: JSON parse error ({exc}) — {preview!r}",
                      file=sys.stderr)
            continue
        if not isinstance(obj, dict):
            if _DEBUG:
                print(f"[MERGE_DEBUG] line {lineno}: skipped non-object value (type={type(obj).__name__})",
                      file=sys.stderr)
            continue
        src = obj.get("source", "")
        if src in ("fetch-pr", "fetch-ci", "fetch-reviews"):
            blobs[src] = obj
        else:
            if _DEBUG:
                print(f"[MERGE_DEBUG] line {lineno}: unrecognised source={src!r} — skipped",
                      file=sys.stderr)
    return blobs


def _ci_section(blob: dict | None) -> dict:
    if not blob:
        return {"overall": "none", "total": 0, "passed": 0, "failed": 0,
                "pending": 0, "runs": []}
    return {
        "overall": blob.get("overall", "none"),
        "total":   blob.get("total", 0),
        "passed":  blob.get("passed", 0),
        "failed":  blob.get("failed", 0),
        "pending": blob.get("pending", 0),
        "runs":    blob.get("runs", []),
    }


def _reviews_section(blob: dict | None) -> dict:
    if not blob:
        return {"review_count": 0, "inline_count": 0,
                "reviews": [], "inline_comments": []}
    return {
        "review_count":    blob.get("review_count", 0),
        "inline_count":    blob.get("inline_count", 0),
        "reviews":         blob.get("reviews", []),
        "inline_comments": blob.get("inline_comments", []),
    }


def main() -> int:
    blobs = _parse_stdin()

    pr = blobs.get("fetch-pr")
    if not pr:
        print("merge-pr-context.py: no fetch-pr blob received — cannot build context",
              file=sys.stderr)
        return 2

    envelope = {
        "schema":        "pr-context-v0",
        "generated_at":  datetime.now(timezone.utc).isoformat(),
        "pr_number":     pr.get("pr_number"),
        "repo":          pr.get("repo", ""),
        "url":           pr.get("url", ""),
        "title":         pr.get("title", ""),
        "body":          pr.get("body", ""),
        "head_ref":      pr.get("head_ref", ""),
        "base_ref":      pr.get("base_ref", ""),
        "head_sha":      pr.get("head_sha", ""),
        "state":         pr.get("state", ""),
        "files_changed": pr.get("files_changed", 0),
        "additions":     pr.get("additions", 0),
        "deletions":     pr.get("deletions", 0),
        "diff":          pr.get("diff", ""),
        "blobs_present": sorted(blobs.keys()),
        "ci":            _ci_section(blobs.get("fetch-ci")),
        "reviews":       _reviews_section(blobs.get("fetch-reviews")),
    }

    print(json.dumps(envelope))

    # Exit 1 (partial) when optional blobs are absent — still usable
    missing = [s for s in ("fetch-ci", "fetch-reviews") if s not in blobs]
    if missing:
        print(f"merge-pr-context.py: optional blobs absent: {missing}",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
