# Proxmox Multi-Control

Manage one or many Proxmox VE hosts from a single OpenClaw agent.

## Features

- **Multi-host**: Manage multiple standalone Proxmox servers from one config
- **Cluster commands**: `cluster-vms`, `cluster-status` across ALL hosts
- **Power control**: Start, stop, reboot, shutdown VMs/containers
- **Snapshots**: Create, list, delete, rollback (with optional RAM state)
- **Backups**: List backups per node/storage
- **Storage**: View storage pools and content
- **Tasks**: Track async operations and logs
- **Backward compatible**: Works with single-host env vars too

## Quick Start

### 1. Create API Token

On each Proxmox host:
1. Login to Proxmox web UI (`https://<ip>:8006`)
2. Datacenter → Permissions → API Tokens → Add
3. Choose a user and token name
4. Copy the secret (shown only once!)

> **Security tip:** Create a dedicated user with only the permissions you need.

### 2. Configure

**Multi-host** — create `~/.openclaw/credentials/proxmox.json`:

```json
{
  "default": "production",
  "hosts": {
    "production": {
      "host": "192.168.1.100",
      "token_id": "admin@pve!agent",
      "token_secret": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "verify_ssl": false
    },
    "backup-server": {
      "host": "192.168.1.101",
      "token_id": "admin@pve!agent",
      "token_secret": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
      "verify_ssl": false
    }
  }
}
```

```bash
chmod 600 ~/.openclaw/credentials/proxmox.json
```

**Single host** — or just set env vars:

```bash
export PVE_HOST="192.168.1.100"
export PVE_TOKEN_ID="admin@pve!agent"
export PVE_TOKEN_SECRET="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 3. Use

```bash
python3 scripts/proxmox.py hosts           # list configured hosts
python3 scripts/proxmox.py cluster-vms     # VMs across ALL hosts
python3 scripts/proxmox.py cluster-status  # health of ALL hosts
python3 scripts/proxmox.py --host backup-server vms  # target specific host
```

## Requirements

- Python 3
- `proxmoxer` (`pip install proxmoxer`)

## License

MIT
