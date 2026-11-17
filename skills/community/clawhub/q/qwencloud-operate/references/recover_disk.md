# Recover: Reclaim Disk Space

Applies when the root filesystem is near full and the app cannot write or start. Only safe,
non-destructive reclaim — never touch application data or the database.

## Inspect first (read-only)

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 \
  --CommandContent "$(printf '%s' 'df -h /; du -xh --max-depth=1 /var/log 2>/dev/null | sort -rh | head; journalctl --disk-usage' | base64)"
aliyun ecs DescribeInvocations --RegionId <region> --InvokeId <invoke-id> --IncludeOutput true
```

## Confirmation gate

- Target: root filesystem on ECS `<ecs-id>` in `<region>`.
- Action: truncate rotated logs and vacuum the journal; clear build caches. State the estimated
  space to reclaim from the inspection.
- Interruption: none.
- Version change: none.
- New cost: none.
- Data safety: application directories, databases, and certificates are never touched.
- Verification: `df -h /` shows headroom; app writes/starts again.
- If it fails: report and stop.

Decline → change nothing.

## Execute (one whitelisted command)

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 \
  --CommandContent "$(printf '%s' 'journalctl --vacuum-size=200M; truncate -s 0 /var/log/nginx/*.log 2>/dev/null; rm -rf /tmp/qwencloud-* /root/.cache/pip /usr/local/share/.cache/yarn 2>/dev/null; df -h /' | base64)"
```

Idempotent. Never `rm` under the app directory or any data path. Then verify and record the audit
entry (`workflow.md`).

## Still short after cleanup → resize the root disk (billed, strong confirmation)

Applies only when `df -h /` is still near full after the cleanup above and the root disk is
physically too small. Resizing **increases cost** and needs strong confirmation.

Get the root disk ID:

```bash
aliyun ecs DescribeInstances --RegionId <region> --InstanceIds '["<ecs-id>"]'
```

Read the system disk's `DiskId` (or use `aliyun ecs DescribeDisks --InstanceId <ecs-id>`).

### Confirmation gate

- Target: root disk `<disk-id>` of ECS `<ecs-id>`.
- Action: resize to `<new-size>` GB (`ResizeDisk`).
- Interruption: online resize usually needs no reboot; the in-instance filesystem must be grown
  afterward to take effect.
- Version change: none.
- New cost: **yes** — the disk is billed at the larger size. State the expected change clearly.
- Verify: `DescribeDisks` shows the new size; after growing the filesystem, `df -h /` shows free
  space.
- On failure: report and stop.

Decline → change nothing.

### Execute (one action)

```bash
aliyun ecs ResizeDisk --RegionId <region> --DiskId <disk-id> --NewSize <new-size> --Type online
```

After resizing the cloud disk, grow the filesystem inside the instance (`growpart` +
`resize2fs`/`xfs_growfs`) via the `RunCommand` whitelist with its own confirmation. Then verify
and record the audit (`workflow.md`).
