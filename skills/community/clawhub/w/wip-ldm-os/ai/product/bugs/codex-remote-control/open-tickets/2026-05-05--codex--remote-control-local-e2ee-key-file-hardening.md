---
title: "Remote Control local E2EE key file persistence should be hardened"
status: open
priority: P2
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Local E2EE Key File Hardening

## Problem

The daemon E2EE private key persists locally under:

```text
~/.codex-daemon/e2ee-key.json
```

The file is chmodded `0600`, which is the right direction, but the persistence path should be hardened.

## Security Review Evidence

Review finding:

```text
P2: local daemon E2EE private-key persistence should be hardened.
```

Source pointer from review:

- `repos/ldm-os/apps/wip-codex-remote-control-private/src/e2ee.ts:24`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/e2ee.ts:106-108`

Additional review note:

- The key write path writes the file, then chmods `0600`.
- There can be a brief window where the file uses default umask permissions.
- Use the write/create mode option, such as `{ mode: 0o600 }`, to set permissions atomically at creation time.

## Expected Behavior

The key file write and read paths are defensive:

- create the file atomically with mode `0600`,
- avoid a world-readable intermediate file,
- verify file mode on read,
- verify owner on read where platform support allows,
- fail closed or repair safely if mode is too permissive,
- keep clear errors actionable without printing private key material.

## Acceptance

- New key file is created with `0600`.
- New key file is created atomically with mode `0600`, not written permissively and chmodded afterward.
- Existing key file with correct owner and `0600` loads.
- Existing key file with overly permissive mode is rejected or repaired safely.
- Atomic write avoids partial/corrupt key file on crash.
- Private key material is never logged.
- Tests cover creation, read, mode verification, and corrupt file behavior.

## Non-Goals

- Do not move keys into hosted storage.
- Do not change the E2EE protocol.
- Do not block Parker-only dogfood on this ticket.
