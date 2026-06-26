---
name: restic-home-backup
description: Design, implement, and operate encrypted restic backups for Linux home directories with encryption, deduplication, automated scheduling, and restore testing. Use when a user asks to back up ~/, set up daily/weekly/monthly backup jobs, harden backup security, troubleshoot restore/integrity issues, or roll out backup automation across multiple workstations.
---

# Restic Home Backup

Deliver a production-ready, unattended restic backup workflow for a Linux home
directory, covering encryption, deduplication, versioned retention, systemd
scheduling, retry logic, durable logging, email alerting, and restore validation.

## Skill contract

- **Name:** `restic-home-backup`
- **Version:** `2.0.0`
- **Problem solved:** Reliable, encrypted, versioned backups of a Linux home
  directory. Supports SSH/SFTP remote repositories, DST-safe scheduling,
  transient-error retries, user-level installs (no root), one-time restore
  audit timers, and reusable multi-host rollout.
- **Inputs:**
  - Backup source user and path
  - Repository endpoint/transport (`local`, `sftp`, `s3`, `b2`, etc.)
  - Timezone (default `America/Los_Angeles`)
  - Retention policy (default: 14 daily / 8 weekly / 12 monthly)
  - Exclude patterns
  - Alert email
- **Outputs:**
  - Installed and initialized restic repository
  - Backup / prune / check / audit scripts under `/usr/local/bin/`
  - Structured log wrapper with start/end/elapsed/exit-code per job
  - systemd service+timer units (system-level or user-level)
  - One-time restore audit timer
  - Retry logic for transient failures (never retries auth/perm errors)
  - Validation evidence: snapshot listing, restore drill, integrity check
  - Controlled failure drills: wrong secret / unreachable repo / bad env file
  - Operator runbook (`references/runbook.md`)
  - Ops checklist (`references/ops-checklist.md`)
- **Safety boundaries (must never violate):**
  - Never print secrets or tokens in chat, log output, or scripts.
  - Never delete snapshots or repositories without explicit user confirmation.
  - Never weaken permissions on credential files (0600 minimum).
  - Never claim backup success without checking exit status and snapshot listing.
  - Default to PLAN-ONLY mode; require explicit `--apply` for system changes.
  - No snapshot deletion during initial engagement; use `--dry-run-prune` to preview.

## Workflow

### 1) Collect backup contract

Minimum required:
- Source path (e.g., `/home/alice`)
- Repository (e.g., `sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17`)
- Retention policy
- Preferred schedule in local timezone

If any critical value is missing, ask targeted questions.

### 2) Show plan (no-change pass)

```bash
bash scripts/bootstrap_restic_home.sh \
  --user alice \
  --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17"
```

This prints the complete plan: files, schedule, retention, secrets approach,
retry logic, legacy cron archival, and dry-run prune preview. Zero changes made.

### 3) Apply system changes

```bash
sudo bash scripts/bootstrap_restic_home.sh \
  --user alice \
  --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17" \
  --hostname devbox17 \
  --timezone "America/Los_Angeles" \
  --mail-to sre-oncall@example.com \
  --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
  --config-dir /etc/home-backup \
  --log-dir /var/log/home-backup \
  --apply \
  --init-repo \
  --enable-timers \
  --run-initial-backup \
  --archive-legacy-cron \
  --dry-run-prune
```

What this does (in order):
1. Creates `/etc/home-backup/` (0700), generates password (0600, never printed)
2. Writes env file (0600) and excludes list
3. Creates log directory `/var/log/home-backup/`
4. Installs logging+retry wrapper (`restic-home-log-run.sh`)
5. Installs 4 operational scripts (backup, prune, check, audit-drill)
6. Writes 8 systemd units (4 service + 4 timer)
7. Archives and removes legacy root crontab entry
8. Enables timers and runs `daemon-reload`
9. Initializes repo (skips if already exists)
10. Starts first backup via systemd
11. Shows `restic forget --dry-run` output (no deletion)

### 4) User-level install (no root required — e.g., labvm3/bob)

```bash
bash scripts/install_userlevel_restic.sh \
  --repo /mnt/offsite/backups/labvm3-home \
  --hostname labvm3 \
  --timezone "America/Los_Angeles" \
  --mail-to sre-oncall@example.com \
  --apply --init-repo --enable-timers --run-initial-backup

# Enable linger (one-time, requires sudo):
sudo loginctl enable-linger bob

# Manage:
systemctl --user list-timers 'restic-home-*'    # list
systemctl --user start restic-home-backup.service  # manual backup
bash scripts/install_userlevel_restic.sh --remove  # remove schedule
```

### 5) End-to-end validation

```bash
sudo bash scripts/validate_restic_setup.sh
```

Runs:
- Snapshot listing
- Restore drill to `/tmp/restore-drill` (verifies `.ssh/config`,
  `Documents/roadmap.md`, `.config/git/config`)
- Cleanup of temp restore directory
- Repository integrity check
- Three failure drills: wrong secret / unreachable repo / unreadable env file
  (each prints the failing command and a one-line corrective action)

### 6) One-time restore audit timer

The bootstrap creates `restic-home-audit.timer` for a single scheduled restore
drill. By default: **2026-04-17 17:00:00 America/Los_Angeles**.

```bash
# Inspect:
systemctl list-timers restic-home-audit.timer --no-pager

# Cancel:
systemctl disable --now restic-home-audit.timer

# Run now:
systemctl start restic-home-audit.service
```

### 7) Package and publish via ClawHub

```bash
# Validate skill structure:
clawhub validate .

# Publish:
clawhub publish .

# Verify clean install (fresh environment, no secrets carried over):
mkdir /tmp/clawhub-verify && cd /tmp/clawhub-verify
clawhub install restic-home-backup
# Run plan-only to confirm scripts are present and executable:
bash restic-home-backup/scripts/bootstrap_restic_home.sh \
  --user testuser --repo sftp:test@localhost:/test
```

## Files in this skill

```
scripts/
  bootstrap_restic_home.sh     System-level install (plan + apply)
  install_userlevel_restic.sh  User-level install for non-root hosts
  validate_restic_setup.sh     End-to-end validation + failure drills

references/
  runbook.md      Full operator runbook (13 sections)
  ops-checklist.md  Quick daily/weekly/monthly reference
```

## Response style requirements

- Name exact file paths, service names, and commands.
- State what changed and how to verify it.
- Never print passwords or tokens.
- End multi-step tasks with an explicit completion status.
- Reference `references/runbook.md` for day-2 operational guidance.
