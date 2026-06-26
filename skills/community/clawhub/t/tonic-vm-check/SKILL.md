---
name: tonic-vm-check
description: |
  🖥️ Instant VM health checks — no config needed after first run.

  Point it at any Docker-based Linux server and get a clean report covering CPU, memory, disk, all running containers (with live stats), MySQL/Postgres database sizes, and Docker image/cache bloat — in one command.

  First time? It asks for your VM details once, saves them, and never asks again.

  Perfect for: post-deploy sanity checks, spotting memory hogs, finding disk space to reclaim, and keeping your server tidy.

  Triggers on: "check VM", "VM resources", "VM health", "how is the server", "Docker usage", "disk usage", "clean up Docker", "free up space".
---

# tonic-vm-check

SSH into a Docker-based VM and report system health, container status, DB sizes, and disk usage.

## Step 1: Load VM Config

Before running any check, look for this block in `TOOLS.md`:

```
### tonic-vm-check
- VM_HOST: <host>
- VM_USER: <user>
- SSH_KEY: <path>
```

**If found:** extract the values and proceed to Step 2.

**If not found:** ask the user once:
> To check your VM, I need a few details (only asked once — saved to TOOLS.md):
> 1. VM IP or hostname
> 2. SSH username (default: ubuntu)
> 3. Path to SSH private key (default: ~/.ssh/id_rsa)

Then append to `TOOLS.md`:

```markdown
### tonic-vm-check
- VM_HOST: <answer>
- VM_USER: <answer>
- SSH_KEY: <answer>
```

Confirm saved, then proceed.

## Step 2: Run the Check

```bash
VM_HOST=<host> VM_USER=<user> SSH_KEY=<key> bash skills/tonic-vm-check/scripts/vm-check.sh [section]
```

Sections: `all` (default) · `system` · `disk` · `containers` · `db` · `docker-df` · `cleanup`

## Step 3: Report

Summarise results:

**🖥️ System** — Uptime, CPU idle%, load average, memory (total / used / available)

**💾 Disk** — `/` usage %, used, free

**🐳 Docker** — Top containers by MEM USAGE; flag any not healthy or recently restarted

**🗄️ DB Sizes** — MySQL and Postgres databases auto-detected on the VM

**🧹 Cleanup Opportunities** — Reclaimable image/cache space; stopped containers worth removing

Always flag items that exceed thresholds:

| Metric | Warning | Critical |
|--------|---------|----------|
| Disk usage | >70% | >85% |
| Memory used | >80% | >90% |
| Load avg (1m) | >2.0 | >4.0 |
| Single container MEM | >1 GB | >2 GB |

## Cleanup Safety Rules

- `docker image prune -af` — safe (unused images only)
- `docker builder prune -f` — safe (build cache only, no data loss)
- `docker container prune` — safe only for stopped containers
- **Never** run `docker system prune -af` without explicit user approval (destroys volumes)
