#!/usr/bin/env python3
"""
Context Gate — Phase 3 of Session Distiller
Polls OpenClaw gateway for session context usage.
Warns at CONTEXT_WARN_PCT, hard-gates at CONTEXT_HARD_PCT.
Auto-distills on hard gate. Sends Telegram alerts.

Usage:
    python3 context-gate.py              # Live run
    python3 context-gate.py --dry-run    # Preview only (no alerts, no distill)
    python3 context-gate.py --version    # Show version

Environment variables:
    CONTEXT_WARN_PCT   Warning threshold (default: 40)
    CONTEXT_HARD_PCT   Hard gate threshold (default: 60)
    BOT_TOKEN          Telegram bot token (required for alerts)
    CHAT_ID            Telegram chat ID for alerts (required for alerts)
"""

__version__ = "0.1.0"

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration (environment-variable overrides)
# ---------------------------------------------------------------------------
CONTEXT_WARN_PCT = int(os.environ.get("CONTEXT_WARN_PCT", "40"))
CONTEXT_HARD_PCT = int(os.environ.get("CONTEXT_HARD_PCT", "60"))
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
GATE_STATE_FILE = SCRIPT_DIR.parent / "gate-state.json"
DISTILL_SCRIPT = SCRIPT_DIR / "distill.py"
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"

# Chars-per-token approximation for JSONL fallback
CHARS_PER_TOKEN = 4

# Session key patterns to SKIP (cron jobs, slash commands — not real conversations)
SKIP_KEY_PATTERNS = ["cron:", "slash:"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def load_gate_state() -> dict:
    """Load per-session gate state tracking.
    Structure: { "<sessionId>": { "warned": bool, "gated": bool } }
    """
    if GATE_STATE_FILE.exists():
        try:
            return json.loads(GATE_STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log(f"⚠️  Corrupt gate-state.json — resetting")
            return {}
    return {}


def save_gate_state(state: dict):
    GATE_STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def send_telegram(message: str, dry_run: bool = False):
    """Send a Telegram message via bot API."""
    if dry_run:
        log(f"DRY RUN — would send: {message}")
        return
    if not BOT_TOKEN or not CHAT_ID:
        log("⚠️  BOT_TOKEN or CHAT_ID not set — skipping Telegram alert")
        return
    try:
        payload = json.dumps({
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        })
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                "-H", "Content-Type: application/json",
                "-d", payload,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        # Check for Telegram API errors
        try:
            resp = json.loads(result.stdout)
            if not resp.get("ok"):
                log(f"⚠️  Telegram API error: {resp.get('description', 'unknown')}")
        except json.JSONDecodeError:
            pass
    except Exception as e:
        log(f"⚠️  Telegram send failed: {e}")


def get_session_status() -> list:
    """Call openclaw gateway call status --json and return session list."""
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/openclaw", "gateway", "call", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            log(f"⚠️  openclaw gateway call status failed (exit {result.returncode})")
            log(f"    stderr: {result.stderr.strip()}")
            return []
        data = json.loads(result.stdout)
        sessions = data.get("sessions", {}).get("recent", [])
        return sessions
    except subprocess.TimeoutExpired:
        log("⚠️  openclaw gateway call status timed out")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        log(f"⚠️  Failed to parse gateway status: {e}")
        return []


def run_distill_for_session(session: dict, dry_run: bool = False) -> bool:
    """Run distill.py --live-session for the given session. Returns True on success."""
    session_id = session.get("sessionId", "unknown")
    if dry_run:
        log(f"DRY RUN — would auto-distill session {session_id[:8]}")
        return True
    try:
        log(f"  Auto-distilling session {session_id[:8]}...")
        result = subprocess.run(
            ["python3", str(DISTILL_SCRIPT), "--live-session", session_id],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode == 0:
            log(f"  ✅ Distillation complete for {session_id[:8]}")
            return True
        else:
            log(f"  ⚠️  Distillation failed (exit {result.returncode})")
            log(f"      stdout: {result.stdout.strip()[:200]}")
            log(f"      stderr: {result.stderr.strip()[:200]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"  ⚠️  Distillation timed out for {session_id[:8]}")
        return False
    except Exception as e:
        log(f"  ⚠️  Distillation error: {e}")
        return False


def estimate_tokens_from_jsonl(session_id: str) -> int:
    """Fallback: estimate token usage by reading the session JSONL file on disk.
    Counts total content chars across all messages and divides by CHARS_PER_TOKEN.
    Returns 0 if file not found or unreadable.
    """
    # Find the session file — active sessions use plain <uuid>.jsonl
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    if not session_file.exists():
        return 0
    try:
        total_chars = 0
        with open(session_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    # JSONL format: content is nested inside entry["message"]
                    msg = entry.get("message", entry)
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        total_chars += len(content)
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                text = block.get("text", "") or block.get("content", "")
                                total_chars += len(str(text))
                except (json.JSONDecodeError, TypeError):
                    continue
        return total_chars // CHARS_PER_TOKEN
    except OSError:
        return 0


def clean_stale_sessions(state: dict, active_session_ids: set) -> dict:
    """Remove gate state entries for sessions that no longer exist (reset/new)."""
    stale = [sid for sid in state if sid not in active_session_ids]
    for sid in stale:
        log(f"  Clearing stale gate state for {sid[:8]}")
        del state[sid]
    return state


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if "--version" in sys.argv:
        print(f"context-gate.py {__version__}")
        sys.exit(0)

    dry_run = "--dry-run" in sys.argv

    log("=" * 50)
    log(f"CONTEXT GATE — {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"Thresholds: warn={CONTEXT_WARN_PCT}% hard={CONTEXT_HARD_PCT}%")
    log("=" * 50)

    # Get live session data
    sessions = get_session_status()
    if not sessions:
        log("No sessions returned from gateway. Exiting.")
        return

    # Filter out cron/slash sessions — only monitor real conversations
    monitored = [
        s for s in sessions
        if not any(pat in s.get("key", "") for pat in SKIP_KEY_PATTERNS)
    ]
    if not monitored:
        log("No direct/group sessions active. Exiting.")
        return

    # Load gate state
    state = load_gate_state()
    active_ids = {s["sessionId"] for s in monitored if "sessionId" in s}
    state = clean_stale_sessions(state, active_ids)

    actions_taken = 0

    for session in monitored:
        sid = session.get("sessionId", "unknown")
        key = session.get("key", "unknown")
        ctx = session.get("contextTokens") or 0
        kind = session.get("kind", "unknown")

        # Derive token usage — try percentUsed first, fall back to inputTokens/contextTokens
        raw_pct = session.get("percentUsed")
        raw_total = session.get("totalTokens")
        input_tokens = session.get("inputTokens")

        if raw_pct is not None and raw_total is not None:
            pct = int(raw_pct)
            total = int(raw_total)
            token_source = "api"
        elif input_tokens is not None and ctx > 0:
            total = int(input_tokens)
            pct = round((total / ctx) * 100)
            token_source = "api:inputTokens"
        else:
            # Fallback: estimate from JSONL file on disk
            total = estimate_tokens_from_jsonl(sid)
            pct = round((total / ctx) * 100) if ctx > 0 and total > 0 else 0
            token_source = "jsonl-estimate"

        # Skip sessions with no context data
        if ctx == 0 or total == 0:
            log(f"\n  Session: {key}")
            log(f"  ⏭  No context data — skipping")
            continue

        log(f"\n  Session: {key}")
        log(f"  Context: {pct}% ({total:,}/{ctx:,} tokens) [{token_source}]")

        # Initialize state for this session if needed
        if sid not in state:
            state[sid] = {"warned": False, "gated": False}

        s = state[sid]

        # --- Hard gate check (check first so we don't double-alert) ---
        if pct >= CONTEXT_HARD_PCT and not s["gated"]:
            log(f"  🛑 HARD GATE — {pct}% >= {CONTEXT_HARD_PCT}%")

            # Auto-distill
            distill_ok = run_distill_for_session(session, dry_run=dry_run)
            distill_status = "✅ Distilled to memory" if distill_ok else "⚠️ Distill failed — flush manually"

            alert = (
                f"🛑 *Context Hard Gate*\n"
                f"Session: `{key}`\n"
                f"Usage: *{pct}%* ({total:,}/{ctx:,} tokens)\n"
                f"{distill_status}\n"
                f"Recommend `/new` now."
            )
            send_telegram(alert, dry_run=dry_run)

            s["gated"] = True
            s["warned"] = True  # Don't send a separate warning
            actions_taken += 1

        # --- Warning check ---
        elif pct >= CONTEXT_WARN_PCT and not s["warned"]:
            log(f"  ⚠️  WARNING — {pct}% >= {CONTEXT_WARN_PCT}%")

            alert = (
                f"⚠️ *Context Warning*\n"
                f"Session: `{key}`\n"
                f"Usage: *{pct}%* ({total:,}/{ctx:,} tokens)\n"
                f"Consider wrapping up or flushing to memory."
            )
            send_telegram(alert, dry_run=dry_run)

            s["warned"] = True
            actions_taken += 1

        else:
            if pct < CONTEXT_WARN_PCT:
                log(f"  ✅ Below threshold")
            elif s["warned"] and not s["gated"]:
                log(f"  ⏭  Already warned (once per session)")
            elif s["gated"]:
                log(f"  ⏭  Already gated (once per session)")

    # Save state
    save_gate_state(state)

    log(f"\n{'=' * 50}")
    log(f"Complete. Actions taken: {actions_taken}")
    log(f"{'=' * 50}")


if __name__ == "__main__":
    main()
