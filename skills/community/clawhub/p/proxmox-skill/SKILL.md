---
name: proxmox
description: "Manage Proxmox VE nodes, VMs, and containers. Can list hardware stats, resources, control power states (start, stop, reboot, shutdown), and manage snapshots (create, list, rollback, delete)."
metadata:
  requires:
    bins: ["python3"]
    python: ["proxmoxer>=2.0.0", "requests>=2.0.0"]
  env: ["PVE_HOST", "PVE_TOKEN_ID", "PVE_TOKEN_SECRET"]
---

# Proxmox Skill

This skill allows the agent to interact with a Proxmox VE cluster to manage virtual machines and containers.

## Tools

### proxmox_list
List Proxmox nodes or all available VMs and containers across the entire cluster.
- Command: python3 {{skillDir}}/scripts/proxmox.py {{type}}
- Args:
  - type: "nodes" or "vms"

### proxmox_node_health
Get hardware-level health stats (CPU usage, RAM, Uptime, Version) for a specific physical node.
- Command: python3 {{skillDir}}/scripts/proxmox.py node_health {{node}}
- Args:
  - node: The name of the Proxmox host (e.g., "pve" or "hydra")

### proxmox_status
Get the real-time status of a specific VM or container.
- Command: python3 {{skillDir}}/scripts/proxmox.py status {{node}} {{kind}} {{vmid}}
- Args:
  - node: The Proxmox node name where the resource lives
  - kind: "qemu" for VMs, "lxc" for containers
  - vmid: The numerical ID of the resource (e.g., "100")

### proxmox_power_action
Perform power management actions. These actions require human approval by default.
- Approval: true
- Command: python3 {{skillDir}}/scripts/proxmox.py {{action}} {{node}} {{kind}} {{vmid}}
- Args:
  - action: "start", "stop", "reboot", or "shutdown"
  - node: The Proxmox node name
  - kind: "qemu" or "lxc"
  - vmid: The ID of the resource

### proxmox_list_snapshots
List all snapshots for a specific VM or container.
- Command: python3 {{skillDir}}/scripts/proxmox.py list_snapshots {{node}} {{kind}} {{vmid}}
- Args:
  - node: The Proxmox node name
  - kind: "qemu" or "lxc"
  - vmid: The ID of the resource

### proxmox_take_snapshot
Create a new snapshot of a VM or container.
- Approval: true
- Command: python3 {{skillDir}}/scripts/proxmox.py take_snapshot {{node}} {{kind}} {{vmid}} {{snapname}} {{description}}
- Args:
  - node: The Proxmox node name
  - kind: "qemu" or "lxc"
  - vmid: The ID of the resource
  - snapname: Snapshot name (alphanumeric, dashes, underscores; no spaces)
  - description: Optional description of the snapshot

### proxmox_rollback_snapshot
Roll a VM or container back to a previously taken snapshot. Destructive — discards changes since the snapshot.
- Approval: true
- Command: python3 {{skillDir}}/scripts/proxmox.py rollback_snapshot {{node}} {{kind}} {{vmid}} {{snapname}}
- Args:
  - node: The Proxmox node name
  - kind: "qemu" or "lxc"
  - vmid: The ID of the resource
  - snapname: Name of the snapshot to roll back to

### proxmox_delete_snapshot
Delete a snapshot. Destructive — the snapshot cannot be recovered.
- Approval: true
- Command: python3 {{skillDir}}/scripts/proxmox.py delete_snapshot {{node}} {{kind}} {{vmid}} {{snapname}}
- Args:
  - node: The Proxmox node name
  - kind: "qemu" or "lxc"
  - vmid: The ID of the resource
  - snapname: Name of the snapshot to delete
