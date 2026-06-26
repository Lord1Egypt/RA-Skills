# VM Memory Oracle

Production-grade memory persistence and lifecycle management for VM-hosted OpenClaw agents.

## What It Does

VM Memory Oracle gives your OpenClaw agent a structured, persistent memory that survives reboots, context compaction, and VM redeployment. It replaces fragile flat-file memory with a 4-layer architecture:

| Layer | Purpose | Storage |
|---|---|---|
| Knowledge Graph | Durable facts, entities, relationships | `facts.jsonl`, `entities.jsonl` |
| Semantic Index | Vector similarity search | `index.bin` (rebuildable) |
| Daily Summaries | Per-day session digests | `daily/YYYY-MM-DD.md` |
| Canonical Memory | Single source of truth | `MEMORY.md` |

Every fact has an activation score that decays over time. Frequently recalled facts stay prominent; unused facts gradually fade and get archived. This keeps your agent's memory focused and relevant.

## Key Features

- **Activation/Decay System** — Facts decay with a configurable half-life (default: 30 days). Recalled facts get boosted. Stale facts get archived, not deleted.
- **Nightly Consolidation** — Automated pipeline: summarize sessions, apply decay, rebuild index, prune stale facts, reconcile MEMORY.md, clean old files.
- **Health Monitoring** — Disk usage, fact count, activation distribution, consolidation duration, and quality probes all tracked in `health.json`.
- **Quality Probes** — Canary facts tested weekly to detect memory recall degradation.
- **Fully Local** — Zero network calls. Zero cloud dependencies. Zero credential handling. All data stays on your VM's filesystem.

## Requirements

- OpenClaw >= 1.8.0
- Linux (designed for VM deployments)
- `jq` (JSON processing)
- `cron` (scheduled tasks)

## Installation

```bash
openclaw skill install vm-memory-oracle
```

Or install from ClawHub:

```bash
clawhub install ssharif/vm-memory-oracle
```

## Quick Start

### 1. Configure your data path

```yaml
# In your OpenClaw agent config
memory_oracle:
  data_path: /data/memory
```

### 2. Initialize the directory structure

```bash
openclaw skill run vm-memory-oracle --action init
```

This creates:
```
/data/memory/
  knowledge-graph/
  embeddings/
  daily/
  sessions/
  activation-metadata.json
  MEMORY.md
  health.json
```

### 3. Set up automated maintenance

```bash
openclaw skill run vm-memory-oracle --action install-cron
```

This registers four cron jobs:
- **23:00** — Daily session summarization
- **00:30** — Full consolidation (decay, index, prune, reconcile)
- **Every 6h** — Health check
- **Sunday 03:00** — Quality probe

### 4. Verify

```bash
openclaw skill run vm-memory-oracle --action health-check
cat /data/memory/health.json | jq .
```

## Configuration Reference

| Parameter | Default | Description |
|---|---|---|
| `data_path` | `/data/memory` | Root directory for all memory files |
| `half_life_days` | `30` | Days until a fact's activation halves |
| `recall_boost` | `0.3` | Activation increase on each recall |
| `search_threshold` | `0.15` | Minimum activation for search results |
| `prune_threshold` | `0.05` | Activation below which facts get archived |
| `max_facts` | `10000` | Hard cap on active facts |
| `session_retention_days` | `30` | Days to keep raw session logs |
| `daily_retention_days` | `365` | Days to keep daily summaries |
| `memory_md_max_lines` | `200` | Maximum lines in MEMORY.md |
| `canary_check_interval` | `weekly` | How often to run quality probes |
| `embedding_model` | `multilingual-e5-large` | Model for semantic embeddings |
| `embedding_device` | `cpu` | Device for embedding inference (`cpu` or `gpu`) |

## VM Deployment Guide

This skill is designed for persistent VM environments where the memory directory lives on a dedicated data disk.

### Azure VM Setup

1. **Attach a separate managed disk** for `/data/memory/` with `deleteOption: Detach` so the disk survives VM redeployment.
2. **Format only on first boot** — use `overwrite: false` in cloud-init to prevent reformatting existing data.
3. **Mount at `/data/memory/`** in `/etc/fstab` with `nofail` option.

### Disk Sizing

| Workload | Recommended Size | Notes |
|---|---|---|
| Light (< 1K facts) | 16 GB | Personal agent |
| Medium (1K-5K facts) | 32 GB | Team agent |
| Heavy (5K-10K facts) | 64 GB | Production fleet |
| With large RAG corpus | 128-256 GB | Domain-specific knowledge |

### Backup

Pair with Azure disk snapshots or local tarballs. The consolidation pipeline creates a local backup before pruning:

```
/data/memory/backups/pre-maintenance-YYYYMMDD.tar.gz
```

Backups older than 7 days are automatically cleaned up.

## How It Works

### Fact Lifecycle

```
Session → Ingestion → Knowledge Graph → Embedding Index
                                ↓
                         Activation: 1.0
                                ↓
                    Decay applied nightly (half-life: 30d)
                                ↓
              ┌─────────────────┼─────────────────┐
              ↓                 ↓                 ↓
        Active (>0.15)   Fading (0.05-0.15)  Archived (<0.05)
        Appears in        Excluded from       Moved to
        search results    search, still       archived-facts.jsonl
                          in graph
```

### Daily Pipeline

```
23:00  Summarize today's sessions → daily/YYYY-MM-DD.md
00:30  Apply decay → activation-metadata.json
       Rebuild embedding index → embeddings/index.bin
       Prune stale facts → archived-facts.jsonl
       Reconcile → MEMORY.md
       Clean old sessions (>30d) and dailies (>365d)
       Health check → health.json
```

## Safety

| Property | Guarantee |
|---|---|
| Network access | None. Zero outbound connections. |
| Credentials | Never read, written, or transmitted. |
| Privilege escalation | Never uses sudo or su. |
| Write behavior | Append-only for facts. Archival instead of deletion. |
| Idempotency | All operations safe to retry. |
| Transparency | All files human-readable (JSONL, Markdown, JSON). |

## Monitoring Integration

`health.json` is designed for easy ingestion into monitoring systems:

- **Azure Log Analytics** — Ship with Azure Monitor Agent using a custom log table.
- **Prometheus** — Parse with a JSON exporter or node-exporter textfile collector.
- **Grafana** — Dashboard the `health.json` fields directly.

### Alert Thresholds

| Metric | Warning | Critical |
|---|---|---|
| Disk usage | > 80% | > 90% |
| Active facts | > 9,000 | > 9,500 |
| Avg activation | < 0.2 or > 0.8 | N/A |
| Quality probe accuracy | < 80% | < 70% |
| Consolidation duration | > 600s | > 1200s |

## Troubleshooting

**Memory not persisting across reboots:**
Check that `/data/memory` is mounted on a separate disk, not the OS disk. Verify the mount with `df -h /data/memory`.

**Consolidation taking too long:**
Reduce `max_facts` or increase `prune_threshold` to archive more aggressively. Check embedding index size — if it exceeds 4 GB, consider switching `embedding_model` to a smaller variant.

**Quality probe failing:**
Canary facts may have decayed. Re-add them with high activation, or lower `half_life_days` to keep important facts active longer.

**MEMORY.md too large:**
Lower `memory_md_max_lines` or increase `search_threshold` so fewer facts qualify for inclusion.

## License

MIT-0 — Use, modify, and redistribute freely. No attribution required.
