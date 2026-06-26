#!/usr/bin/env python3
"""
Incremental doc updater and diff generator. Optionally sends a notification via the OpenClaw CLI when updates are found (uses local openclaw message command, no direct network calls).
Scans OpenClaw docs for changes, updates the SQLite index,
generates version diffs, and optionally sends a local OpenClaw notification when changes are detected.

Standalone Python 3, stdlib only.
"""

import json
import os
import sys
import hashlib
import sqlite3
import subprocess
import argparse
import shutil
import difflib
import time
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# No separate config.json — all settings live in openclaw.json under:
#   skills.entries.skilled-openclaw-advisor.config
OPENCLAW_JSON_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
STATE_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/state.json")
DB_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/index.db")
DIFFS_DIR = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/diffs")
PREV_DOCS_DIR = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/versions/prev_docs")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(filepath):
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    """Load a JSON file, returning {} if missing or invalid."""
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_oc_config():
    """Load skill config from openclaw.json. Returns {} on failure."""
    try:
        with open(OPENCLAW_JSON_PATH, "r", encoding="utf-8") as f:
            oc_json = json.load(f)
        return oc_json.get("skills", {}).get("entries", {}).get("skilled-openclaw-advisor", {}).get("config", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(path, data):
    """Write data as pretty-printed JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def utcnow_iso():
    """Current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def parse_frontmatter(text):
    """Extract YAML frontmatter fields (title, summary, read_when) and body.

    Frontmatter is delimited by --- on the first line and the next ---.
    We do a minimal key: value parse (no nested YAML) to stay stdlib-only.
    """
    title = ""
    summary = ""
    read_when = ""
    body = text

    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break
        if end_idx is not None:
            fm_lines = lines[1:end_idx]
            body = "\n".join(lines[end_idx + 1:])
            for line in fm_lines:
                if ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip().lower()
                    val = val.strip().strip('"').strip("'")
                    if key == "title":
                        title = val
                    elif key == "summary":
                        summary = val
                    elif key == "read_when":
                        read_when = val

    return title, summary, read_when, body


def scan_docs(docs_path):
    """Walk docs_path and return {relative_path: sha256} for all .md files."""
    result = {}
    for root, _dirs, files in os.walk(docs_path):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, docs_path)
            result[rel] = sha256_file(full)
    return result


def diff_summary(old_path, new_path):
    """Generate a short unified-diff summary between two files.

    Returns the first 3 changed lines joined with ' | ', or a fallback.
    """
    if not os.path.isfile(old_path):
        return "New file"

    with open(old_path, "r", encoding="utf-8", errors="replace") as f:
        old_lines = f.readlines()
    with open(new_path, "r", encoding="utf-8", errors="replace") as f:
        new_lines = f.readlines()

    diff_lines = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    # Collect first 3 actual change lines (skip +++ / --- headers)
    changes = []
    for line in diff_lines:
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") or line.startswith("-"):
            changes.append(line.rstrip()[:80])
            if len(changes) >= 3:
                break

    if changes:
        return " | ".join(changes)[:200]
    return "Content updated"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Incremental OpenClaw docs updater")
    parser.add_argument("--force", action="store_true", help="Re-index all files regardless of changes")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    args = parser.parse_args()

    start_time = time.monotonic()

    # ------------------------------------------------------------------
    # Step 1: Load config + state
    # ------------------------------------------------------------------
    config = load_oc_config()
    state = load_json(STATE_PATH)

    # docsPath: prefer openclaw.json config, fall back to state.json (set by build_index.py)
    docs_path = config.get("docsPath") or state.get("docsPath", "")
    if not docs_path or not os.path.isdir(docs_path):
        print(f"Error: docsPath not set or does not exist: {docs_path!r}")
        print(f"Set docsPath in skills.entries.skilled-openclaw-advisor.config in openclaw.json,")
        print(f"or run build_index.py first to auto-detect and cache it in state.json.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 2: Get current version
    # ------------------------------------------------------------------
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=10
        )
        current_version = result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Warning: could not get openclaw version: {e}")
        current_version = "unknown"

    # ------------------------------------------------------------------
    # Step 3: Scan current docs
    # ------------------------------------------------------------------
    current_docs = scan_docs(docs_path)
    print(f"Scanned {len(current_docs)} doc(s) in {docs_path}")

    # ------------------------------------------------------------------
    # Step 4: Compare with doc_meta in DB
    # ------------------------------------------------------------------
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure tables exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS docs (
            path TEXT PRIMARY KEY,
            title TEXT,
            summary TEXT,
            read_when TEXT,
            body TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doc_meta (
            path TEXT PRIMARY KEY,
            checksum TEXT,
            mtime REAL,
            size INTEGER
        )
    """)
    conn.commit()

    # Load existing checksums from DB
    cur.execute("SELECT path, checksum FROM doc_meta")
    db_docs = {row[0]: row[1] for row in cur.fetchall()}

    current_paths = set(current_docs.keys())
    db_paths = set(db_docs.keys())

    added = current_paths - db_paths
    removed = db_paths - current_paths
    modified = {p for p in current_paths & db_paths if current_docs[p] != db_docs[p]}

    # --force: treat everything as modified
    if args.force:
        modified = current_paths - added
        print("Force mode: re-indexing all files")

    total_changes = len(added) + len(removed) + len(modified)

    # ------------------------------------------------------------------
    # Step 5: Nothing changed and version matches
    # ------------------------------------------------------------------
    indexed_version = state.get("indexedVersion", "")
    if total_changes == 0 and current_version == indexed_version:
        state["lastCheck"] = utcnow_iso()
        if not args.dry_run:
            save_json(STATE_PATH, state)
        print("No changes. Index up to date.")
        conn.close()
        sys.exit(0)

    # ------------------------------------------------------------------
    # Step 6: Changes detected OR version changed
    # ------------------------------------------------------------------
    if args.dry_run:
        print(f"\n[DRY RUN] Would update {total_changes} file(s):")
        for p in sorted(added):
            print(f"  + {p}")
        for p in sorted(modified):
            print(f"  ~ {p}")
        for p in sorted(removed):
            print(f"  - {p}")
        print(f"Version: {indexed_version or 'unknown'} -> {current_version}")
        conn.close()
        sys.exit(0)

    # 6a. Copy current docs to PREV_DOCS_DIR (for diffing against old versions)
    os.makedirs(os.path.dirname(PREV_DOCS_DIR), exist_ok=True)
    # Only copy if we have previous data to diff against; keep existing prev if present
    if not os.path.isdir(PREV_DOCS_DIR):
        # First run or cleaned up — snapshot current state (diffs will say "New file")
        shutil.copytree(docs_path, PREV_DOCS_DIR, dirs_exist_ok=True)

    # 6b. Re-index changed files
    for rel_path in sorted(added | modified):
        full_path = os.path.join(docs_path, rel_path)
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        title, summary, read_when, body = parse_frontmatter(raw)
        checksum = current_docs[rel_path]
        stat = os.stat(full_path)

        cur.execute("DELETE FROM docs WHERE path = ?", (rel_path,))
        cur.execute(
            "INSERT INTO docs (path, title, summary, read_when, body) VALUES (?, ?, ?, ?, ?)",
            (rel_path, title, summary, read_when, body),
        )
        cur.execute(
            "INSERT OR REPLACE INTO doc_meta (path, checksum, mtime, size) VALUES (?, ?, ?, ?)",
            (rel_path, checksum, stat.st_mtime, stat.st_size),
        )

    for rel_path in sorted(removed):
        cur.execute("DELETE FROM docs WHERE path = ?", (rel_path,))
        cur.execute("DELETE FROM doc_meta WHERE path = ?", (rel_path,))

    conn.commit()
    conn.close()

    # 6c. Build diff JSON
    version_from = indexed_version or "unknown"
    modified_entries = []
    for p in sorted(modified):
        old_file = os.path.join(PREV_DOCS_DIR, p)
        new_file = os.path.join(docs_path, p)
        summary = diff_summary(old_file, new_file)
        modified_entries.append({"path": p, "summary": summary})

    diff_data = {
        "version_from": version_from,
        "version_to": current_version,
        "timestamp": utcnow_iso(),
        "added": sorted(added),
        "removed": sorted(removed),
        "modified": modified_entries,
        "total_changes": total_changes,
    }

    os.makedirs(DIFFS_DIR, exist_ok=True)
    diff_file = os.path.join(DIFFS_DIR, f"v{current_version}.json")
    save_json(diff_file, diff_data)

    # 6d. Optionally notify via local OpenClaw CLI (no direct network calls)
    msg = (
        f"\U0001F4DA OpenClaw Docs Updated: v{version_from} \u2192 v{current_version}\n"
        f"\u2705 {len(added)} added | \u270F\uFE0F {len(modified)} modified | \u274C {len(removed)} removed\n"
        f"Diff saved: diffs/v{current_version}.json"
    )
    try:
        tg = subprocess.run(
            ["openclaw", "message", "send", "--channel", "telegram",
             "--target", "8494006989", "--message", msg],
            capture_output=True, text=True, timeout=30,
        )
        if tg.returncode != 0:
            print(f"Warning: Telegram notification failed (rc={tg.returncode}): {tg.stderr.strip()}")
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Warning: Could not send Telegram notification: {e}")

    # 6e. Update state.json only (config lives in openclaw.json)
    state["indexedVersion"] = current_version
    state["lastCheck"] = utcnow_iso()
    state["lastDiff"] = diff_file
    save_json(STATE_PATH, state)

    # 6f. Clean up PREV_DOCS_DIR, then snapshot current docs for next run
    shutil.rmtree(PREV_DOCS_DIR, ignore_errors=True)
    shutil.copytree(docs_path, PREV_DOCS_DIR, dirs_exist_ok=True)

    # ------------------------------------------------------------------
    # Step 7: Print summary
    # ------------------------------------------------------------------
    elapsed = time.monotonic() - start_time
    print(
        f"Updated {total_changes} files "
        f"({len(added)} added, {len(modified)} modified, {len(removed)} removed) "
        f"in {elapsed:.1f}s"
    )


if __name__ == "__main__":
    main()
