---
name: self-backup
description: >
  Backup and restore OpenClaw agent configuration, skills, memory, and workspace files.
  Use when asked to "backup", "backup yourself", "create a restore point", "archive my agent",
  "export configuration", "save current state", or "setup auto-backup".
  Also handles restore: "restore from backup", "recover agent", "reinstall from backup".
---

# Self Backup & Restore

Backup and restore your OpenClaw agent's complete state, including: configuration, skills, memory, and workspace files.

## What Gets Backed Up

| Category | Path | Priority |
|----------|------|----------|
| OpenClaw config | `~/.openclaw/openclaw.json` | ⭐⭐⭐ Required |
| API credentials | `~/.openclaw/.env` | ⭐⭐⭐ Required |
| Skills | `~/.openclaw/workspace/skills/` | ⭐⭐⭐ Required |
| Memory files | `~/.openclaw/workspace/memory/` | ⭐⭐⭐ Required |
| Identity files | `MEMORY.md` `SOUL.md` `IDENTITY.md` `USER.md` | ⭐⭐⭐ Required |
| Config files | `AGENTS.md` `TOOLS.md` `HEARTBEAT.md` | ⭐⭐ Important |
| Cron jobs | `~/.openclaw/cron/jobs.json` | ⭐⭐ Important |
| Credentials | `~/.openclaw/credentials/` | ⭐⭐ Important |

## What's NOT Backed Up

- `~/.openclaw/logs/` — logs, not needed
- `~/.openclaw/media/` — media cache, too large
- `~/.openclaw/workspace/.venv-*/` — Python envs, can be rebuilt
- `~/.openclaw/completions/` — history cache

---

## Run Backup

```bash
python3 ~/.openclaw/workspace/skills/self-backup/scripts/backup.py
```

Output: `~/backups/openclaw-backup-YYYY-MM-DD_HHMM.tar.gz`

## Run Restore

```bash
python3 ~/.openclaw/workspace/skills/self-backup/scripts/restore.py ~/backups/openclaw-backup-YYYY-MM-DD_HHMM.tar.gz
```

## List Backups

```bash
python3 ~/.openclaw/workspace/skills/self-backup/scripts/backup.py --list
```

## Setup Weekly Auto-Backup (via OpenClaw cron)

```bash
openclaw cron add \
  --name "weekly-self-backup" \
  --cron "0 2 * * 0" \
  --tz "Asia/Shanghai" \
  --message "Run backup: python3 ~/.openclaw/workspace/skills/self-backup/scripts/backup.py and report result" \
  --session isolated \
  --announce \
  --channel telegram
```

---

## After Restore: Rebuild Steps

1. **Reinstall OpenClaw** (fresh machine only)
   ```bash
   npm install -g openclaw
   ```

2. **Restore backup**
   ```bash
   python3 restore.py openclaw-backup-YYYY-MM-DD.tar.gz
   ```

3. **Rebuild Python environment** (not included in backup)
   ```bash
   cd ~/.openclaw/workspace
   python3 -m venv .venv-stock
   source .venv-stock/bin/activate
   pip install yfinance pandas numpy pandas-ta ta ddgs tavily-python requests beautifulsoup4
   ```

4. **Re-login ClawHub**
   ```bash
   clawhub auth login --token <YOUR_TOKEN> --no-browser
   ```

5. **Verify**
   ```bash
   openclaw status && openclaw doctor
   ```
