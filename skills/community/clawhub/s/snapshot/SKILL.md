---
name: snapshot
description: >
  Backup and restore the .openclaw agent folder — encrypted snapshots pushed to a
  private GitHub repo. Use this skill whenever the user mentions backup, restore,
  snapshot, save state, migrate workspace, move to a new machine, or any request
  to preserve or recover the .openclaw agent. Also trigger when the user asks
  about available backup versions, wants to check backup status, or needs to set
  up the backup system on a new workspace. Even casual phrasing like "save my
  agent" or "load my stuff on the new box" should trigger this skill.
metadata:
  openclaw:
    requires:
      env:
        - BACKUP_PASSWORD
        - GITHUB_PAT
        - GITHUB_USERNAME
        - REPO_NAME
    primaryEnv: BACKUP_PASSWORD
---

# Snapshot — OpenClaw Backup & Restore

Encrypted backup and restore for the `~/.openclaw` agent folder.  
Backups are GPG-encrypted, chunked for GitHub's 100MB file limit, and pushed to a private repo.

## How it works

- **backup** — tar.gz → GPG encrypt → split into ≤95MB chunks → push to GitHub
- **restore** — clone repo → pick version → reassemble chunks → verify checksum → decrypt → extract
- **setup** — install GPG, clone/init the GitHub transport repo

Each backup version lives in its own folder with a manifest:
```
backups/openclaw-{timestamp}/
├── manifest.json
├── part-000.gpg
├── part-001.gpg
└── ...
```

Last 10 backups are kept; older ones are auto-deleted.

---

## Prerequisites

Before running any command, verify:

1. **GPG is installed.** If not: `sudo apt-get update && sudo apt-get install -y gnupg gpg-agent`
2. **Credentials are configured** (see below)
3. **Setup has been run at least once** on this workspace: `python3 scripts/setup.py`

### Providing credentials

The scripts need these values: `BACKUP_PASSWORD`, `GITHUB_PAT`, `GITHUB_USERNAME`, and optionally `REPO_NAME` (defaults to `openclaw-transport`).

Provide them via **any** of these methods (checked in this order):

1. **OpenClaw's env file (recommended):** Add to `~/.openclaw/.env`:
   ```
   BACKUP_PASSWORD=your-strong-password
   GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_USERNAME=YourGitHubUsername
   REPO_NAME=openclaw-transport
   ```
   Then in `openclaw.json`, just enable the skill:
   ```json
   "skills": { "entries": { "snapshot": { "enabled": true } } }
   ```

2. **Skill-local env file:** Copy `env-example.txt` to `.env` in this skill's directory and fill in values. Useful for standalone usage outside OpenClaw.

3. **Shell environment:** Export the variables in your shell profile.

---

## Commands

All scripts live in the `scripts/` subdirectory of this skill.

### Take a backup
```bash
python3 <skill-path>/scripts/backup.py
```
Non-interactive. Compresses, encrypts, chunks if needed, pushes to GitHub.  
Auto-deletes versions older than the most recent 10.

### Restore a backup
```bash
# Restore the latest version (non-interactive, best for AI agents)
python3 <skill-path>/scripts/restore.py --latest

# Restore a specific version by timestamp
python3 <skill-path>/scripts/restore.py --version 20260227-120000

# List available versions without restoring
python3 <skill-path>/scripts/restore.py --list

# Interactive mode (prompts user to pick — use only in human-attended sessions)
python3 <skill-path>/scripts/restore.py
```

### Run setup (first time or new workspace)
```bash
python3 <skill-path>/scripts/setup.py
```
Safe to run multiple times. Installs GPG if missing, clones or syncs the transport repo.

---

## Typical workflows

**Always run setup.py before backup or restore.** It's idempotent (safe to run every time) and ensures GPG is installed, the transport repo exists, and the local repo is synced with GitHub. This prevents issues like missing repos, stale local state, or remotely deleted backups not being reflected locally.

### "Back up my agent"
1. Run `python3 <skill-path>/scripts/setup.py`
2. Run `python3 <skill-path>/scripts/backup.py`
3. Report the timestamp and size to the user

### "Restore my agent" or "Load the latest backup"
1. Run `python3 <skill-path>/scripts/setup.py`
2. Run `python3 <skill-path>/scripts/restore.py --latest`
3. Tell the user it's done and suggest restarting: `openclaw gateway restart`

### "Show me available backups"
1. Run `python3 <skill-path>/scripts/setup.py`
2. Run `python3 <skill-path>/scripts/restore.py --list`
3. Present the version list to the user

### "Set up backups on this new workspace"
1. Confirm the user has a `.env` file with credentials (help them create one from `env-example.txt` if not)
2. Run `python3 <skill-path>/scripts/setup.py`

### "Restore a specific version"
1. Run `python3 <skill-path>/scripts/setup.py`
2. Run `python3 <skill-path>/scripts/restore.py --list` to show available versions
3. Ask the user which timestamp they want
4. Run `python3 <skill-path>/scripts/restore.py --version <timestamp>`

---

## Important notes

- **All `.env` files are excluded from backups** — both `~/.openclaw/.env` (OpenClaw root secrets) and the skill's own `.env`. Credentials never end up in encrypted archives.
- The transport repo (`~/openclaw-transport/`) lives outside `.openclaw` and is not backed up.
- The skill scripts themselves **are** backed up as part of `.openclaw`.
- WhatsApp sessions are excluded (workspace-specific). User must reconnect after restore.
- After restoring, the user should restart their agent: `openclaw gateway restart`