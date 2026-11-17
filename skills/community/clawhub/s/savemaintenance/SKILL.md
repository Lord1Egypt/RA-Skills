---
name: savemaintenance
description: "Deterministic reconciliation of conversation-log.md, FTS5 index, and saved conversations — one-shot fix or maintenance run"
homepage: https://github.com/mirza-alam/openclaw-savemaintenance
emoji: 🏥
requires:
  bins: [python3]
metadata:
  openclaw:
    emoji: "🏥"
    requires:
      bins: [python3]
    install:
      - id: setup
        kind: setup
        label: "Create savemaintenance directory"
        run: "mkdir -p ~/.openclaw/workspace/savemaintenance && mkdir -p ~/.openclaw/workspace/savemaintenance/backups && mkdir -p ~/.openclaw/workspace/savemaintenance/snapshots"
      - id: check-prereqs
        kind: check
        label: "Verify saved conversations and memory index exist"
        run: "test -d ~/.openclaw/workspace/saved || echo 'WARN: ~/.openclaw/workspace/saved/ does not exist yet (run save skill setup first)' ; test -f ~/.openclaw/workspace/saved/memory-index.py || echo 'WARN: memory-index.py not found — install the save skill first'"
---

# savemaintenance — Memory System Reconcile Pipeline

**One-shot tool for keeping the three-tier memory system coherent.** Cross-references the conversation log against files on disk, rebuilds the FTS5 index, runs a full audit. Zero external dependencies.

## The Problem

The three-tier memory system (log → FTS5 index → files) is designed for consistency, but things drift:

- Files get deleted but their log entries remain (orphans)
- Files get added outside the save workflow but never get indexed
- The FTS5 index gets stale
- The topic map and stub index need regeneration

`savemaintenance` is the repair pipeline for all of the above. Run it weekly, or after any bulk operation on saved conversations.

## Usage

```bash
# Copy the pipeline to the workspace
cp -r {baseDir}/. ~/.openclaw/workspace/savemaintenance/

# Dry run first — see what would change
cd ~/.openclaw/workspace/savemaintenance && python3 full-reconcile.py --dry

# Full repair: backup → reconcile → rebuild → audit
./run.sh

# Or run individual steps
python3 full-reconcile.py --step backup
python3 full-reconcile.py --step reconcile
python3 full-reconcile.py --step rebuild
python3 full-reconcile.py --step audit
```

## What It Does

### 1. Backup
Copies `conversation-log.md` and `topic-index.json` to timestamped backups.

### 2. Reconcile
- Removes log entries where the `.md` file no longer exists
- Adds entries for `.md` files not in the log (reads `# Title` from file content)
- Sorts all entries by date descending
- Updates the header count

### 3. Rebuild
Regenerates the FTS5 index at `/dev/shm/memory-index.db` from scratch.

### 4. Audit
Reports: orphan entries, missing files, index coherence, directory hygiene.

## Scripts

| File | Purpose |
|---|---|
| `run.sh` | Entry point — snapshot then full reconcile |
| `full-reconcile.py` | Core pipeline (backup → reconcile → rebuild → audit) |
| `snapshot.py` | Manual snapshot/restore tool |
| `README.md` | Full documentation |

## Snapshots

```bash
python3 snapshot.py                # Auto-timestamped snapshot
python3 snapshot.py take <tag>     # Named snapshot
python3 snapshot.py list           # List all snapshots
```

Snapshots go to `backups/` by default.

## Edge Cases Handled

- **Empty log file** — creates a fresh log from scratch
- **New files added between runs** — adds them without removing existing entries
- **Deleted files still in log** — entries are removed
- **Renamed files** — detected as "dead entry + new orphan" pair
- **Dry run** — preview changes without writing anything

## Default Paths

| Path | Default |
|---|---|
| Saved conversations | `~/.openclaw/workspace/saved/` |
| Conversation log | `~/.openclaw/workspace/saved/conversation-log.md` |
| Memory index | `/dev/shm/memory-index.db` |
| Backup dir | `~/.openclaw/workspace/savemaintenance/backups/` |

Set `OPENCLAW_WORKSPACE` env var to override `~/.openclaw/workspace`.

## Dependencies

- Python 3.8+ (standard library only — no pip packages)
- SQLite3 FTS5 (bundled with Python)
- The `save` skill from ClawHub (for memory-index.py)
