# ⏱🪞 Time Clawshine — OpenClaw Time Machine

[![CI](https://github.com/marzliak/quick-backup-restore/actions/workflows/ci.yml/badge.svg)](https://github.com/marzliak/quick-backup-restore/actions/workflows/ci.yml)

**Restic-powered encrypted snapshots for OpenClaw.**

Time Clawshine is a local-first time machine for OpenClaw: hourly incremental snapshots, fast restore by time/snapshot/file, integrity checks, retention, and privacy defaults that keep external egress off unless you opt in. It is not a plain tarball backup; restic handles encryption, deduplication, and snapshot history.

Security note: setup can run with `sudo`, install dependencies, register systemd/cron persistence, back up sensitive OpenClaw memory/sessions/config, restore over current files, and prune old recovery points. Telegram, healthcheck.io / hc-style pings, and ClawHub update checks are optional and disabled by default.

**Platform:** Linux only (bash scripts). macOS works with Homebrew restic but is untested. Windows not supported.

Read [SECURITY.md](SECURITY.md) and [PRIVACY.md](PRIVACY.md) before installing on a production agent.

---

## Quick start

From OpenClaw / ClawHub:

```bash
openclaw skills search quick-backup-restore
openclaw skills install quick-backup-restore
```

Use the slug `quick-backup-restore`; some OpenClaw CLI versions do not accept
the owner-prefixed form `marzliak/quick-backup-restore`.

From GitHub:

```bash
git clone https://github.com/marzliak/quick-backup-restore
cd quick-backup-restore
bash bin/setup.sh --dry-run  # preview deps, files, scheduler, and privacy settings
nano config.yaml             # optional: review paths and opt in to integrations
sudo bin/setup.sh            # installs deps, initializes repo, registers scheduler
```

Or, repo-only setup (no apt-get, no cron, no /usr/local/bin changes):

```bash
sudo bin/setup.sh --no-system-install
```

Done. Backups run every hour at :05 by default.

---

## Flags

| Flag | Script | Description |
|------|--------|-------------|
| `--help` / `-h` | all scripts | Show usage and exit |
| `--dry-run` | `setup.sh` | Preview dependencies, system files, scheduler, and privacy settings without changes |
| `--skip-backup` | `setup.sh` | Skip the initial validation backup after setup |
| `--no-system-install` | `setup.sh` | Repo-only setup: creates repo dir, generates password, inits restic. Skips apt-get, cron registration, and binary install to `/usr/local/bin` |
| `--assume-yes` / `-y` | `setup.sh` | Skip dependency installation confirmation prompt (for CI/automated use) |
| `--dry-run` | `backup.sh` | Show what would be backed up without writing |
| `--keep-last N` | `prune.sh` | Override retention for this run |
| `--older-than DURATION` | `prune.sh` | Remove snapshots older than duration (e.g. `7d`, `24h`) |
| `--dry-run` | `prune.sh` | Preview cleanup without deleting |
| `--yes` / `-y` | `prune.sh` | Skip confirmation prompt |
| `--yes` / `-y` | `uninstall.sh` | Skip confirmation (system files only, preserves data) |
| `--purge` | `uninstall.sh` | Also delete repository, password file, and logs (DESTRUCTIVE) |

---

## Customize paths

```bash
sudo bin/customize.sh
```

Scans your system locally (100% offline — no API calls) and suggests:
- Extra paths worth backing up (e.g. `~/.config`, custom scripts)
- Junk patterns to exclude (e.g. `node_modules`, `*.log`)

Shows suggestions and asks for confirmation before changing `config.yaml`.
Credential stores such as `~/.ssh` and `~/.gnupg` are not auto-suggested. Add them manually only when you intend to create encrypted backup copies of those credentials and have strong controls around the repository and password file.

---

## Status check

```bash
sudo bin/status.sh
```

Shows: version, snapshot count, last snapshot time, repo size, disk free, password file status, cron status, integrity check counter, update availability, and recent log lines.

---

## Cleanup (prune)

```bash
sudo bin/prune.sh                     # use config retention
sudo bin/prune.sh --keep-last 24      # keep only last 24
sudo bin/prune.sh --older-than 7d     # remove older than 7 days
sudo bin/prune.sh --dry-run           # preview without deleting
```

Shows before/after snapshot count and repo size. If Telegram is explicitly enabled, sends only a minimal cleanup-complete notification by default.

---

## Self-test

```bash
bash bin/test.sh
```

Validates: dependencies, config syntax, shell syntax on all scripts, privacy/security defaults, healthcheck URL validation, notification redaction, and a full backup→restore→verify roundtrip in a temp directory. No root required.

---

## Uninstall

```bash
# Remove system files (preserves your backups and password)
sudo bin/uninstall.sh

# Remove everything including backups (DESTRUCTIVE — asks for confirmation)
sudo bin/uninstall.sh --purge
```

Removes: systemd timer/service, cron job, logrotate config, installed binary, lock and marker files.
Preserves (unless `--purge`): backup repository, password file, log file, source files.

---

## What gets backed up

OpenClaw's runtime context — not the full system. Your agent's brain, not the OS.

| Path | Contents |
|------|----------|
| `workspace/` | MEMORY.md, SOUL.md, USER.md, skills, memory modules |
| `sessions/` | Full agent session history (JSONL) |
| `openclaw.json` | Config, gateway settings |
| `cron/` | Scheduled jobs |

All paths configurable in `config.yaml`.

---

## Example output

After `sudo bin/setup.sh`:

```
[2026-03-04 18:17:02] [INFO ] Checking dependencies...
[2026-03-04 18:17:03] [INFO ] restic 0.17.3, yq 4.44.1 — OK
[2026-03-04 18:17:04] [INFO ] Initializing restic repository at /var/backups/time-clawshine
[2026-03-04 18:17:05] [INFO ] Repository initialized OK
[2026-03-04 18:17:06] [INFO ] Cron job registered: 5 * * * *
[2026-03-04 18:17:06] [INFO ] --- Time Clawshine setup complete ---
```

After `sudo bin/backup.sh` (first run):

```
[2026-03-04 18:18:01] [INFO ] Starting backup...
[2026-03-04 18:18:02] [INFO ]   snapshot 702a8854 saved
[2026-03-04 18:18:03] [INFO ] --- Time Clawshine finished ---
```

After `sudo bin/backup.sh` (subsequent runs — incremental):

```
[2026-03-04 19:05:01] [INFO ] Starting backup...
[2026-03-04 19:05:01] [INFO ]   using parent snapshot 702a8854
[2026-03-04 19:05:01] [INFO ]   snapshot 596e1cb3 saved
[2026-03-04 19:05:02] [INFO ] --- Time Clawshine finished ---
```

Listing snapshots:

```
$ restic -r /var/backups/time-clawshine --password-file /etc/time-clawshine.pass snapshots

ID        Time                 Host     Tags  Paths
-------------------------------------------------------
702a8854  2026-03-04 18:18:02  openclaw       /root/.openclaw/...
596e1cb3  2026-03-04 19:05:01  openclaw       /root/.openclaw/...
add992ac  2026-03-04 20:05:04  openclaw       /root/.openclaw/...
3e55adb1  2026-03-04 21:05:03  openclaw       /root/.openclaw/...
9e5c0e23  2026-03-04 22:05:03  openclaw       /root/.openclaw/...
-------------------------------------------------------
5 snapshots
```

---

## Restore

```bash
# Interactive — lists snapshots and prompts for confirmation
sudo bin/restore.sh

# Restore by time — "2 hours ago", "yesterday"
sudo bin/restore.sh "2h ago" --target /tmp/openclaw-restore
sudo bin/restore.sh yesterday --target /tmp/openclaw-restore

# Restore latest snapshot to a temp dir (safe, non-destructive)
sudo bin/restore.sh latest --target /tmp/openclaw-restore

# Restore a specific file from latest snapshot
sudo bin/restore.sh latest --file /root/.openclaw/workspace/MEMORY.md --target /tmp/openclaw-restore
```

Restoring to `/` can overwrite current OpenClaw state and requires the exact confirmation phrase `RESTORE TO /` after the mandatory dry-run preview.

---

## Installing as an OpenClaw workspace skill

After cloning, symlink into your workspace so it appears in the Control UI:

```bash
mkdir -p /root/.openclaw/workspace/skills
ln -s /path/to/time-clawshine /root/.openclaw/workspace/skills/time-clawshine
```

The skill will appear as `openclaw-workspace` in the Skills panel.

---

## Configuration

Everything in `config.yaml` — fully commented:

```yaml
repository:
  path: /var/backups/time-clawshine   # local path (or any restic backend)
  password_file: /etc/time-clawshine.pass  # auto-generated by setup.sh

retention:
  keep_last: 72   # 3 days at 1/hour

schedule:
  cron: "5 * * * *"   # every hour at :05

backup:
  paths:
    - /root/.openclaw/workspace
    - /root/.openclaw/agents/main/sessions
    - /root/.openclaw/openclaw.json
    - /root/.openclaw/cron
  exclude:
    - "*.bak"
    - "*.tmp"
    - ".git"

integrity:
  check_every: 24   # restic check every N backups (0 = disabled)

safety:
  min_disk_mb: 500  # abort backup if less than this free

notifications:
  telegram:
    enabled: false       # set to true to get pinged on failures
    bot_token: ""        # from @BotFather
    chat_id: ""          # from @userinfobot
    daily_digest: false  # daily summary via Telegram

  healthcheck:           # external uptime monitoring (healthchecks.io / hc-style)
    enabled: false
    url: ""              # e.g. https://hc-ping.com/<uuid> or self-hosted hc
    ping_start: true     # GET <url>/start at backup start (to measure duration)

privacy:
  local_only: true             # blocks Telegram, healthcheck, and update checks
  send_error_details: false    # do not send raw command output externally
  include_hostname: false      # do not include hostname in external messages

updates:
  check: false  # optional daily version check against ClawHub
```

### Security and privacy defaults

`privacy.local_only: true` is the hard egress gate. While it is true, Telegram,
healthcheck, and update checks are blocked even if their individual blocks are
edited. To enable an external integration, set `privacy.local_only: false`, then
enable only the integration you want.

External failure notifications are minimized by default: no hostname and no raw
error output. Setting `privacy.send_error_details: true` may send a short
sanitized error excerpt to the configured third party.

### About the `healthcheck` block

Telegram alerts only fire when the backup **runs and fails**. If the scheduler
itself breaks (cron/systemd misconfigured, timer disabled by an upgrade,
container restart), Telegram stays silent and you only find out when you
need a restore. The `healthcheck` block pings an external uptime endpoint:

| Event | Endpoint hit |
|-------|--------------|
| Backup starts (if `ping_start: true`) | `<url>/start` |
| Backup succeeds | `<url>` |
| Backup fails (any of: paths missing, disk low, restic backup/forget/prune/check) | `<url>/fail` |

Point `url` at a [healthchecks.io](https://healthchecks.io) check (or a
self-hosted instance) configured to expect a ping every hour. URLs must use
`https://` unless they point to loopback localhost. If two
consecutive pings are missed, the service alerts you. Pings have a 10s
timeout and 2 retries; a ping failure is logged without the full endpoint URL
and never aborts the backup.

---

## How it fits in your backup strategy

```
Time Clawshine              ← time machine layer (this tool)
    ↓ hourly, local, 72 snapshots
Full DR backup          ← disaster recovery layer (e.g. restic to remote NAS/cloud)
    ↓ daily, off-VM
```

Time Clawshine protects against "the agent broke its own memory 2 hours ago."
Your DR backup protects against "the VM is gone."

---

## Dependencies

Auto-installed by `setup.sh`: `restic`, `yq` v4, `curl`, `jq`.
`yq` is downloaded from GitHub only when missing and is installed only after
SHA256 verification from the release checksum file. The setup script does not
use `curl | bash`.

## Platform support

| Platform | Status |
|----------|--------|
| Linux    | ✅ Supported |
| macOS    | ⚠️ Untested (requires `brew install restic yq jq`) |
| Windows  | ❌ Not supported (bash scripts) |

## License

MIT — see [LICENSE.txt](LICENSE.txt)

---

## Author

**Leandro Marz** ([@marzliak](https://github.com/marzliak))

## Links

- **Repository:** [github.com/marzliak/quick-backup-restore](https://github.com/marzliak/quick-backup-restore)
- **ClawHub:** [quick-backup-restore](https://clawhub.ai/marzliak/quick-backup-restore)
- **Issues:** [github.com/marzliak/quick-backup-restore/issues](https://github.com/marzliak/quick-backup-restore/issues)
- **Security:** [SECURITY.md](SECURITY.md)
- **Privacy:** [PRIVACY.md](PRIVACY.md)
