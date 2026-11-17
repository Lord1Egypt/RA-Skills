#!/usr/bin/env python3
"""
savemaintenance — One-shot memory system reconciliation pipeline.

Usage:
  python3 full-reconcile.py          # Full run: backup → reconcile → rebuild → audit
  python3 full-reconcile.py --dry    # Dry run: show what would change, don't write
  python3 full-reconcile.py --step log   # Run a single step

Steps (run consecutively in full mode):
  1. backup    — Snapshot conversation-log.md to backup dir
  2. reconcile — Cross-reference log ↔ disk, add orphans, remove dead entries
  3. rebuild   — Rebuild FTS5 index + stub-index.md
  4. audit     — Run full audit, report findings

Paths:
  - Saved conversations: ~/.openclaw/workspace/saved/
  - Conversation log:    ~/.openclaw/workspace/saved/conversation-log.md
  - Memory index:        /dev/shm/memory-index.db
  - Backup dir:          ~/.openclaw/workspace/savemaintenance/backups/
"""

import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Configuration ─────────────────────────────────────────
WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace")).resolve()
SAVED_DIR = Path(os.path.expanduser("~/.openclaw/workspace/saved"))
PROJECT_DIR = Path(os.path.expanduser("~/.openclaw/workspace/savemaintenance"))
BACKUP_DIR = PROJECT_DIR / "backups"
FTS5_DB = Path("/dev/shm/memory-index.db")
STUB_PATH = WORKSPACE / "stub-index.md"
TOPIC_PATH = SAVED_DIR / "topic-index.json"
CONV_LOG = SAVED_DIR / "conversation-log.md"
INDEX_SCRIPT = SAVED_DIR / "memory-index.py"
AUDIT_SCRIPT = MEMORY_DIR / "memory-audit.py"

# Exclude from reconciliation
IGNORE_FILES = {"conversation-log.md", "conversation-log-footer.md", "stub-index.md"}

# ── Helpers ────────────────────────────────────────────────

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")

def log(msg):
    print(f"  [{timestamp()}] {msg}")

def extract_desc(fpath, fname):
    """Generate a human-readable description from a markdown file."""
    try:
        content = fpath.read_text(errors='replace')
        for cl in content.split('\n'):
            cl = cl.strip()
            if cl.startswith('# ') and len(cl) > 3:
                return cl[2:].strip()
        for cl in content.split('\n'):
            cl = cl.strip()
            if cl.startswith('## ') and len(cl) > 4:
                return cl[3:].strip()
        # First substantial line
        for cl in content.split('\n'):
            cl = cl.strip()
            if cl and not cl.startswith('**') and not cl.startswith('---') and len(cl) > 10:
                return cl[:80].strip()
    except:
        pass
    # Filename fallback
    stem = fname.replace('.md', '')
    stem = re.sub(r'^20\d{2}-\d{2}-\d{2}[-_]?', '', stem)
    stem = re.sub(r'[-_]', ' ', stem)
    stem = re.sub(r'\s+', ' ', stem).strip()
    return stem[:80] if stem else fname

def extract_date(fname):
    """Extract YYYY-MM-DD from filename or file mtime."""
    dm = re.search(r'(20\d{2}-\d{2}-\d{2})', fname)
    if dm:
        return dm.group(1)
    fpath = SAVED_DIR / fname
    if fpath.exists():
        return datetime.fromtimestamp(fpath.stat().st_mtime).strftime('%Y-%m-%d')
    return "1970-01-01"


# ── Steps ──────────────────────────────────────────────────

def step_backup(dry_run=False):
    """Backup conversation-log.md and topic-index.json."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    
    for label, src in [("conversation-log", CONV_LOG), ("topic-index", TOPIC_PATH)]:
        if src.exists():
            dst = BACKUP_DIR / f"{label}_{ts}.md"
            if not dry_run:
                shutil.copy2(src, dst)
                log(f"Backed up {label} → {dst}")
            else:
                log(f"[DRY] Would backup {label} → {dst}")
    
    log("Backup complete ✓")


def step_reconcile(dry_run=False):
    """Cross-reference conversation-log.md against files on disk.
    
    1. Parse current log entries
    2. Remove entries for files that no longer exist
    3. Add entries for orphan files not in the log
    4. Sort by date descending
    5. Update entry count in header
    """
    log("Reconciling conversation-log.md...")
    
    # Parse current log
    text = CONV_LOG.read_text() if CONV_LOG.exists() else "# Conversation Log\n_0 conversations_\n"
    lines = text.split("\n")
    
    header = []
    entries = []
    in_header = True
    for line in lines:
        m = re.match(r'-\s+\*\*(\d{4}-\d{2}-\d{2})\*\*\s+(.+?):\s*(.*)', line)
        if m and in_header:
            in_header = False
        if in_header:
            header.append(line)
        elif m:
            entries.append((m.group(1), m.group(2).strip(), m.group(3)))
    
    log(f"  Parsed {len(entries)} entries from log")
    
    # Files on disk
    disk_files = {}
    if SAVED_DIR.exists():
        for f in SAVED_DIR.iterdir():
            if f.is_file() and f.name.endswith('.md') and f.name not in IGNORE_FILES:
                disk_files[f.name] = f
    
    log(f"  Found {len(disk_files)} .md files on disk")
    
    # Remove entries for missing files
    before_remove = len(entries)
    entries = [e for e in entries if e[1] in disk_files]
    removed = before_remove - len(entries)
    if removed:
        log(f"  Removed {removed} dead entries (files no longer on disk)")
    
    # Add orphan files
    log_fnames = {e[1] for e in entries}
    orphans = sorted(disk_files.keys() - log_fnames)
    added = 0
    for fname in orphans:
        if fname in IGNORE_FILES:
            continue
        fpath = disk_files[fname]
        desc = extract_desc(fpath, fname)
        date = extract_date(fname)
        entries.append((date, fname, desc))
        added += 1
    
    if added:
        log(f"  Added {added} orphan entries")
    
    if removed == 0 and added == 0:
        log("  No changes needed — log is in sync ✓")
        return
    
    # Sort descending by date
    entries.sort(key=lambda e: e[0], reverse=True)
    
    # Rebuild file
    new_lines = header[:]
    if header and header[-1] != '':
        new_lines.append('')
    for e in entries:
        new_lines.append(f'- **{e[0]}** {e[1]}: {e[2]}')
    
    # Update count in header
    for i, h in enumerate(new_lines):
        cm = re.match(r'_(\d+) conversations_', h.strip())
        if cm:
            new_lines[i] = f'_{len(entries)} conversations_'
            break
    
    new_text = '\n'.join(new_lines) + '\n'
    
    if not dry_run:
        CONV_LOG.write_text(new_text)
        log(f"Written: {len(entries)} entries ✓")
    else:
        log(f"[DRY] Would write: {len(entries)} entries")
    
    # Also update save skill header count to match
    actual_count = len(entries)
    log(f"Final entry count: {actual_count}")


def step_rebuild(dry_run=False):
    """Rebuild FTS5 index and stub-index.md."""
    if not INDEX_SCRIPT.exists():
        log(f"ERROR: Index script not found at {INDEX_SCRIPT}")
        return
    
    log("Rebuilding FTS5 index + stub-index.md...")
    
    if not dry_run:
        result = subprocess.run(
            ["python3", str(INDEX_SCRIPT), "build"],
            cwd=str(WORKSPACE),
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                log(f"  {line}")
            # Verify DB
            if FTS5_DB.exists():
                db_size = FTS5_DB.stat().st_size
                log(f"FTS5 DB: {db_size:,} bytes ({db_size/1024:.0f} KB)")
                try:
                    conn = sqlite3.connect(str(FTS5_DB))
                    count = conn.execute("SELECT COUNT(*) FROM idx").fetchone()[0]
                    conn.close()
                    log(f"Indexed entries: {count}")
                except Exception as e:
                    log(f"  Verify failed: {e}")
        else:
            log(f"Rebuild failed (exit {result.returncode}): {result.stderr.strip()}")
    else:
        log("[DRY] Would rebuild FTS5 index")


def step_audit(dry_run=False):
    """Run the audit script."""
    if not AUDIT_SCRIPT.exists():
        log(f"ERROR: Audit script not found at {AUDIT_SCRIPT}")
        return
    
    log("Running memory audit...")
    result = subprocess.run(
        ["python3", str(AUDIT_SCRIPT)],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.strip().split('\n'):
        log(f"  {line}")
    if result.stderr.strip():
        log(f"  Stderr: {result.stderr.strip()}")


def full_reconcile(dry_run=False):
    """Run all steps in sequence."""
    print(f"\n{'=' * 60}")
    print(f"SAVEMAINTENANCE — Full Reconcile")
    print(f"Target: {SAVED_DIR}")
    print(f"Log:    {CONV_LOG}")
    print(f"Index:  {FTS5_DB}")
    print(f"Mode:   {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"{'=' * 60}\n")
    
    step_backup(dry_run)
    print()
    step_reconcile(dry_run)
    print()
    step_rebuild(dry_run)
    print()
    step_audit(dry_run)
    
    print(f"\n--- Full reconcile {'[DRY]' if dry_run else ''} complete ---")


# ── Main ─────────────────────────────────────────────────

if __name__ == "__main__":
    dry_run = '--dry' in sys.argv or '-n' in sys.argv
    
    if '--step' in sys.argv:
        idx = sys.argv.index('--step')
        if idx + 1 < len(sys.argv):
            step_name = sys.argv[idx + 1]
            steps = {
                'backup': step_backup,
                'reconcile': step_reconcile,
                'rebuild': step_rebuild,
                'audit': step_audit,
            }
            if step_name in steps:
                steps[step_name](dry_run)
            else:
                print(f"Unknown step: {step_name}. Options: {', '.join(steps.keys())}")
                sys.exit(1)
        else:
            print("--step requires a step name")
            sys.exit(1)
    else:
        full_reconcile(dry_run)
