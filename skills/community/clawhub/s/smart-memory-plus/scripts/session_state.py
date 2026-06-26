#!/usr/bin/env python3
"""
session_state.py — HOT RAM: Session-Scoped Working Memory (SESSION-STATE.md)
Replaces shell-based session_state.sh to eliminate shell injection risks.
Implements WAL (Write-Ahead Log) protocol for durability.
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
STATE_DIR = WORKSPACE / "memory" / "session-states"
# Session isolation: --session-key <key> auto-derives a short safe ID from the full session key
# Or: --channel <name> for manual channel isolation
# Or: SESSION_CHANNEL env var
# Falls back to global SESSION-STATE.md (in workspace root) if none set
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def _safe_id(raw: str) -> str:
    """Derive a filesystem-safe short ID from a session key or channel name."""
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", raw)
    if not cleaned:
        return ""
    # If it looks like a Discord/Telegram numeric channel ID, use it as-is
    if cleaned.isdigit() and len(cleaned) >= 10:
        return cleaned
    # Otherwise hash long strings to keep filenames short
    if len(cleaned) > 32:
        import hashlib
        return hashlib.sha256(cleaned.encode()).hexdigest()[:12]
    return cleaned

def _resolve_state_file(channel: str | None = None, session_key: str | None = None) -> Path:
    sid = ""
    if session_key:
        # Extract meaningful part: "agent:main:discord:channel:123456" → "123456"
        parts = session_key.split(":")
        # Use the last segment if it looks like an ID, otherwise hash the whole thing
        sid = _safe_id(parts[-1] if parts else session_key)
        if not sid or sid == "main":
            sid = _safe_id(session_key)
    elif channel:
        sid = _safe_id(channel)
    else:
        sid = _safe_id(os.environ.get("SESSION_CHANNEL", ""))
    if sid:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        return STATE_DIR / f"SESSION-STATE-{sid}.md"
    return WORKSPACE / "SESSION-STATE.md"

STATE_FILE = _resolve_state_file()

# Patterns that indicate sensitive data — refuse to write
SENSITIVE_PATTERNS = [
    re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"(?:api[_-]?key|token|secret|bearer)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"clh_[A-Za-z0-9]{30,}", re.IGNORECASE),  # ClawHub tokens
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),   # OpenAI keys
    re.compile(r"ghp_[A-Za-z0-9]{30,}", re.IGNORECASE),  # GitHub PAT
]


def sanitize(text: str) -> str:
    """Remove control characters and normalize whitespace."""
    # Strip control chars except newline/tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text.strip()


def check_sensitive(text: str) -> str | None:
    """Check if text contains sensitive data. Returns reason or None."""
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            return f"Refused: input matches sensitive pattern ({pattern.pattern[:40]}...)"
    return None


def ensure_state():
    """Create SESSION-STATE.md if it doesn't exist."""
    if not STATE_FILE.exists():
        content = f"""# SESSION-STATE.md — Active Working Memory (HOT RAM)

This file is the agent's "RAM" — survives compaction, restarts, distractions.
Write BEFORE responding (WAL protocol).

## Current Task
[None]

## Key Context
[None yet]

## Recent Decisions
[None yet]

## Pending Actions
- [ ] None

## Blockers
[None]

---
*Initialized: {TIMESTAMP}*
"""
        STATE_FILE.write_text(content, encoding="utf-8")


def read_state() -> str:
    ensure_state()
    return STATE_FILE.read_text(encoding="utf-8")


def write_state(content: str):
    STATE_FILE.write_text(content, encoding="utf-8")


def cmd_init():
    ensure_state()
    # Force re-init
    content = STATE_FILE.read_text(encoding="utf-8")
    content = re.sub(r"\*Initialized:.*?\*", f"*Initialized: {TIMESTAMP}*", content)
    content = re.sub(r"\*Updated:.*?\*", f"*Updated: {TIMESTAMP}*", content)
    # Reset sections
    content = re.sub(r"(## Current Task\n).*?(\n## )", r"\1[None]\n\n*Updated: " + TIMESTAMP + r"*\n\2", content, flags=re.DOTALL)
    write_state(content)
    print(f"Initialized: {STATE_FILE}")


def cmd_get():
    print(read_state())


def cmd_task(task: str):
    err = check_sensitive(task)
    if err:
        print(err)
        return
    task = sanitize(task)
    ensure_state()
    content = read_state()
    content = re.sub(
        r"(## Current Task\n).*?(\n## )",
        f"\\1{task}\n\n*Updated: {TIMESTAMP}*\\n\\2",
        content,
        flags=re.DOTALL,
    )
    write_state(content)
    print(f"Task set: {task}")


def cmd_context(key: str, value: str):
    err = check_sensitive(value)
    if err:
        print(err)
        return
    key = sanitize(key)
    value = sanitize(value)
    ensure_state()
    content = read_state()
    entry = f"- **{key}**: {value} *({TIMESTAMP})*"
    if "[None yet]" in content:
        content = content.replace("[None yet]", entry, 1)
    else:
        content = content.replace("## Recent Decisions", f"{entry}\n\n## Recent Decisions", 1)
    write_state(content)
    print(f"Context: {key} = {value}")


def cmd_decide(decision: str):
    err = check_sensitive(decision)
    if err:
        print(err)
        return
    decision = sanitize(decision)
    ensure_state()
    content = read_state()
    entry = f"- **{TIMESTAMP}**: {decision}"
    if "## Recent Decisions" in content:
        parts = content.split("## Recent Decisions", 1)
        after = parts[1]
        if "[None yet]" in after:
            after = after.replace("[None yet]", entry, 1)
        else:
            after = "\n" + entry + after
        content = parts[0] + "## Recent Decisions" + after
    write_state(content)
    print(f"Decided: {decision}")


def cmd_pending(action: str):
    err = check_sensitive(action)
    if err:
        print(err)
        return
    action = sanitize(action)
    ensure_state()
    content = read_state()
    if "- [ ] None" in content:
        content = content.replace("- [ ] None", f"- [ ] {action}", 1)
    else:
        content = content.replace("## Blockers", f"- [ ] {action}\n\n## Blockers", 1)
    write_state(content)
    print(f"Pending: {action}")


def cmd_done(action: str):
    action = sanitize(action)
    ensure_state()
    content = read_state()
    # Escape for regex
    escaped = re.escape(action)
    new_content = re.sub(r"- \[ \] " + escaped, f"- [x] {action} ✓", content)
    if new_content == content:
        print(f"Action not found: {action}")
    else:
        write_state(new_content)
        print(f"Done: {action}")


def cmd_blocker(blocker: str):
    err = check_sensitive(blocker)
    if err:
        print(err)
        return
    blocker = sanitize(blocker)
    ensure_state()
    content = read_state()
    entry = f"- **{TIMESTAMP}**: {blocker}"
    if "## Blockers" in content:
        parts = content.split("## Blockers", 1)
        after = parts[1]
        if "[None]" in after:
            after = after.replace("[None]", entry, 1)
        else:
            after = "\n" + entry + after
        content = parts[0] + "## Blockers" + after
    write_state(content)
    print(f"Blocker: {blocker}")


def cmd_clear():
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    cmd_init()
    print("State cleared.")


def cmd_snapshot():
    """Save current SESSION-STATE.md as a timestamped snapshot."""
    ensure_state()
    snapshot_dir = WORKSPACE / "memory" / "session-snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    snapshot_file = snapshot_dir / f"session-{ts}.md"
    content = read_state()
    snapshot_file.write_text(content, encoding="utf-8")
    # Keep only last 20 snapshots
    snapshots = sorted(snapshot_dir.glob("session-*.md"))
    while len(snapshots) > 20:
        snapshots.pop(0).unlink()
    print(f"Snapshot saved: {snapshot_file}")


def cmd_restore(latest: bool = False, file: str | None = None):
    """Restore SESSION-STATE.md from a snapshot."""
    snapshot_dir = WORKSPACE / "memory" / "session-snapshots"
    if not snapshot_dir.exists():
        print("No snapshots found.")
        return

    if file:
        snapshot_file = Path(file)
        if not snapshot_file.exists():
            snapshot_file = snapshot_dir / file
    else:
        snapshots = sorted(snapshot_dir.glob("session-*.md"))
        if not snapshots:
            print("No snapshots found.")
            return
        snapshot_file = snapshots[-1]

    if not snapshot_file.exists():
        print(f"Snapshot not found: {snapshot_file}")
        return

    # Save current state before overwriting
    if STATE_FILE.exists():
        cmd_snapshot()

    content = snapshot_file.read_text(encoding="utf-8")
    write_state(content)
    print(f"Restored from: {snapshot_file}")


def cmd_snapshots():
    """List available snapshots."""
    snapshot_dir = WORKSPACE / "memory" / "session-snapshots"
    if not snapshot_dir.exists():
        print("No snapshots found.")
        return
    snapshots = sorted(snapshot_dir.glob("session-*.md"))
    if not snapshots:
        print("No snapshots found.")
        return
    for s in snapshots:
        size = s.stat().st_size
        mtime = datetime.fromtimestamp(s.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"  {s.name}  ({size}B, {mtime} UTC)")
    print(f"Total: {len(snapshots)} snapshots")


def main():
    # Parse --channel / --session-key flags before command
    channel = None
    session_key = None
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == "--channel" and i + 1 < len(argv):
            channel = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
        elif argv[i] == "--session-key" and i + 1 < len(argv):
            session_key = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
        elif argv[i] in ("--channel", "--session-key"):
            print(f"Error: {argv[i]} requires a value")
            sys.exit(1)
        else:
            i += 1

    # Re-resolve STATE_FILE with given flags
    global STATE_FILE
    STATE_FILE = _resolve_state_file(channel=channel, session_key=session_key)

    if len(argv) < 1:
        print("Usage: session_state.py [--channel <name>] [--session-key <key>] {init|get|task|context|decide|pending|done|blocker|clear|snapshot|restore|snapshots} [args]")
        sys.exit(1)

    cmd = argv[0]
    args = argv[1:]

    commands = {
        "init": lambda: cmd_init(),
        "get": lambda: cmd_get(),
        "task": lambda: cmd_task(" ".join(args)),
        "context": lambda: cmd_context(args[0], " ".join(args[1:])) if len(args) >= 2 else print("Usage: context <key> <value>"),
        "decide": lambda: cmd_decide(" ".join(args)),
        "pending": lambda: cmd_pending(" ".join(args)),
        "done": lambda: cmd_done(" ".join(args)),
        "blocker": lambda: cmd_blocker(" ".join(args)),
        "clear": lambda: cmd_clear(),
        "snapshot": lambda: cmd_snapshot(),
        "restore": lambda: cmd_restore(file=" ".join(args) if args else None),
        "snapshots": lambda: cmd_snapshots(),
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print(f"Unknown command: {cmd}")
        print("Available: init, get, task, context, decide, pending, done, blocker, clear, snapshot, restore, snapshots")
        sys.exit(1)


if __name__ == "__main__":
    main()
