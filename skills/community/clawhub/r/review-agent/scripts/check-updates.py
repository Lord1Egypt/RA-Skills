#!/usr/bin/env python3
"""check-updates.py — compare the installed review-agent version against the
latest GitHub release and return a short status line.

Design: passive, cache-backed. Network only when cache is stale (>24h).

Sources of truth:
  - local version:  <skill_dir>/VERSION  (single line, e.g. "1.0.0")
  - remote version: GitHub releases API `tag_name`, stripped of leading 'v'

Cache:
  ~/.review-agent/.update-check.json   (ttl_seconds=86400)

Outputs (stdout):
  - "" (empty) when up to date, or if the check fails / is disabled
  - a single line when an update is available, e.g.:
      "update available: review-agent 1.1.0 (you have 1.0.0) — see release notes at <url>"

The empty-on-no-news contract lets callers inline it:

    UPDATE=$(bash <skill>/scripts/check-updates.sh --oneline)
    [ -n "$UPDATE" ] && echo "$UPDATE"

Flags:
  --oneline        emit a single line only (default)
  --json           emit a structured object
  --force          ignore cache TTL
  --disable        touch ~/.review-agent/.update-check.disabled and exit 0
  --enable         remove the disable marker

Exit codes:
  0 — ran successfully (regardless of whether an update was found)
  0 — disabled (soft no-op)
  0 — network failure (fail open — never block on this)
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


REPO = "jimmyag2026-prog/review-agent-skill"   # standalone skill repo (v2+)
# Fallback to the monorepo so v1 installs still find updates
FALLBACK_REPO = "jimmyag2026-prog/review-agent"
RELEASES_API = f"https://api.github.com/repos/{REPO}/releases/latest"
TAGS_API     = f"https://api.github.com/repos/{REPO}/tags"
REPO_URL     = f"https://github.com/{REPO}"
CACHE_TTL_SECONDS = 24 * 3600

SKILL_DIR = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_DIR / "VERSION"
ROOT = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
CACHE_FILE = ROOT / ".update-check.json"
DISABLE_FILE = ROOT / ".update-check.disabled"


def local_version():
    if not VERSION_FILE.exists():
        return None
    v = VERSION_FILE.read_text().strip()
    return v or None


def semver_tuple(v):
    """Turn '1.2.3' / 'v1.2.3' / '1.2.3-rc1' into (1,2,3) for comparison.
    Non-parseable → (0,0,0). Pre-release suffixes are ignored for ordering."""
    if not v:
        return (0, 0, 0)
    v = v.strip().lstrip("v")
    m = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", v)
    if not m:
        return (0, 0, 0)
    maj, minr, pat = m.group(1), m.group(2), m.group(3) or "0"
    return (int(maj), int(minr), int(pat))


def read_cache():
    if not CACHE_FILE.exists():
        return None
    try:
        d = json.loads(CACHE_FILE.read_text())
        ts = d.get("checked_at_epoch", 0)
        if (datetime.now().timestamp() - ts) < CACHE_TTL_SECONDS:
            return d
    except Exception:
        pass
    return None


def write_cache(payload):
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    except Exception:
        pass


def _get_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "review-agent-update-check",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())


def fetch_latest():
    """Returns (tag, url, notes_excerpt) or None on failure. Never raises.

    Tries the GitHub Releases API first (has release notes). Falls back to the
    Tags API — the repo may publish via tags without formal release objects.
    """
    try:
        data = _get_json(RELEASES_API)
        tag  = (data.get("tag_name") or "").strip()
        if tag:
            return (tag,
                    data.get("html_url") or f"{REPO_URL}/releases/tag/{tag}",
                    (data.get("body") or "")[:240])
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return None
        # 404 → repo has no releases; fall through to tags
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    except Exception:
        return None

    # Tags fallback — the API returns commit order; find the highest semver
    try:
        tags = _get_json(TAGS_API)
        if not isinstance(tags, list) or not tags:
            return None
        candidates = [t.get("name", "") for t in tags if t.get("name")]
        candidates.sort(key=semver_tuple, reverse=True)
        top = candidates[0]
        return (top, f"{REPO_URL}/releases/tag/{top}", "")
    except Exception:
        return None


def decide(local, remote_tag):
    if not remote_tag:
        return {"state": "unknown"}
    lt = semver_tuple(local)
    rt = semver_tuple(remote_tag)
    if rt > lt:
        return {"state": "update_available"}
    return {"state": "up_to_date"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oneline", action="store_true", default=True)
    ap.add_argument("--json", dest="as_json", action="store_true")
    ap.add_argument("--force", action="store_true", help="ignore cache TTL")
    ap.add_argument("--disable", action="store_true",
                    help="skip all future checks until --enable")
    ap.add_argument("--enable", action="store_true",
                    help="re-enable update checks")
    args = ap.parse_args()

    ROOT.mkdir(parents=True, exist_ok=True)

    if args.disable:
        DISABLE_FILE.touch()
        print("update checks disabled")
        return
    if args.enable:
        DISABLE_FILE.unlink(missing_ok=True)
        print("update checks re-enabled")
        return

    # Short-circuit on disable
    if DISABLE_FILE.exists():
        if args.as_json:
            print(json.dumps({"state": "disabled"}))
        return

    local = local_version()
    if not local:
        # No VERSION file — silently no-op
        if args.as_json:
            print(json.dumps({"state": "no_local_version"}))
        return

    # Try cache first
    cached = None if args.force else read_cache()
    if cached and "remote_tag" in cached:
        remote_tag = cached["remote_tag"]
        remote_url = cached.get("remote_url", "")
        remote_notes = cached.get("remote_notes", "")
        from_cache = True
    else:
        fetched = fetch_latest()
        if not fetched:
            # Network failure — fail open
            if args.as_json:
                print(json.dumps({"state": "fetch_failed", "local": local}))
            return
        remote_tag, remote_url, remote_notes = fetched
        write_cache({
            "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "checked_at_epoch": datetime.now().timestamp(),
            "local": local,
            "remote_tag": remote_tag,
            "remote_url": remote_url,
            "remote_notes": remote_notes,
        })
        from_cache = False

    decision = decide(local, remote_tag)
    state = decision["state"]

    if args.as_json:
        print(json.dumps({
            "state": state,
            "local": local,
            "remote_tag": remote_tag,
            "remote_url": remote_url,
            "from_cache": from_cache,
        }, ensure_ascii=False))
        return

    # Oneline output
    if state == "update_available":
        print(f"update available: review-agent {remote_tag} "
              f"(you have {local}) — {remote_url}")
    # up_to_date / unknown → print nothing (quiet)


if __name__ == "__main__":
    main()
