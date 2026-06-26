# Proxmox VE command and auth reference

Use this file when the task needs a slightly wider map of common PVE commands, remote API patterns, or troubleshooting context.

## Read-only discovery map

Cluster and nodes:

```bash
pvesh get /version
pvesh get /cluster/status
pvesh get /cluster/resources
pvesh get /nodes
pvesh get /nodes/<node>/status
```

Guests by type:

```bash
pvesh get /nodes/<node>/qemu
pvesh get /nodes/<node>/lxc
qm list
pct list
```

Guest details:

```bash
qm status <vmid>
qm config <vmid>
pct status <vmid>
pct config <vmid>
pvesh get /nodes/<node>/qemu/<vmid>/status/current
pvesh get /nodes/<node>/lxc/<vmid>/status/current
```

Recent tasks:

```bash
pvesh get /nodes/<node>/tasks --limit 20
```

## Common lifecycle commands

QEMU:

```bash
qm start <vmid>
qm shutdown <vmid>
qm stop <vmid>
qm reboot <vmid>
qm reset <vmid>
```

LXC:

```bash
pct start <vmid>
pct shutdown <vmid>
pct stop <vmid>
pct reboot <vmid>
```

Prefer graceful actions first. Use hard-stop style commands only when clearly intended.

## Snapshots

QEMU:

```bash
qm listsnapshot <vmid>
qm snapshot <vmid> <name>
qm delsnapshot <vmid> <name>
qm rollback <vmid> <name>
```

LXC:

```bash
pct listsnapshot <vmid>
pct snapshot <vmid> <name>
pct delsnapshot <vmid> <name>
pct rollback <vmid> <name>
```

## Remote API pattern

Prefer `pvesh` on the host when available. If the task explicitly requires HTTP API usage, keep examples generic and secret-safe.

API token auth example:

```bash
export PVE_HOST='proxmox.example.com:8006'
export PVE_USER='automation@pam'
export PVE_TOKEN_ID='automation'
export PVE_TOKEN_SECRET='replace-me'
export PVE_AUTH_HEADER="PVEAPIToken=${PVE_USER}!${PVE_TOKEN_ID}=${PVE_TOKEN_SECRET}"

curl -sk \
  -H "Authorization: ${PVE_AUTH_HEADER}" \
  "https://${PVE_HOST}/api2/json/nodes"
```

Notes:
- Do not echo real token values back into chat.
- `-k` is common in labs with self-signed certs; prefer valid TLS where possible.
- For write operations through the API, confirm the intended endpoint and method before running anything destructive.

## Troubleshooting checklist

1. Confirm you are on a Proxmox host or have valid remote access.
2. Run `pveversion` and `pvesh get /version`.
3. Discover nodes with `pvesh get /nodes` before building deeper paths.
4. Confirm whether the target is QEMU (`qm`) or LXC (`pct`).
5. Check current guest state before lifecycle actions.
6. Check recent tasks if a command appears to hang or already ran.
7. Re-check state after each mutation.
