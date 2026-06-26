# Restic Home Backup — Operator Runbook

**Version:** 2.0.0  
**Applies to:** devbox17 (system-level) and labvm3 (user-level)  
**Contact for alerts:** sre-oncall@example.com

---

## 1. Architecture overview

```
devbox17 (/home/alice)
  ├── /etc/home-backup/env           (root-only, 0600)
  ├── /etc/home-backup/password      (root-only, 0600, auto-generated)
  ├── /etc/home-backup/excludes.txt
  ├── /usr/local/bin/restic-home-backup.sh
  ├── /usr/local/bin/restic-home-prune.sh
  ├── /usr/local/bin/restic-home-check.sh
  ├── /usr/local/bin/restic-home-audit-drill.sh
  ├── /usr/local/bin/restic-home-log-run.sh  (logging + retry wrapper)
  ├── /etc/systemd/system/restic-home-{backup,prune,check,audit}.{service,timer}
  └── /var/log/home-backup/{backup,prune,check,audit-drill}.log

Remote repository:
  sftp:backupsvc@10.50.8.24:/srv/backups/home/devbox17
  (restic: encrypted AES-256, deduplicated, versioned)
```

**Retry logic for transient network errors:**
Failure → classify error → if transient (connection refused / timeout / SSH error)
→ `systemd-run --on-active=1200` schedules one retry in 20 min
→ marker file `/run/restic-home-backup-retry-pending` prevents infinite loops
→ success or second failure clears the marker.
Auth errors and env-file permission errors are never retried.

---

## 2. What changed on disk

| Path | Change | Notes |
|------|--------|-------|
| `/etc/home-backup/` | Created (0700, root) | New secure config dir |
| `/etc/home-backup/env` | Created (0600) | All runtime vars; no secrets printed |
| `/etc/home-backup/password` | Created (0600, auto) | Never displayed anywhere |
| `/etc/home-backup/excludes.txt` | Created | 6 exclusion patterns |
| `/etc/home-backup/legacy-crontab-*.txt` | Created | Archive of old root crontab |
| `/usr/local/bin/restic-home-*.sh` | Created (5 scripts) | |
| `/etc/systemd/system/restic-home-*` | Created (8 units) | 4 service+timer pairs |
| `/var/log/home-backup/` | Created (0750) | Structured durable logs |
| Root crontab | Legacy `home-backup` entry removed | Archived above |

**No snapshots were removed during this engagement.**
The prune timer is enabled for future runs. Before the first live prune run:

```bash
# Preview without deletion:
source /etc/home-backup/env
restic forget --dry-run \
  --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
  --group-by "host,paths"
```

---

## 3. Daily checks

```bash
# Timer status and next elapse:
systemctl list-timers restic-home-backup.timer --no-pager

# Structured log (START / END / elapsed / exit=0):
tail -30 /var/log/home-backup/backup.log

# Journal (full output):
journalctl -u restic-home-backup.service --since "24 hours ago" --no-pager

# Snapshot list:
source /etc/home-backup/env && restic snapshots --group-by host

# Retry pending?
[[ -f /run/restic-home-backup-retry-pending ]] && echo "RETRY PENDING" || echo "ok"
```

Healthy log pattern:
```
[2026-03-18T11:15:42Z] START  job=backup  cmd=/usr/bin/restic backup ...
[2026-03-18T11:19:07Z] END    job=backup  exit=0  elapsed=205s
```

---

## 4. Weekly checks

Runs every Saturday 05:10 America/Los_Angeles (+ up to 10 min random jitter).

```bash
# Timer status:
systemctl list-timers restic-home-prune.timer --no-pager

# Prune log:
tail -40 /var/log/home-backup/prune.log

# Snapshot count (expect ~34 slots once history accumulates):
source /etc/home-backup/env && restic snapshots --group-by host
```

---

## 5. Monthly checks

Runs on the 2nd of each month at 06:20 America/Los_Angeles (+ jitter).

```bash
# Timer status:
systemctl list-timers restic-home-check.timer --no-pager

# Check log:
tail -60 /var/log/home-backup/check.log

# Manual run:
systemctl start restic-home-check.service
```

Healthy output includes: `no errors were found`

---

## 6. Restore drills

### Quick spot-check:

```bash
source /etc/home-backup/env
DRILL=/tmp/restore-drill
rm -rf "$DRILL" && mkdir -p "$DRILL"
restic restore latest --target "$DRILL"

for f in .ssh/config Documents/roadmap.md .config/git/config; do
  [[ -f "$DRILL/home/alice/$f" ]] \
    && echo "PRESENT: $f" \
    || echo "ABSENT:  $f"
done

rm -rf "$DRILL"
```

### Restore a specific file:

```bash
source /etc/home-backup/env
restic restore latest \
  --include "/home/alice/Documents/roadmap.md" \
  --target /tmp/restore-drill
```

### Restore a specific snapshot:

```bash
source /etc/home-backup/env
restic snapshots           # note snapshot ID
restic restore abc12345 --target /tmp/restore-drill
```

---

## 7. Missed-job debugging

**Step 1 — Check timer history:**
```bash
systemctl list-timers 'restic-home-*' --no-pager
journalctl -u restic-home-backup.service --since "48 hours ago" --no-pager
```

**Step 2 — Check service exit status:**
```bash
systemctl status restic-home-backup.service
tail -50 /var/log/home-backup/backup.log
```

**Step 3 — Manual reproduce:**
```bash
source /etc/home-backup/env
/usr/bin/restic backup "${BACKUP_SOURCE}" \
  --exclude-file="${BACKUP_EXCLUDES_FILE}" \
  --host "${BACKUP_HOSTNAME}" --verbose
```

**Step 4 — Verify file permissions:**
```bash
stat /etc/home-backup/env /etc/home-backup/password
# Expected: -rw------- 1 root root
```

**Common failures:**

| Symptom | Log pattern | Fix |
|---------|-------------|-----|
| Wrong password | `wrong password or no key found` | Check `RESTIC_PASSWORD_FILE` in env |
| SSH auth fails | `ssh: handshake failed` | Verify root SSH key on backup server |
| Repo unreachable | `connection refused` / `no route to host` | Check network to 10.50.8.24 |
| Env file unreadable | `permission denied` + env path | `chmod 600 /etc/home-backup/env` |
| Disk full on source | `no space left on device` | Free space, then re-run |

---

## 8. Legacy cron replacement — root cause

The previous schedule was:
```
30 2 * * * /usr/local/bin/home-backup
```

**Root cause 1 — PATH not set in crontab:**
Cron runs with a minimal environment: `PATH=/usr/bin:/bin`. The script at
`/usr/local/bin/home-backup` is in `/usr/local/bin`, which is **not** in cron's
default PATH. So cron could not find the command and either silently discarded
the run or emailed a "command not found" error to root's mailbox (unread).

The fix: always specify full path in crontab, or set `PATH=` at the top of the
crontab file. The new systemd-based design avoids this entirely because:
- Systemd `ExecStart=` always takes an absolute path.
- `EnvironmentFile=` loads the env before the script runs.

**Root cause 2 — DST spring-forward caused the 2026-03-08 run to be skipped:**
On 2026-03-08 at 02:00 PST, clocks sprang forward to 03:00 PDT. The time
02:30 AM **never existed** that day. The cron job was scheduled for 02:30 AM,
so it was simply skipped — cron does not catch up missed runs.

Systemd timers with `Persistent=true` **do** catch up: when the machine boots
after a missed window, the service is started once immediately.

The new backup schedule (04:15 AM) is deliberately placed outside the
01:00–03:00 window where DST transitions occur, eliminating both the skip
(spring-forward) and the double-run (fall-back) risk.

---

## 9. Schedule reference and next 5 run times

All times are America/Los_Angeles. Times shown with + 0–10 min random jitter.

| Job | OnCalendar | Next 5 base times |
|-----|-----------|-------------------|
| Daily backup | `*-*-* 04:15:00 America/Los_Angeles` | 2026-03-20, 21, 22, 23, 24 at 04:15 PDT |
| Weekly prune | `Sat *-*-* 05:10:00 America/Los_Angeles` | 2026-03-21, 28, Apr-4, 11, 18 at 05:10 PDT |
| Monthly check | `*-*-02 06:20:00 America/Los_Angeles` | Apr-2, May-2, Jun-2, Jul-2, Aug-2 at 06:20 |

Verify on the host:
```bash
systemd-analyze calendar --iterations=5 "*-*-* 04:15:00 America/Los_Angeles"
systemd-analyze calendar --iterations=5 "Sat *-*-* 05:10:00 America/Los_Angeles"
systemd-analyze calendar --iterations=5 "*-*-02 06:20:00 America/Los_Angeles"
```

---

## 10. labvm3 user-level schedule

**User:** bob | **Source:** /home/bob | **Repo:** /mnt/offsite/backups/labvm3-home

Config lives entirely under `~bob/.config/restic-home/` and
`~bob/.config/systemd/user/`. Same retention, timezone, and exclusion rules.

### Install:
```bash
bash install_userlevel_restic.sh \
  --repo /mnt/offsite/backups/labvm3-home \
  --hostname labvm3 \
  --timezone "America/Los_Angeles" \
  --mail-to sre-oncall@example.com \
  --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
  --apply --init-repo --enable-timers --run-initial-backup

# Enable linger so timers fire without login (one-time, needs sudo):
sudo loginctl enable-linger bob
```

### List timers:
```bash
systemctl --user list-timers 'restic-home-*' --no-pager
```

### Manual backup:
```bash
systemctl --user start restic-home-backup.service
journalctl --user -u restic-home-backup.service -n 40 --no-pager
```

### Remove schedule:
```bash
bash install_userlevel_restic.sh --remove
# Config files are preserved; to fully clean:
rm -rf ~/.config/restic-home ~/.local/share/restic-home ~/.local/bin/restic-home-*.sh
```

---

## 11. Restore audit one-time timer

A one-time restore drill is scheduled for **2026-04-17 17:00:00 America/Los_Angeles**.

It restores the latest snapshot to `/tmp/restore-drill`, verifies three canonical
files, reports results, emails `sre-oncall@example.com`, then removes the temp dir.

### Inspect the timer:
```bash
systemctl list-timers restic-home-audit.timer --no-pager
systemctl status restic-home-audit.timer
systemd-analyze calendar "2026-04-17 17:00:00 America/Los_Angeles"
```

### Cancel the timer:
```bash
systemctl disable --now restic-home-audit.timer
```

### Re-schedule for a different date:
```bash
# Edit the OnCalendar line:
systemctl edit --full restic-home-audit.timer
# Then reload:
systemctl daemon-reload && systemctl enable --now restic-home-audit.timer
```

### Run drill immediately (without waiting):
```bash
systemctl start restic-home-audit.service
journalctl -u restic-home-audit.service -f
```

---

## 12. Secrets management

- **Password file** (`/etc/home-backup/password`): root-only (0600). Auto-generated with `openssl rand -base64 48`. Never printed in logs, scripts, or this document. To rotate: delete file, re-run bootstrap with `--apply`.
- **Env file** (`/etc/home-backup/env`): root-only (0600). Contains `RESTIC_REPOSITORY` and `RESTIC_PASSWORD_FILE`. Does not contain the password itself.
- **SSH key for remote access**: root's SSH key (`~root/.ssh/id_ed25519` or similar) must be authorized on `backupsvc@10.50.8.24`. The key should be dedicated and passphrase-free for unattended operation. Restrict it on the server side with `command="rrsync /srv/backups/home/devbox17"` in `authorized_keys`.

---

## 13. Rolling out to additional workstations

```bash
# 1. Copy the skill bundle to the new host
scp -r restic-home-backup/ root@newhostname:/tmp/

# 2. Run plan to review (no changes):
bash /tmp/restic-home-backup/scripts/bootstrap_restic_home.sh \
  --user <username> \
  --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/<newhostname>" \
  --hostname <newhostname>

# 3. Apply:
bash /tmp/restic-home-backup/scripts/bootstrap_restic_home.sh \
  --user <username> \
  --repo "sftp:backupsvc@10.50.8.24:/srv/backups/home/<newhostname>" \
  --hostname <newhostname> \
  --timezone "America/Los_Angeles" \
  --mail-to sre-oncall@example.com \
  --keep-daily 14 --keep-weekly 8 --keep-monthly 12 \
  --apply --init-repo --enable-timers --run-initial-backup \
  --archive-legacy-cron --dry-run-prune

# 4. Validate:
bash /tmp/restic-home-backup/scripts/validate_restic_setup.sh
```

Each host gets its own repository subdirectory and its own password (auto-generated on first run). Passwords are **never shared between hosts**.

Install from ClawHub registry (clean environment):
```bash
npm install -g clawhub
clawhub install restic-home-backup
# Follow SKILL.md instructions
```
