# Restic Home Backup — Ops Checklist

## Daily checks
- `systemctl list-timers restic-home-backup.timer --no-pager`
- `tail -30 /var/log/home-backup/backup.log`  (look for `exit=0`)
- `journalctl -u restic-home-backup.service -n 40 --no-pager`
- `source /etc/home-backup/env && restic snapshots --group-by host`
- `[[ -f /run/restic-home-backup-retry-pending ]] && echo "RETRY PENDING"`

## Weekly checks
- `systemctl list-timers restic-home-prune.timer --no-pager`
- `tail -40 /var/log/home-backup/prune.log`
- Verify snapshot count aligns with retention (14d / 8w / 12m).

## Monthly checks
- `systemctl list-timers restic-home-check.timer --no-pager`
- `tail -60 /var/log/home-backup/check.log`  (look for `no errors were found`)
- Perform restore drill (see below).

## Restore drill
```bash
source /etc/home-backup/env
DRILL=/tmp/restore-drill
rm -rf "$DRILL" && mkdir -p "$DRILL"
restic restore latest --target "$DRILL"
for f in .ssh/config Documents/roadmap.md .config/git/config; do
  [[ -f "$DRILL/home/alice/$f" ]] && echo "PRESENT: $f" || echo "ABSENT: $f"
done
rm -rf "$DRILL"
```

## Common failures

### Wrong password
- Pattern: `wrong password or no key found`
- Check: `RESTIC_PASSWORD_FILE` path in `/etc/home-backup/env` is correct.
- Fix: `chmod 600 /etc/home-backup/password`

### Repo unreachable
- Pattern: `connection refused` / `no route to host` / `ssh: connect`
- Check: `ssh backupsvc@10.50.8.24 echo ok`
- Fix: verify network, SSH key authorization, firewall rules.

### Env file unreadable
- Pattern: `permission denied` mentioning env or password path
- Fix: `chmod 600 /etc/home-backup/env /etc/home-backup/password && chown root:root ...`

### DST / time not found (legacy cron only — does not apply to systemd timers)
- Symptom: job skipped on day of spring-forward (e.g., 2026-03-08)
- Root cause: cron does not catch up missed runs; 02:30 AM did not exist
- Fix: already resolved — new schedule is 04:15 AM (outside DST window) with `Persistent=true`

## Manual operations

```bash
# Run backup now:
systemctl start restic-home-backup.service

# Run prune dry-run (no deletion):
source /etc/home-backup/env
restic forget --dry-run --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --group-by "host,paths"

# Run integrity check:
systemctl start restic-home-check.service

# View all timers:
systemctl list-timers 'restic-home-*' --no-pager

# All logs:
ls -lh /var/log/home-backup/
```

## Safety reminders
- Never run `restic forget --prune` without reviewing `--dry-run` first.
- Never delete repository data without explicit user confirmation.
- The password file is auto-generated and never displayed; store it in your secrets vault separately.
- Keep SSH key for `backupsvc@10.50.8.24` in root's authorized_keys on the backup server with minimal permissions.
