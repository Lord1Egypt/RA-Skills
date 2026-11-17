# Server-to-Server rsync via Temporary Key

> **⚠️ SECURITY WARNING — DEPRECATED PATTERN**
>
> Copying a private SSH key to a remote server (even temporarily) is a **credential staging vulnerability**. If the remote server is compromised, the attacker gains access to all servers that key can authenticate to.
>
> **Preferred alternatives (in order):**
> 1. **SSH tunneled with ForwardAgent** (section below) — no key copy, keys stay on client
> 2. **Pull-via-jump** (section below) — data passes through client, no key on remote
> 3. **Temporary key copy** — LAST RESORT, only with a dedicated single-purpose key that has minimal access
>
> **If you must use the temporary key pattern:**
> - Create a **dedicated single-purpose key** with access ONLY to the destination server
> - Never use your primary key
> - Verify cleanup: `ssh server-a 'ls -la /tmp/transfer_key'` after rsync
> - The key file WILL PERSIST if the process is interrupted (kill -9, network drop, crash)

When you need to sync data **between two remote servers** but local
ForwardAgent is not working (no ssh-agent running) and you have no root
to install rsync locally.

## Step Zero: Verify source and destination

Before running rsync, **always confirm**:

1. **The source path exists** on server A — the user might refer to a
   path that no longer exists (e.g. `/var/www/html` changed to `/var/www/`):
   ```bash
   ssh user@server-a 'ls -la /path/source/' 2>&1
   ```
   If it fails, inspect `/var/www/` or `/srv/` to find the actual structure.

2. **The destination directory is writable** by the user on server B:
   ```bash
   ssh -p <PORT> user@server-b 'touch /path/dest/.test_write && rm /path/dest/.test_write' 2>&1
   ```
   If it fails (Permission denied):
   - Try `sudo mkdir -p /path/dest/` (some servers have NOPASSWD)
   - If sudo **also** fails (needs password), **use an alternative path**
     where the user already has write permission (e.g. `~/backup/` or
     `/home/user/backup/`)
   - Inform the user about the alternative path and offer future adjustment

## The Problem

```
You (client)
  ├── have the SSH key on disk
  ├── NO ssh-agent running
  └── CANNOT install packages (no sudo/root)
       │
       ▼
   Server A ──── ??? ────► Server B
   (source)                (destination)
```

`rsync` does not support two remote destinations directly. ForwardAgent
does not work if there is no agent running locally to forward.

**⚠️  Do NOT copy private keys to remote servers.** See the safe variants below.

## Variants

### Via SSH tunneled with ForwardAgent (preferred)

If ssh-agent is running and server-a accepts ForwardAgent:

```bash
ssh -A user@server-a \
  'rsync -avz -e "ssh -p <DEST_PORT> -o StrictHostKeyChecking=yes" \
     /path/source/ \
     user@server-b:/path/dest/'
```

### Pull via jump (data passes through client)

When the above is not viable (e.g. server-a has no rsync):

```bash
# Pull from server-a to local /tmp/
rsync -avz -e "ssh -i ~/.ssh/your-key" \
  user@server-a:/path/source/ /tmp/staging/

# Push from local /tmp/ to server-b
rsync -avz -e "ssh -i ~/.ssh/your-key -p <PORT>" \
  /tmp/staging/ user@server-b:/path/dest/

# Clean up staging
rm -rf /tmp/staging
```

⚠️ **Downside:** all traffic passes through the client twice.

<details>
<summary>⚠️  DANGEROUS: Temporary key copy (LAST RESORT — click to expand)</summary>

> **🚫  CREDENTIAL STAGING VULNERABILITY — READ BEFORE USING**
>
> Copying a private SSH key to a remote server (even temporarily) exposes
> credentials to a host you may not fully trust. If server-a is compromised,
> the attacker gains access to every server that key can authenticate to.
>
> **Only proceed if ALL of the following are true:**
> - [ ] You created a **dedicated single-purpose key** with access ONLY to server-b
> - [ ] Your primary key is NOT used — this is a throwaway key scoped to one destination
> - [ ] ForwardAgent and pull-via-jump are genuinely impossible
> - [ ] You have explicit user approval
> - [ ] You will verify cleanup: `ssh server-a 'ls -la /dev/shm/transfer_key'` after rsync
>
> **The key file WILL PERSIST if the process is interrupted** (kill -9, network drop, crash).

```bash
# 1. Copy the key to the source server (use /dev/shm, not /tmp)
scp ~/.ssh/single-purpose-key user@server-a:/dev/shm/transfer_key

# 2. Set correct permission (SSH requires 600)
ssh user@server-a 'chmod 600 /dev/shm/transfer_key'

# 3. Execute rsync from server-a → server-b
ssh user@server-a \
  'rsync -avz --delete --progress \
     -e "ssh -i /dev/shm/transfer_key -p <DEST_PORT> -o StrictHostKeyChecking=yes" \
     /path/source/ \
     user@<SERVER_B>:/path/dest/'

# 4. Remove the temporary key and verify
ssh user@server-a 'shred -u /dev/shm/transfer_key && echo "CLEANUP VERIFIED"'
```

</details>

## Pitfalls

| Problem | Cause | Solution |
|----------|-------|---------|
| `Permission denied` at step 3 | Key does not have 600 permission on server A | Run `chmod 600 /dev/shm/transfer_key` |
| `rsync: command not found` (local) | Client without rsync, no sudo | Use pull-via-jump instead |
| `IO error encountered -- skipping file deletion` | File with denied permission on source server (e.g. Docker volume) | Ignore — `--delete` skips, remove manually if needed |
| False positive: `--delete` flagged as MEDIUM risk | Tool detects `rsync --delete` as destructive | Explain it's a mirror (not a wipe), ask for approval |
| `rsync error: some files/attrs were not transferred (code 23)` | Docker volumes (pgdata, db/mysql) without read permission | Normal for volumes — source code was transferred; verify with `du -sh` |
| Key cleanup fails and key stays on server A | Script interrupted mid-way | Always verify after: `ssh server-a 'ls -la /dev/shm/transfer_key'` |

## Checklist

- [ ] Does server A have `rsync` installed? (99% of Linux servers do)
- [ ] Does the SSH alias resolve? Test with `ssh <alias> 'echo OK'` before scp
- [ ] Does the copied key have 600 permission?
- [ ] After rsync, was the key removed?
- [ ] Verify destination with `ls -la` + `du -sh`
- [ ] Does server A have outbound access to server B (firewall?)
- [ ] Does the source path exist? (confirm with `ls -la` before rsync)
