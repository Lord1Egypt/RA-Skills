# Remote Backup Cleanup via SSH

> **⚠️ DESTRUCTIVE OPERATIONS:** All commands in this document delete data permanently. 
> - **Always dry-run first** with `-ls` or `-printf` to verify what will be deleted
> - **Require explicit user confirmation** before running any command with `-delete`
> - Pass `--confirm-dangerous` AND set `SSH_EXECUTOR_ALLOW_DANGEROUS=1` when using `ssh-run.sh` for these commands
> - See `safety.md` for the full confirmation policy

Clean up old backups on remote servers using `find -mtime +N -delete`.

## Basic pattern

```bash
# With ssh-executor (requires SSH_EXECUTOR_ALLOW_DANGEROUS=1 + --confirm-dangerous):
SSH_EXECUTOR_ALLOW_DANGEROUS=1 ssh-run.sh --host <host> --user <user> --vault-key <key> \
    --confirm-dangerous -- 'find /srv/backup -type f -mtime +15 -delete'

# Direct SSH (manual, no guardrails):
ssh <user>@<host> 'find /srv/backup -type f -mtime +15 -delete'
```

The `-delete` flag only works after `-type f` (prevents accidentally deleting directories).

## Permission model — common pitfall

Deleting a file does **not** require write permission on the **file** — it requires write permission (`w`) on the **directory** that contains it.

### Quick diagnosis

```bash
# View complete hierarchy permissions
namei -l /srv/backup/2026-06-13/backup_file.tar.gz
```

### Typical scenario

```
drwxr-xr-x root backup  srv/backup/        # backup group has r-x, missing w
drwxr-xr-x root backup  2026-06-13/        # backup group has r-x, missing w
-rw-r--r-- root backup  file.tar.gz         # group read-only — irrelevant
```

Even if the **remote user** is in the `backup` group (via `groups` or `id`) and the **files** are `root:backup`, deletion fails with `Permission denied` if the directory lacks `w` for the group.

### Solutions (in order of preference)

| Approach | Requirement | Risks |
|-----------|-----------|--------|
| **sudo** | Remote user's sudo password | Simplest, but needs interaction |
| **chmod g+w on directories** | Directory owner or sudo | Permission stays open; requires directory owner |
| **Cron job as root** | Backup service runs as root | Ideal for automated routine |
| **ACL** | Filesystem with ACL support | `setfacl -m g:backup:rwx /srv/backup` |

### Real case example

A common scenario encountered in production:

- Server with backup directories owned by `root:backup`, permissions `drwxr-xr-x`
- The remote user is in the `backup` group but lacks write permission on directories
- Backup files are owned by `root:root` (or `root:backup`)
- Deletion fails without sudo because directories lack `w` for the `backup` group

This is not a file permission issue — it's a **directory write permission** issue.
The solution is sudo, `chmod g+w` on directories, ACLs, or a cron job as root.

## Useful commands

```bash
# Dry-run: list files older than 15 days with size
ssh <host> 'find /srv/backup /archive/backup -type f -mtime +15 -ls'

# Count and total size
ssh <host> 'find /srv/backup /archive/backup -type f -mtime +15 -printf "%s\n" | awk "{sum+=\$1} END {printf \"Files: %d, Size: %.2f GB\n\", NR, sum/1073741824}"'

# Delete (runs as user, fails without write permission on directories)
ssh <host> 'find /srv/backup /archive/backup -type f -mtime +15 -delete'

# Delete with sudo (requires password)
ssh <host> 'sudo find /srv/backup /archive/backup -type f -mtime +15 -delete'
```

## Note on `-delete`

`find ... -delete` implies `-depth`, so it processes subdirectories before parents. Safe for files. For leftover empty directories, a second `find ... -type d -empty -delete` cleans up the remains.
