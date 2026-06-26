# Installation Guide

## Prerequisites

- Python 3.8+
- OpenClaw workspace at `~/.openclaw/workspace-alfred/` (or custom via `SUBCONSCIOUS_WORKSPACE`)
- Self-improving agent skill at `~/.openclaw/workspace-alfred/.learnings/` (optional but recommended)

## Quick Install

```bash
cd ~/.openclaw/skills/subconscious/scripts
chmod +x install.sh
./install.sh
```

The installer will:
1. Create memory store directories (`memory/subconscious/`)
2. Initialize `core.json`, `live.json`, `pending.jsonl`
3. Install cron jobs (tick/5min, rotate/hourly, review/6am)
4. Create logs directory
5. Run a status check to verify

## Manual Install (without cron)

```bash
# Set workspace (if not default)
export SUBCONSCIOUS_WORKSPACE=~/.openclaw/workspace-alfred

# Create memory dirs
mkdir -p $SUBCONSCIOUS_WORKSPACE/memory/subconscious/snapshots
touch $SUBCONSCIOUS_WORKSPACE/memory/subconscious/pending.jsonl

# Initialize files
echo '{"version": "1.5", "items": []}' > $SUBCONSCIOUS_WORKSPACE/memory/subconscious/core.json
echo '{"version": "1.5", "items": []}' > $SUBCONSCIOUS_WORKSPACE/memory/subconscious/live.json

# Manual cron entries
echo "*/5 * * * * cd ~/.openclaw/skills/subconscious/scripts && python3 subconscious_metabolism.py tick >> ~/.openclaw/workspace-alfred/logs/subconscious_tick.log 2>&1" | crontab -
echo "0 * * * * cd ~/.openclaw/skills/subconscious/scripts && python3 subconscious_metabolism.py rotate --enable-promotion >> ~/.openclaw/workspace-alfred/logs/subconscious_rotate.log 2>&1" | crontab -
echo "0 6 * * * cd ~/.openclaw/skills/subconscious/scripts && python3 subconscious_metabolism.py review >> ~/.openclaw/workspace-alfred/logs/subconscious_review.log 2>&1" | crontab -
```

## Custom Workspace

```bash
export SUBCONSCIOUS_WORKSPACE=/path/to/your/workspace
```

All paths will be computed relative to this.

## Upgrading

```bash
# Pull latest, then re-run install
cd ~/.openclaw/skills/subconscious
git pull
./scripts/install.sh
```

## Uninstall

```bash
# Remove cron entries
crontab -l | grep -v "subconscious_metabolism" | crontab -

# Memory store is preserved at memory/subconscious/
# Delete separately if desired:
# rm -rf ~/.openclaw/workspace-alfred/memory/subconscious/
```
