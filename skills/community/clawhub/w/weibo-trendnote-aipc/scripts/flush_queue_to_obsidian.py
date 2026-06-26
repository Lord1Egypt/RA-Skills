#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
flush_queue_to_obsidian.py - Flush queued summaries to Obsidian via notesmd-cli.

Called by skill_runner.py, which optionally loads env.ps1 first.
Environment variables such as NOTESMD_BIN and OBSIDIAN_VAULT may come from env.ps1 or existing process env.

Exit codes:  0 = Success,  1 = Error
"""

import json, os, subprocess, sys, io
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

STATE_DIR   = r"C:\Users\Intel\.openclaw\state\weibo_hot"
QUEUE_JSONL = os.path.join(STATE_DIR, "queue.jsonl")
QUEUE_DONE  = os.path.join(STATE_DIR, "queue.done.jsonl")
WRITTEN_IDS = os.path.join(STATE_DIR, "written_ids.json")
LAST_FLUSH  = os.path.join(STATE_DIR, "last_flush.txt")

NOTESMD_BIN = os.environ.get("NOTESMD_BIN", r"C:\Users\Intel\scoop\shims\notesmd-cli.exe")
VAULT_NAME  = os.environ.get("OBSIDIAN_VAULT", "test")
NOTE_PATH   = os.environ.get("OBSIDIAN_NOTE_PATH", r"Inbox\Weibo Hot.md")
WRITE_MODE  = os.environ.get("OBSIDIAN_WRITE_MODE", "append_to_file")
CST = timezone(timedelta(hours=8))


def ensure_notesmd_config():
    """Ensure notesmd-cli config directory exists.

    notesmd-cli uses Go's os.UserConfigDir() which on Windows looks at %APPDATA%.
    Under NSSM SYSTEM, APPDATA may not be set or point to a non-existent dir.
    We force APPDATA and create the notesmd-cli config dir if needed.
    """
    appdata = r"C:\Users\Intel\AppData\Roaming"
    os.environ["APPDATA"] = appdata
    os.environ["USERPROFILE"] = r"C:\Users\Intel"
    os.environ["HOME"] = r"C:\Users\Intel"

    config_dir = os.path.join(appdata, "notesmd-cli")
    os.makedirs(config_dir, exist_ok=True)

    # If no config file exists, create a minimal one with the default vault
    config_file = os.path.join(config_dir, "config.yaml")
    if not os.path.isfile(config_file):
        print(f"[notesmd] Creating default config at {config_file}")
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(f"defaultVault: {VAULT_NAME}\n")


def load_written_ids():
    try:
        with open(WRITTEN_IDS, "r", encoding="utf-8") as f: return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError): return set()


def save_written_ids(ids):
    tmp = WRITTEN_IDS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: json.dump(sorted(ids), f)
    safe_replace(tmp, WRITTEN_IDS)


def safe_replace(src, dst):
    if os.path.exists(dst):
        bak = dst + ".bak"
        try:
            if os.path.exists(bak): os.remove(bak)
            os.rename(dst, bak)
        except OSError: os.remove(dst)
    os.rename(src, dst)


def read_queue():
    if not os.path.isfile(QUEUE_JSONL): return []
    records = []
    with open(QUEUE_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try: records.append(json.loads(line))
                except json.JSONDecodeError: pass
    return records


def get_markdown(record):
    if record.get("md"): return record["md"]
    p = record.get("md_path", "")
    if p and os.path.isfile(p):
        with open(p, "r", encoding="utf-8") as f: return f.read()
    return None


def write_to_obsidian(content):
    note = datetime.now(CST).strftime("%Y-%m-%d") + ".md" if WRITE_MODE == "daily_append" else NOTE_PATH
    cmd = [NOTESMD_BIN, "create", note, "--content", content, "--append"]
    if VAULT_NAME: cmd.extend(["--vault", VAULT_NAME])

    # Build env with APPDATA set for notesmd-cli
    env = os.environ.copy()
    env["APPDATA"] = r"C:\Users\Intel\AppData\Roaming"
    env["USERPROFILE"] = r"C:\Users\Intel"
    env["HOME"] = r"C:\Users\Intel"

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                           encoding="utf-8", errors="replace", env=env)
        if r.returncode != 0:
            print(f"[notesmd] CLI error (code {r.returncode}): {(r.stderr or '')[:500]}", file=sys.stderr)
            if r.stdout: print(f"[notesmd] stdout: {r.stdout[:500]}", file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[notesmd] Timed out", file=sys.stderr); return False
    except FileNotFoundError:
        print(f"[notesmd] Not found: {NOTESMD_BIN}", file=sys.stderr); return False
    except Exception as e:
        print(f"[notesmd] Error: {e}", file=sys.stderr); return False


def write_atomic(path, content):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: f.write(content)
    safe_replace(tmp, path)


def main():
    os.makedirs(STATE_DIR, exist_ok=True)

    # Ensure notesmd-cli config exists before any calls
    ensure_notesmd_config()

    print(f"[config] NOTESMD={NOTESMD_BIN} VAULT={VAULT_NAME} NOTE={NOTE_PATH}")

    records = read_queue()
    if not records: print("[flush] Queue empty."); return

    written_ids = load_written_ids()
    pending = [r for r in records if r.get("id") not in written_ids]
    if not pending: print(f"[flush] All {len(records)} already written."); return

    print(f"[flush] {len(pending)} pending...")
    ok, fail, done = 0, 0, []

    for rec in pending:
        rid, title = rec.get("id", "?"), rec.get("title", "untitled")
        print(f"  Writing: {title} ({rid})...")
        md = get_markdown(rec)
        if not md: fail += 1; print("  [skip] No content.", file=sys.stderr); continue
        if write_to_obsidian("\n\n---\n\n" + md):
            written_ids.add(rid); done.append(rec); ok += 1; print("  [ok]")
        else:
            fail += 1; print("  [fail]")

    save_written_ids(written_ids)
    if done:
        with open(QUEUE_DONE, "a", encoding="utf-8") as f:
            for r in done: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    remaining = [r for r in records if r.get("id") not in written_ids]
    tmp = QUEUE_JSONL + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in remaining: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    safe_replace(tmp, QUEUE_JSONL)

    write_atomic(LAST_FLUSH, datetime.now(CST).isoformat())
    print(f"[flush] Done. ok={ok} fail={fail} remaining={len(remaining)}")


if __name__ == "__main__":
    try: main()
    except Exception as e: print(f"[error] {e}", file=sys.stderr); sys.exit(1)
