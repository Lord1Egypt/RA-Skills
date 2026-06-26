---
name: skill-updater
description: Local-modification-preserving clawhub skill updater. Saves changes as diff patch, applies to new versions, reports conflicts clearly. No forced overwrites.
metadata:
  openclaw:
    requires:
      bins: [python3, clawhub, diff, patch]
      env: [OPENCLAW_SKILLS_DIR]  # default: /root/.openclaw/workspace/skills
    triggers: [skill更新, auto update, git sync]
---

# Skill-Updater

> Local-modification-preserving clawhub skill updater.

## What It Does

You modified a clawhub-installed skill → clawhub released a new version → Skill-Updater updates while **preserving your local changes**.

## How It Works

```
Step 1: Save modifications
  → Scans skill directory, generates unified diff patch
  → Backs up originals to .skill-updater/originals/

Step 2: clawhub update
  → clawhub update downloads new version files

Step 3: Try to merge
  → patch --dry-run attempts to apply changes to new version
  → Success: written with your changes preserved ✅
  → Fail: show diff, user decides manually
```

## File Structure

```
skill-dir/
├── .skill-updater/
│   ├── mod.patch       # unified diff of your changes
│   └── originals/       # snapshot of original files at install time
└── [skill files]
```

## CLI

```bash
# Dry-run: preview which skills have updates and conflicts
python3 git_update.py

# Apply updates
python3 git_update.py --apply

# Update specific skill
python3 git_update.py --apply --skill <slug>

# Show saved modifications
python3 git_update.py --show-patch

# Discard modifications (accept new version, drop your changes)
python3 git_update.py --discard --skill <slug>
```

## Conflict Handling

| Situation | Result |
|-----------|--------|
| Patch applies cleanly | New version + your changes preserved ✅ |
| Same area modified by both | Show diff, user decides |
| No local modifications | Direct clawhub update ✅ |
| Choose to discard | Delete patch, accept new version |

## Requirements

- Python 3.8+
- `clawhub` CLI
- `diff` (coreutils)
- `patch` (coreutils)

## Before Installing

1. **Dry-run first** — Always run `python3 git_update.py` without `--apply` first to preview
2. **Backup** — For important skills, manually back up your modifications before using `--discard`
