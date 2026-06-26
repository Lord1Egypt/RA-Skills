#!/usr/bin/env python3
"""
Session Distiller — Batch-process completed OpenClaw session transcripts
into structured daily memory files.

Phase 1: Process closed sessions (.reset/.deleted/.bak suffixes)
Phase 2: Live distill-in-place with offset tracking for approved group chats
Phase 3: Granola meeting note distillation from memory/granola/ into daily memory files
Phase 4: Captain's Log AM/PM ingestion from memory/captains-log-YYYY-MM-DD-{am,pm}.md

Usage:
    python3 distill.py [--dry-run] [--no-trash] [--file <path>] [--min-age-hours 24]
    python3 distill.py --live [--dry-run]                  # Cron mode: process approved live sessions
    python3 distill.py --live-session <session-id> [--dry-run]  # On-demand: distill a specific live session
    python3 distill.py --meeting-notes [--dry-run] [--limit N] [--trash]  # Distill meeting notes (preferred)
    python3 distill.py --granola [--dry-run] [--limit N] [--trash]  # Distill Granola meeting notes (deprecated)
    python3 distill.py --daily-log [--dry-run] [--limit N]  # Ingest daily log AM/PM files (preferred)
    python3 distill.py --captains-log [--dry-run] [--limit N]  # Ingest Captain's Log AM/PM files (deprecated)
"""

__version__ = "0.5.1"

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Configurable paths (override via env vars or edit defaults below) ──
MEETING_NOTES_DIR = os.environ.get('MEETING_NOTES_DIR', 'memory/granola')
DAILY_LOG_DIR     = os.environ.get('DAILY_LOG_DIR',     'memory')
DAILY_LOG_PATTERN = os.environ.get('DAILY_LOG_PATTERN', 'captains-log-{date}-{watch}.md')
MEMORY_DIR        = os.environ.get('MEMORY_DIR',        'memory')

# --- Configuration ---
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
_BASE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = Path(MEMORY_DIR) if os.path.isabs(MEMORY_DIR) else _BASE / MEMORY_DIR
GRANOLA_DIR = Path(MEETING_NOTES_DIR) if os.path.isabs(MEETING_NOTES_DIR) else _BASE / MEETING_NOTES_DIR
CAPTAINS_LOG_INGESTED_FILE = Path(__file__).parent.parent / "captains-log-ingested.json"
CAPTAINS_LOG_INGESTED_DIR = MEMORY_DIR / "captains-log" / "ingested"
GRANOLA_INGESTED_DIR = GRANOLA_DIR / "ingested"
GRANOLA_INGESTED_FILE = Path(__file__).parent.parent / "granola-ingested.json"
GRANOLA_PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "distill-granola.txt"
PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "distill.txt"
OFFSETS_FILE = Path(__file__).parent.parent / "offsets.json"
SUFFIXES = (".reset", ".deleted", ".bak")

# --- Live Distill Allowlist ---
# Only explicitly approved sessions get live distill-in-place treatment.
# Format: session_key (from sessions.json) -> human label (for logging)
# Session keys are stable across rotations; UUIDs are looked up at runtime.
LIVE_ALLOWLIST_KEYS = {
    "agent:main:telegram:group:-5166698025": "Claw & Order (Jim + Sylvie)",
}

SESSIONS_INDEX = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"


def resolve_live_allowlist() -> dict:
    """Resolve session keys to current UUIDs via sessions.json.

    Returns: {session_uuid: human_label}
    Falls back to empty dict if sessions.json is missing or unreadable.
    """
    if not SESSIONS_INDEX.exists():
        print(f"⚠️  sessions.json not found — live distill unavailable")
        return {}
    try:
        with open(SESSIONS_INDEX, "r", encoding="utf-8") as f:
            index = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Could not read sessions.json: {e}")
        return {}

    resolved = {}
    for session_key, label in LIVE_ALLOWLIST_KEYS.items():
        entry = index.get(session_key)
        if not entry:
            print(f"⚠️  Session key not found in sessions.json: {session_key}")
            continue
        uuid = entry.get("sessionId")
        if not uuid:
            print(f"⚠️  No sessionId for key: {session_key}")
            continue
        resolved[uuid] = label
        print(f"   Resolved {session_key} → {uuid[:8]}... ({label})")
    return resolved

# Noise patterns to filter out of transcripts before distillation
NOISE_PATTERNS = [
    r"^HEARTBEAT_OK$",
    r"^NO_REPLY$",
    r"^NO_FLUSH$",
    r"Read HEARTBEAT\.md if it exists",
    r"A cron job .* just completed successfully",
    r"No new emails\. Nothing to report",
    r"Nothing new in the inbox",
    r"\[System Message\].*George Email Check",
    r"^HEARTBEAT_OK",
    r"Ships Bells",
    r"Run silently:",
    r"Stats: runtime \d+s",
    r"A completed cron job is ready for user delivery",
    r"Reply ONLY: NO_REPLY",
]
NOISE_RE = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


def is_noise(text: str) -> bool:
    """Check if a message is routine noise that should be filtered."""
    if not text or not text.strip():
        return True
    stripped = text.strip()
    if len(stripped) < 5:
        return True
    for pattern in NOISE_RE:
        if pattern.search(stripped):
            return True
    return False


def find_eligible_sessions(min_age_hours: int = 24, specific_file: str = None) -> list:
    """Find session files eligible for distillation."""
    if specific_file:
        p = Path(specific_file)
        if p.exists():
            return [p]
        print(f"ERROR: File not found: {specific_file}")
        return []

    if not SESSIONS_DIR.exists():
        print(f"ERROR: Sessions directory not found: {SESSIONS_DIR}")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=min_age_hours)
    eligible = []

    for f in SESSIONS_DIR.iterdir():
        if not f.is_file():
            continue
        # Check if file has one of our target suffixes
        name = f.name
        has_suffix = False
        for suffix in SUFFIXES:
            if suffix in name:
                has_suffix = True
                break
        if not has_suffix:
            continue

        # Check age by file modification time
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime > cutoff:
            continue

        eligible.append(f)

    # Sort by modification time (oldest first)
    eligible.sort(key=lambda f: f.stat().st_mtime)
    return eligible


def extract_session_uuid(filepath: Path) -> str:
    """Extract the session UUID from the filename."""
    # Format: {uuid}.jsonl.{suffix}.{timestamp}
    name = filepath.name
    uuid_match = re.match(r"^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", name)
    if uuid_match:
        return uuid_match.group(1)
    return name.split(".")[0]


def extract_session_date(filepath: Path) -> str:
    """Extract the date (YYYY-MM-DD) from the session file timestamp or mtime."""
    name = filepath.name
    # Try to extract date from the suffix timestamp (e.g., .reset.2026-02-19T16-25-42.461Z)
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})T", name)
    if date_match:
        return date_match.group(1)
    # Fall back to file modification time
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    return mtime.strftime("%Y-%m-%d")


def parse_session(filepath: Path) -> list:
    """Parse a session JSONL file and extract meaningful messages."""
    messages = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # OpenClaw JSONL format: {"type":"message","message":{"role":"...","content":...}}
            if entry.get("type") != "message":
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = ""

            # Handle different content formats
            raw_content = msg.get("content", "")
            if isinstance(raw_content, str):
                content = raw_content
            elif isinstance(raw_content, list):
                # Content can be a list of parts (text, images, etc.)
                text_parts = []
                for part in raw_content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                    elif isinstance(part, str):
                        text_parts.append(part)
                content = "\n".join(text_parts)

            # Skip empty and noise
            if is_noise(content):
                continue

            # Only keep user and assistant messages (skip system, tool results)
            if role in ("user", "assistant"):
                # Truncate very long messages (tool dumps, etc.)
                if len(content) > 2000:
                    content = content[:2000] + "\n[...truncated...]"
                messages.append({"role": role, "content": content})

    return messages


def format_transcript(messages: list) -> str:
    """Format parsed messages into a readable transcript for distillation."""
    lines = []
    for msg in messages:
        prefix = "PHIL:" if msg["role"] == "user" else "GEORGE:"
        lines.append(f"{prefix} {msg['content']}")
    return "\n\n".join(lines)


def get_existing_daily_log(date_str: str) -> str:
    """Read the existing daily memory file if it exists."""
    daily_file = MEMORY_DIR / f"{date_str}.md"
    if daily_file.exists():
        return daily_file.read_text(encoding="utf-8")
    return ""


def already_distilled(date_str: str, session_uuid: str) -> bool:
    """Check if this session has already been distilled into the daily file."""
    existing = get_existing_daily_log(date_str)
    return session_uuid[:8] in existing


def distill_transcript(transcript: str, existing_log: str, session_uuid: str, date_str: str) -> str:
    """Call the LLM to distill the transcript. Returns markdown or NO_DISTILL."""
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

    full_prompt = f"""{prompt_template}

--- EXISTING DAILY LOG (do not duplicate) ---
{existing_log if existing_log else "(empty — no existing log for this date)"}

--- SESSION TRANSCRIPT ---
{transcript}
"""

    # Call via OpenClaw's litellm proxy (localhost:4000)
    payload = {
        "model": "claude-opus-4-6",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.1,
    }

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                "http://localhost:4000/v1/chat/completions",
                "-H", "Content-Type: application/json",
                "-H", "Authorization: Bearer sk-1234",
                "-d", json.dumps(payload),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        response = json.loads(result.stdout)
        content = response["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        print(f"  ERROR: Distillation failed: {e}")
        return None


def append_to_daily_log(date_str: str, session_uuid: str, distilled: str, source_file: str):
    """Append distilled content to the daily memory file."""
    daily_file = MEMORY_DIR / f"{date_str}.md"

    section = f"""
## Session Distillation — {session_uuid[:8]}
- **Distilled:** {datetime.now().strftime("%Y-%m-%d %H:%M CST")}
- **Source:** session {session_uuid[:8]} ({Path(source_file).name})

{distilled}
"""

    if daily_file.exists():
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write("\n" + section)
    else:
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(f"# Captain's Log — {date_str}\n{section}")

    print(f"  ✅ Appended to {daily_file.name}")


def trash_file(filepath: Path):
    """Move file to macOS Trash."""
    try:
        subprocess.run(["trash", str(filepath)], check=True, capture_output=True)
        print(f"  🗑  Trashed: {filepath.name}")
    except FileNotFoundError:
        print(f"  ⚠️  'trash' command not found. Install: brew install trash")
        print(f"      File NOT deleted: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  Trash failed: {e}")
        print(f"      File NOT deleted: {filepath}")


def process_session(filepath: Path, dry_run: bool = False, no_trash: bool = False):
    """Process a single session file."""
    session_uuid = extract_session_uuid(filepath)
    date_str = extract_session_date(filepath)
    file_size = filepath.stat().st_size

    print(f"\n📄 {filepath.name}")
    print(f"   UUID: {session_uuid[:8]}  Date: {date_str}  Size: {file_size:,} bytes")

    # Check if already distilled
    if already_distilled(date_str, session_uuid):
        if not dry_run and not no_trash:
            print(f"   ♻️  Already distilled — trashing source")
            trash_file(filepath)
            return "trash-prior"
        else:
            print(f"   ⏭  Already distilled — skipping")
            return "skipped"

    # Parse
    messages = parse_session(filepath)
    if not messages or len(messages) < 3:
        print(f"   ⏭  No meaningful content ({len(messages) if messages else 0} msgs) — skipping")
        return "empty"

    print(f"   📝 {len(messages)} meaningful messages extracted")

    # Format transcript
    transcript = format_transcript(messages)

    if dry_run:
        print(f"   🔍 DRY RUN — would distill {len(transcript):,} chars")
        print(f"   🔍 DRY RUN — would append to {DAILY_LOG_DIR}/{date_str}.md")
        # Show a preview of what we'd send
        preview = transcript[:500] + ("..." if len(transcript) > 500 else "")
        print(f"   --- TRANSCRIPT PREVIEW ---")
        for line in preview.split("\n")[:10]:
            print(f"   | {line[:100]}")
        return "dry-run"

    # Get existing log for dedup context
    existing_log = get_existing_daily_log(date_str)

    # Distill
    print(f"   🧠 Distilling {len(transcript):,} chars...")
    distilled = distill_transcript(transcript, existing_log, session_uuid, date_str)

    if distilled is None:
        return "error"

    if distilled.strip() == "NO_DISTILL":
        print(f"   ⏭  Nothing worth remembering — skipping")
        return "no-distill"

    # Append
    append_to_daily_log(date_str, session_uuid, distilled, str(filepath))

    # Trash
    if not no_trash:
        trash_file(filepath)
    else:
        print(f"   📌 --no-trash: source file kept")

    return "distilled"


# --- Phase 2: Live Distill-in-Place ---

def load_offsets() -> dict:
    """Load the offset tracking file."""
    if OFFSETS_FILE.exists():
        with open(OFFSETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_offsets(offsets: dict):
    """Save the offset tracking file."""
    with open(OFFSETS_FILE, "w", encoding="utf-8") as f:
        json.dump(offsets, f, indent=2)


def get_session_file(session_id: str) -> Path:
    """Find the live session file for a given session ID."""
    candidate = SESSIONS_DIR / f"{session_id}.jsonl"
    if candidate.exists():
        return candidate
    return None


def parse_session_from_offset(filepath: Path, offset: int) -> tuple:
    """Parse a session JSONL file from a given line offset. Returns (messages, new_offset)."""
    messages = []
    current_line = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            current_line = line_num
            if line_num <= offset:
                continue
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get("type") != "message":
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = ""

            raw_content = msg.get("content", "")
            if isinstance(raw_content, str):
                content = raw_content
            elif isinstance(raw_content, list):
                text_parts = []
                for part in raw_content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                    elif isinstance(part, str):
                        text_parts.append(part)
                content = "\n".join(text_parts)

            if is_noise(content):
                continue

            if role in ("user", "assistant"):
                if len(content) > 2000:
                    content = content[:2000] + "\n[...truncated...]"
                messages.append({"role": role, "content": content})

    return messages, current_line


def process_live_session(session_id: str, label: str, dry_run: bool = False) -> str:
    """Process a live session using offset tracking. Returns result status."""
    filepath = get_session_file(session_id)
    if filepath is None:
        print(f"\n❌ Session file not found for {session_id} ({label})")
        return "error"

    file_size = filepath.stat().st_size
    offsets = load_offsets()
    last_offset = offsets.get(session_id, 0)

    print(f"\n🧴 {label}")
    print(f"   File: {filepath.name}  Size: {file_size:,} bytes")
    print(f"   Last offset: line {last_offset}")

    # Safety check: if file is smaller than expected (rotation/reset), start from 0
    total_lines = sum(1 for _ in open(filepath, "r", encoding="utf-8"))
    if last_offset > total_lines:
        print(f"   ⚠️  File appears rotated (offset {last_offset} > {total_lines} lines). Resetting to 0.")
        last_offset = 0

    # Parse from offset
    messages, new_offset = parse_session_from_offset(filepath, last_offset)

    if new_offset == last_offset:
        print(f"   ⏭  No new lines since last run")
        return "no-new"

    if not messages or len(messages) < 3:
        print(f"   ⏭  Not enough new content ({len(messages) if messages else 0} msgs, {new_offset - last_offset} new lines)")
        # Still update offset so we don't re-scan empty lines
        if not dry_run:
            offsets[session_id] = new_offset
            save_offsets(offsets)
        return "empty"

    print(f"   📝 {len(messages)} meaningful messages from lines {last_offset + 1}-{new_offset}")

    transcript = format_transcript(messages)
    date_str = datetime.now().strftime("%Y-%m-%d")

    if dry_run:
        print(f"   🔍 DRY RUN — would distill {len(transcript):,} chars")
        print(f"   🔍 DRY RUN — would append to {DAILY_LOG_DIR}/{date_str}.md")
        print(f"   🔍 DRY RUN — would update offset to line {new_offset}")
        preview = transcript[:500] + ("..." if len(transcript) > 500 else "")
        print(f"   --- TRANSCRIPT PREVIEW ---")
        for line in preview.split("\n")[:10]:
            print(f"   | {line[:100]}")
        return "dry-run"

    # Get existing log for dedup context
    existing_log = get_existing_daily_log(date_str)

    # Distill
    print(f"   🧠 Distilling {len(transcript):,} chars...")
    distilled = distill_transcript(transcript, existing_log, session_id, date_str)

    if distilled is None:
        return "error"

    if distilled.strip() == "NO_DISTILL":
        print(f"   ⏭  Nothing worth remembering — updating offset only")
        offsets[session_id] = new_offset
        save_offsets(offsets)
        return "no-distill"

    # Append to daily log (marked as live distill)
    daily_file = MEMORY_DIR / f"{date_str}.md"
    section = f"""
## Session Distillation — {session_id[:8]} (live)
- **Distilled:** {datetime.now().strftime("%Y-%m-%d %H:%M CST")}
- **Source:** {label} (lines {last_offset + 1}-{new_offset})

{distilled}
"""

    if daily_file.exists():
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write("\n" + section)
    else:
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(f"# Captain's Log — {date_str}\n{section}")

    print(f"   ✅ Appended to {daily_file.name}")

    # Update offset
    offsets[session_id] = new_offset
    save_offsets(offsets)
    print(f"   📌 Offset updated: {last_offset} → {new_offset}")

    return "distilled"


def run_live_distill(session_id: str = None, dry_run: bool = False):
    """Run live distillation — either a specific session or all approved sessions."""
    print("=" * 60)
    print("SESSION DISTILLER — LIVE MODE 🧴")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    # Resolve session keys → current UUIDs
    allowlist = resolve_live_allowlist()

    targets = {}
    if session_id:
        # On-demand: specific session — may be a session key OR a UUID
        # If it looks like a session key (contains ':'), try to resolve it via allowlist first
        resolved_id = session_id
        resolved_label = "On-demand (not in allowlist)"

        if ":" in session_id:
            # It's a session key — look it up in sessions.json directly
            if SESSIONS_INDEX.exists():
                try:
                    with open(SESSIONS_INDEX, "r", encoding="utf-8") as f:
                        index = json.load(f)
                    entry = index.get(session_id)
                    if entry and entry.get("sessionId"):
                        resolved_id = entry["sessionId"]
                        resolved_label = entry.get("subject") or entry.get("displayName") or session_id
                        print(f"\n   Resolved session key {session_id} → {resolved_id[:8]}... ({resolved_label})")
                    else:
                        print(f"\n⚠️  Session key not found in sessions.json: {session_id}")
                except (json.JSONDecodeError, OSError) as e:
                    print(f"\n⚠️  Could not read sessions.json: {e}")

        if resolved_id in allowlist:
            targets[resolved_id] = allowlist[resolved_id]
        else:
            # Allow on-demand for any session, but warn
            targets[resolved_id] = resolved_label
            if ":" not in session_id:  # Only warn if it wasn't a key we resolved
                print(f"\n⚠️  Session {resolved_id} is not in the approved allowlist.")
                print(f"    Processing on-demand as requested, but it won't be included in scheduled runs.")
    else:
        # Scheduled: all approved sessions
        targets = dict(allowlist)

    if not targets:
        print("\nNo live sessions to process.")
        return

    print(f"\nTargets: {len(targets)} session(s)")

    results = {}
    for sid, label in targets.items():
        result = process_live_session(sid, label, dry_run=dry_run)
        results[result] = results.get(result, 0) + 1

    # Summary
    print("\n" + "=" * 60)
    print("LIVE DISTILL SUMMARY")
    for k, v in results.items():
        if v > 0:
            print(f"  {k}: {v}")
    print("=" * 60)


# --- Phase 3: Granola Distillation ---

def load_granola_ingested() -> set:
    """Load the set of already-ingested Granola UUIDs."""
    if GRANOLA_INGESTED_FILE.exists():
        try:
            with open(GRANOLA_INGESTED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("ingested", []))
        except (json.JSONDecodeError, OSError):
            return set()
    return set()


def save_granola_ingested(ingested: set):
    """Persist the ingested UUID set."""
    with open(GRANOLA_INGESTED_FILE, "w", encoding="utf-8") as f:
        json.dump({"ingested": sorted(ingested)}, f, indent=2)


def parse_granola_filename(filepath: Path) -> tuple:
    """Parse date and UUID8 from a Granola filename.

    Expected pattern: YYYY-MM-DD_title_uuid8.md
    Returns: (date_str, uuid8) or (None, None) if unparseable.
    """
    name = filepath.stem  # strip .md
    # Match date at start
    date_match = re.match(r"^(\d{4}-\d{2}-\d{2})_", name)
    if not date_match:
        return None, None
    date_str = date_match.group(1)
    # UUID8 is the last underscore-separated token
    parts = name.split("_")
    uuid8 = parts[-1] if parts else None
    if not uuid8 or len(uuid8) < 6:
        return date_str, None
    return date_str, uuid8


def distill_granola_note(content: str, existing_log: str, title: str, date_str: str) -> str:
    """Call the LLM to distill a Granola meeting note. Returns markdown or NO_DISTILL."""
    if GRANOLA_PROMPT_FILE.exists():
        prompt_template = GRANOLA_PROMPT_FILE.read_text(encoding="utf-8")
    else:
        # Fallback inline prompt if file missing
        prompt_template = """You are a memory distillation engine. Your job is to extract durable knowledge from a Granola meeting note.

INPUT: A structured meeting summary from Granola (already summarized — not a raw transcript).

OUTPUT: A concise markdown section containing only information worth remembering for future sessions.

EXTRACT:
- Decisions made and their rationale
- Action items (owner + task)
- Key technical facts, architecture choices, config values
- People mentioned and their roles
- Project/ticket references
- Blockers or risks identified
- Anything that changes prior understanding

SKIP:
- Meeting logistics (room, time, attendance pleasantries)
- Information already covered in the EXISTING DAILY LOG — do not duplicate
- Raw URLs unless they are the primary reference

FORMAT:
- Use bullet points, not paragraphs
- Group related items under bold topic headers
- Keep each bullet to 1-2 lines max
- If the note contained nothing worth remembering, output exactly: NO_DISTILL

TONE: Factual, terse, third-person. This is a log, not a narrative."""

    full_prompt = f"""{prompt_template}

--- EXISTING DAILY LOG (do not duplicate) ---
{existing_log if existing_log else "(empty — no existing log for this date)"}

--- GRANOLA MEETING NOTE: {title} ---
{content}
"""

    payload = {
        "model": "claude-opus-4-6",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.1,
    }

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                "http://localhost:4000/v1/chat/completions",
                "-H", "Content-Type: application/json",
                "-H", "Authorization: Bearer sk-1234",
                "-d", json.dumps(payload),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        response = json.loads(result.stdout)
        content_out = response["choices"][0]["message"]["content"]
        return content_out.strip()
    except Exception as e:
        print(f"  ERROR: Granola distillation failed: {e}")
        return None


def append_granola_to_daily_log(date_str: str, uuid8: str, title: str, distilled: str, source_file: str):
    """Append distilled Granola content to the daily memory file."""
    daily_file = MEMORY_DIR / f"{date_str}.md"

    section = f"""
## Granola — {title} ({uuid8})
- **Distilled:** {datetime.now().strftime("%Y-%m-%d %H:%M CST")}
- **Source:** {Path(source_file).name}

{distilled}
"""

    if daily_file.exists():
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write("\n" + section)
    else:
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(f"# Captain's Log — {date_str}\n{section}")

    print(f"  ✅ Appended to {daily_file.name}")


def process_granola_file(filepath: Path, ingested: set, dry_run: bool = False, use_trash: bool = False) -> str:
    """Process a single Granola meeting note file. Returns result status."""
    date_str, uuid8 = parse_granola_filename(filepath)

    if not date_str or not uuid8:
        print(f"\n⏭  {filepath.name} — unparseable filename, skipping")
        return "skipped"

    # Derive a clean title from filename (strip date prefix and uuid8 suffix)
    stem = filepath.stem
    title_raw = stem[len(date_str) + 1:]  # strip YYYY-MM-DD_
    title = "_".join(title_raw.split("_")[:-1]).replace("_", " ").title()  # strip uuid8, humanise

    print(f"\n📋 {filepath.name}")
    print(f"   Date: {date_str}  UUID8: {uuid8}  Title: {title}")

    # Check sidecar ingested set
    if uuid8 in ingested:
        print(f"   ⏭  Already ingested — skipping")
        return "skipped"

    # Check daily file for dedup
    if already_distilled(date_str, uuid8):
        print(f"   ⏭  Already in daily log — marking ingested")
        ingested.add(uuid8)
        return "skipped"

    # Read content
    try:
        content = filepath.read_text(encoding="utf-8").strip()
    except OSError as e:
        print(f"  ERROR: Could not read file: {e}")
        return "error"

    if not content or len(content) < 50:
        print(f"   ⏭  Empty or too short — skipping")
        return "empty"

    if dry_run:
        print(f"   🔍 DRY RUN — would distill {len(content):,} chars")
        print(f"   🔍 DRY RUN — would append to {DAILY_LOG_DIR}/{date_str}.md")
        return "dry-run"

    # Get existing log for dedup context
    existing_log = get_existing_daily_log(date_str)

    # Distill
    print(f"   🧠 Distilling {len(content):,} chars...")
    distilled = distill_granola_note(content, existing_log, title, date_str)

    if distilled is None:
        return "error"

    if distilled.strip() == "NO_DISTILL":
        print(f"   ⏭  Nothing worth remembering — marking ingested")
        ingested.add(uuid8)
        return "no-distill"

    # Append to daily log
    append_granola_to_daily_log(date_str, uuid8, title, distilled, str(filepath))

    # Mark ingested
    ingested.add(uuid8)

    # Move to ingested/ or trash
    GRANOLA_INGESTED_DIR.mkdir(parents=True, exist_ok=True)
    if use_trash:
        trash_file(filepath)
    else:
        dest = GRANOLA_INGESTED_DIR / filepath.name
        filepath.rename(dest)
        print(f"  📦 Moved to ingested/")

    return "distilled"


def run_granola_distill(dry_run: bool = False, limit: int = None, use_trash: bool = False):
    """Run Granola distillation mode — process all un-ingested meeting notes."""
    print("=" * 60)
    print("SESSION DISTILLER — GRANOLA MODE 📋")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    if limit:
        print(f"Limit: {limit} files")
    print("=" * 60)

    if not GRANOLA_DIR.exists():
        print(f"\nERROR: Granola directory not found: {GRANOLA_DIR}")
        return

    # Load ingested state
    ingested = load_granola_ingested()
    print(f"\nPreviously ingested: {len(ingested)} notes")

    # Find eligible files — .md only, skip _transcript.md, skip already in ingested/
    candidates = []
    for f in sorted(GRANOLA_DIR.iterdir()):
        if not f.is_file():
            continue
        if not f.name.endswith(".md"):
            continue
        if f.name.endswith("_transcript.md"):
            continue
        candidates.append(f)

    print(f"Candidates found: {len(candidates)}")

    if limit:
        candidates = candidates[:limit]
        print(f"Limiting to first {limit} files")

    if not candidates:
        print("\nNo Granola files to process.")
        return

    results = {"distilled": 0, "skipped": 0, "empty": 0, "no-distill": 0, "error": 0, "dry-run": 0}

    for filepath in candidates:
        result = process_granola_file(filepath, ingested, dry_run=dry_run, use_trash=use_trash)
        results[result] = results.get(result, 0) + 1

    # Persist ingested state (even on dry-run, we don't write)
    if not dry_run:
        save_granola_ingested(ingested)
        print(f"\n💾 Ingested index saved: {len(ingested)} total notes")

    print("\n" + "=" * 60)
    print("GRANOLA SUMMARY")
    for k, v in results.items():
        if v > 0:
            print(f"  {k}: {v}")
    print("=" * 60)


# --- Phase 4: Captain's Log Ingestion ---

def load_captains_log_ingested() -> set:
    """Load the set of already-ingested Captain's Log filenames."""
    if CAPTAINS_LOG_INGESTED_FILE.exists():
        try:
            with open(CAPTAINS_LOG_INGESTED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("ingested", []))
        except (json.JSONDecodeError, OSError):
            return set()
    return set()


def save_captains_log_ingested(ingested: set):
    """Persist the ingested Captain's Log filename set."""
    with open(CAPTAINS_LOG_INGESTED_FILE, "w", encoding="utf-8") as f:
        json.dump({"ingested": sorted(ingested)}, f, indent=2)


def parse_captains_log_filename(filepath: Path) -> tuple:
    """Parse date and watch (am/pm) from a Captain's Log filename.

    Expected pattern: captains-log-YYYY-MM-DD-am.md or captains-log-YYYY-MM-DD-pm.md
    Returns: (date_str, watch) or (None, None) if unparseable.
    """
    name = filepath.stem  # strip .md
    match = re.match(r"^captains-log-(\d{4}-\d{2}-\d{2})-(am|pm)$", name)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def already_captains_log_ingested(date_str: str, watch: str) -> bool:
    """Check if this Captain's Log entry is already in the daily file."""
    existing = get_existing_daily_log(date_str)
    marker = f"Captain's Log — {watch.upper()}"
    return marker in existing


def process_captains_log_file(filepath: Path, ingested: set, dry_run: bool = False, use_trash: bool = False, no_move: bool = False) -> str:
    """Process a single Captain's Log file. Returns result status."""
    date_str, watch = parse_captains_log_filename(filepath)

    if not date_str or not watch:
        print(f"\n⏭  {filepath.name} — unparseable filename, skipping")
        return "skipped"

    filename_key = filepath.name
    print(f"\n🪵 {filepath.name}")
    print(f"   Date: {date_str}  Watch: {watch.upper()}")

    # Check sidecar
    if filename_key in ingested:
        print(f"   ⏭  Already ingested — skipping")
        return "skipped"

    # Check daily file for dedup
    if already_captains_log_ingested(date_str, watch):
        print(f"   ⏭  Already in daily log — marking ingested")
        ingested.add(filename_key)
        return "skipped"

    # Read content
    try:
        content = filepath.read_text(encoding="utf-8").strip()
    except OSError as e:
        print(f"  ERROR: Could not read file: {e}")
        return "error"

    if not content or len(content) < 50:
        print(f"   ⏭  Empty or too short — skipping")
        return "empty"

    watch_label = "Morning Watch" if watch == "am" else "Dog Watch"

    if dry_run:
        print(f"   🔍 DRY RUN — would append {len(content):,} chars to {DAILY_LOG_DIR}/{date_str}.md")
        print(f"   🔍 DRY RUN — header: ## Captain's Log — {watch.upper()} ({watch_label})")
        if use_trash:
            print(f"   🔍 DRY RUN — would trash source file")
        elif no_move:
            print(f"   🔍 DRY RUN — would keep source file (--no-move)")
        else:
            print(f"   🔍 DRY RUN — would move to captains-log/ingested/")
        return "dry-run"

    # Append directly — no LLM needed, already structured
    daily_file = MEMORY_DIR / f"{date_str}.md"
    section = f"""
## Captain's Log — {watch.upper()} ({watch_label})
- **Ingested:** {datetime.now().strftime("%Y-%m-%d %H:%M CST")}
- **Source:** {filepath.name}

{content}
"""
    if daily_file.exists():
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write("\n" + section)
    else:
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(f"# Captain's Log — {date_str}\n{section}")

    print(f"  ✅ Appended to {daily_file.name}")

    # Mark ingested
    ingested.add(filename_key)

    # Move/trash/keep source file
    if use_trash:
        trash_file(filepath)
    elif no_move:
        print(f"  📌 --no-move: source file kept")
    else:
        CAPTAINS_LOG_INGESTED_DIR.mkdir(parents=True, exist_ok=True)
        dest = CAPTAINS_LOG_INGESTED_DIR / filepath.name
        filepath.rename(dest)
        print(f"  📦 Moved to captains-log/ingested/")

    return "ingested"


def run_captains_log_ingest(dry_run: bool = False, limit: int = None, use_trash: bool = False, no_move: bool = False):
    """Run Captain's Log ingestion mode — process all un-ingested AM/PM log files."""
    print("=" * 60)
    print("SESSION DISTILLER — CAPTAIN'S LOG MODE 🪵")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    if limit:
        print(f"Limit: {limit} files")
    if use_trash:
        print(f"Cleanup: trash source files")
    elif no_move:
        print(f"Cleanup: keep source files (--no-move)")
    else:
        print(f"Cleanup: move to captains-log/ingested/ (default)")
    print("=" * 60)

    # Load ingested state
    ingested = load_captains_log_ingested()
    print(f"\nPreviously ingested: {len(ingested)} files")

    # Find eligible files — captains-log-YYYY-MM-DD-am.md / pm.md, sorted chronologically
    candidates = []
    for f in sorted(MEMORY_DIR.iterdir()):
        if not f.is_file():
            continue
        if not f.name.endswith(".md"):
            continue
        date_str, watch = parse_captains_log_filename(f)
        if not date_str or not watch:
            continue
        candidates.append(f)

    # Sort: AM before PM for same date (alphabetical sort handles this naturally)
    candidates.sort(key=lambda f: f.name)

    print(f"Candidates found: {len(candidates)}")

    if limit:
        candidates = candidates[:limit]
        print(f"Limiting to first {limit} files")

    if not candidates:
        print("\nNo Captain's Log files to process.")
        return

    results = {"ingested": 0, "skipped": 0, "empty": 0, "error": 0, "dry-run": 0}

    for filepath in candidates:
        result = process_captains_log_file(filepath, ingested, dry_run=dry_run, use_trash=use_trash, no_move=no_move)
        results[result] = results.get(result, 0) + 1

    # Persist ingested state
    if not dry_run:
        save_captains_log_ingested(ingested)
        print(f"\n💾 Ingested index saved: {len(ingested)} total files")

    print("\n" + "=" * 60)
    print("CAPTAIN'S LOG SUMMARY")
    for k, v in results.items():
        if v > 0:
            print(f"  {k}: {v}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Session Distiller for OpenClaw")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing or trashing")
    parser.add_argument("--no-trash", action="store_true", help="Keep source files after processing")
    parser.add_argument("--file", type=str, help="Process a specific session file")
    parser.add_argument("--min-age-hours", type=int, default=24, help="Minimum file age in hours (default: 24)")
    parser.add_argument("--live", action="store_true", help="Process approved live sessions (Phase 2)")
    parser.add_argument("--live-session", type=str, help="On-demand: distill a specific live session by ID")
    parser.add_argument("--meeting-notes", action="store_true", help="Distill meeting notes into daily memory files (Phase 3)")
    parser.add_argument("--granola", action="store_true", help="[deprecated: use --meeting-notes] Distill Granola meeting notes (Phase 3)")
    parser.add_argument("--daily-log", action="store_true", help="Ingest daily log AM/PM files into memory (Phase 4)")
    parser.add_argument("--captains-log", action="store_true", help="[deprecated: use --daily-log] Ingest Captain's Log AM/PM files (Phase 4)")
    parser.add_argument("--limit", type=int, default=None, help="Max files to process in this run (granola/captains-log mode)")
    parser.add_argument("--trash", action="store_true", help="Trash source files instead of moving to ingested/ (granola/captains-log mode)")
    parser.add_argument("--no-move", action="store_true", help="Keep source files in place after ingestion (captains-log mode)")
    args = parser.parse_args()

    # Handle deprecated flag aliases
    if args.granola:
        print("⚠️  --granola is deprecated; use --meeting-notes instead", file=sys.stderr)
        args.meeting_notes = True
    if args.captains_log:
        print("⚠️  --captains-log is deprecated; use --daily-log instead", file=sys.stderr)
        args.daily_log = True

    # Phase 4: Daily log ingestion mode
    if args.daily_log:
        run_captains_log_ingest(dry_run=args.dry_run, limit=args.limit, use_trash=args.trash, no_move=args.no_move)
        return

    # Phase 3: Meeting notes distill mode
    if args.meeting_notes:
        run_granola_distill(dry_run=args.dry_run, limit=args.limit, use_trash=args.trash)
        return

    # Phase 2: Live distill mode
    if args.live or args.live_session:
        run_live_distill(session_id=args.live_session, dry_run=args.dry_run)
        return

    print("=" * 60)
    print("SESSION DISTILLER")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Min age: {args.min_age_hours} hours")
    print(f"Trash: {'disabled' if args.no_trash else 'enabled'}")
    print("=" * 60)

    # Find eligible sessions
    eligible = find_eligible_sessions(args.min_age_hours, args.file)

    if not eligible:
        print("\nNo eligible session files found.")
        return

    print(f"\nFound {len(eligible)} eligible session file(s):")

    # Process
    results = {"distilled": 0, "skipped": 0, "empty": 0, "no-distill": 0, "error": 0, "dry-run": 0}

    for filepath in eligible:
        result = process_session(filepath, dry_run=args.dry_run, no_trash=args.no_trash)
        results[result] = results.get(result, 0) + 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    for k, v in results.items():
        if v > 0:
            print(f"  {k}: {v}")
    print("=" * 60)


if __name__ == "__main__":
    main()
