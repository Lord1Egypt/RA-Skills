---
name: "Sentinel - AI Agent State Guardian"
description: "Automated backup, integrity monitoring, and self-healing for AI agent workspaces. Detects unexpected changes, creates automatic backups, self-heals from corruption."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["backup", "integrity", "monitoring", "self-healing", "state", "guardian", "protection"]
license: "MIT"
---

# Sentinel - AI Agent State Guardian

Use this skill to protect AI agent workspaces from corruption, accidental changes, and data loss. Sentinel hashes your critical files, detects unexpected changes, creates rolling backups, and restores from backup when corruption is detected.

## When to Use This Skill

Invoke this skill when:
- A user wants to protect their agent workspace from accidental overwrites
- You need to detect if critical files (agent config, memory/, state files) were modified unexpectedly
- Auto-backup is needed before any destructive operation
- You need to restore a workspace to a known-good state after corruption

## Setup

```python
# Copy config_example.py to sentinel_config.py and edit it:
WORKSPACE_ROOT = "/path/to/workspace"
BACKUP_DIR = "/path/to/backups"
STATE_FILE = "/path/to/sentinel_state.json"
CRITICAL_FILES = ["agent.md", "memory/*.md", "config/*.json"]
CHECK_INTERVAL_SECONDS = 600   # check every 10 minutes
MAX_BACKUP_VERSIONS = 10       # keep 10 rolling backups per file
AUTO_RESTORE_ON_CORRUPTION = True
DEBUG = False
```

## Core Operations

### Run Monitoring Cycle
```python
import sentinel_config as config
from sentinel import Sentinel

s = Sentinel(config)
s.run_once()          # one monitoring pass
s.run_continuous()    # continuous loop (blocks)
```

### CLI Usage
```bash
python3 sentinel.py --once          # run one cycle and exit
python3 sentinel.py --continuous    # run continuous monitoring
python3 sentinel.py --status        # show current status
```

### Generate Workspace Manifest
```python
import sentinel_config as config
from sentinel_manifest import ManifestGenerator

generator = ManifestGenerator(config)
manifest = generator.generate_manifest()
generator.save_manifest(manifest, Path("workspace_manifest.json"))
```

### Compare Two Manifests
```python
diff = generator.compare_manifests(old_manifest, new_manifest)
generator.print_diff_summary(diff)
# diff has: added_files, deleted_files, modified_files, added_dirs, deleted_dirs
```

### Restore from Backup
```python
import sentinel_config as config
from sentinel_restore import RestoreTool
from pathlib import Path

tool = RestoreTool(config)

# List all backups
tool.list_all_backups()

# Restore latest backup of a file
tool.restore_latest(Path(config.WORKSPACE_ROOT) / "memory/state.json")

# Interactive restore (lets you pick from backup list)
tool.interactive_restore(Path(config.WORKSPACE_ROOT) / "memory/state.json")

# Find latest backup path without restoring
backup_path = tool.find_latest_backup(Path(config.WORKSPACE_ROOT) / "memory/state.json")
```

### CLI Restore
```bash
python3 sentinel_restore.py --file memory/state.json --latest
python3 sentinel_restore.py --file memory/state.json --interactive
python3 sentinel_restore.py --list
```

## Integrity Violation Responses

When violations are detected, Sentinel can:
- **Alert only** — log and notify, take no action
- **Auto-restore** — revert changed files from latest clean snapshot
- **Quarantine** — move changed files to quarantine dir, restore originals

Configure in `sentinel_config.py`:
```python
ON_VIOLATION = "alert"     # "alert" | "restore" | "quarantine"
```

## What Sentinel Detects

- File content changes (hash mismatch)
- Deleted files that should exist
- New files in monitored directories
- Permission changes on critical files

See README.md for full configuration reference and advanced scheduling options.
