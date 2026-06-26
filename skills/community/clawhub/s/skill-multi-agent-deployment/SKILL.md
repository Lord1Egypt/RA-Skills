---
name: multi-agent-deployment
description: >
  Deploy production-grade multi-agent fleets in OpenClaw with battle-tested
  scripts, cloud deployment templates, and shared memory infrastructure.
  Use when: (1) Deploying multiple specialized AI agents with routing,
  (2) Setting up shared memory between agents, (3) Deploying to cloud
  platforms (DigitalOcean, AWS, GCP, K8s), (4) Building agent teams for
  business workflows, (5) Moving from single-agent to production multi-agent
  setups. Includes working Python scripts, cloud deployment configs, and
  troubleshooting guides based on real deployments.
---

# Multi-Agent Deployment Skill for OpenClaw

**Production deployment focus.** This skill provides **executable scripts** and
**cloud-ready configurations** — not just documentation. Unlike pure
coordination-pattern skills, this gives you working infrastructure:
`agent_setup.py` creates your agent directories, `routing_config.py`
generates OpenClaw config, `memory_sync.py` wires shared memory,
`fleet_validate.py` checks your deployment health, and
`deploy_script.sh` ships to DigitalOcean, AWS, GCP, Azure, or Kubernetes.

| Who this is for | What you get |
|---|---|
| OpenClaw users running 1 agent → need a fleet | Scripts, templates, working configs |
| Developers deploying to cloud (DO/AWS/GCP) | Platform YAML/JSON templates + Dockerfile |
| Teams needing shared memory across agents | File-based shared memory with locking + TTL |
| Anyone testing multi-agent architectures | 5 agent type templates + routing rules |

---

## Quick Start (5 minutes)

```bash
# 1. Create 5 agent directories with SOUL.md + AGENTS.md templates
python scripts/agent_setup.py --agents coordinator,research,builder,auditor,personal --output ./agents

# 2. Generate OpenClaw routing config
python scripts/routing_config.py --input ./agents --output ~/.openclaw/config.json

# 3. Initialize shared memory
python scripts/memory_sync.py --init --path ./shared_memory

# 4. Validate your fleet (new!)
python scripts/fleet_validate.py --agents ./agents --config ~/.openclaw/config.json

# 5. Deploy (or dry-run first)
bash scripts/deploy_script.sh --platform digitalocean --region nyc3 --dry-run
```

---

## What's Included

### 🐍 Python Scripts (working, tested)

| Script | Purpose | Key Features |
|--------|---------|-------------|
| `scripts/agent_setup.py` | Scaffold agent directories | Reads templates from `assets/templates/`, creates 5 agent types + shared dir |
| `scripts/routing_config.py` | Generate OpenClaw config.json | Per-agent routing rules, fallback to coordinator, shared memory wiring, **health probes**, **rate limits** |
| `scripts/memory_sync.py` | File-based shared memory | JSON persistence, file-locking, TTL per key, event journaling, agent stats, **typed schema validation** |
| `scripts/fleet_validate.py` | Validate deployment health | Agent structure, routing config, shared memory, template integrity check |
| `scripts/deploy_script.sh` | One-click cloud deploy | DO App Spec, AWS ECS, GCP Cloud Run, Azure ACI, K8s manifests |

### 📁 Asset Templates
| File | Purpose |
|------|--------|
| `assets/templates/SOUL.md` | Agent personality + mission template (populated by agent_setup.py) |
| `assets/templates/AGENTS.md` | Operating rules and protocols template |

### 📚 Reference Docs
- [references/architecture.md](references/architecture.md): Full agent architecture patterns (coordinator-centric, peer-to-peer, pipeline)
- [references/troubleshooting.md](references/troubleshooting.md): 6 common failure patterns with recovery procedures
- [references/workflows.md](references/workflows.md): Workflow DAG templates with pipeline execution patterns (v1.2.0+)
- [references/memory-schemas.md](references/memory-schemas.md): Typed inter-agent memory schemas with validation rules (v1.2.0+)

### ☁️ Cloud Deployment Configs
- `deployments/digitalocean/app.yaml` — DigitalOcean App Platform
- `deployments/aws/task-definition.json` — AWS ECS
- `deployments/gcp/cloudrun.yaml` — GCP Cloud Run
- `deployments/azure/container-instance.yaml` — Azure Container Instances
- `deployments/k8s/deployment.yaml` — Kubernetes deployment + HPA
- `deployments/Dockerfile.openclaw` — Container image for gateway
*(Shipped with skill — customize or regenerate with deploy_script.sh)*

---

## Architecture Overview

The skill supports three deployment-tested agent topologies:

### 1. Coordinator-Centric (recommended start)
```
User → Coordinator → [Research, Builder, Auditor, Personal]
                      → Shared Memory ← all
```
Best for: business workflows, clear task handoffs, teams < 10 agents.

### 2. Peer-to-Peer
```
Agents ↔ Event Bus ↔ Shared Memory
```
Best for: creative/research workflows, emergent coordination, high collaboration.

### 3. Pipeline
```
Research → Builder → Auditor → Deploy
```
Best for: content creation, data processing, linear workflows.

*See [references/architecture.md](references/architecture.md) for full topology diagrams and config examples.*

---

## Shared Memory Design

Two backends available — **file** (default, zero deps) and **SQLite** (production).

**File backend** (zero infrastructure):
- **Atomic writes** via temp file + replace
- **File locking** with configurable timeout
- **TTL-based expiration** on shared keys
- **Event journaling** (daily JSONL files)
- **Agent statistics** (read/write counts, last active)
- **Auto-cleanup** of expired entries
- **Typed schema validation** for structured inter-agent data (v1.2.0+)

```bash
# Write data (free-form, file backend)
python scripts/memory_sync.py --write 'coordinator:task_status:{"status":"active"}'

# Write data with schema validation
python scripts/memory_sync.py --write 'coordinator:current_task:{"task_id":"t001","assigned_by":"coordinator","assigned_to":"research","priority":"high","title":"Research trends","description":"Analyze marketplace"}' --schema task_assignment

# Read data
python scripts/memory_sync.py --read 'research:search_results'

# View agent stats
python scripts/memory_sync.py --stats

# List available typed schemas
python scripts/memory_sync.py --list-schemas

# List all shared keys (v1.3.0)
python scripts/memory_sync.py --keys

# Count keys per agent (v1.3.0)
python scripts/memory_sync.py --count-by-agent

# Cleanup expired
python scripts/memory_sync.py --cleanup

# === SQLite Backend (production, v1.3.0) ===

# Initialize SQLite shared memory
python scripts/memory_sync.py --backend sqlite --init --path ./shared_memory

# Write with SQLite backend
python scripts/memory_sync.py --backend sqlite --write 'coordinator:task:{"id":"t1"}'

# Migrate from file to SQLite
python scripts/memory_sync.py --migrate-to-sqlite ./shared_memory

# Reclaim SQLite space
python scripts/memory_sync.py --backend sqlite --compact
```

For high-concurrency production, use the **SQLite backend** (`--backend sqlite`) with WAL mode
for concurrent reads/writes and ACID transactions — all from the Python std library, no pip install needed.

Migrate from file to SQLite:
```bash
python scripts/memory_sync.py --migrate-to-sqlite ./shared_memory
```

### HTTP REST API (v1.4.0+)

Expose shared memory over HTTP using **only Python stdlib** — no pip install needed.
Start the API server with `--listen`:

```bash
# Start server (default: port 8080, bind 127.0.0.1)
python scripts/memory_sync.py --listen --backend sqlite --path ./shared_memory
```

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/keys?agent=X` | List keys (optional agent filter) |
| GET | `/count` | Keys per agent |
| GET | `/stats` | Full statistics |
| GET | `/schemas` | Available typed schemas |
| GET | `/read/<a>/<k>` | Read a value |
| POST | `/write` | Write a value (JSON body) |

```bash
# Write via API
curl -X POST http://localhost:8080/write -H "Content-Type: application/json" \
  -d '{"agent_id":"coordinator","key":"task:t001","value":{"task_id":"t001","assigned_to":"research"},"schema":"task_assignment"}'
```

CORS headers included for web-based dashboards.

---

## Cloud Deployment

```bash
# Dry-run (generates configs only)
bash scripts/deploy_script.sh --platform aws --region us-east-1 --dry-run

# Actual deploy
bash scripts/deploy_script.sh --platform digitalocean --region nyc3 --size s-2vcpu-2gb
```

The script:
1. Detects or accepts platform (`--platform digitalocean|aws|gcp|azure|k8s`)
2. Generates platform-specific configs under `deployments/<platform>/`
3. Dockerfile included for containerized gateway
4. Generates deployment summary in `deployments/deployment-summary.md`

---

## Common Use Cases

### E-commerce Support Team
Customer → Coordinator → [Support, Inventory, Analytics, Order]

### Content Creation Team
Research → Writer → Editor → Publisher (pipeline pattern)

### Development Team
Planner → Coder → Tester → Deployer → Auditor (pipeline + audit gate)

### Personal Productivity
Coordinator → [Research, Builder, Personal Assistant]

---

## Agent Types Included

| Agent | Mission | Default Router |
|-------|---------|---------------|
| **coordinator** | Route requests, monitor availability, resolve conflicts | `help`, `assist`, `support` |
| **research** | Gather and synthesize web information | `research`, `find`, `search`, `look up`, `what is` |
| **builder** | Write code, create files, debug | `build`, `create`, `write`, `code`, `script`, `develop` |
| **auditor** | Review quality, security, compliance | `review`, `check`, `audit`, `validate`, `test` |
| **personal** | Scheduling, reminders, communication | `schedule`, `remind`, `calendar`, `email`, `message` |

---

## Monitoring, Security & Recovery

### Agent Monitoring
- Shared memory stats: `python scripts/memory_sync.py --stats`
- SQLite stats (production): `python scripts/memory_sync.py --backend sqlite --stats`
- List all keys: `python scripts/memory_sync.py --keys`
- Keys per agent: `python scripts/memory_sync.py --count-by-agent`
- Event journal: `tail -f shared_memory/events/$(date +%Y%m%d).jsonl`
- System health: `openclaw agents list && openclaw gateway status`

### Security Perimeter
| Layer | Protection |
|-------|-----------|
| Workspace isolation | Each agent has separate dirs |
| Memory isolation | Shared memory via API only (file-locked) |
| Tool restrictions | Only necessary tools per agent type |
| Audit logging | All writes logged to event journal |

### Recovery Procedures
See [references/troubleshooting.md](references/troubleshooting.md) for:
- Complete system failure recovery
- Data corruption restoration
- Individual agent recovery
- Configuration drift fixes

---

## Why This Skill Over Competitors

| Dimension | This Skill | Pure Coordination Skills |
|-----------|-----------|------------------------|
| **Focus** | Production deployment | Agent coordination patterns |
| **Scripts** | 4 working Python/bash scripts | Usually documentation-only |
| **Cloud** | Multi-platform (DO/AWS/GCP/Azure/K8s) | Rarely included |
| **Templates** | SOUL.md + AGENTS.md (populated at runtime) | Often static examples |
| **Shared Memory** | Working file-based system with locking, TTL, stats | Conceptual description |
| **Troubleshooting** | 6 failure patterns with executable recovery steps | Generic advice |

---

## OpenClaw 2026.x Integration Patterns

This skill's outputs work with OpenClaw 2026.2+ and 2026.3+ features:
- `sessions_spawn` for sub-agent task delegation
- `cron` for scheduled multi-agent workflows
- Shared memory as communication bridge between agents
- Routing rules for message-to-agent direction
- `fleet_validate.py` for post-deployment health checks
- `openclaw agents` management commands for fleet lifecycle

### 2026.3+ Feature Notes

The latest routing config generator (`routing_config.py`) automatically generates
configurations for these 2026.3+ features—no manual editing needed:

- **Agent health probes**: Each agent entry has `healthCheck` config
  with interval, timeout, and retry settings
- **Gateway-level rate limiting**: Per-agent `rateLimit` settings
  (30 req/min, 5 concurrent)
- **Structured memory types**: `memory_sync.py` now supports typed schema
  validation via `--schema` flag. See
  [references/memory-schemas.md](references/memory-schemas.md) for
  all available schemas (task_assignment, status_update, research_finding,
  etc.)
- **Workflow DAGs**: 5 ready-to-use pipeline execution templates in
  [references/workflows.md](references/workflows.md) — content creation,
  development sprints, customer support, data pipelines, and daily briefings
  with topological dependency ordering and execution scripts

---

## Troubleshooting Quick Reference

**Agents not responding?**
```bash
openclaw agents list           # Are they running?
journalctl -u openclaw-gateway | tail -20  # Any errors?
```

**Wrong routing?**
```bash
python scripts/routing_config.py --input ./agents --config-output ./routing-test.json
```

**Shared memory corruption?**
```bash
python -m json.tool shared_memory/shared_data.json  # Validate JSON
python scripts/memory_sync.py --cleanup              # Remove expired
python scripts/memory_sync.py --list-schemas         # See available typed schemas
```

**Fleet health check?**
```bash
python scripts/fleet_validate.py --agents ./agents --config ~/.openclaw/config.json
```

**Schema validation on write?**
```bash
python scripts/memory_sync.py --write 'coordinator:task:{"task_id":"t1","assigned_to":"research"}' --schema task_assignment
```

---

## Version History

| Version | Date | Changes |
|---------|------|--------|
| 1.4.0 | 2026-05-27 | **HTTP REST API** — `--listen` flag starts zero-dep REST server exposing shared memory over HTTP. GET/POST for read, write, keys, stats, count, cleanup, schemas, health. CORS headers, stdlib only |
| 1.3.0 | 2026-05-26 | **SQLite backend** — WAL-mode concurrent shared memory, ACID transactions, `--backend sqlite`, `--migrate-to-sqlite` tool, `--keys` and `--count-by-agent` utilities, `--compact` for space reclamation. No pip deps required. SKILL.md and memory-schemas.md updated with SQLite docs |
| 1.2.0 | 2026-05-25 | Structured memory schemas with validation; health probes in routing config; memory-schemas.md reference; rate limiting; `--schema` and `--list-schemas` flags; **workflows.md** with 5 DAG templates; schema validation bug fix (inner data fields + correct schema type); reference list expanded |
| 1.1.0 | 2026-05-23 | Fleet validation script added; deployment config templates shipped; date bug fixed; OpenClaw 2026.3+ pattern notes |
| 1.0.1 | 2026-05-11 | Templates unified; agent_setup.py reads from assets/templates/; _meta.json + origin tracking added |
| 1.0.0 | 2026-04-02 | Initial release — agent setup, routing config, memory sync, cloud deploy |

---

*Based on production patterns from Abhi's multi-agent deployment experience. Tested with OpenClaw 2026.2+.*
*Published on [ClawHub](https://clawhub.ai) — slug: multi-agent-deployment*