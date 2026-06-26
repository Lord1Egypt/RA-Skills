---
name: proxmox-ve
description: Use Proxmox VE (PVE) through the `pvesh`, `qm`, and `pct` CLIs for cluster, node, VM, and LXC inspection plus routine lifecycle work. Trigger when tasks mention Proxmox, PVE, qemu guests, LXC containers, snapshots, node status, VM/container start-stop-restart actions, or API-style paths such as `/nodes`, `/cluster`, `/qemu`, or `/lxc`.
---

# Proxmox VE

Use the local Proxmox CLI first. Prefer read-only inspection before any mutating action, and confirm before stopping guests, rolling back snapshots, or changing configuration.

## Safe workflow

1. Verify the environment and auth context.
2. Discover nodes and guests with read-only commands.
3. Check current state before proposing an action.
4. Perform the smallest requested mutation.
5. Re-check status and report what changed.

Start with lightweight inspection:

```bash
pveversion
hostname
pvesh get /version
pvesh get /nodes
pvesh get /cluster/status
```

If the user did not specify a node, discover it first instead of guessing.

## Read-first inspection

List nodes:

```bash
pvesh get /nodes
```

List QEMU VMs on a node:

```bash
pvesh get /nodes/<node>/qemu
qm list
```

List LXC containers on a node:

```bash
pvesh get /nodes/<node>/lxc
pct list
```

Inspect a specific VM or container:

```bash
qm status <vmid>
qm config <vmid>
pct status <vmid>
pct config <vmid>
```

If the user only gives a VMID and not the guest type, identify it first instead of guessing:

```bash
qm list
pct list
pvesh get /cluster/resources --type vm
```

Useful cluster and node checks:

```bash
pvesh get /cluster/resources
pvesh get /nodes/<node>/status
pvesh get /nodes/<node>/tasks --limit 10
```

Prefer JSON when the output will be parsed or compared:

```bash
pvesh get /nodes --output-format json
pvesh get /nodes/<node>/qemu --output-format json
```

## Guest lifecycle actions

Check state first, then act.

Recommended sequence:
1. Identify the node and guest type.
2. Check current guest status.
3. Confirm the exact action if it is disruptive.
4. Run the smallest matching command.
5. Re-check status and report the result.

QEMU VM actions:

```bash
qm start <vmid>
qm stop <vmid>
qm shutdown <vmid>
qm reboot <vmid>
qm reset <vmid>
```

LXC container actions:

```bash
pct start <vmid>
pct stop <vmid>
pct shutdown <vmid>
pct reboot <vmid>
```

Guidance:
- Prefer `shutdown`/`reboot` for graceful operations.
- Use `stop` only when the user explicitly wants a forced stop or graceful shutdown is not working.
- Mention whether the target is a QEMU VM (`qm`) or LXC container (`pct`) before running the command.

## Snapshot workflow

Inspect snapshots before creating, deleting, or rolling back.

QEMU snapshots:

```bash
qm listsnapshot <vmid>
qm snapshot <vmid> <snapshot-name>
qm delsnapshot <vmid> <snapshot-name>
qm rollback <vmid> <snapshot-name>
```

LXC snapshots:

```bash
pct listsnapshot <vmid>
pct snapshot <vmid> <snapshot-name>
pct delsnapshot <vmid> <snapshot-name>
pct rollback <vmid> <snapshot-name>
```

Rules:
- Confirm before `rollback` or `delsnapshot`.
- Use clear, generic snapshot names in examples such as `pre-update` or `before-maintenance`.
- Report post-action status after snapshot operations.

## API-style access with `pvesh`

Use `pvesh` when the user asks for API-like inspection or when you need structured output without hand-building HTTP requests.

Examples:

```bash
pvesh get /cluster/resources
pvesh get /nodes/<node>/qemu/<vmid>/status/current
pvesh get /nodes/<node>/lxc/<vmid>/status/current
```

Use `pvesh usage <path>` to discover parameters for less common endpoints:

```bash
pvesh usage /nodes/<node>/qemu/<vmid>/status/current -v
```

Read `references/commands-and-auth.md` when the task needs API token guidance, remote API examples, or a broader command map.

## Bundled scripts

Use the bundled Python helpers when the user wants reusable code or a minimal scriptable PVE API client.

Scripts:
- `scripts/pve_api.py` — generic GET/POST helper for API paths
- `scripts/list_nodes.py` — list nodes
- `scripts/list_guests.py <node> [--kind qemu|lxc|all]` — list guests on a node
- `scripts/guest_status.py <node> <qemu|lxc> <vmid>` — fetch current status

Expected environment variables:

```bash
export PVE_HOST='proxmox.example.com'
export PVE_USER='automation@pam'
export PVE_TOKEN_ID='automation'
export PVE_TOKEN_SECRET='replace-me'
```

Example usage:

```bash
python3 {baseDir}/scripts/list_nodes.py
python3 {baseDir}/scripts/list_guests.py pve-node-1 --kind all
python3 {baseDir}/scripts/guest_status.py pve-node-1 qemu 100
python3 {baseDir}/scripts/pve_api.py /cluster/resources
```

## Auth and environment guidance

On a Proxmox host, local CLI access is often enough:

```bash
whoami
pveversion
pvesh get /version
```

For remote API usage, prefer environment variables over hardcoding secrets:

```bash
export PVE_HOST='proxmox.example.com'
export PVE_USER='automation@pam'
export PVE_REALM='pam'
export PVE_TOKEN_ID='automation'
export PVE_TOKEN_SECRET='replace-me'
```

Do not print or paste real secrets back into chat. If credentials are missing, ask for them or ask the user to authenticate locally.

## Guardrails

- Do not assume VMID ownership or guest purpose from the numeric ID alone.
- Do not reboot, stop, reset, roll back, or delete without explicit user intent.
- Prefer node and guest discovery commands before suggesting actions.
- After any mutation, run a status check and summarize the result.
- If the task expands into storage, networking, clustering changes, or backup jobs, inspect first and ask before editing.
