#!/usr/bin/env python3
"""Build a full SQLite FTS5 search index of OpenClaw documentation."""

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime

# --- Constants ---
# No separate config.json — all settings live in openclaw.json under:
#   skills.entries.skilled-openclaw-advisor.config
OPENCLAW_JSON_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
STATE_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/state.json")
DB_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/index.db")

# ---------------------------------------------------------------------------
# DEFAULTS — change these to adjust out-of-the-box behaviour.
# ---------------------------------------------------------------------------
DEFAULTS = {
    "docsPath": None,   # Auto-detected if not set
}
# ---------------------------------------------------------------------------


def load_json(path):
    """Load a JSON file, returning empty dict if missing or invalid."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(path, data):
    """Write data to a JSON file, creating parent dirs if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_oc_config():
    """Load skill config from openclaw.json. Falls back to DEFAULTS."""
    try:
        with open(OPENCLAW_JSON_PATH, "r") as f:
            oc_json = json.load(f)
        return oc_json.get("skills", {}).get("entries", {}).get("skilled-openclaw-advisor", {}).get("config", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def detect_docs_path(config):
    """Detect the OpenClaw docs directory. Tries multiple strategies in order."""

    # a) Check openclaw.json skill config docsPath
    configured = config.get("docsPath")
    if configured and os.path.isdir(configured):
        return configured

    # b) npm root -g + /openclaw/docs
    try:
        result = subprocess.run(
            ["npm", "root", "-g"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            candidate = os.path.join(result.stdout.strip(), "openclaw", "docs")
            if os.path.isdir(candidate):
                return candidate
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # c) which openclaw → resolve symlink → walk up looking for docs/
    try:
        result = subprocess.run(
            ["which", "openclaw"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            real = os.path.realpath(result.stdout.strip())
            # Walk up from the resolved binary looking for a docs/ subdir
            current = os.path.dirname(real)
            for _ in range(10):  # limit depth to avoid infinite loops
                docs_candidate = os.path.join(current, "docs")
                if os.path.isdir(docs_candidate):
                    return docs_candidate
                parent = os.path.dirname(current)
                if parent == current:
                    break
                current = parent
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # d) Hardcoded fallback
    fallback = os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/docs")
    if os.path.isdir(fallback):
        return fallback

    # e) All strategies failed
    print("Could not detect OpenClaw docs path", file=sys.stderr)
    sys.exit(1)


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content.

    Returns (metadata_dict, body_without_frontmatter).
    Handles the subset of YAML we care about: title, summary, read_when.
    """
    meta = {}
    body = content

    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return meta, body

    # Find the closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return meta, body

    # Parse the frontmatter block (simple key: value YAML)
    fm_lines = lines[1:end_idx]
    current_key = None
    current_list = None

    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for list item under current key
        if stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue

        # Flush any pending list
        if current_list is not None and current_key:
            meta[current_key] = current_list
            current_list = None

        # Parse key: value
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                meta[key] = value
            else:
                # Could be followed by a list
                current_list = None

    # Flush final pending list
    if current_list is not None and current_key:
        meta[current_key] = current_list

    # Strip frontmatter from body
    body = "\n".join(lines[end_idx + 1:])

    return meta, body


def extract_title_from_body(body):
    """Find the first ATX heading (# Title) in the body."""
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def detect_lang(rel_path):
    """Detect language from doc path prefix. Returns 'zh-CN', 'ja-JP', etc. or 'en'."""
    parts = rel_path.replace("\\", "/").split("/")
    if len(parts) > 1:
        prefix = parts[0]
        if "-" in prefix or prefix in ("zh", "ja", "ko", "fr", "de", "es", "pt"):
            return prefix
    return "en"


def sha256_file(path):
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_openclaw_version():
    """Run openclaw --version and return the version string."""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "unknown"


def build_index(docs_path, force=False):
    """Walk docs_path and build/update the FTS5 search index."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doc_meta (
            path TEXT PRIMARY KEY,
            mtime REAL,
            size INTEGER,
            checksum TEXT
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(
            path UNINDEXED,
            lang UNINDEXED,
            title,
            summary,
            read_when,
            body,
            tokenize="porter unicode61"
        )
    """)
    conn.commit()

    indexed_count = 0

    for root, _dirs, files in os.walk(docs_path):
        for fname in files:
            if not fname.endswith(".md"):
                continue

            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, docs_path)
            stat = os.stat(full_path)
            checksum = sha256_file(full_path)

            # Incremental: skip if checksum matches (unless --force)
            if not force:
                cur.execute(
                    "SELECT checksum FROM doc_meta WHERE path = ?", (rel_path,)
                )
                row = cur.fetchone()
                if row and row[0] == checksum:
                    continue

            # Read and parse the file
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            meta, body = parse_frontmatter(content)

            title = meta.get("title", "")
            summary = meta.get("summary", "")
            read_when = meta.get("read_when", "")

            # Join list values with space
            if isinstance(read_when, list):
                read_when = " ".join(read_when)
            if isinstance(title, list):
                title = " ".join(title)
            if isinstance(summary, list):
                summary = " ".join(summary)

            # Fallback title from first heading
            if not title:
                title = extract_title_from_body(body)

            # Detect language from path prefix
            lang = detect_lang(rel_path)

            # Update FTS index (delete old entry first)
            cur.execute("DELETE FROM docs WHERE path = ?", (rel_path,))
            cur.execute(
                "INSERT INTO docs (path, lang, title, summary, read_when, body) VALUES (?, ?, ?, ?, ?, ?)",
                (rel_path, lang, title, summary, read_when, body),
            )

            # Update metadata
            cur.execute(
                "INSERT OR REPLACE INTO doc_meta (path, mtime, size, checksum) VALUES (?, ?, ?, ?)",
                (rel_path, stat.st_mtime, stat.st_size, checksum),
            )

            indexed_count += 1

    conn.commit()
    conn.close()

    return indexed_count


def main():
    parser = argparse.ArgumentParser(
        description="Build SQLite FTS5 search index for OpenClaw docs"
    )
    parser.add_argument(
        "--force", action="store_true", default=False,
        help="Force full rebuild, ignoring cached checksums"
    )
    args = parser.parse_args()

    start = time.time()

    # Load existing config and state
    config = {**DEFAULTS, **load_oc_config()}
    state = load_json(STATE_PATH)

    # Step 1: Detect docs path
    docs_path = detect_docs_path(config)
    state["docsPath"] = docs_path

    # Step 2: Build the index
    indexed = build_index(docs_path, force=args.force)

    # Step 3: Get version
    version = get_openclaw_version()
    state["indexedVersion"] = version

    # Step 4: Update timestamps and write state only (config lives in openclaw.json)
    state["lastCheck"] = datetime.utcnow().isoformat() + "Z"
    save_json(STATE_PATH, state)

    # Step 5: Summary
    elapsed = time.time() - start
    print(f"Indexed {indexed} files in {elapsed:.1f}s (version {version})")


if __name__ == "__main__":
    main()
