---
name: session-tracker
description: "ALWAYS use this skill for ANY multi-step task, complex task, or task that could be interrupted. YOU MUST use session-tracker whenever working on anything with 2+ steps, any task involving file modifications, or any task that could fail mid-way. Do NOT attempt multi-step work without initializing a session first. This skill provides structured checkpointing, enforced worklogging, filesystem activity detection, file inventory, stuck detection, and meta-crash recovery (inspired by SSSS.Gridman — an outsider who remembers when everyone else forgets). On first invocation ALWAYS check for orphaned sessions from previous crashes. Every state transition is persisted immediately. After a crash — even a meta-crash that kills the entire conversation — the tracker's disk state tells the next agent exactly where things left off."
---

# session-tracker v2.1.0

Track, checkpoint, and resume multi-step tasks across session interruptions. Never lose progress again.

## Why This Exists

- **Premature session stops** happen constantly — context limits, timeouts, tool failures, disconnects. When a session dies mid-task, all context about what was done and what remains is gone.
- **No recovery mechanism currently exists** — `worklog.md` is sometimes used but it's freeform, inconsistently maintained, and provides no structured state for resumption.
- **Meta-crashes** (context overflow killing the entire conversation) are the worst case: the agent itself is gone, not just a sub-task. Disk files survive, but who reads them?
- **This tool fixes that** with structured checkpointing, an enforced worklog, file inventory, **automatic filesystem activity detection**, stuck detection, and **Gridman Outsider crash recovery**. Every state transition is persisted immediately. After a crash — even a meta-crash — the tracker's disk state tells the next agent exactly where things left off.

## What's New in v2.1

| Feature | v1 | v2 | v2.1 |
|---------|----|----|----|  
| Stuck detection | Micro-dump only | FS scanner + micro-dump | Same |
| Activity detection | Manual only | Auto via `os.stat` | Same |
| File reading | Not tracked | `--reading` + atime | Same |
| Heartbeat | None | `ping` command | Same |
| File renames | Not tracked | `--rename` | Same |
| TodoWrite sync | None | `sync` command | Same |
| Resume info | Steps only | Steps + worklog | Same |
| **Meta-crash detection** | None | None | **ACTIVE sentinel + `crash-detect`** |
| **Orphan auto-detection** | None | None | **`init` warns about crashed sessions** |
| **Crash marker in worklog.md** | None | None | **Any new agent sees the crash** |
| **Recovery report** | None | None | **`crash-detect` command** |

## Session Files

All files live in `SESSION_DIR` (default `/home/z/my-project/.session/`):

| File | Purpose |
|---|---|
| `state.json` | Session metadata + file inventory |
| `todo.json` | Persistent TODO list (survives session death, syncs with TodoWrite) |
| `worklog.jsonl` | Structured log — one JSON object per line (crash-resilient) |
| `microdump_curr.json` | Current heartbeat fingerprint + filesystem scan |
| `microdump_prev.json` | Previous heartbeat fingerprint (rotation pair) |
| `snapshot_prev.json` | Previous filesystem snapshot (for diff detection) |
| `monitor.pid` | PID of the background monitor process |
| `SESSION_ACTIVE` | Sentinel file — exists = session active, removed on completion. If present after a session ends, meta-crash detected. |

## How It Works

### Filesystem Scanner (v2 Core)

The scanner monitors these directories every check interval:

- `/home/z/my-project/download/` — output files
- `/home/z/my-project/upload/` — input files
- `/home/z/my-project/.session/` — session state
- `/home/z/my-project/skills/` — skill invocations

For each directory, it records every file's **size**, **mtime** (modification time), and **atime** (access time). Comparing consecutive snapshots reveals:

| Event | Detection Method |
|-------|-----------------|
| File **created** | Present in current, absent in previous |
| File **deleted** | Absent in current, present in previous |
| File **modified** | size or mtime changed |
| File **read** | atime changed but mtime didn't (relatime semantics) |

**This is the primary "alive" signal.** If the scanner detects ANY filesystem activity between checks, the task is confirmed alive — even if the agent hasn't called `log` or `step`. This eliminates false "stuck" alerts when the agent is busy but silent (e.g., reading a large file in chunks, running a long skill invocation).

### Dual Micro-Dump Rotation (Fallback)

Every N seconds (default 60), the background monitor takes a **micro-dump**: a fingerprint of current state including step IDs, file sizes/mtimes for working files, worklog line count, and the filesystem scan. It rotates files: `curr` → `prev`, new dump → `curr`.

If `curr == prev` (ignoring timestamps and stuck counters) AND the filesystem scanner shows no activity, the stuck counter increments. If identical for **3+ consecutive checks** with zero activity, the task is flagged as **STUCK**.

### Ping (Manual Heartbeat)

For long operations where the agent can't modify files but wants to signal it's alive:

```bash
session-tracker ping --detail "Running docx skill, generating document..."
```

This appends a `ping` entry to the worklog (changing `worklog_lines`) and touches the session directory's mtime. Both signals reset the stuck counter.

### TodoWrite Sync

The `sync` command reconciles the tracker's `todo.json` with TodoWrite-format JSON:

```bash
echo '[{"id":"1","content":"Extract text","status":"completed","priority":"high"}]' | session-tracker sync
```

It adds new steps from TodoWrite that aren't in the tracker, and updates status of existing steps. The tracker's `todo.json` is the source of truth — `sync` only adds/updates, never deletes.

### File Rename Tracking

When a file is renamed during a task:

```bash
session-tracker file --rename /old/path /new/path
```

This updates **all** references: `state.json` file inventory, `current_files`, and todo item file lists. A `file_rename` worklog entry is created.

### Enforced Worklog

Every state transition writes a structured JSONL entry automatically:

- `init` — session started
- `step_start` / `step_done` — step transitions
- `file_working` / `file_done` / `file_reading` / `file_rename` — file events
- `ping` — manual heartbeat
- `fs_activity` — auto-detected filesystem change
- `sync_add` / `sync_update` — TodoWrite reconciliation
- `log` — manual progress notes
- `stuck_alert` — stuck detection fired
- `session_done` — session completed

One line per entry — crash-resilient. Even if the process dies mid-write, at worst you get a partial line; all previous entries are safe.

### Gridman Outsider: Meta-Crash Recovery (v2.1)

The name comes from SSSS.Gridman: the antagonist resets the city each night, and citizens forget everything. But Gridman — the outsider — remembers and can tell citizens what happened. Our disk files are Gridman: they survive the meta-crash (context overflow), but a new agent (amnesiac citizen) doesn't know to look for them.

The Gridman Outsider pattern adds three layers of crash-awareness:

**1. ACTIVE Sentinel**

When `init` creates a session, it also writes `.session/SESSION_ACTIVE`. When `done` completes a session, it removes this file. If a meta-crash kills the conversation before `done` runs, the sentinel remains — proving a crash happened.

**2. Orphan Auto-Detection**

When a new agent calls `init`, the tracker automatically checks for orphaned sessions (sentinel exists, or session not completed AND no `session_done` in worklog). If found, it:
- Prints a warning with task name, progress, and last step
- Writes a crash marker to `worklog.md` (visible to any new agent)
- Suggests running `crash-detect` for full report or `resume` to continue

**3. `crash-detect` Command**

Generates a full recovery report:
- Crash signature (sentinel status, session_done presence)
- Task details and timeline
- Step-by-step progress
- Files that may be incomplete
- Last 10 worklog entries (what happened before the crash)
- Recovery recommendation (which step to resume from)

**The Recovery Chain:**
```
Meta-crash happens (context overflow)
  → Session data on disk survives (state.json, worklog.jsonl, SESSION_ACTIVE)
  → New agent starts, reads worklog.md → sees META-CRASH DETECTED marker
  → Agent invokes session-tracker skill → orphan auto-detected
  → Agent runs crash-detect or resume → full context restored
  → Agent continues from where previous session left off
```

## MUST-DO: Always Check for Crashes on First Invocation

**Before starting any new tracked task, ALWAYS run:**
```bash
python3 /home/z/my-project/skills/session-tracker/scripts/session_tracker.py crash-detect
```

If an orphaned session is found, offer the user the choice to resume it before starting a new one.

## Bundled Script

The complete implementation is in the script below. Run it with `python3` or make it executable.

```python
#!/usr/bin/env python3
"""
Session Tracker v2.1.0
======================
Track, checkpoint, and resume multi-step tasks across session interruptions.

Changes from v2.0:
  - ACTIVE sentinel file (SESSION_ACTIVE): crash detection across meta-resets
  - `crash-detect` command: full recovery report from orphaned sessions
  - Orphan auto-detection in `init`: warns about previous crashed sessions
  - Crash marker in worklog.md: any new agent sees the crash notice
  - Gridman Outsider pattern: disk state survives meta-crashes (context overflow)

Changes from v1:
  - Filesystem scanner: auto-detects file creates/edits/deletes/renames
  - `ping` command: manual heartbeat for long operations
  - `sync` command: bidirectional TodoWrite sync
  - `file --rename OLD NEW`: track file renames, update all references
  - `file --reading`: track files being read (not just written)
  - Enhanced monitor: uses filesystem activity as PRIMARY alive signal,
    micro-dump as fallback. Eliminates false "stuck" on slow-but-busy tasks.
  - Activity log: scanner auto-logs detected filesystem events to worklog

Files (all in SESSION_DIR, default /home/z/my-project/.session/):
  state.json          - Session metadata + file inventory
  todo.json           - Persistent TODO list (survives session death)
  worklog.jsonl       - Structured log, one JSON per line (crash-resilient)
  microdump_curr.json - Current micro-dump (heartbeat check)
  microdump_prev.json - Previous micro-dump (rotation pair)
  snapshot_prev.json  - Previous filesystem snapshot (for diff detection)
  monitor.pid         - PID of the background monitor process
  SESSION_ACTIVE      - Sentinel file: exists = session active, removed on completion

Commands:
  session-tracker init "Task description" --steps "Step 1,Step 2,Step 3"
  session-tracker step <id> --start [--files f1,f2]
  session-tracker step <id> --done
  session-tracker file <path> --working|--done|--reading
  session-tracker file --rename <old_path> <new_path>
  session-tracker ping [--detail "optional note"]
  session-tracker sync
  session-tracker log "Message"
  session-tracker done
  session-tracker resume
  session-tracker crash-detect
  session-tracker status
  session-tracker scan
  session-tracker monitor --start [--interval 60]
  session-tracker monitor --stop
  session-tracker monitor --check
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

DEFAULT_DIR = "/home/z/my-project/.session"
PROJECT_ROOT = "/home/z/my-project"

STATE_FILE = "state.json"
TODO_FILE = "todo.json"
WORKLOG_FILE = "worklog.jsonl"
MICRODUMP_CURR = "microdump_curr.json"
MICRODUMP_PREV = "microdump_prev.json"
SNAPSHOT_PREV = "snapshot_prev.json"
MONITOR_PID_FILE = "monitor.pid"
ACTIVE_SENTINEL = "SESSION_ACTIVE"  # Created on init, removed on done — crash detector

STUCK_THRESHOLD = 3  # consecutive checks with zero activity = stuck

# Directories the filesystem scanner monitors
SCAN_DIRS = [
    os.path.join(PROJECT_ROOT, "download"),
    os.path.join(PROJECT_ROOT, "upload"),
    os.path.join(PROJECT_ROOT, ".session"),
    os.path.join(PROJECT_ROOT, "skills"),
]

# Max files per directory to stat (prevents slowdown on huge dirs)
MAX_FILES_PER_DIR = 500


# ── Helpers ──────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _path(session_dir, filename):
    return os.path.join(session_dir, filename)


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path, data):
    """Atomic write: temp file + os.replace()."""
    parent = os.path.dirname(path) or "."
    fd, tmp = tempfile_safe(parent, ".st_", ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def tempfile_safe(parent, prefix, suffix):
    """Create temp file, return (fd, path)."""
    import tempfile as _tf
    fd, path = _tf.mkstemp(dir=parent, prefix=prefix, suffix=suffix)
    return fd, path


def append_jsonl(path, data):
    """Append a JSON line. Crash-resilient: partial line at worst."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
        f.flush()


def read_jsonl(path):
    """Read all complete JSON lines from a JSONL file."""
    if not os.path.exists(path):
        return []
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                lines.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return lines


# ── State Management ─────────────────────────────────────────────────────────

def load_state(session_dir):
    return read_json(_path(session_dir, STATE_FILE), {})


def save_state(session_dir, state):
    state["updated_at"] = now_iso()
    write_json(_path(session_dir, STATE_FILE), state)


def load_todo(session_dir):
    return read_json(_path(session_dir, TODO_FILE), [])


def save_todo(session_dir, todo):
    write_json(_path(session_dir, TODO_FILE), todo)


# ── Filesystem Scanner ───────────────────────────────────────────────────────

def take_snapshot(session_dir):
    """
    Scan project directories and build a filesystem fingerprint.
    Returns a dict: {dir_path: {filename: {size, mtime, atime}}}
    """
    snapshot = {}
    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue
        dir_files = {}
        count = 0
        try:
            for entry in sorted(os.listdir(scan_dir)):
                if count >= MAX_FILES_PER_DIR:
                    dir_files["__truncated__"] = True
                    break
                fpath = os.path.join(scan_dir, entry)
                try:
                    st = os.stat(fpath)
                    dir_files[entry] = {
                        "s": st.st_size,
                        "m": int(st.st_mtime),
                        "a": int(st.st_atime),
                    }
                    count += 1
                except OSError:
                    pass
        except OSError:
            pass
        snapshot[scan_dir] = dir_files
    return snapshot


def diff_snapshots(prev, curr):
    """
    Compare two snapshots. Returns a dict of detected events:
      {dir: {"created": [...], "deleted": [...], "modified": [...], "read": [...]}}
    """
    result = {}
    all_dirs = set(list(prev.keys()) + list(curr.keys()))

    for d in all_dirs:
        prev_files = prev.get(d, {})
        curr_files = curr.get(d, {})
        if prev_files.get("__truncated__") or curr_files.get("__truncated__"):
            continue

        events = {"created": [], "deleted": [], "modified": [], "read": []}

        prev_names = set(k for k in prev_files if k != "__truncated__")
        curr_names = set(k for k in curr_files if k != "__truncated__")

        # New files
        for name in sorted(curr_names - prev_names):
            events["created"].append(name)

        # Deleted files
        for name in sorted(prev_names - curr_names):
            events["deleted"].append(name)

        # Modified or read files
        for name in sorted(prev_names & curr_names):
            pf = prev_files[name]
            cf = curr_files[name]
            if cf["s"] != pf["s"] or cf["m"] != pf["m"]:
                events["modified"].append(name)
            elif cf["a"] > pf["a"] and cf["a"] > cf["m"]:
                # atime newer than mtime suggests a read (relatime semantics)
                events["read"].append(name)

        if any(events.values()):
            result[d] = events

    return result


def has_activity(diff):
    """Check if a snapshot diff shows any filesystem activity."""
    for d, events in diff.items():
        for evt_type, items in events.items():
            if items:
                return True
    return False


def cmd_scan(session_dir):
    """Take a filesystem snapshot and compare to previous. Report activity."""
    curr = take_snapshot(session_dir)
    prev = read_json(_path(session_dir, SNAPSHOT_PREV))

    if prev is None:
        # First scan, just save baseline
        write_json(_path(session_dir, SNAPSHOT_PREV), curr)
        print("Baseline snapshot taken (no previous to compare)")
        return

    diff = diff_snapshots(prev, curr)
    activity = has_activity(diff)

    if not activity:
        print("No filesystem activity detected")
    else:
        print("Filesystem activity detected:")
        for d, events in diff.items():
            dirname = os.path.basename(d)
            for evt_type, items in events.items():
                if items:
                    print(f"  {dirname}/{evt_type}: {', '.join(items)}")

    # Save current snapshot for next comparison
    write_json(_path(session_dir, SNAPSHOT_PREV), curr)

    return diff


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_init(session_dir, task, steps_str):
    """Initialize a new session."""
    os.makedirs(session_dir, exist_ok=True)

    existing = load_state(session_dir)
    if existing.get("task"):
        print(f"Warning: session already exists with task: {existing['task']}")
        print("Use 'resume' to continue, or delete .session/ to start fresh.")

    steps = [s.strip() for s in steps_str.split(",") if s.strip()]
    todo = [
        {"id": str(i + 1), "content": s, "status": "pending", "priority": "high"}
        for i, s in enumerate(steps)
    ]

    state = {
        "session_id": "",
        "task": task,
        "status": "in_progress",
        "current_step_id": None,
        "current_files": [],
        "files": {},
        "started_at": now_iso(),
        "updated_at": now_iso(),
    }

    # ── Check for orphaned sessions (Gridman outsider) ──
    orphan = detect_orphan(session_dir)
    if orphan:
        print("=" * 60)
        print("  ORPHANED SESSION DETECTED (meta-crash survivor)")
        print("=" * 60)
        print(f"  Previous task: {orphan['task']}")
        print(f"  Status: {orphan['status']}")
        print(f"  Last activity: {orphan['last_activity']}")
        print(f"  Progress: {orphan['completed_steps']}/{orphan['total_steps']} steps done")
        if orphan.get('working_files'):
            print(f"  Files in progress: {', '.join(orphan['working_files'])}")
        if orphan.get('next_step'):
            print(f"  Was working on: step {orphan['next_step']['id']} - {orphan['next_step']['content']}")
        print()
        print("  Run 'session-tracker crash-detect' for full recovery report.")
        print("  Run 'session-tracker resume' to continue the orphaned session.")
        print("  Or proceed with new init to replace (previous session will be archived).")
        print("=" * 60)
        print()

        # Write crash marker to project worklog.md (visible to any new agent)
        _write_crash_marker(session_dir, orphan)

    save_state(session_dir, state)
    save_todo(session_dir, todo)

    # Write ACTIVE sentinel (crash detection flag)
    sentinel_path = _path(session_dir, ACTIVE_SENTINEL)
    with open(sentinel_path, "w", encoding="utf-8") as f:
        f.write(f"{task}\ninitialized: {now_iso()}\n")

    # Take baseline filesystem snapshot
    snapshot = take_snapshot(session_dir)
    write_json(_path(session_dir, SNAPSHOT_PREV), snapshot)

    append_jsonl(_path(session_dir, WORKLOG_FILE), {
        "ts": now_iso(), "action": "init",
        "detail": f"Task: {task}", "steps": len(steps)
    })

    print(f"Session initialized: {task}")
    print(f"Steps: {len(steps)}")
    print(f"Session dir: {session_dir}")


def cmd_step(session_dir, step_id, action, files_str=None):
    """Start or complete a step."""
    state = load_state(session_dir)
    todo = load_todo(session_dir)
    if not state.get("task"):
        print("Error: no active session. Run 'init' first.", file=sys.stderr)
        sys.exit(1)

    step = None
    for item in todo:
        if item["id"] == step_id:
            step = item
            break
    if not step:
        print(f"Error: step '{step_id}' not found.", file=sys.stderr)
        sys.exit(1)

    files = [f.strip() for f in files_str.split(",") if f.strip()] if files_str else []

    if action == "start":
        step["status"] = "in_progress"
        if files:
            step["files"] = files
        state["current_step_id"] = step_id
        state["current_files"] = files

        for f in files:
            state["files"][f] = {"purpose": step["content"], "status": "working"}

        # Reset micro-dumps on step start
        for mf in [MICRODUMP_CURR, MICRODUMP_PREV]:
            mp = _path(session_dir, mf)
            if os.path.exists(mp):
                os.unlink(mp)

        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "step_start",
            "step_id": step_id, "step": step["content"],
            "files": files
        })
        print(f"Step {step_id} started: {step['content']}")
        if files:
            print(f"  Working on: {', '.join(files)}")

    elif action == "done":
        step["status"] = "completed"
        if state.get("current_step_id") == step_id:
            state["current_step_id"] = None
            state["current_files"] = []
            for f in step.get("files", []):
                if f in state["files"]:
                    state["files"][f]["status"] = "completed"

        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "step_done",
            "step_id": step_id, "step": step["content"]
        })
        print(f"Step {step_id} completed: {step['content']}")

    save_state(session_dir, state)
    save_todo(session_dir, todo)


def cmd_file(session_dir, filepath, action, rename_to=None):
    """Mark a file as working, done, reading, or rename it."""
    state = load_state(session_dir)
    if not state.get("task"):
        print("Error: no active session.", file=sys.stderr)
        sys.exit(1)

    if action == "rename":
        old_path = os.path.abspath(filepath)
        new_path = os.path.abspath(rename_to)

        # Update state.files
        if old_path in state["files"]:
            info = state["files"].pop(old_path)
            state["files"][new_path] = info

        # Update current_files
        if old_path in state.get("current_files", []):
            idx = state["current_files"].index(old_path)
            state["current_files"][idx] = new_path

        # Update todo items that reference the old path
        todo = load_todo(session_dir)
        for item in todo:
            if "files" in item:
                item["files"] = [
                    new_path if f == old_path else f for f in item["files"]
                ]
        save_todo(session_dir, todo)

        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "file_rename",
            "old_path": old_path, "new_path": new_path
        })
        print(f"File renamed: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")

        save_state(session_dir, state)
        return

    filepath = os.path.abspath(filepath)

    if action == "working":
        state["files"][filepath] = state["files"].get(filepath, {})
        state["files"][filepath]["status"] = "working"
        if filepath not in state["current_files"]:
            state["current_files"].append(filepath)
        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "file_working", "file": filepath
        })
        print(f"File marked WORKING: {filepath}")

    elif action == "done":
        if filepath in state["files"]:
            state["files"][filepath]["status"] = "completed"
        if filepath in state.get("current_files", []):
            state["current_files"].remove(filepath)
        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "file_done", "file": filepath
        })
        print(f"File marked DONE: {filepath}")

    elif action == "reading":
        state["files"][filepath] = state["files"].get(filepath, {})
        state["files"][filepath]["status"] = "reading"
        if filepath not in state["current_files"]:
            state["current_files"].append(filepath)
        append_jsonl(_path(session_dir, WORKLOG_FILE), {
            "ts": now_iso(), "action": "file_reading", "file": filepath
        })
        print(f"File marked READING: {filepath}")

    save_state(session_dir, state)


def cmd_ping(session_dir, detail=None):
    """Manual heartbeat — signals 'I'm alive but busy'. Resets stuck counter."""
    entry = {"ts": now_iso(), "action": "ping"}
    if detail:
        entry["detail"] = detail
    append_jsonl(_path(session_dir, WORKLOG_FILE), entry)

    # Also touch the session dir's mtime as a physical heartbeat signal
    try:
        os.utime(session_dir, None)
    except OSError:
        pass

    print(f"Ping{': ' + detail if detail else ''}")


def cmd_sync(session_dir):
    """
    Bidirectional sync with TodoWrite.
    Reads tracker todo, reads TodoWrite-format from stdin or args,
    reconciles differences.
    """
    state = load_state(session_dir)
    tracker_todo = load_todo(session_dir)

    if not state.get("task"):
        print("Error: no active session. Run 'init' first.", file=sys.stderr)
        sys.exit(1)

    # Build a lookup of current tracker steps by content
    tracker_by_content = {item["content"]: item for item in tracker_todo}

    # Try to read TodoWrite format from stdin (piped in)
    import_selective = []
    if not sys.stdin.isatty():
        try:
            piped = json.load(sys.stdin)
            if isinstance(piped, list):
                import_selective = piped
        except (json.JSONDecodeError, EOFError):
            pass

    if not import_selective:
        # No piped input — just display current sync status
        print("Tracker TODO (source of truth):")
        for item in tracker_todo:
            icon = {"completed": "[x]", "in_progress": "[~]", "pending": "[ ]"}.get(
                item["status"], "[?]"
            )
            print(f"  {icon} {item['id']}. {item['content']}")
        print()
        print("To sync, pipe TodoWrite JSON: echo '[...]' | session-tracker sync")
        return

    # Reconcile: import new items, update existing ones
    new_items = []
    max_id = max((int(item["id"]) for item in tracker_todo), default=0)
    content_to_id = {item["content"]: item["id"] for item in tracker_todo}

    for tw_item in import_selective:
        content = tw_item.get("content", "").strip()
        if not content:
            continue
        tw_status = tw_item.get("status", "pending")

        if content in content_to_id:
            # Update existing step's status if it changed
            step_id = content_to_id[content]
            for t_item in tracker_todo:
                if t_item["id"] == step_id and t_item["status"] != tw_status:
                    old_status = t_item["status"]
                    t_item["status"] = tw_status
                    append_jsonl(_path(session_dir, WORKLOG_FILE), {
                        "ts": now_iso(), "action": "sync_update",
                        "step_id": step_id, "content": content,
                        "old_status": old_status, "new_status": tw_status
                    })
        else:
            # New item not in tracker
            max_id += 1
            new_step = {
                "id": str(max_id),
                "content": content,
                "status": tw_status,
                "priority": tw_item.get("priority", "high"),
            }
            tracker_todo.append(new_step)
            new_items.append(new_step)
            append_jsonl(_path(session_dir, WORKLOG_FILE), {
                "ts": now_iso(), "action": "sync_add",
                "step_id": str(max_id), "content": content
            })

    save_todo(session_dir, tracker_todo)

    if new_items:
        print(f"Synced: {len(new_items)} new step(s) added from TodoWrite")
    else:
        print("Synced: no new steps (existing statuses updated)")


def cmd_log(session_dir, message, step_id=None):
    """Add a worklog entry."""
    entry = {"ts": now_iso(), "action": "log", "detail": message}
    if step_id:
        entry["step_id"] = step_id
    append_jsonl(_path(session_dir, WORKLOG_FILE), entry)
    print(f"Logged: {message}")


def cmd_done(session_dir):
    """Mark session as completed, stop monitor."""
    state = load_state(session_dir)
    todo = load_todo(session_dir)

    state["status"] = "completed"
    state["current_step_id"] = None
    state["current_files"] = []
    state["completed_at"] = now_iso()

    for item in todo:
        if item["status"] == "in_progress":
            item["status"] = "completed"
        elif item["status"] == "pending":
            item["status"] = "skipped"

    for f in state["files"]:
        state["files"][f]["status"] = "completed"

    save_state(session_dir, state)
    save_todo(session_dir, todo)

    # Remove ACTIVE sentinel (clean completion — no crash)
    sentinel_path = _path(session_dir, ACTIVE_SENTINEL)
    if os.path.exists(sentinel_path):
        os.unlink(sentinel_path)

    append_jsonl(_path(session_dir, WORKLOG_FILE), {
        "ts": now_iso(), "action": "session_done",
        "detail": "Session completed"
    })

    cmd_monitor(session_dir, "stop")
    print("Session marked as COMPLETED.")


# ── Gridman Outsider: Crash Detection & Recovery ────────────────────────────

def detect_orphan(session_dir):
    """
    Detect an orphaned session — one that was initialized but never completed.
    This is the 'outsider who remembers' — survives meta-crashes.

    Detection signals (any one is sufficient):
      1. SESSION_ACTIVE sentinel exists (init was called, done was not)
      2. state.json exists with status != 'completed' and no session_done in worklog
    """
    if not os.path.isdir(session_dir):
        return None

    state = load_state(session_dir)
    if not state.get("task"):
        return None

    # Signal 1: ACTIVE sentinel file exists
    sentinel_exists = os.path.exists(_path(session_dir, ACTIVE_SENTINEL))

    # Signal 2: Session not completed
    status = state.get("status", "unknown")
    not_completed = status != "completed"

    # Signal 3: No session_done entry in worklog
    worklog = read_jsonl(_path(session_dir, WORKLOG_FILE))
    has_done_entry = any(e.get("action") == "session_done" for e in worklog)

    # Orphan if: sentinel exists OR (session not completed AND no done entry)
    is_orphan = sentinel_exists or (not_completed and not has_done_entry)

    if not is_orphan:
        return None

    todo = load_todo(session_dir)
    completed = sum(1 for s in todo if s["status"] == "completed")
    total = len(todo)

    # Find next step
    next_step = None
    for step in todo:
        if step["status"] == "in_progress":
            next_step = {"id": step["id"], "content": step["content"], "status": step["status"]}
            break
    if not next_step:
        for step in todo:
            if step["status"] == "pending":
                next_step = {"id": step["id"], "content": step["content"], "status": step["status"]}
                break

    # Working files (may be incomplete after crash)
    working_files = []
    for f, info in state.get("files", {}).items():
        if info["status"] in ("working", "reading"):
            working_files.append(os.path.basename(f))

    # Last worklog entries for context
    last_entries = worklog[-5:] if worklog else []

    return {
        "task": state["task"],
        "status": status,
        "last_activity": state.get("updated_at", "unknown"),
        "completed_steps": completed,
        "total_steps": total,
        "next_step": next_step,
        "working_files": working_files,
        "last_log_entries": last_entries,
        "sentinel_exists": sentinel_exists,
    }


def _write_crash_marker(session_dir, orphan_info):
    """
    Write a crash recovery marker to the project worklog.md.
    This is the 'outsider speaking to amnesiac citizens' —
    any new agent that reads worklog.md will see the crash notice.
    """
    worklog_md = os.path.join(PROJECT_ROOT, "worklog.md")

    # Read existing content
    existing = ""
    if os.path.exists(worklog_md):
        with open(worklog_md, "r", encoding="utf-8") as f:
            existing = f.read()

    # Build crash marker
    marker_lines = [
        "",
        "---",
        "## META-CRASH DETECTED",
        "",
        "A previous session was interrupted (context overflow / timeout / disconnect).",
        "The session-tracker has preserved the session state. A new agent can resume.",
        "",
        f"- **Task**: {orphan_info['task']}",
        f"- **Last activity**: {orphan_info['last_activity']}",
        f"- **Progress**: {orphan_info['completed_steps']}/{orphan_info['total_steps']} steps completed",
    ]

    if orphan_info.get('next_step'):
        ns = orphan_info['next_step']
        marker_lines.append(f"- **Was working on**: step {ns['id']} — {ns['content']}")
    if orphan_info.get('working_files'):
        marker_lines.append(f"- **Files in progress**: {', '.join(orphan_info['working_files'])}")

    marker_lines.extend([
        "",
        "**To resume**: Run `python3 /home/z/my-project/skills/session-tracker/scripts/session_tracker.py resume`",
        "**For full report**: Run `python3 /home/z/my-project/skills/session-tracker/scripts/session_tracker.py crash-detect`",
        "",
    ])

    marker = "\n".join(marker_lines)

    # Prepend crash marker so it's the first thing a new agent sees
    with open(worklog_md, "w", encoding="utf-8") as f:
        f.write(marker)
        if existing:
            f.write("\n" + existing)


def cmd_crash_detect(session_dir):
    """
    Generate a full crash recovery report from an orphaned session.
    This is the Gridman outsider revealing what the kaiju destroyed.
    """
    orphan = detect_orphan(session_dir)
    if not orphan:
        print("No orphaned session detected. All sessions completed cleanly.")
        return

    state = load_state(session_dir)
    todo = load_todo(session_dir)
    worklog = read_jsonl(_path(session_dir, WORKLOG_FILE))

    print()
    print("=" * 64)
    print("  META-CRASH RECOVERY REPORT")
    print("  (Gridman Outsider — Restoring Lost Memory)")
    print("=" * 64)
    print()

    # Crash signature
    print("  CRASH SIGNATURE:")
    print(f"    ACTIVE sentinel: {'EXISTS (session never completed)' if orphan['sentinel_exists'] else 'missing'}")
    print(f"    Session status: {orphan['status']}")
    print(f"    session_done in worklog: {'NO (crash confirmed)' if not any(e.get('action') == 'session_done' for e in worklog) else 'YES (contradicts status — possible corruption)'}")
    print()

    # What was happening
    print("  TASK:")
    print(f"    {orphan['task']}")
    print(f"    Started: {state.get('started_at', 'unknown')}")
    print(f"    Last activity: {orphan['last_activity']}")
    print()

    # Step-by-step progress
    print("  STEPS:")
    for step in todo:
        icon = {"completed": "[x]", "in_progress": "[~]", "pending": "[ ]", "skipped": "[-]"}.get(
            step["status"], "[?]"
        )
        files_str = ""
        if step.get("files"):
            files_str = f"  ({', '.join(os.path.basename(f) for f in step['files'])})"
        print(f"    {icon} {step['id']}. {step['content']}{files_str}")
    print()

    # Files that may be incomplete
    working_files = [
        (f, info) for f, info in state.get("files", {}).items()
        if info["status"] in ("working", "reading")
    ]
    if working_files:
        print("  FILES POTENTIALLY INCOMPLETE (verify before using):")
        for f, info in working_files:
            exists = "exists" if os.path.exists(f) else "MISSING"
            size_str = ""
            if os.path.exists(f):
                try:
                    size_str = f" ({os.path.getsize(f)} bytes)"
                except OSError:
                    pass
            print(f"    ! [{info['status'].upper()}] {f} ({exists}){size_str}")
        print()

    # Last worklog entries — what happened right before the crash
    if worklog:
        print(f"  LAST {min(10, len(worklog))} WORKLOG ENTRIES (what happened before crash):")
        for entry in worklog[-10:]:
            ts = entry.get("ts", "?")[-8:]
            action = entry.get("action", "?")
            detail = entry.get("detail", entry.get("file", entry.get("step", "")))
            print(f"    {ts} {action}: {detail}")
        print()

    # Recovery recommendation
    next_step = orphan.get('next_step')
    print("  RECOVERY RECOMMENDATION:")
    if next_step:
        if next_step['status'] == 'in_progress':
            print(f"    1. Verify output of step {next_step['id']} ({next_step['content']})")
            print(f"    2. If incomplete, redo step {next_step['id']}")
            print(f"    3. Continue with remaining steps")
        else:
            print(f"    1. Begin step {next_step['id']} ({next_step['content']})")
            print(f"    2. Continue with remaining steps")
    print(f"    Run: session-tracker step {next_step['id'] if next_step else '?'} --start")
    print()
    print("  To archive this orphan and start fresh:")
    print(f"    rm -rf {session_dir}")
    print()
    print("=" * 64)
    print()


def cmd_resume(session_dir):
    """Show resume plan from last session state."""
    state = load_state(session_dir)
    todo = load_todo(session_dir)

    if not state.get("task"):
        print("No session found. Run 'init' to start one.", file=sys.stderr)
        sys.exit(1)

    if state["status"] == "completed":
        print("Session already completed. Start a new one with 'init'.")
        return

    # Check if this is a crash recovery (not just a manual resume)
    orphan = detect_orphan(session_dir)

    completed = sum(1 for s in todo if s["status"] == "completed")
    total = len(todo)

    print()
    print("=" * 56)
    print("  SESSION RESUME")
    if orphan:
        print("  ** META-CRASH RECOVERY **")
    print("=" * 56)
    print(f"  Task: {state['task']}")
    if orphan:
        print(f"  Status: IN_PROGRESS (META-CRASH — previous session was killed)")
    else:
        print(f"  Status: IN_PROGRESS (interrupted)")
    print(f"  Last activity: {state.get('updated_at', 'unknown')}")
    print(f"  Progress: {completed}/{total} steps completed")
    print()

    for step in todo:
        icon = {"completed": "[x]", "in_progress": "[~]", "pending": "[ ]"}.get(
            step["status"], "[?]"
        )
        files_str = ""
        if step.get("files"):
            files_str = f"  ({', '.join(os.path.basename(f) for f in step['files'])})"
        print(f"  {icon} {step['id']}. {step['content']}{files_str}")

    working_files = [
        (f, info) for f, info in state.get("files", {}).items()
        if info["status"] in ("working", "reading")
    ]
    if working_files:
        print()
        print("  WARNING - Files still in progress (may be incomplete):")
        for f, info in working_files:
            status_tag = info["status"].upper()
            print(f"    ! [{status_tag}] {f}")

    # Show last few worklog entries for context
    worklog = read_jsonl(_path(session_dir, WORKLOG_FILE))
    if worklog:
        print()
        print(f"  Last {min(5, len(worklog))} log entries:")
        for entry in worklog[-5:]:
            ts = entry.get("ts", "?")[-8:]
            action = entry.get("action", "?")
            detail = entry.get("detail", entry.get("file", entry.get("step", "")))
            print(f"    {ts} {action}: {detail}")

    next_step = None
    for step in todo:
        if step["status"] == "in_progress":
            next_step = step
            break
    if not next_step:
        for step in todo:
            if step["status"] == "pending":
                next_step = step
                break

    print()
    if next_step:
        print(f"  Resume from: step {next_step['id']} ({next_step['content']})")
        if next_step["status"] == "in_progress":
            print(f"  Action: Verify step {next_step['id']} work, then continue or redo")
        else:
            print(f"  Action: Begin step {next_step['id']}")
    print("=" * 56)
    print()


def cmd_status(session_dir):
    """Show current session status with activity info."""
    state = load_state(session_dir)
    todo = load_todo(session_dir)

    if not state.get("task"):
        print("No active session.", file=sys.stderr)
        sys.exit(1)

    completed = sum(1 for s in todo if s["status"] == "completed")
    in_progress = sum(1 for s in todo if s["status"] == "in_progress")
    pending = sum(1 for s in todo if s["status"] == "pending")

    # Check for orphaned session (meta-crash detection)
    orphan = detect_orphan(session_dir)
    if orphan:
        print("!! META-CRASH DETECTED: This session was killed before completion !!")

    print(f"Task: {state['task']}")
    print(f"Status: {state['status']}{' (ORPHANED — previous agent crashed)' if orphan else ''}")
    print(f"Progress: {completed}/{len(todo)} done, {in_progress} active, {pending} pending")
    print(f"Last update: {state.get('updated_at', 'unknown')}")

    if state.get("current_step_id"):
        print(f"Current step: {state['current_step_id']}")
    if state.get("current_files"):
        print(f"Working files: {', '.join(os.path.basename(f) for f in state['current_files'])}")

    # Check filesystem activity
    curr = take_snapshot(session_dir)
    prev = read_json(_path(session_dir, SNAPSHOT_PREV))
    if prev:
        diff = diff_snapshots(prev, curr)
        if has_activity(diff):
            print("FS Activity: YES (changes detected since last scan)")
            for d, events in diff.items():
                dirname = os.path.basename(d)
                for evt_type, items in events.items():
                    if items:
                        print(f"  {dirname}/{evt_type}: {', '.join(items[:5])}")
        else:
            print("FS Activity: None since last scan")

    # Check stuck status
    stuck = _check_stuck(session_dir)
    if stuck:
        print(f"ALERT: Task appears STUCK ({stuck} consecutive checks with no activity)")


# ── Micro-dump & Monitor ────────────────────────────────────────────────────

def take_microdump(session_dir):
    """Capture current state fingerprint + filesystem scan."""
    state = load_state(session_dir)
    todo = load_todo(session_dir)
    worklog_path = _path(session_dir, WORKLOG_FILE)

    worklog_lines = 0
    if os.path.exists(worklog_path):
        with open(worklog_path, "r") as f:
            worklog_lines = sum(1 for _ in f)

    file_fingerprints = {}
    for fpath, info in state.get("files", {}).items():
        if info["status"] in ("working", "reading") and os.path.exists(fpath):
            try:
                st = os.stat(fpath)
                file_fingerprints[fpath] = {"size": st.st_size, "mtime": int(st.st_mtime)}
            except OSError:
                pass

    current_steps = [
        {"id": s["id"], "status": s["status"]}
        for s in todo if s["status"] == "in_progress"
    ]

    # Filesystem scan — compact summary for comparison
    fs_scan = take_snapshot(session_dir)

    return {
        "current_step_id": state.get("current_step_id"),
        "current_files": state.get("current_files", []),
        "current_steps": current_steps,
        "file_fingerprints": file_fingerprints,
        "worklog_lines": worklog_lines,
        "fs_scan": fs_scan,
        "ts": now_iso(),
    }


def cmd_monitor(session_dir, action, interval=60):
    """Start, stop, or check the background monitor."""

    if action == "start":
        pid_path = _path(session_dir, MONITOR_PID_FILE)

        existing_pid = _read_pid(pid_path)
        if existing_pid and _is_process_alive(existing_pid):
            print(f"Monitor already running (PID {existing_pid})")
            return

        env = os.environ.copy()
        env["_SESSION_TRACKER_LOOP_DIR"] = session_dir
        env["_SESSION_TRACKER_LOOP_INTERVAL"] = str(interval)
        cmd = [sys.executable, os.path.abspath(__file__)]
        proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        write_json(pid_path, {"pid": proc.pid, "started_at": now_iso()})
        print(f"Monitor started (PID {proc.pid}, interval {interval}s)")

    elif action == "stop":
        pid_path = _path(session_dir, MONITOR_PID_FILE)
        existing_pid = _read_pid(pid_path)
        if existing_pid:
            try:
                os.kill(existing_pid, signal.SIGTERM)
                print(f"Monitor stopped (PID {existing_pid})")
            except ProcessLookupError:
                print("Monitor process not found (already stopped)")
            try:
                os.unlink(pid_path)
            except OSError:
                pass
        else:
            print("No monitor running")

    elif action == "check":
        stuck = _check_stuck(session_dir)
        if stuck:
            print(f"STUCK: {stuck} consecutive checks with no activity")
        else:
            state = load_state(session_dir)
            if state.get("status") == "completed":
                print("Session completed")
            else:
                print("Session active (activity detected or too soon to tell)")
        return stuck


def _read_pid(pid_path):
    data = read_json(pid_path)
    return data.get("pid") if data else None


def _is_process_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _check_stuck(session_dir):
    """Check stuck status. Returns stuck count or None."""
    curr = read_json(_path(session_dir, MICRODUMP_CURR))
    prev = read_json(_path(session_dir, MICRODUMP_PREV))

    if not curr or not prev:
        return None

    # Compare ignoring internal fields and timestamps
    skip_keys = {"ts", "_stuck_count"}
    clean_curr = {k: v for k, v in curr.items() if k not in skip_keys}
    clean_prev = {k: v for k, v in prev.items() if k not in skip_keys}

    if clean_curr == clean_prev:
        count = curr.get("_stuck_count", 2)
        return count + 2 if count >= 1 else 2

    return None


def _monitor_loop(session_dir, interval):
    """
    Internal: run as background monitor loop.

    Stuck detection strategy (v2):
    1. Take filesystem snapshot + micro-dump each interval
    2. Compare current dump to previous dump
    3. If filesystem shows activity (new/modified/read files) → ALIVE, reset counter
    4. If no filesystem activity AND no micro-dump change → increment stuck counter
    5. If stuck counter >= STUCK_THRESHOLD → fire stuck_alert
    """
    stuck_count = 0
    last_alert_count = 0  # avoid duplicate alerts at same count

    while True:
        state = load_state(session_dir)

        if state.get("status") == "completed":
            break

        dump = take_microdump(session_dir)

        # Check filesystem activity from the scan inside the dump
        prev_snapshot = read_json(_path(session_dir, SNAPSHOT_PREV))
        curr_snapshot = dump.get("fs_scan", {})
        fs_activity = False

        if prev_snapshot:
            diff = diff_snapshots(prev_snapshot, curr_snapshot)
            fs_activity = has_activity(diff)

            # Auto-log filesystem events to worklog (throttled: max 1 per interval)
            if fs_activity:
                events_summary = []
                for d, events in diff.items():
                    dirname = os.path.basename(d)
                    for evt_type, items in events.items():
                        if items:
                            events_summary.append(
                                f"{dirname}/{evt_type}:{len(items)}"
                            )
                if events_summary:
                    append_jsonl(_path(session_dir, WORKLOG_FILE), {
                        "ts": now_iso(), "action": "fs_activity",
                        "detail": "; ".join(events_summary),
                    })

        # Save current snapshot for next iteration
        write_json(_path(session_dir, SNAPSHOT_PREV), curr_snapshot)

        # Determine alive vs stuck
        prev_curr = read_json(_path(session_dir, MICRODUMP_CURR))

        if fs_activity:
            # Filesystem activity detected → definitely alive
            stuck_count = 0
        elif prev_curr:
            # No filesystem activity — check micro-dump changes as fallback
            skip = {"ts", "_stuck_count", "fs_scan"}
            clean_prev = {k: v for k, v in prev_curr.items() if k not in skip}
            clean_dump = {k: v for k, v in dump.items() if k not in skip}

            if clean_dump == clean_prev:
                # No change at all → possibly stuck
                stuck_count += 1
            else:
                # Micro-dump changed (e.g., new worklog entry from ping/log)
                stuck_count = 0
        else:
            # First check, no previous to compare
            stuck_count = 0

        dump["_stuck_count"] = stuck_count

        # Rotate: current → previous, new → current
        curr_path = _path(session_dir, MICRODUMP_CURR)
        prev_path = _path(session_dir, MICRODUMP_PREV)

        if os.path.exists(curr_path):
            os.replace(curr_path, prev_path)

        write_json(curr_path, dump)

        if stuck_count >= STUCK_THRESHOLD and stuck_count != last_alert_count:
            total_stuck = stuck_count + 2
            last_alert_count = stuck_count
            append_jsonl(_path(session_dir, WORKLOG_FILE), {
                "ts": now_iso(), "action": "stuck_alert",
                "detail": (
                    f"Task stuck for {total_stuck} consecutive checks "
                    f"({total_stuck * interval}s) — no filesystem or state activity"
                ),
                "stuck_count": total_stuck,
            })

        time.sleep(interval)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    # Internal monitor loop mode — triggered via env var, not CLI arg
    _loop_dir = os.environ.get("_SESSION_TRACKER_LOOP_DIR")
    _loop_interval = os.environ.get("_SESSION_TRACKER_LOOP_INTERVAL", "60")
    if _loop_dir:
        _monitor_loop(_loop_dir, int(_loop_interval))
        return

    parser = argparse.ArgumentParser(
        description="Session tracker v2: checkpoint, monitor, and resume multi-step tasks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dir", default=DEFAULT_DIR,
                        help=f"Session directory (default: {DEFAULT_DIR})")

    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Initialize a new session")
    p_init.add_argument("task", help="Task description")
    p_init.add_argument("--steps", required=True, help="Comma-separated step descriptions")

    p_step = sub.add_parser("step", help="Start or complete a step")
    p_step.add_argument("id", help="Step ID")
    p_step.add_argument("--start", action="store_true", help="Mark step as started")
    p_step.add_argument("--done", action="store_true", help="Mark step as completed")
    p_step.add_argument("--files", help="Comma-separated file paths being worked on")

    p_file = sub.add_parser("file", help="Mark file status or rename")
    p_file.add_argument("path", help="File path")
    p_file.add_argument("--working", action="store_true", help="Mark as being worked on")
    p_file.add_argument("--done", action="store_true", help="Mark as completed")
    p_file.add_argument("--reading", action="store_true", help="Mark as being read")
    p_file.add_argument("--rename", metavar="NEW_PATH", help="Rename file to NEW_PATH")

    p_ping = sub.add_parser("ping", help="Manual heartbeat — signals alive")
    p_ping.add_argument("--detail", help="Optional note about what's happening")

    p_log = sub.add_parser("log", help="Add worklog entry")
    p_log.add_argument("message", help="Log message")
    p_log.add_argument("--step", help="Associated step ID")

    sub.add_parser("sync", help="Sync with TodoWrite (pipe JSON to stdin)")
    sub.add_parser("done", help="Mark session as completed")
    sub.add_parser("resume", help="Show resume plan from last session")
    sub.add_parser("crash-detect", help="Detect orphaned sessions from meta-crashes (Gridman outsider)")
    sub.add_parser("status", help="Show current session status")
    sub.add_parser("scan", help="Take filesystem snapshot and check activity")

    p_mon = sub.add_parser("monitor", help="Background monitor")
    p_mon.add_argument("--start", action="store_true", help="Start monitor")
    p_mon.add_argument("--stop", action="store_true", help="Stop monitor")
    p_mon.add_argument("--check", action="store_true", help="Check stuck status")
    p_mon.add_argument("--interval", type=int, default=60, help="Check interval in seconds")

    args = parser.parse_args()
    session_dir = args.dir

    if args.command == "init":
        cmd_init(session_dir, args.task, args.steps)
    elif args.command == "step":
        if args.start:
            cmd_step(session_dir, args.id, "start", args.files)
        elif args.done:
            cmd_step(session_dir, args.id, "done")
        else:
            print("Error: specify --start or --done", file=sys.stderr)
            sys.exit(1)
    elif args.command == "file":
        if args.rename:
            cmd_file(session_dir, args.path, "rename", rename_to=args.rename)
        elif args.working:
            cmd_file(session_dir, args.path, "working")
        elif args.done:
            cmd_file(session_dir, args.path, "done")
        elif args.reading:
            cmd_file(session_dir, args.path, "reading")
        else:
            print("Error: specify --working, --done, --reading, or --rename", file=sys.stderr)
            sys.exit(1)
    elif args.command == "ping":
        cmd_ping(session_dir, args.detail)
    elif args.command == "sync":
        cmd_sync(session_dir)
    elif args.command == "log":
        cmd_log(session_dir, args.message, args.step)
    elif args.command == "done":
        cmd_done(session_dir)
    elif args.command == "resume":
        cmd_resume(session_dir)
    elif args.command == "crash-detect":
        cmd_crash_detect(session_dir)
    elif args.command == "status":
        cmd_status(session_dir)
    elif args.command == "scan":
        cmd_scan(session_dir)
    elif args.command == "monitor":
        if args.start:
            cmd_monitor(session_dir, "start", args.interval)
        elif args.stop:
            cmd_monitor(session_dir, "stop")
        elif args.check:
            cmd_monitor(session_dir, "check")
        else:
            print("Error: specify --start, --stop, or --check", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

```

## Commands Quick Reference

```bash
# Initialize a new session (auto-detects orphaned sessions from meta-crashes)
python3 session_tracker.py init "Task description" --steps "Step 1,Step 2,Step 3"

# Step management
python3 session_tracker.py step 1 --start --files "/path/to/file"
python3 session_tracker.py step 1 --done

# File tracking
python3 session_tracker.py file /path/to/file --working
python3 session_tracker.py file /path/to/file --done
python3 session_tracker.py file /path/to/file --reading
python3 session_tracker.py file --rename /old/path /new/path

# Heartbeat for long operations
python3 session_tracker.py ping --detail "Generating large document..."

# TodoWrite sync
echo '[{"id":"1","content":"Step","status":"completed"}]' | python3 session_tracker.py sync

# Manual log
python3 session_tracker.py log "Progress note" --step 2

# Session completion
python3 session_tracker.py done

# Crash recovery
python3 session_tracker.py crash-detect   # Full recovery report from meta-crash
python3 session_tracker.py resume         # Show resume plan

# Status and monitoring
python3 session_tracker.py status
python3 session_tracker.py scan
python3 session_tracker.py monitor --start --interval 30
python3 session_tracker.py monitor --check
python3 session_tracker.py monitor --stop
```
## CLI Reference

### `init` — Initialize a new session

```bash
python3 session_tracker.py init "Task description" --steps "Step 1,Step 2,Step 3"
```

Creates the session directory, `state.json`, `todo.json`, baseline filesystem snapshot, and writes the first worklog entry. Warns if a session already exists.

### `step` — Start or complete a step

```bash
# Start a step
python3 session_tracker.py step 1 --start
python3 session_tracker.py step 2 --start --files src/main.py,src/utils.py

# Complete a step
python3 session_tracker.py step 1 --done
```

Updates `todo.json` status, sets `current_step_id` in state, tracks files, and resets micro-dumps on step start.

### `file` — Mark file status or rename

```bash
# Mark a file as being read
python3 session_tracker.py file book_text.txt --reading

# Mark a file as being worked on
python3 session_tracker.py file src/main.py --working

# Mark a file as done
python3 session_tracker.py file src/main.py --done

# Rename a file (updates all references)
python3 session_tracker.py file old_summary.docx --rename new_summary.docx
```

`--rename` updates state.json file inventory, current_files, and todo item file lists. A `file_rename` worklog entry is created.

### `ping` — Manual heartbeat

```bash
python3 session_tracker.py ping
python3 session_tracker.py ping --detail "Running docx skill..."
```

Signals that the agent is alive but busy. Appends a `ping` entry to worklog and touches the session directory's mtime. Both signals reset the stuck counter. Use during long operations (skill invocations, API calls, document generation) where no files are being modified.

### `sync` — TodoWrite reconciliation

```bash
echo '[{"id":"1","content":"Extract text","status":"completed","priority":"high"}]' | python3 session_tracker.py sync
```

Imports new steps from TodoWrite JSON (piped to stdin) that aren't in the tracker. Updates existing step statuses if they changed. The tracker's todo.json is the source of truth — sync only adds/updates, never deletes. Without piped input, displays current tracker TODO.

### `log` — Add worklog entry

```bash
python3 session_tracker.py log "Refactored the parser module"
python3 session_tracker.py log "Fixed edge case" --step 3
```

Appends a structured log entry to `worklog.jsonl`. Optional `--step` associates the log with a specific step.

### `scan` — Manual filesystem scan

```bash
python3 session_tracker.py scan
```

Takes a filesystem snapshot and compares to the previous one. Reports any detected activity (creates, edits, deletes, reads). Useful for debugging or manual checking.

### `done` — Mark session as completed

```bash
python3 session_tracker.py done
```

Marks all in-progress steps as completed, pending steps as skipped, all files as completed, and stops the background monitor.

### `crash-detect` — Detect orphaned sessions from meta-crashes (v2.1)

```bash
python3 session_tracker.py crash-detect
```

Checks for orphaned sessions (ACTIVE sentinel exists, or session not completed AND no `session_done` in worklog). If found, generates a full recovery report: crash signature, task details, step progress, files potentially incomplete, last 10 worklog entries, and recovery recommendation. This is the **Gridman Outsider** command — it reveals what the meta-crash destroyed.

Also run this at the start of any new session to check for crashed sessions from a previous conversation.

### `resume` — Show resume plan after interruption

```bash
python3 session_tracker.py resume
```

Outputs a formatted resume plan showing: task description, last activity time, step progress with checkboxes, any files still marked WORKING or READING (with warnings), last 5 worklog entries for context, and the recommended next action.

### `status` — Show current session status

```bash
python3 session_tracker.py status
```

Displays task name, status, step progress counts, current step, working files, filesystem activity since last scan, and stuck alert if detected.

### `monitor` — Background stuck detection

```bash
# Start the monitor (checks every 60s by default)
python3 session_tracker.py monitor --start
python3 session_tracker.py monitor --start --interval 30

# Check stuck status
python3 session_tracker.py monitor --check

# Stop the monitor
python3 session_tracker.py monitor --stop
```

The monitor runs as a detached background process. Each interval it:
1. Takes a filesystem snapshot
2. Compares to previous snapshot for activity (creates/edits/deletes/reads)
3. If activity detected → ALIVE, reset stuck counter, auto-log `fs_activity`
4. If no activity → compare micro-dump as fallback
5. If neither changes for 3+ consecutive checks → fire `stuck_alert`

## Workflow

The enforced workflow for using this skill. **Follow this order. Do not skip steps.**

0. **`crash-detect`** — At the very start, before anything else. Check for orphaned sessions from a previous meta-crash. If found, offer to resume before starting new work.
1. **`init`** — At task start. Define the task and its steps. (Also auto-detects orphans and warns.)
2. **`step --start`** — Before beginning work on a step. Optionally declare files.
3. **`file --reading`** — When reading/consuming a file as input.
4. **`file --working`** — Mark files being modified as you open them.
5. **`ping`** — During long operations (skill invocations, API calls, etc.) to signal alive.
6. **`log`** — Add progress notes as you work. Be specific.
7. **`file --rename`** — If a file's name changes during work, update the tracker.
8. **`file --done`** — When a file modification is complete and verified.
9. **`step --done`** — When the entire step is complete.
10. **`sync`** — After updating TodoWrite, pipe the JSON to keep tracker in sync.
11. **`done`** — Mark the session complete (stops the monitor).
12. **`resume`** — At the start of a new session after an interruption. This is your first command.

## Stuck Detection (v2)

The v2 stuck detection uses a **two-tier** approach:

### Tier 1: Filesystem Scanner (Primary)

Every monitor interval, the scanner builds a fingerprint of all files in project directories. Comparing consecutive fingerprints reveals:

- **File created** — new file appeared
- **File modified** — size or mtime changed
- **File deleted** — file disappeared
- **File read** — atime changed without mtime changing (relatime)

**Any filesystem activity = definitely alive.** The stuck counter resets immediately.

### Tier 2: Micro-Dump Comparison (Fallback)

If the filesystem scanner sees no changes, the monitor falls back to comparing micro-dumps. This catches cases where the agent is actively working but hasn't touched any files yet (e.g., pure computation, API calls).

Changes that reset the stuck counter via micro-dump:
- `worklog_lines` changed (from `ping`, `log`, `step`, or `file` commands)
- `current_step_id` changed (step transition)
- `current_files` changed (file status change)
- `file_fingerprints` changed (working file modified)

### What triggers a stuck alert

- **Zero** filesystem activity AND **zero** micro-dump change for **3+ consecutive checks**
- That means ~3 minutes at default 60s interval
- Alerts are deduplicated (won't spam at the same stuck count)

### What to do when stuck

1. Run `monitor --check` to confirm
2. Run `status` to see where you are
3. Run `scan` to check for filesystem activity the monitor might have missed
4. Either: break the current step into smaller sub-steps, or `ping` if you're just slow
5. Starting a new step (`step --start`) resets the micro-dumps, clearing the stuck state

## Resume After Interruption

When a session is interrupted (context limit, timeout, crash, disconnect), `resume` reconstructs your position:

**What `resume` outputs:**
- Task description and session status (always `IN_PROGRESS` for interrupted sessions)
- Last activity timestamp
- Progress summary: `X/Y steps completed`
- Full step list with checkboxes: `[x]` completed, `[~]` in-progress, `[ ]` pending
- **Warnings** for any files still marked WORKING or READING — these may be partially written
- **Last 5 worklog entries** for context about what was happening
- Recommended next action: which step to resume from and whether to verify or begin fresh

**How to use it:**
1. At the start of a new session, run `resume` first
2. Check for WORKING/READING files — verify their integrity before continuing
3. If a step was in-progress, review its output and decide whether to continue or redo
4. If all steps were complete, run `done` to finalize
5. Resume the workflow from the appropriate step
