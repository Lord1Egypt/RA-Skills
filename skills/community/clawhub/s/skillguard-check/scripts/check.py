#!/usr/bin/env python3
"""
skillguard-check: discover locally-installed AI Skills and query each one
against skill-guard's public audit database. Outputs one JSON object on
stdout describing blocked / high-risk / safe / unaudited entries.

No third-party deps. No writes to disk. No data leaves the machine other
than the per-skill GET to skillguard.vip.

Usage:
  python3 check.py
  python3 check.py --api https://skillguard.vip       # default
  python3 check.py --extra-path /opt/my-skills        # add a discovery path
  python3 check.py --slug some-skill                  # check one slug only

Exit code:
  0  no blocked or high-risk skills
  1  at least one blocked or high-risk skill found
  2  unexpected error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

DEFAULT_API = "https://skillguard.vip"
DEFAULT_PATHS = [
    Path.home() / ".claude" / "skills",
    Path.home() / ".openclaw" / "skills",
    Path.home() / ".local" / "share" / "claude-skills",
    Path.home() / ".skills",
    Path.home() / "Library" / "Application Support" / "Claude" / "skills",
]
TIMEOUT_SEC = 10
USER_AGENT = "skillguard-check/1.0 (+https://skillguard.vip)"


def discover(paths: list[Path]) -> list[dict[str, str]]:
    """Return [{slug, path}] for every immediate subdir of every existing path,
    deduped by slug (first hit wins)."""
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for root in paths:
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if not entry.is_dir():
                continue
            slug = entry.name
            # ignore dot-dirs and obvious non-skill noise
            if slug.startswith(".") or slug in {"node_modules", "__pycache__"}:
                continue
            if slug in seen:
                continue
            seen.add(slug)
            out.append({"slug": slug, "path": str(entry)})
    return out


def fetch_audit(api: str, slug: str) -> dict[str, Any] | None:
    """Return the parsed audit JSON, None if the skill isn't in the database
    (HTTP 404), or a dict with `_err` for transport-level errors."""
    url = f"{api.rstrip('/')}/skills/clawhub/{slug}.json"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        return {"_err": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"_err": f"network: {e.reason}"}
    except Exception as e:  # pragma: no cover - defensive
        return {"_err": f"{type(e).__name__}: {e}"}


def classify(audit: dict[str, Any]) -> str:
    """Bucket the audit result into one of: blocked / highRisk / medium / safe."""
    if audit.get("blocked"):
        return "blocked"
    risk = (audit.get("riskLevel") or "").lower()
    if risk in ("critical", "high"):
        return "highRisk"
    if risk == "medium":
        return "medium"
    return "safe"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit installed AI Skills against skillguard.vip")
    parser.add_argument("--api", default=DEFAULT_API, help="Base URL (default: %(default)s)")
    parser.add_argument("--extra-path", action="append", default=[], help="Additional discovery path (repeatable)")
    parser.add_argument("--slug", action="append", default=[], help="Check this slug only (repeatable, skips discovery)")
    parser.add_argument("--concurrency", type=int, default=8, help="Parallel HTTP requests (default: %(default)s)")
    parser.add_argument("--pretty", action="store_true", help="Indent the JSON output")
    args = parser.parse_args(argv)

    if args.slug:
        skills = [{"slug": s, "path": "(via --slug)"} for s in args.slug]
    else:
        paths = list(DEFAULT_PATHS) + [Path(p) for p in args.extra_path]
        skills = discover(paths)

    blocked: list[dict[str, Any]] = []
    high: list[dict[str, Any]] = []
    medium: list[dict[str, Any]] = []
    safe_count = 0
    unaudited: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    if not skills:
        print(json.dumps({
            "total": 0, "audited": 0, "unauditedCount": 0,
            "blocked": [], "highRisk": [], "medium": [], "safe": 0,
            "unaudited": [], "errors": [],
            "checkedAt": _now(),
            "discoveryPaths": [str(p) for p in (DEFAULT_PATHS + [Path(p) for p in args.extra_path])],
        }, indent=2 if args.pretty else None))
        return 0

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        futures = {ex.submit(fetch_audit, args.api, s["slug"]): s for s in skills}
        for fut in as_completed(futures):
            s = futures[fut]
            audit = fut.result()
            if audit is None:
                unaudited.append({**s, "reason": "not in skill-guard database"})
                continue
            if audit.get("_err"):
                errors.append({**s, "error": audit["_err"]})
                continue
            entry = {
                **s,
                "score": audit.get("score"),
                "riskLevel": audit.get("riskLevel"),
                "findingsCount": audit.get("findingsCount"),
                "auditUrl": audit.get("canonicalUrl"),
                "lastScannedAt": audit.get("lastScannedAt"),
            }
            bucket = classify(audit)
            if bucket == "blocked":
                blocked.append(entry)
            elif bucket == "highRisk":
                high.append(entry)
            elif bucket == "medium":
                medium.append(entry)
            else:
                safe_count += 1

    # Stable sort: worst first inside each bucket.
    blocked.sort(key=lambda e: (e.get("score") or 0))
    high.sort(key=lambda e: (e.get("score") or 0))
    medium.sort(key=lambda e: (e.get("score") or 0))

    out = {
        "total": len(skills),
        "audited": len(skills) - len(unaudited) - len(errors),
        "unauditedCount": len(unaudited),
        "blocked": blocked,
        "highRisk": high,
        "medium": medium,
        "safe": safe_count,
        "unaudited": unaudited,
        "errors": errors,
        "checkedAt": _now(),
        "api": args.api,
    }
    print(json.dumps(out, indent=2 if args.pretty else None, ensure_ascii=False))
    return 1 if (blocked or high) else 0


def _now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:  # pragma: no cover - defensive
        print(json.dumps({"error": "FATAL", "message": str(e)}), file=sys.stderr)
        sys.exit(2)
