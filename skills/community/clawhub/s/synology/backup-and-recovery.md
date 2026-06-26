# Backup and Recovery

Use this file when the user asks about Hyper Backup, snapshots, rsync, migration, ransomware response, or restoration.

## Backup Layers

- Hyper Backup is for versioned backup and destination-aware restore workflows.
- Snapshot Replication is for faster local rollback and replication where supported.
- Rsync or external copies help when the target must be readable outside Synology tooling.
- Synology Drive sync is sync, not backup. Treat it as a convenience layer, not a recovery guarantee.

## Recovery-First Questions

Ask these before changing anything:

- What data matters most if only one workload can be restored first?
- What is the newest backup that has actually completed?
- Has any restore path been tested, even partially?
- Is the incident deletion, corruption, ransomware, failed upgrade, or hardware loss?

## Containment Rules

- On suspected ransomware or bad sync, stop automated sync or replication before it overwrites healthy copies.
- Do not start cleanup, dedupe, or mass deletes until a recovery snapshot of the situation exists.
- Preserve evidence of what changed and when before re-enabling jobs.

## Restore Order

Prefer the smallest successful restore over the biggest heroic restore:

1. Restore one file or one folder to prove the path works.
2. Validate permissions and application behavior.
3. Restore the highest-value workload next.
4. Only then broaden to full-share or full-system recovery.

## Hyper Backup Checklist

- Verify source share or package coverage, not just job existence.
- Verify destination reachability and available space.
- Verify the last successful run and whether failures are repeating.
- Verify encryption and key-handling expectations before disaster day.

## Snapshot Checklist

- Confirm filesystem and package support before promising snapshot-based recovery.
- Check retention depth and replication lag.
- Confirm whether rollback affects live services that write constantly.
- If using snapshots for ransomware response, isolate the threat path before restore.

## What Never Counts as Backup

- SHR or RAID alone
- a single USB disk that is never checked
- cloud sync without versioning
- snapshot-only plans on the same failure domain
- untested backup jobs
