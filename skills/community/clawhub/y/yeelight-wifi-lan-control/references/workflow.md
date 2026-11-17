# Workflow

## Operation Routing

| User intent | Runtime operation | Confirmation |
| --- | --- | --- |
| Find or refresh lights | `discover`, `devices.refresh` | no write |
| Inspect current state | `inspect`, `device.inspect` | no write |
| Basic light control | semantic light operation | `executionRequested` |
| Rename locally | `device.alias.set`, `device.alias.batch_set` | explicit save |
| Rename on device | `name.set` | explicit device write |
| Rooms | `room.*` | explicit persistent change |
| Groups | `group.*` | explicit persistent change |
| Scenes | `scene.*` | explicit persistent change; apply is a LAN write |
| Recovery | `operation.recover` | recovery confirmation |
| Schedules | `schedule.*` | explicit persistent change; Host owns recurrence |
| Store export/repair/reset | `store.*` | reset/repair require confirmation |

## Selection Rules

Use saved friendly references first. Resolve aliases, rooms, groups, and scenes to
stable device IDs inside the runtime. Refresh stale saved targets before a write. A
new endpoint requires the opaque rebind challenge; do not ask the user to compare raw
IP addresses. If the same ID appears from different senders in one discovery window,
report an identity collision and do not import it.

Expand all selectors before dispatch. One identical idempotent action may be kept
once. Conflicting actions and repeated `toggle`, relative, or flow actions stop the
whole plan before any LAN write.

## Response Shape

Use the runtime envelope fields `status`, `operation`, `devices`, `result`,
`verification`, `warnings`, `nextActions`, and `error`. Present friendly aliases and
models. Keep protocol IDs, endpoints, sender addresses, raw headers, and packets
private.
