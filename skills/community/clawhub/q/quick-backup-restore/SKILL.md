---
name: quick-backup-restore
description: "Restic-powered encrypted time machine for OpenClaw: hourly incremental snapshots, fast restore by time/snapshot/file, local-only privacy defaults, integrity checks, retention, and optional alerts. Setup can run with sudo, install dependencies, create systemd/cron persistence, restore over current files, and prune or purge recovery data."
metadata: { "openclaw": { "emoji": "⏱", "requires": { "bins": ["bash", "openssl", "curl", "jq"], "auto_install": ["restic", "yq"] }, "install": [{ "id": "setup", "kind": "shell", "label": "Run Time Clawshine setup", "command": "sudo bash {baseDir}/bin/setup.sh" }], "homepage": "https://github.com/marzliak/quick-backup-restore", "capabilities": { "filesystem": ["read configured backup paths", "write encrypted restic repository", "restore snapshots to target paths", "forget/prune snapshots", "optional destructive purge"], "system": ["sudo setup", "optional package install", "optional systemd timer or cron", "optional logrotate and /usr/local/bin install"], "network": ["optional Telegram", "optional healthcheck", "optional ClawHub update check", "blocked by privacy.local_only by default"], "sensitive_data": ["OpenClaw memory", "sessions", "config", "user-added paths may contain secrets"] } } }
---

# ⏱🦞 Time Clawshine — OpenClaw Time Machine

**Your agent just nuked its own memory. Now what?**

You spent weeks training your OpenClaw agent — building memory, refining context, tuning personality. Then one bad session wipes it. Gone. And your last "real" backup? Yesterday. Maybe last week.

**Time Clawshine gives OpenClaw a local encrypted time machine.** Every hour, restic takes an incremental snapshot of your agent's brain — memory, sessions, config, everything. Only changed bytes are stored, so backups stay fast and compact. When things break (and they will), you roll back by time, snapshot, or file to *exactly* the moment before it happened. Not yesterday. Not "the last backup." The exact hour.

Security note: this is a privileged backup/restore tool, not a narrow read-only helper. Setup can install packages and a scheduler with `sudo`; restore can overwrite current files; retention/prune can remove old recovery points; and optional external integrations can send minimal operational metadata only after explicit opt-in.

**One command to install. Zero maintenance. Just works.**

```bash
sudo bash {baseDir}/bin/setup.sh
```

### Why this exists

| Problem | Without Time Clawshine | With Time Clawshine |
|---------|----------------------|---------------------|
| Agent overwrites MEMORY.md | Hope you saved a copy | `restore.sh "2h ago"` |
| Bad session corrupts context | Rebuild from scratch | Roll back one snapshot |
| "What changed?" | No idea | `restic diff` between any two snapshots |
| Disk fills up | Backup keeps growing | Dedup — only deltas stored |
| Something fails | You find out next week | Local log, optional minimal Telegram ping |

### What's under the hood

- **Restic** — battle-tested backup engine, AES-256 encryption, incremental deduplication
- **72 snapshots / 3 days** of history at hourly resolution (configurable)
- **Disk guard** — aborts before filling your disk, optionally alerts via Telegram
- **Integrity checks** — automatic `restic check` every 24 backups
- **Daily digest** — Telegram summary with snapshot count, repo size, disk free
- **Healthcheck ping** — opt-in healthchecks.io / hc-style endpoint pings (`/start`, `/`, `/fail`) so you also know when the backup *stops running*, not just when it fails
- **Update awareness** — optional ClawHub check, disabled by default, never auto-updates
- **Status dashboard** — `bin/status.sh` for a full health check at a glance
- **Repository cleanup** — `bin/prune.sh` to manually reclaim disk space
- **Self-test** — `bin/test.sh` validates backup→restore→verify roundtrip
- **Guided setup** — agent reads `SETUP_GUIDE.md` and walks the user through every option
- **Dry-run mode** — `backup.sh --dry-run` to validate without writing
- **Uninstall** — `bin/uninstall.sh` for clean removal (preserves data by default)
- **Local-only by default** — no Telegram, healthcheck, or update-check egress unless `privacy.local_only` is explicitly disabled

---

## Technical reference

**Repository:** configured in `{baseDir}/config.yaml`
**Log:** configured in `config.yaml` under `logging.file` (rotated weekly via logrotate)
**Password file:** configured in `config.yaml` under `repository.password_file` (chmod 600 — **back this up separately**)

---

## When the user asks to set up or install Time Clawshine

**First, read `{baseDir}/SETUP_GUIDE.md` and walk the user through each step interactively.** The guide covers Telegram, frequency, retention, extra paths, disk safety, and repo location. Configure `config.yaml` based on their answers before running setup.

If installing from ClawHub in OpenClaw, use the slug-only form:
```bash
openclaw skills install quick-backup-restore
```
Some OpenClaw CLI versions reject owner-prefixed slugs such as `marzliak/quick-backup-restore`.

If the user wants a quick install without customization:

1. Check if already set up:
   ```bash
   sudo bash {baseDir}/bin/status.sh
   ```
2. Run setup:
   Preview first if the user wants to see dependencies, system files, and scheduler changes without modifying the machine:
   ```bash
   bash {baseDir}/bin/setup.sh --dry-run
   ```
   ```bash
   sudo bash {baseDir}/bin/setup.sh
   ```
   For repo-only setup (no apt-get, no cron, no /usr/local/bin changes):
   ```bash
   sudo bash {baseDir}/bin/setup.sh --no-system-install
   ```
   For CI/automated setup (skip confirmation prompts):
   ```bash
   sudo bash {baseDir}/bin/setup.sh --assume-yes
   ```
3. Confirm setup succeeded:
   ```bash
   sudo bash {baseDir}/bin/status.sh
   ```

---

## When the user asks to run a manual backup

```bash
sudo bash {baseDir}/bin/backup.sh
```

Then confirm with:
```bash
sudo bash {baseDir}/bin/status.sh
```

---

## When the user asks to check backup status or history

Run the status dashboard:
```bash
sudo bash {baseDir}/bin/status.sh
```

Or show the last 20 log lines:
```bash
sudo tail -20 "$(yq e '.logging.file' {baseDir}/config.yaml)"
```

List all snapshots (most recent first):
```bash
sudo bash {baseDir}/bin/restore.sh --help
# Or directly:
REPO=$(yq e '.repository.path' {baseDir}/config.yaml)
PASS=$(yq e '.repository.password_file' {baseDir}/config.yaml)
restic -r "$REPO" --password-file "$PASS" snapshots
```

Show what changed between the two most recent snapshots:
```bash
REPO=$(yq e '.repository.path' {baseDir}/config.yaml)
PASS=$(yq e '.repository.password_file' {baseDir}/config.yaml)
SNAPS=$(restic -r "$REPO" --password-file "$PASS" snapshots --json | jq -r '.[-2:][].id')
restic -r "$REPO" --password-file "$PASS" diff $SNAPS
```

---

## When the user asks to restore or roll back

**Interactive restore (recommended — always dry-runs first):**
```bash
sudo bash {baseDir}/bin/restore.sh
```

**Restore by time (e.g. "roll back 2 hours"):**
```bash
sudo bash {baseDir}/bin/restore.sh "2h ago" --target /tmp/tc-restore
sudo bash {baseDir}/bin/restore.sh yesterday --target /tmp/tc-restore
```

**Restore a specific file from the latest snapshot:**
```bash
sudo bash {baseDir}/bin/restore.sh latest --file /root/.openclaw/workspace/MEMORY.md --target /tmp/tc-restore
# Preview the result, then move manually:
# cp /tmp/tc-restore/root/.openclaw/workspace/MEMORY.md /root/.openclaw/workspace/MEMORY.md
```

**Restore a specific snapshot by ID:**
```bash
sudo bash {baseDir}/bin/restore.sh <snapshot_id>
```

Always confirm with the user before executing a full restore to `/`.
For a restore targeting `/`, the script requires the exact confirmation phrase `RESTORE TO /`.

---

## When the user asks to check repo integrity

```bash
REPO=$(yq e '.repository.path' {baseDir}/config.yaml)
PASS=$(yq e '.repository.password_file' {baseDir}/config.yaml)
restic -r "$REPO" --password-file "$PASS" check
```

---

## When the user asks to change configuration

Edit `{baseDir}/config.yaml` with the requested changes (schedule, retention, paths, Telegram credentials), then re-run setup to apply:
```bash
sudo bash {baseDir}/bin/setup.sh
```

---

## When the user asks to customize backup paths

Run the local path analyzer (100% offline — no API calls, no data leaves the machine):
```bash
sudo bash {baseDir}/bin/customize.sh
```

This scans the system for:
- Extra paths worth backing up (e.g. `~/.config`, custom scripts)
- Common junk patterns to exclude (e.g. `node_modules`, `*.log`, `cache/`)

Shows suggestions and asks for confirmation before changing `config.yaml`.
Credential stores such as `~/.ssh` and `~/.gnupg` are not auto-suggested. Add them only after explicit user approval and only when repository access and password-file backup are strongly controlled.

---

## When the user asks to clean up or free disk space

```bash
sudo bash {baseDir}/bin/prune.sh
```

Options:
- `--keep-last 24` — keep only last 24 snapshots
- `--older-than 7d` — remove snapshots older than 7 days
- `--dry-run` — preview what would be removed
- `--yes` — skip confirmation prompt

---

## When the user asks to run a dry-run or test backup

**Dry-run (validates without writing):**
```bash
sudo bash {baseDir}/bin/backup.sh --dry-run
```

**Self-test (full backup→restore→verify roundtrip in temp directory):**
```bash
bash {baseDir}/bin/test.sh
```

---

## Important notes

- **Silent by design:** cron/systemd runs every hour at :05 and logs to the configured log file. No output unless there is a failure.
- **Telegram fires only on failure.** If the user has not configured `bot_token` and `chat_id`, failures are logged only.
- **This is the time machine layer.** It protects against "the agent broke something in the last 3 days." It is NOT a disaster recovery backup — that should be handled by an off-VM backup (e.g. restic to a remote server).
- **Password:** The restic repository is AES-256 encrypted. The password file location is configured in `config.yaml` (chmod 600). Losing it means losing access to all snapshots.
- **Never commit `secrets.env` or `.pass` files to git.** They are excluded via `.gitignore`.

---

## When the user asks to uninstall or remove Time Clawshine

```bash
sudo bash {baseDir}/bin/uninstall.sh
```

This removes all system artifacts (systemd timer/service, cron, logrotate, binary, lock/marker files) but **preserves** the backup repository and password file.

To also delete all backup data (irreversible):
```bash
sudo bash {baseDir}/bin/uninstall.sh --purge
```

The source files in the skill directory are never touched — can re-install with `sudo bin/setup.sh`.

---

## When the user asks to check for updates

Run the status dashboard which includes update info:
```bash
sudo bash {baseDir}/bin/status.sh
```

Or check manually:
```bash
openclaw skills update quick-backup-restore
```

Note: `backup.sh` automatically checks for updates once per day (if `updates.check: true` in config). It logs a warning when a new version is available but never updates automatically.
