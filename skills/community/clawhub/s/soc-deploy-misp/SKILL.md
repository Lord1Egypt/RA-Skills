---
name: soc-deploy-misp
version: 1.0.0
description: "Deploy MISP threat intelligence platform on any Docker-ready Linux host. Official misp-docker project with automatic MariaDB memory tuning (prevents OOM on small VMs), API key generation via cake CLI, and credential management."
tags:
  - soc
  - misp
  - threat-intelligence
  - security
  - docker
  - automation
  - ioc
category: security
---

# SOC Deploy: MISP (Malware Information Sharing Platform)

Deploy MISP threat intelligence platform on any Docker-ready Linux host using the official misp-docker project.

**This skill does NOT create VMs.** It expects an SSH target with Docker installed. Use `hyperv-create-vm` or `proxmox-create-vm` first if you need infrastructure.

## When to Use

- "deploy misp"
- "set up misp"
- "install misp"
- "threat intel platform"
- "ioc sharing platform"

## User Inputs

| Parameter | Default | Required |
|-----------|---------|----------|
| SSH target | - | Yes (user@host) |
| Admin email | admin@misp.local | No |
| Admin password | ChangeMe123! | No |
| Host RAM (for buffer pool) | 4GB | No |

## Prerequisites Check

```bash
# SSH works
ssh <target> "echo OK"

# Docker + Compose v2
ssh <target> "docker --version && docker compose version"

# RAM check (need 3GB+ free)
ssh <target> "free -h | grep Mem"
```

## Execution

### Single command deployment

```bash
scp scripts/setup.sh <target>:~/
ssh <target> "bash ~/setup.sh 'admin@misp.local' '<password>'"
```

### What setup.sh does

1. **Clone official misp-docker** from GitHub
2. **Configure .env:**
   - `MISP_BASEURL`, `MISP_ADMIN_EMAIL`, `MISP_ADMIN_PASSPHRASE`
   - Generate random MySQL passwords
   - Set `INNODB_BUFFER_POOL_SIZE` based on host RAM (CRITICAL)
3. **`docker compose up -d`**
4. **Poll for MISP readiness** (5-10 min on first boot for DB migrations)
5. **Generate API key** via cake CLI:
   ```bash
   docker compose exec -T misp /var/www/MISP/app/Console/cake user change_authkey <email>
   ```
6. **Verify API** with `/servers/getVersion`
7. **Save credentials** to `~/misp/api-key.txt`

### Output to User

```
MISP deployed!

URL: https://<target>
Admin: admin@misp.local / <password>
API Key: <key>

MCP Connection:
  MISP_URL=https://<target>
  MISP_API_KEY=<key>
  MISP_VERIFY_SSL=false

Note: Self-signed HTTPS. Use curl -k for API calls.
Credentials saved to: ~/misp/api-key.txt
```

## InnoDB Buffer Pool Sizing

The #1 failure on small VMs. Default buffer pool is 2GB, which kills MariaDB on 4GB hosts.

| Host RAM | INNODB_BUFFER_POOL_SIZE |
|----------|------------------------|
| 4 GB | 512M |
| 8 GB | 2048M |
| 16 GB | 4096M |

## Critical Gotchas

See `references/gotchas.md` for full details:

1. **MariaDB OOM (showstopper):** Default InnoDB buffer pool is 2GB. On 4GB hosts, MariaDB crashes instantly. MUST set `INNODB_BUFFER_POOL_SIZE` in `.env`
2. **Recovery from OOM:** `docker compose down -v` to wipe failed DB volume, fix `.env`, restart
3. **First boot is slow:** 5-10 min for DB schema creation and initial data load
4. **Self-signed HTTPS:** Use `curl -k` for all API calls
5. **Advanced authkeys:** Enabled by default. `cake` CLI is the most reliable key generation method
6. **MISP web UI:** `https://<ip>` (port 443, not 80)

## Timeout Strategy

Total: ~12-15 min (docker pull + first boot + setup). Split:
- Turn 1: Clone, configure, `docker compose up -d` (~3 min + pull time)
- Turn 2: Wait for health + generate API key (~5-7 min)

## Pairs With

- `hyperv-create-vm` - create a Hyper-V VM, then deploy MISP on it
- `proxmox-create-vm` - create a Proxmox LXC/VM, then deploy MISP on it
- `soc-deploy-thehive` - deploy TheHive alongside for case management
