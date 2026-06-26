# Sentinel Limitations

**What Sentinel doesn't do — be honest about the gaps.**

---

## Not a Full Backup Solution

Sentinel is **not** a replacement for proper backup infrastructure:

- **No cloud backup** — All backups are local. If your disk fails, backups are gone too.
- **No encryption** — Backups are stored as plain files. Use disk encryption if needed.
- **No compression** — Backups consume full file size. Large workspaces = large backup directories.
- **No incremental backups** — Each backup is a full copy. Storage grows with every change.
- **No deduplication** — Identical files in different locations are stored separately.

**Recommendation:** Use Sentinel for fast local recovery. Use a separate tool (rsync, rclone, Backblaze) for off-site archival.

---

## Limited Corruption Detection

Sentinel detects obvious corruption (empty files, hash mismatches), but:

- **No semantic validation** — Won't detect if a JSON file has valid syntax but wrong data
- **No schema checking** — Can't verify if a config file has required fields
- **No content analysis** — Won't detect if your agent's memory suddenly became gibberish
- **No cross-file consistency** — Can't detect if file A and file B are now inconsistent

**Recommendation:** Sentinel catches file-level corruption. You need application-level validation for semantic errors.

---

## Not Real-Time

Sentinel runs on a schedule (default: every 10 minutes):

- **Delayed detection** — Changes won't be detected until next check cycle
- **No instant backup** — File could change 100 times between checks; only last state is backed up
- **No inotify/fswatch** — Doesn't use filesystem watchers (those can miss events during restarts)

**Recommendation:** If you need real-time monitoring, use filesystem watches. Sentinel is for periodic integrity checks.

---

## Process Detection Is Best-Effort

Sentinel tries to avoid backing up files in use, but:

- **Platform differences** — File locking works differently on Windows vs. Unix
- **False positives** — May skip files that aren't actually locked
- **False negatives** — May attempt to back up files that are locked (will fail gracefully)
- **No process identification** — Can't tell which process has a file open

**Recommendation:** If critical files are frequently in use, increase `CHECK_INTERVAL_SECONDS` to reduce contention.

---

## No Network Backup

Sentinel operates on local files only:

- **No remote monitoring** — Can't monitor files on network shares (may be slow/unreliable)
- **No SSH/SFTP** — Can't back up files from remote servers
- **No cloud storage** — Can't directly back up to S3, Dropbox, etc.

**Recommendation:** Use Sentinel locally, then sync backup directory to remote storage separately.

---

## No Version Control Integration

Sentinel is not Git:

- **No branching** — Can't create multiple backup branches
- **No merging** — Can't merge changes from different backups
- **No diffs** — Can't show line-by-line differences (only file-level changes)
- **No blame** — Can't track who/what made a change

**Recommendation:** For code and structured data, use Git. Sentinel is for unversioned state files.

---

## Limited Restore Intelligence

Sentinel restores files, but:

- **No dependency tracking** — Won't restore related files together
- **No timestamp coordination** — Can't restore "all files as they were at 3pm yesterday"
- **No partial restore** — Restores entire file; can't restore specific lines/sections
- **No conflict resolution** — If current file differs from backup, you choose: overwrite or cancel

**Recommendation:** Review restore operations carefully. Sentinel gives you the tools; you make the decisions.

---

## No Automatic Pruning (Yet)

Sentinel respects `MAX_BACKUP_VERSIONS`, but:

- **Not yet implemented** — Current version keeps all backups (pruning is planned)
- **Manual cleanup required** — You'll need to delete old backup directories yourself
- **No retention policy** — Can't auto-delete backups older than X days

**Recommendation:** Monitor backup directory size. Delete old timestamped directories manually when needed.

---

## No Multi-Machine Coordination

Sentinel runs on one machine:

- **No distributed state** — Can't coordinate backups across multiple agents/machines
- **No consensus** — If two machines run Sentinel on the same files, they'll conflict
- **No leader election** — Can't automatically decide which instance is authoritative

**Recommendation:** Run one Sentinel instance per workspace. Don't share state files across machines.

---

## No Rollback of Directory Moves

Sentinel tracks files, not directory structure:

- **No directory rename tracking** — If you rename a directory, Sentinel sees deleted + new files
- **No move detection** — Can't tell if file was moved vs. deleted + recreated
- **No bulk restore** — Can't restore an entire directory tree as it was

**Recommendation:** Use `sentinel_manifest.py` to snapshot directory structure before major reorganizations.

---

## What Sentinel Is

Sentinel is a **safety net**, not a silver bullet. It prevents catastrophic data loss from common failures (accidental deletes, file corruption, bad edits). It doesn't replace proper backup infrastructure, version control, or application-level validation.

**Use Sentinel for:** Fast recovery from local file failures.

**Don't use Sentinel for:** Long-term archival, disaster recovery, distributed systems, version control.

---

## Planned Improvements

Features we're considering for future releases:

- Automatic backup pruning based on retention policy
- Webhook alerts for integrations (Slack, Discord, email)
- Compression for backup storage
- Encrypted backup support
- Filesystem watch mode (real-time monitoring)
- Cross-file consistency rules
- Partial file restore (line-level recovery)

No promises. Sentinel is open source (MIT). Contributions welcome.
