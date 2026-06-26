#!/usr/bin/env python3
"""FTS5 query interface for OpenClaw docs index. Stdlib only."""

import argparse
import glob
import json
import os
import sqlite3
import sys

# ---------------------------------------------------------------------------
# DEFAULTS — change these to adjust out-of-the-box behaviour.
# All can be overridden via skills.entries.skilled-openclaw-advisor.config in openclaw.json.
# ---------------------------------------------------------------------------
DEFAULTS = {
    "defaultLang":        "en",       # Language filter: "en" or "zh-CN"
    "defaultVerbosity":   "standard", # "concise" | "standard" | "detailed"
    "mandatoryQueryFirst": False,     # Emit strong suggestion to query before answering
    "maxResults":          5,         # Max results returned (agent mode uses min(3, maxResults))
    "agentMode":           False,     # Always use compact agent output regardless of --mode
    "fallbackToEnglish":   True,      # Fall back to English if requested lang has no results
    "includeOnlineUrl":    True,      # Include https://docs.openclaw.ai/... links in detailed output
}
# ---------------------------------------------------------------------------

OPENCLAW_JSON_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
STATE_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/state.json")
DB_PATH = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/index.db")
DIFFS_DIR = os.path.expanduser("~/.openclaw/skills-data/skilled-openclaw-advisor/diffs")

# FTS5 special characters that require quoting
FTS5_SPECIAL = set(':-*"^')


def load_config():
    """Load skill config. Priority: openclaw.json > DEFAULTS."""
    oc_cfg = {}
    try:
        with open(OPENCLAW_JSON_PATH, "r") as f:
            oc_json = json.load(f)
        oc_cfg = (
            oc_json
            .get("skills", {})
            .get("entries", {})
            .get("skilled-openclaw-advisor", {})
            .get("config", {})
        )
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return {**DEFAULTS, **oc_cfg}


def escape_query(query):
    """Wrap query in double quotes if it contains FTS5 special chars."""
    if any(ch in FTS5_SPECIAL for ch in query):
        return f'"{query}"'
    return query


def extract_bullets(body, max_bullets=3):
    """Extract up to N bullet/numbered lines from body text."""
    bullets = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")) or (
            len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ".)"
        ):
            bullets.append(stripped)
            if len(bullets) >= max_bullets:
                break
    return bullets


def find_snippet(body, query, max_len=80):
    """Find first occurrence of query term in body, return surrounding snippet."""
    lower_body = body.lower()
    lower_query = query.lower().strip('"')
    idx = lower_body.find(lower_query)
    if idx == -1:
        return body[:max_len].replace("\n", " ").strip()
    start = max(0, idx - 20)
    end = min(len(body), start + max_len)
    snippet = body[start:end].replace("\n", " ").strip()
    return snippet


# --- Formatters ---

def format_agent(rows, query, verbosity, config):
    """Agent mode: ultra-concise."""
    limit = min(3, config["maxResults"])
    lines = []
    for path, title, summary, _rw, body, _rank in rows[:limit]:
        snippet = find_snippet(body or "", query)
        line = f"[{path}] {title}: {snippet}"
        lines.append(line[:100])
        if verbosity == "standard" and summary:
            lines.append(f"  {summary[:100]}")
    return "\n".join(lines)


def format_human(rows, query, verbosity, config):
    """Human mode with verbosity levels."""
    blocks = []
    limit = config["maxResults"]
    for path, title, summary, _rw, body, _rank in rows[:limit]:
        body = body or ""
        summary = summary or ""

        if verbosity == "concise":
            text = summary if summary else body[:100].replace("\n", " ")
            blocks.append(f"## {title}\n{text}\nDoc: {path}\n")

        elif verbosity == "standard":
            bullets = extract_bullets(body)
            bullet_text = "\n".join(bullets)
            parts = [f"## {title}", summary]
            if bullet_text:
                parts.append(bullet_text)
            parts.append(f"Doc: {path}\n")
            blocks.append("\n".join(parts))

        elif verbosity == "detailed":
            url_path = path[:-3] if path.endswith(".md") else path
            parts = [f"## {title}", summary, "", body[:600], f"Doc: {path}"]
            if config["includeOnlineUrl"]:
                parts.append(f"Online: https://docs.openclaw.ai/{url_path}")
            parts.append("")
            blocks.append("\n".join(parts))

    return "\n".join(blocks)


# --- Special commands ---

def show_diff():
    """Show the latest diff file."""
    pattern = os.path.join(DIFFS_DIR, "*.json")
    files = sorted(glob.glob(pattern), reverse=True)
    if not files:
        print("No diffs found.")
        return

    with open(files[0], "r") as f:
        data = json.load(f)

    added = data.get("added", [])
    modified = data.get("modified", [])
    removed = data.get("removed", [])

    print(
        f"Version: {data.get('version_from', '?')} -> {data.get('version_to', '?')} "
        f"({data.get('timestamp', '?')})"
    )
    print(f"Added: {len(added)} | Modified: {len(modified)} | Removed: {len(removed)}")

    if added:
        print("\nAdded:")
        for item in added:
            print(f"  {item}" if isinstance(item, str) else f"  {item.get('path', item)}")

    if modified:
        print("\nModified:")
        for item in modified:
            if isinstance(item, dict):
                print(f"  {item.get('path', '?')}: {item.get('summary', '')}")
            else:
                print(f"  {item}")

    if removed:
        print("\nRemoved:")
        for item in removed:
            print(f"  {item}" if isinstance(item, str) else f"  {item.get('path', item)}")


def show_status():
    """Print state.json and indexed file count."""
    try:
        with open(STATE_PATH, "r") as f:
            state = json.load(f)
        print(json.dumps(state, indent=2))
    except FileNotFoundError:
        print("State file not found.")

    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        try:
            count = conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
            print(f"Indexed files: {count}")
        finally:
            conn.close()
    else:
        print("Index not found.")


def list_diffs():
    """List all diff JSON files in DIFFS_DIR."""
    pattern = os.path.join(DIFFS_DIR, "*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        print("No diffs found.")
        return
    for f in files:
        print(os.path.basename(f))


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Query OpenClaw docs FTS5 index")
    parser.add_argument("--query", type=str, help="Search query string")
    parser.add_argument("--mode", choices=["agent", "human"], default="human")
    parser.add_argument("--verbosity", choices=["concise", "standard", "detailed"])
    parser.add_argument("--lang", type=str, help="Language filter: en, zh-CN (default from config)")
    parser.add_argument("--diff", action="store_true", help="Show latest diff")
    parser.add_argument("--status", action="store_true", help="Show index status")
    parser.add_argument("--list-diffs", action="store_true", help="List all diffs")
    args = parser.parse_args()

    # Handle special commands first
    if args.diff:
        show_diff()
        return
    if args.status:
        show_status()
        return
    if args.list_diffs:
        list_diffs()
        return

    if not args.query:
        parser.error("--query is required unless using --diff, --status, or --list-diffs")

    # Load config (openclaw.json > DEFAULTS)
    config = load_config()

    # Resolve effective mode/verbosity/lang
    mode = "agent" if config["agentMode"] else args.mode
    verbosity = args.verbosity or config["defaultVerbosity"]
    lang = args.lang or config["defaultLang"]

    # Emit mandatory query suggestion if enabled (agent sees this as a directive)
    if config["mandatoryQueryFirst"] and mode != "agent":
        print(
            "📚 [openclaw-docs] Query this index before answering any OpenClaw question. "
            "Do not rely on training data for OpenClaw specifics.\n"
        )

    # Check index exists
    if not os.path.exists(DB_PATH):
        print("Index not found. Run build_index.py first.")
        sys.exit(1)

    # Execute FTS5 query with language filter
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        escaped = escape_query(args.query)
        fetch_limit = max(50, config["maxResults"] * 5)
        cols = [r[1] for r in conn.execute("PRAGMA table_info(docs)").fetchall()]

        if "lang" in cols:
            rows = conn.execute(
                "SELECT path, title, summary, read_when, body, rank "
                "FROM docs WHERE docs MATCH ? AND lang = ? ORDER BY rank LIMIT ?",
                (escaped, lang, fetch_limit),
            ).fetchall()
            if not rows and config["fallbackToEnglish"] and lang != "en":
                rows = conn.execute(
                    "SELECT path, title, summary, read_when, body, rank "
                    "FROM docs WHERE docs MATCH ? AND lang = 'en' ORDER BY rank LIMIT ?",
                    (escaped, fetch_limit),
                ).fetchall()
        else:
            # Old index without lang column — filter by path prefix
            all_rows = conn.execute(
                "SELECT path, title, summary, read_when, body, rank "
                "FROM docs WHERE docs MATCH ? ORDER BY rank LIMIT ?",
                (escaped, fetch_limit),
            ).fetchall()
            locale_prefixes = ("zh-CN/", "ja-JP/", "ko/", "fr/", "de/", "es/", "pt/")
            if lang == "en":
                rows = [r for r in all_rows if not any(r[0].startswith(p) for p in locale_prefixes)]
            else:
                rows = [r for r in all_rows if r[0].startswith(f"{lang}/")]
            if not rows and config["fallbackToEnglish"] and lang != "en":
                rows = [r for r in all_rows if not any(r[0].startswith(p) for p in locale_prefixes)]

    except sqlite3.OperationalError as e:
        print(f"Query error: {e}")
        print("Tip: try wrapping your query in double quotes if it contains special characters.")
        sys.exit(1)
    finally:
        conn.close()

    if not rows:
        print("No results found.")
        return

    if mode == "agent":
        print(format_agent(rows, args.query, verbosity, config))
    else:
        print(format_human(rows, args.query, verbosity, config))


if __name__ == "__main__":
    main()
