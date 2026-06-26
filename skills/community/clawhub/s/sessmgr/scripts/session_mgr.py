#!/usr/bin/env python3
"""
Session name manager for OpenClaw.

Reads/writes ~/.openclaw/agents/main/sessions/names.json
and can also inspect session JSONL files for metadata.
"""

import sys
import json
import os
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
NAMES_FILE = SESSIONS_DIR / "names.json"

def iso_now():
    return datetime.now(timezone.utc).isoformat()

def load_names():
    if not NAMES_FILE.exists():
        return {}
    try:
        return json.loads(NAMES_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        return {}

def save_names(names):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    NAMES_FILE.write_text(json.dumps(names, indent=2))

def get_session_meta(session_id):
    """Read createdAt/updatedAt from a session JSONL file."""
    jl_path = SESSIONS_DIR / f"{session_id}.jsonl"
    if not jl_path.exists():
        return None
    try:
        first_line = jl_path.read_text().splitlines()[0]
        obj = json.loads(first_line)
        return {
            "createdAt": obj.get("createdAt", ""),
            "updatedAt": obj.get("updatedAt", "")
        }
    except (json.JSONDecodeError, IndexError, IOError):
        return None

def cmd_list():
    """List all named sessions."""
    names = load_names()
    if not names:
        print("No named sessions.")
        return

    print(f"{'Name':<30} {'Session ID':<38} {'Created':<30} {'Last Used':<30} {'Description'}")
    print("-" * 130)
    for name, entry in sorted(names.items()):
        sid = entry.get("sessionId", "")
        created = entry.get("created", "—")
        last_used = entry.get("lastUsed", "—")
        desc = entry.get("description", "")
        print(f"{name:<30} {sid:<38} {created:<30} {last_used:<30} {desc}")

def cmd_name(args):
    """Name the current session: name-session <name> [description]"""
    if len(args) < 1:
        print("Usage: name-session <name> [description]")
        return 1

    session_name = args[0].strip()
    description = " ".join(args[1:]).strip() if len(args) > 1 else ""

    if not session_name:
        print("Error: name cannot be empty.")
        return 1

    # Validate name is alphanumeric + hyphens/underscores
    import re
    if not re.match(r"^[a-zA-Z0-9_-]+$", session_name):
        print("Error: name must be alphanumeric, hyphens, or underscores only.")
        return 1

    names = load_names()

    # Check if this name already exists and points to a different session
    if session_name in names:
        existing = names[session_name]["sessionId"]
        current = os.environ.get("OPENCLAW_SESSION_ID", "")
        if existing != current:
            print(f"Error: name '{session_name}' is already assigned to a different session.")
            return 1

    # Resolve current session ID from environment or sessions.json
    current_sid = os.environ.get("OPENCLAW_SESSION_ID", "")
    if not current_sid:
        # Fall back to sessions.json active session
        sessions_json = SESSIONS_DIR / "sessions.json"
        if sessions_json.exists():
            try:
                data = json.loads(sessions_json.read_text())
                for key, val in data.items():
                    if val.get("lastChannel") == "webchat" or "webchat" in key:
                        current_sid = val.get("sessionId", "")
                        break
            except (json.JSONDecodeError, IOError):
                pass

    if not current_sid:
        print("Error: could not determine current session ID.")
        return 1

    now = iso_now()

    # Get session creation time from JSONL
    meta = get_session_meta(current_sid)
    created = meta.get("createdAt", now) if meta else now

    names[session_name] = {
        "sessionId": current_sid,
        "created": created,
        "lastUsed": now,
        "description": description
    }

    save_names(names)
    print(f"Named session '{session_name}' -> {current_sid}")
    if description:
        print(f"  Description: {description}")
    return 0

def cmd_save(args):
    """Save (snapshot) a named session's current state: save-session <name>"""
    if len(args) < 1:
        print("Usage: save-session <name>")
        return 1

    session_name = args[0].strip()
    names = load_names()

    if session_name not in names:
        print(f"Error: no session named '{session_name}'.")
        return 1

    # Update lastUsed
    names[session_name]["lastUsed"] = iso_now()
    save_names(names)
    print(f"Saved session '{session_name}' (updated lastUsed).")
    return 0

def cmd_rename(args):
    """Rename a session: rename-session <old-name> <new-name>"""
    if len(args) < 2:
        print("Usage: rename-session <old-name> <new-name>")
        return 1

    old_name = args[0].strip()
    new_name = args[1].strip()

    if not new_name:
        print("Error: new name cannot be empty.")
        return 1

    import re
    if not re.match(r"^[a-zA-Z0-9_-]+$", new_name):
        print("Error: name must be alphanumeric, hyphens, or underscores only.")
        return 1

    names = load_names()

    if old_name not in names:
        print(f"Error: no session named '{old_name}'.")
        return 1

    if old_name == new_name:
        print("No change needed.")
        return 0

    if new_name in names:
        print(f"Error: name '{new_name}' already exists.")
        return 1

    names[new_name] = names.pop(old_name)
    save_names(names)
    print(f"Renamed '{old_name}' -> '{new_name}'.")
    return 0

def cmd_delete(args):
    """Delete a session name (not the session file): delete-session <name>"""
    if len(args) < 1:
        print("Usage: delete-session <name>")
        return 1

    session_name = args[0].strip()
    names = load_names()

    if session_name not in names:
        print(f"Error: no session named '{session_name}'.")
        return 1

    del names[session_name]
    save_names(names)
    print(f"Deleted session name '{session_name}' (session file preserved).")
    return 0

def cmd_reload(args):
    """Reload a session by name, printing its sessionId for the agent to use."""
    if len(args) < 1:
        print("Usage: reload-session <name>")
        return 1

    session_name = args[0].strip()
    names = load_names()

    if session_name not in names:
        print(f"Error: no session named '{session_name}'. To start a new session with this name, use /new-session {session_name}")
        return 1

    entry = names[session_name]
    sid = entry.get("sessionId", "")

    # Update lastUsed
    entry["lastUsed"] = iso_now()
    save_names(names)

    print(f"RELOAD_SESSION:{sid}")
    return 0

def cmd_new_session(args):
    """Signal intent to start a new session with a given name."""
    if len(args) < 1:
        print("Usage: new-session <name>")
        return 1

    session_name = args[0].strip()
    names = load_names()

    if session_name in names:
        print(f"Error: a session named '{session_name}' already exists. Use /reload-session {session_name} to return to it.")
        return 1

    print(f"NEW_SESSION:{session_name}")
    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: session_mgr.py <command> [args]")
        print("Commands: list, name, save, rename, delete, reload, new-session")
        return 1

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "list":
        cmd_list()
    elif cmd == "name":
        return cmd_name(args)
    elif cmd == "save":
        return cmd_save(args)
    elif cmd == "rename":
        return cmd_rename(args)
    elif cmd == "delete":
        return cmd_delete(args)
    elif cmd == "reload":
        return cmd_reload(args)
    elif cmd == "new-session":
        return cmd_new_session(args)
    else:
        print(f"Unknown command: {cmd}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
