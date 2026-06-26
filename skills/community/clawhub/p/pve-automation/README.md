# pve-automation

English | [简体中文](./README.zh-CN.md)

A Proxmox VE (PVE) automation repository with two layers:

1. A runnable Python API client/CLI (`scripts/pve_client.py`)
2. A Codex skill document for broader PVE automation workflows (`SKILL.md`)

This repository is not just a few demo commands. It provides an extensible PVE automation foundation plus practical operations guidance.

## Repository Structure

- `scripts/pve_client.py`: executable API client and CLI
- `SKILL.md`: PVE automation capabilities, API workflows, and best practices
- `evals/evals.json`: evaluation metadata

## Implemented Capabilities (Code Layer)

`PVEClient` currently implements the following API operations:

- Node operations
  - `list_nodes`
  - `get_node_status`
- VM (QEMU) operations
  - `list_vms`
  - `get_vm_status`
  - `start_vm`
  - `stop_vm`
  - `shutdown_vm`
  - `reset_vm`
  - `create_vm`
  - `delete_vm`
  - `clone_vm`
- LXC container operations
  - `list_containers`
  - `get_container_status`
  - `start_container`
  - `stop_container`
  - `create_container`
  - `delete_container`
- Task operations
  - `get_task_status`
  - `wait_for_task`
- Storage operations
  - `list_storage`
  - `get_storage_content`
- Cluster operations
  - `get_cluster_resources`
  - `get_cluster_status`
- Snapshot operations
  - `list_snapshots`
  - `create_snapshot`
  - `rollback_snapshot`

### Implemented CLI Commands

The current CLI supports:

- `list-nodes`
- `list-vms <node>`
- `list-containers <node>`
- `start-vm <node> <vmid>`
- `stop-vm <node> <vmid>`
- `create-vm <node> --vmid ... --name ... [--memory] [--cores] [--storage] [--disk] [--net] [--iso]`
- `wait-task <node> <upid> [--timeout]`

## Skill Coverage (Workflow/Documentation Layer)

`SKILL.md` covers a broader PVE automation scope, including:

- Authentication and connectivity
  - API token auth
  - Ticket/CSRF auth
  - custom API port handling
- Core resource operations
  - nodes, VMs, LXCs, cluster status, tasks
- Templates and images
  - template listing, download, aplinfo usage
- Cloud-init
  - configuration strategy for `ciuser`, `cipassword`, `ipconfig`, `cicustom`, etc.
- Snapshots and backups
  - VM snapshot create/rollback
  - backup create/restore/cleanup/query
- Storage and networking
  - storage content workflows, upload paths, network parameter conventions
- Safety and reliability
  - resource checks (capacity/quota)
  - dry-run strategy for batch operations
  - common error patterns and handling
- Advanced ops workflows (API-level)
  - HA (High Availability)
  - live migration
  - PCI/GPU passthrough configuration
  - scheduled jobs (for example backup plans)
  - permissions (users/roles/API tokens)
  - notifications (webhooks/targets/matchers)
  - replication
  - firewall (node-level and VM-level)
  - storage configuration
  - certificate and ACME plugin management
  - node maintenance operations

Note: some items in "Skill Coverage" are documented workflows and API guidance, not CLI one-liners yet. You can extend `scripts/pve_client.py` with additional subcommands as needed.

## Requirements

- Python 3.9+
- `requests`
- `urllib3`

Install dependencies:

```bash
pip install requests urllib3
```

## Authentication Parameters

Supported environment variables:

- `PVE_HOST`: PVE host or IP
- `PVE_USER`: PVE user (default: `root@pam`)
- `PVE_TOKEN_ID`: API token ID
- `PVE_SECRET`: API token secret

Example:

```bash
export PVE_HOST=192.168.1.10
export PVE_USER=root@pam
export PVE_TOKEN_ID=automation
export PVE_SECRET=your-token-secret
```

You can also override via CLI globals:

```bash
python scripts/pve_client.py --host 192.168.1.10 --user root@pam --token-id automation --token-secret 'xxx' list-nodes
```

## Quick Examples

```bash
# 1) List nodes
python scripts/pve_client.py list-nodes

# 2) List VMs on a node
python scripts/pve_client.py list-vms pve-node-1

# 3) Create a VM
python scripts/pve_client.py create-vm pve-node-1 \
  --vmid 120 \
  --name test-vm \
  --memory 4096 \
  --cores 2 \
  --storage local-lvm \
  --disk 32 \
  --net 'virtio,bridge=vmbr0'

# 4) Start VM
python scripts/pve_client.py start-vm pve-node-1 120
```

## Use as a Python Library

```python
from scripts.pve_client import PVEClient

client = PVEClient()

# Cluster resources
resources = client.get_cluster_resources()

# VM snapshot
client.create_snapshot('pve-node-1', 120, 'before-upgrade')
```

## Production Notes

- Current implementation uses `verify=False` (SSL verification disabled), suitable only for trusted internal environments
- For production, use valid certificates and enable SSL verification
- Apply least-privilege principles to API tokens; avoid over-privileged root tokens
