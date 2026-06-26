# Storage and Shares

Use this file when the problem touches volumes, capacity, shared folders, permissions, snapshots, or migration between disks and volumes.

## Read-Only Preflight

Collect these facts before proposing a storage change:

```bash
cat /etc.defaults/VERSION
uname -a
df -h
df -i
cat /proc/mdstat
mount
```

From DSM, also capture:
- Storage Manager health and the active parity check or repair state
- volume filesystem and free-space percentage
- shared folder list, encryption state, and recycle-bin rules
- snapshot policy and recent backup status

## Capacity Logic

- Full volume beats almost every abstract performance theory. If free space is collapsing, solve that first.
- Separate raw disk size, usable pool capacity, volume free space, and snapshot retention. These are not the same number.
- Large thumbnail or indexing backlogs can hide as storage pressure and I/O contention, not just CPU issues.

## Shared Folder Changes

- Confirm whether the folder is user-facing, package-managed, or a backup target before changing permissions.
- Prefer additive changes first: new group, test account, temporary share, or new destination folder.
- If a permission rewrite is unavoidable, record current groups, ACL intent, and the rollback plan before touching anything.

## Snapshot and Btrfs Guidance

- Do not promise snapshot workflows until filesystem and package support are verified on the target NAS.
- Snapshots help with short-window rollback and ransomware containment, but they do not replace off-device backup.
- When pruning snapshots, check business retention needs first or you may destroy the only usable rollback point.

## Migration Sequence

For volume, shared-folder, or disk migrations:

1. Confirm current backup freshness and restore path.
2. State the target layout and what packages depend on the current path.
3. Move the least critical data first when possible.
4. Validate package behavior and permissions before moving the next workload.
5. Keep the old location intact until the new path is verified.

## Red Flags

- Volume above roughly 85 percent used
- ongoing parity check, scrub, or repair during another risky change
- shared folder used by Drive, Photos, backup, or containers without dependency mapping
- delete plan without snapshot, backup, or file-level restore proof
