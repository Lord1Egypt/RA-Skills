# savemaintenance — Memory System Reconcile Pipeline

Deterministic pipeline for keeping the memory system coherent and audited in a single shot.

## Quick Start

```bash
cd ~/.openclaw/workspace/savemaintenance
./run.sh              # Full reconcile (backup → reconcile log → rebuild index → audit)
./run.sh --dry        # Dry run — show what would change, don't touch files
```

## Scripts

| Script | Purpose |
|---|---|
| `run.sh` | Shell entry point — pre-flight snapshot then full reconcile |
| `full-reconcile.py` | Core pipeline (backup → reconcile → rebuild → audit) |
| `snapshot.py` | Manual snapshot/restore tool |

### full-reconcile.py

**Steps (run in sequence):**

1. **backup** — Snapshot conversation-log.md + topic-index.json to `backups/`
2. **reconcile** — Cross-reference conversation-log ↔ files on disk
   - Removes entries for files that no longer exist
   - Adds entries for orphan files not in the log
   - Sorts by date descending, updates header count
3. **rebuild** — Runs `memory-index.py build` to regenerate FTS5 index
4. **audit** — Runs `memory-audit.py` and reports findings

**Advanced usage:**

```bash
python3 full-reconcile.py                       # Full pipeline
python3 full-reconcile.py --dry                  # Dry run
python3 full-reconcile.py --step backup          # Single step
python3 full-reconcile.py --step reconcile       # Reconcile only
```

### snapshot.py

```bash
python3 snapshot.py              # Take snapshot (timestamp name)
python3 snapshot.py take mytag   # Take snapshot with custom tag
python3 snapshot.py list         # List available snapshots
```

## Architecture

```
~/.openclaw/workspace/savemaintenance/
├── run.sh                  # Shell entry point
├── full-reconcile.py       # Core pipeline
├── snapshot.py             # Snapshot tool
├── README.md
├── backups/                # Pre-reconcile backups (auto)
└── snapshots/              # Manual snapshots
```

## Dependencies

- Python 3.8+
- `memory-index.py` at `~/.openclaw/workspace/saved/memory-index.py` (from the `save` skill)
- SQLite built-in (for FTS5)
- `~/.openclaw/workspace/saved/` — populated with .md files

## What It Fixes

| Problem | Fix |
|---|---|
| Log entries for deleted files | Removed from conversation-log.md |
| Files on disk not in log | Added with auto-generated description |
| Stale FTS5 index | Rebuilt from scratch |
| File count mismatch | Header count updated to match |
