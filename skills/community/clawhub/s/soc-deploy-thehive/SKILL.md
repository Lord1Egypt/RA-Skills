---
name: soc-deploy-thehive
version: 1.0.0
description: "Deploy TheHive 5 + Cortex 3 incident response platform on any Docker-ready Linux host. Automates account creation, API key generation, Cortex CSRF handling, and TheHive-Cortex integration wiring. Platform-agnostic."
tags:
  - soc
  - thehive
  - cortex
  - incident-response
  - security
  - docker
  - automation
  - mcp
category: security
---

# SOC Deploy: TheHive 5.4 + Cortex 3.1.8

Deploy TheHive + Cortex incident response platform on any Docker-ready Linux host.

**This skill does NOT create VMs.** It expects an SSH target with Docker installed. Use `hyperv-create-vm` or `proxmox-create-vm` first if you need infrastructure.

## When to Use

- "deploy thehive"
- "set up thehive"
- "install thehive and cortex"
- "thehive lab"
- "incident response platform"

## User Inputs

| Parameter | Default | Required |
|-----------|---------|----------|
| SSH target | - | Yes (user@host) |
| Admin password | ChangeMe123! | No |
| Org name (Cortex) | SOC | No |
| TheHive secret | (generated 40-char) | No |

## Prerequisites Check

```bash
# SSH works
ssh <target> "echo OK"

# Docker + Compose v2
ssh <target> "docker --version && docker compose version"

# RAM check (need 4GB+ free)
ssh <target> "free -h | grep Mem"
```

## Execution

### Single command deployment

```bash
scp scripts/setup.sh <target>:~/
scp references/docker-compose.yml <target>:~/thehive-cortex/docker-compose.yml
ssh <target> "bash ~/setup.sh '<password>' '<org-name>'"
```

### What setup.sh does (from thehive-cortex-setup-guide.md)

1. **Create directory + write docker-compose.yml**
2. **`docker compose up -d`** (Cassandra + ES + TheHive + Cortex)
3. **Poll health endpoints** until all services respond:
   - `GET :9200/_cluster/health` (Elasticsearch)
   - `GET :9000/api/status` (TheHive)
   - `GET :9001/api/status` (Cortex)
4. **TheHive admin setup:**
   - `POST /api/v1/login` with `admin@thehive.local` / `secret`
   - `POST /api/v1/user/admin@thehive.local/password/change` (NOT PATCH)
   - `POST /api/v1/user/admin@thehive.local/key/renew` -> API key
5. **Cortex setup (CSRF dance):**
   - `POST /api/maintenance/migrate`
   - `POST /api/user` (create superadmin, first-user endpoint)
   - `POST /api/login` -> session cookie
   - `GET /api/user/admin` -> capture `CORTEX-XSRF-TOKEN` cookie
   - `POST /api/organization` (with CSRF cookie + header)
   - `POST /api/user` (org admin, with CSRF)
   - `POST /api/user/<org-admin>/key/renew` (with CSRF) -> org key
   - `POST /api/user/admin/key/renew` (with CSRF) -> super key
6. **Wire integration:**
   - Update docker-compose.yml: add `--cortex-hostnames cortex --cortex-keys <org-admin-key>`
   - `docker compose up -d thehive` (restart only TheHive)
   - Wait 30s for TheHive startup
7. **Verify both APIs** respond with Bearer keys
8. **Write credentials** to `~/thehive-cortex/api-keys.txt`

### Output to User

```
TheHive + Cortex deployed!

TheHive: http://<target>:9000
Cortex:  http://<target>:9001

Credentials:
  TheHive admin:     admin@thehive.local / <password>
  Cortex superadmin: admin / <password>
  Cortex org admin:  <org>-admin (API key only)

API Keys:
  TheHive:           <key>
  Cortex superadmin: <key>
  Cortex org admin:  <key>

MCP Connection:
  THEHIVE_URL=http://<target>:9000
  THEHIVE_API_KEY=<key>
  CORTEX_URL=http://<target>:9001
  CORTEX_API_KEY=<key>

Keys saved to: ~/thehive-cortex/api-keys.txt
```

## Critical Gotchas

See `references/gotchas.md` for full details:

1. **Cortex CSRF (biggest automation blocker):** Cookie `CORTEX-XSRF-TOKEN` + header `X-CORTEX-XSRF-TOKEN` on ALL mutating requests. Standard Play Framework bypass headers do NOT work. After first API key, use `Authorization: Bearer` to skip CSRF
2. **TheHive password endpoint:** `POST /password/change` with `currentPassword`+`password`. The PATCH endpoint returns 204 but silently ignores the password field
3. **Bash `!` in passwords:** Use `printf '...' | curl -d @-`, not direct `-d` with exclamation marks
4. **First-user one-shot:** Cortex `POST /api/user` without auth only works when zero users exist
5. **TheHive startup delay:** 15-30s after compose up (waits for Cassandra)
6. **Secret length:** TheHive Play Framework JWT needs 32+ char secret
7. **Use org admin key** (not superadmin) for TheHive-Cortex integration (least privilege)

## API Quick Reference

See `references/api-reference.md` for the full endpoint list.

## Timeout Strategy

Setup takes ~5-7 min (mostly waiting for services). If docker images are not cached, add ~5 min for pull. Split into:
- Turn 1: `docker compose up -d` + pull images (~5 min)
- Turn 2: Account setup + API keys (~3 min)

## Pairs With

- `hyperv-create-vm` - create a Hyper-V VM, then deploy TheHive on it
- `proxmox-create-vm` - create a Proxmox LXC/VM, then deploy TheHive on it
- `soc-deploy-misp` - deploy MISP alongside for threat intelligence
