---
name: vmware-aria
description: >
  Use this skill whenever the user needs VMware Aria Operations data — performance metrics, alerts, capacity planning, anomaly detection, and automated reports.
  Directly handles: query resource metrics, list/acknowledge/cancel alerts, manage alert definitions, check capacity and time-remaining forecasts, detect anomalies, generate and manage reports.
  Always use this skill for "check vSphere capacity", "what Aria Operations alerts are active", "show VMware anomalies", "generate an Aria report", "rightsizing recommendations", or any Aria/vRealize Operations task.
  Combined with LLM, Aria data powers natural language reports: "give me a capacity report" → Aria collects data → LLM formats the report.
  Do NOT use for real-time vCenter alarms/events (use vmware-monitor), VM operations (use vmware-aiops), or NSX networking (use vmware-nsx).
  For load balancing/AVI/AKO use vmware-avi.
installer:
  kind: uv
  package: vmware-aria
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["VMWARE_ARIA_CONFIG"],"bins":["vmware-aria"],"config":["~/.vmware-aria/config.yaml","~/.vmware-aria/.env"]},"optional":{"env":["VMWARE_<TARGET>_PASSWORD"],"bins":["vmware-policy"]},"primaryEnv":"VMWARE_ARIA_CONFIG","homepage":"https://github.com/zw008/VMware-Aria","emoji":"📊","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All write operations audited to ~/.vmware/audit.db.
  Credentials: Each Aria Operations target requires a per-target password env var in ~/.vmware-aria/.env following the pattern VMWARE_<TARGET_NAME_UPPER>_PASSWORD. Passwords are never logged or echoed.
  Read-heavy: 20 of 27 tools are read-only. Write operations limited to alert acknowledge/cancel, alert definition management, and report management.
  No webhooks, no outbound network calls, no guest operations. Local only: stdio MCP + Aria Operations REST API (HTTPS 443).
  Transitive dependencies: Only vmware-policy (audit/policy). No post-install scripts or background services.
---

# VMware Aria Operations

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "Aria" are trademarks of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-Aria](https://github.com/zw008/VMware-Aria) under the MIT license.

VMware Aria Operations (vRealize Operations) AI-assisted monitoring — 27 MCP tools for resources, alerts, alert definitions, capacity planning, anomaly detection, report automation, and platform health.

> Domain-focused monitoring skill for Aria Operations 8.x / vRealize Operations 8.x.
> **Companion skills**: [vmware-nsx](https://github.com/zw008/VMware-NSX) (networking), [vmware-aiops](https://github.com/zw008/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (read-only vSphere), [vmware-avi](https://github.com/zw008/VMware-AVI) (AVI/ALB/AKO), [vmware-harden](https://github.com/zw008/VMware-Harden) (compliance baselines).
> | [vmware-pilot](../vmware-pilot/SKILL.md) (workflow orchestration) | [vmware-policy](../vmware-policy/SKILL.md) (audit/policy)

## What This Skill Does

| Category | Tools | Count |
|----------|-------|:-----:|
| **Resources** | list, get details, metrics, health badge, top consumers | 5 |
| **Alerts** | list, get details, acknowledge, cancel, list definitions | 5 |
| **Alert Definitions** | list symptoms, create definition, enable/disable, delete | 4 |
| **Capacity** | cluster overview, remaining capacity, time remaining, rightsizing | 4 |
| **Reports** | list templates, generate, list, get status+download URL, delete | 5 |
| **Anomaly** | list anomalies, risk badge | 2 |
| **Health** | Aria platform health, collector group status | 2 |

**Total**: 27 tools (20 read-only + 7 write)

## Quick Install

```bash
uv tool install vmware-aria
vmware-aria doctor
```

## When to Use This Skill

**Performance monitoring (daily proactive checks):**
- Check VM contention: CPU Ready %, Memory Balloon, Swap usage
- Fetch time-series metrics for any resource (CPU, memory, disk, network)
- Find top consumers by CPU/memory/disk/network
- Check per-resource anomaly counts and risk badge scores

**Alert management:**
- List, investigate, acknowledge, or cancel active alerts
- List or filter alert definitions (templates)
- Create new alert definitions from symptom definitions (post-RCA)
- Enable or disable alert definitions; delete obsolete ones

**Capacity planning:**
- Cluster capacity remaining (CPU, memory, disk headroom)
- Time-until-full prediction per cluster
- Right-sizing: find over-provisioned or under-utilized VMs
- Capacity overview with Aria's built-in recommendations

**Report automation:**
- Generate scheduled or on-demand reports (capacity, performance, SLA)
- Poll report status until COMPLETED; get PDF/CSV download URL
- Delete generated reports after download

**Use companion skills for**:
- VM lifecycle: create, clone, snapshot, power → `vmware-aiops`
- NSX networking: segments, gateways, NAT, routing → `vmware-nsx`
- vSphere inventory, real-time alarms, events → `vmware-monitor`
- Storage: iSCSI, vSAN, datastores → `vmware-storage`
- Load balancing, AVI/ALB, AKO, Ingress → `vmware-avi`

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|-------------------|
| Aria Operations monitoring, alerts, capacity | **vmware-aria** ← this skill |
| VM lifecycle, deployment, guest ops | **vmware-aiops** |
| NSX networking: segments, gateways, NAT, routing | **vmware-nsx** |
| Read-only vSphere inventory, events, alarms | **vmware-monitor** |
| Storage: iSCSI, vSAN, datastores | **vmware-storage** |
| Multi-step workflows with approval | **vmware-pilot** |
| Compliance baselines (CIS / 等保 / PCI-DSS), drift detection, LLM remediation advisor | **vmware-harden** (`uv tool install vmware-harden`) |
| Load balancer, AVI, ALB, AKO, Ingress | **vmware-avi** (`uv tool install vmware-avi`) |
| Audit log query | **vmware-policy** (`vmware-audit` CLI) |

## Common Workflows

> **Diagnostic investigations**: Before running any "why is X slow / failing / down" workflow, follow [`references/investigation-protocol.md`](references/investigation-protocol.md). It enforces the four root-cause completeness criteria (falsifiability / sufficiency / necessity / mechanism) and the up-to-three-rounds deepening loop. Stopping at a partial conclusion is an anti-pattern — always self-check against the criteria before outputting a report.

### Daily VM Health Check (Proactive Ops)

**Judgment**: don't chase the highest CPU consumer — chase the highest **contention** consumer. A VM at 90% CPU on a quiet host is healthy; a VM at 30% CPU but 15% Ready is starving. Key metrics: CPU Ready, Memory Balloon, Disk Latency.

1. Find top CPU consumers → `vmware-aria resource top --metric cpu|usage_average --top 20` (this is the **starting set**, not the answer)
2. Check CPU Ready on hot VMs → `vmware-aria resource metrics <vm-id> --metrics cpu.ready.summation --hours 24`
   - >5% = warning, >10% = problem, >20% = critical
3. Check memory pressure → `vmware-aria resource metrics <vm-id> --metrics mem.balloon.average,mem.swapped.average --hours 24`
   - Balloon >0 = ESXi reclaiming memory; Swap >0 = severe — act immediately
4. List active CRITICAL/IMMEDIATE alerts → `vmware-aria alert list --criticality CRITICAL`
5. Check anomaly counts → `vmware-aria anomaly list`
6. Cross-validate against the [investigation protocol](references/investigation-protocol.md) before reporting any "root cause" — high consumption is rarely the root, usually a downstream symptom

### Investigate High CPU Alert

1. List active CRITICAL alerts → `vmware-aria alert list --criticality CRITICAL`
2. Get alert details + symptoms → `vmware-aria alert get <alert-id>`
3. Find top CPU consumers → `vmware-aria resource top --metric cpu|usage_average`
4. Fetch 24h CPU metrics for the hot VM → `vmware-aria resource metrics <vm-id> --metrics cpu|usage_average --hours 24`
5. Check risk badge → `vmware-aria anomaly risk <vm-id>`
6. Acknowledge the alert → `vmware-aria alert acknowledge <alert-id>`

### Capacity Planning

1. List clusters → `vmware-aria resource list --kind ClusterComputeResource`
2. Get remaining capacity → `vmware-aria capacity remaining <cluster-id>`
3. Predict time until full → `vmware-aria capacity time-remaining <cluster-id>`
4. Get capacity overview with recommendations → `vmware-aria capacity overview <cluster-id>`
5. Find rightsizing candidates → `vmware-aria capacity rightsizing`

### Post-Incident: Create Detection Alert (RCA Follow-up)

After resolving an incident, create an early-warning alert to prevent recurrence. Alert definition management is **MCP-only** (no CLI subcommands):

1. Find matching symptom definitions → MCP `list_symptom_definitions` (filter by `name_filter` / `resource_kind`)
2. Create alert definition referencing symptoms → MCP `create_alert_definition` with name, resource_kind, symptom_definition_ids, criticality (any one symptom firing triggers the alert)
3. Verify it appears in definitions → `vmware-aria alert definitions --name "Gold VM CPU"` (criticality shown is the max severity across the definition's states)
4. Enable or disable later → MCP `set_alert_definition_state`

### Generate Capacity Report

1. Find report template → `vmware-aria report definitions --name "Capacity"`
2. Trigger report generation → `vmware-aria report generate <definition-id> --resources <resource-id>` (the Report API requires at least one resource UUID)
3. Poll until completed → `vmware-aria report get <report-id>` (repeat until `status == COMPLETED`)
4. Download via the returned `download_url` (PDF) or `csv_url`
5. Clean up → `vmware-aria report delete <report-id>`

### Multi-Target Operations

All commands accept `--target <name>` to operate against a specific Aria Ops instance:

```bash
vmware-aria alert list --target prod
vmware-aria resource top --target lab
```

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | ~2K tokens vs ~8K for MCP |
| Cloud models (Claude, GPT-4o) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | Type-safe parameters, structured output |

## MCP Tools (27 — 20 read, 7 write)

All MCP tools accept an optional `target` parameter to select which Aria Operations instance to connect to.

| Category | Tool | Type | Description |
|----------|------|:----:|-------------|
| Resource | `list_resources` | Read | List VMs, hosts, clusters by resource kind |
| | `get_resource` | Read | Get resource details with health, risk, efficiency badges |
| | `get_resource_metrics` | Read | Fetch time-series metric stats for any resource |
| | `get_resource_health` | Read | Get health badge score (0–100) |
| | `get_top_consumers` | Read | Rank resources by CPU, memory, disk, or network usage |
| Alerts | `list_alerts` | Read | List active alerts with criticality and resource ID (resolve names via `get_resource`) |
| | `get_alert` | Read | Get alert details with contributing symptoms (recommendations live on the alert definition) |
| | `acknowledge_alert` | **Write** | Mark an alert as acknowledged (does not close it) |
| | `cancel_alert` | **Write** | Cancel (dismiss) an active alert |
| | `list_alert_definitions` | Read | List alert templates configured in Aria Ops |
| Alert Defs | `list_symptom_definitions` | Read | List symptom definitions — use IDs when creating alert defs |
| | `create_alert_definition` | **Write** | Create new alert definition from symptom definition IDs |
| | `set_alert_definition_state` | **Write** | Enable or disable an alert definition |
| | `delete_alert_definition` | **Write** | Delete an alert definition permanently |
| Capacity | `get_capacity_overview` | Read | Group-level remaining % + per-dimension headroom and days-until-full |
| | `get_remaining_capacity` | Read | Remaining CPU, memory, disk before hitting limits |
| | `get_time_remaining` | Read | Days until cluster capacity is exhausted |
| | `list_rightsizing_recommendations` | Read | VMs to resize: over/under-provisioned |
| Reports | `list_report_definitions` | Read | List available report definition templates |
| | `generate_report` | **Write** | Trigger report generation (async; returns report_id) |
| | `list_reports` | Read | List generated reports, optionally by definition |
| | `get_report` | Read | Poll report status + get PDF/CSV download URLs |
| | `delete_report` | **Write** | Delete a generated report |
| Anomaly | `list_anomalies` | Read | Per-resource anomaly counts (System Attributes\|total_alarms metric) |
| | `get_resource_riskbadge` | Read | Risk score (0–100): likelihood of future problems |
| Health | `get_aria_health` | Read | Aria platform node status (ONLINE/OFFLINE) |
| | `list_collector_groups` | Read | Collector agents status and connectivity |

**Read/write split**: 20 read-only, 7 write. All write operations are audit-logged to `~/.vmware/audit.db` (via vmware-policy).

## CLI Quick Reference

```bash
# Resources
vmware-aria resource list [--kind VirtualMachine|HostSystem|ClusterComputeResource] [--name <filter>]
vmware-aria resource get <resource-id>
vmware-aria resource metrics <resource-id> --metrics cpu|usage_average,mem|usage_average --hours 4
vmware-aria resource metrics <vm-id> --metrics cpu.ready.summation,mem.balloon.average --hours 24
vmware-aria resource health <resource-id>
vmware-aria resource top --metric cpu|usage_average --kind VirtualMachine --top 10

# Alerts
vmware-aria alert list [--criticality CRITICAL|IMMEDIATE|WARNING|INFORMATION]
vmware-aria alert get <alert-id>
vmware-aria alert acknowledge <alert-id>
vmware-aria alert cancel <alert-id>
vmware-aria alert definitions [--name <filter>]

# Alert Definitions: creation/enable/disable/delete and symptom-definition
# lookup are MCP-only tools (list_symptom_definitions, create_alert_definition,
# set_alert_definition_state, delete_alert_definition) — no CLI subcommands.

# Capacity
vmware-aria capacity overview <cluster-id>
vmware-aria capacity remaining <resource-id>
vmware-aria capacity time-remaining <resource-id>
vmware-aria capacity rightsizing [--resource-id <vm-id>]

# Reports (async: generate → poll get → download → delete)
vmware-aria report definitions [--name <filter>]
vmware-aria report generate <definition-id> --resources <id1,id2>   # at least one resource UUID required
vmware-aria report list [--definition-id <id>]
vmware-aria report get <report-id>        # poll until status == COMPLETED; shows download_url
vmware-aria report delete <report-id>

# Anomaly
vmware-aria anomaly list [--resource-id <id>]
vmware-aria anomaly risk <resource-id>

# Health
vmware-aria health status
vmware-aria health collectors

# Diagnostics
vmware-aria doctor [--skip-auth]
```

### Key Metric Names (for `resource metrics` command)

| Metric | API Key | What It Means |
|--------|---------|--------------|
| CPU Ready % | `cpu.ready.summation` | vCPU waiting for physical core; >5% = warning |
| CPU Used | `cpu.used.summation` | Actual CPU execution time |
| CPU Demand | `cpu.demand.average` | Total MHz requested by VM |
| Memory Active | `mem.active.average` | Actively used by guest OS (sizing) |
| Memory Consumed | `mem.consumed.average` | Footprint on host (capacity) |
| Memory Balloon | `mem.balloon.average` | **>0 = ESXi reclaiming memory** |
| Memory Swap | `mem.swapped.average` | **>0 = severe pressure** |
| Disk Read Latency | `disk.read.average` | Read I/O latency ms |
| Disk Write Latency | `disk.write.average` | Write I/O latency ms |
| Net Received | `net.received.average` | Inbound network KB/s |
| Net Transmitted | `net.transmitted.average` | Outbound network KB/s |

> Full CLI reference with all options and output formats: see `references/cli-reference.md`

## Troubleshooting

### "Token not found" error after setup

The token acquisition request failed. Verify:
1. Aria Ops is reachable: `vmware-aria doctor`
2. The `auth_source` in config matches your environment (LOCAL, LDAP, AD)
3. The password env var follows the naming convention: `VMWARE_ARIA_<TARGET>_PASSWORD`

### Resources appear missing from list_resources

The collector agent may be offline. Check `list_collector_groups` for any collectors in a DOWN state. Restart the affected collector from the Aria Ops UI under Administration > Collector Groups.

### Metrics return empty data

The resource may not have metric collection configured, or the requested metric key is incorrect. Verify metric keys against the resource's available metrics in the Aria Ops UI (Metrics tab on the resource detail page).

### "Password not found" error

Variable names follow the pattern `VMWARE_ARIA_<TARGET_NAME_UPPER>_PASSWORD` where hyphens become underscores. Example: target `prod` needs `VMWARE_ARIA_PROD_PASSWORD`. Check your `~/.vmware-aria/.env` file.

### `invalid peer certificate: UnknownIssuer` when running uvx (corporate TLS proxy)

`uvx` re-resolves dependencies from PyPI on every launch. Behind a corporate TLS-intercepting proxy whose CA is not in uv's bundled cert store, the handshake fails. Use the v1.5.15+ recommended single-command form `vmware-aria mcp` (after `uv tool install vmware-aria` — no network on launch), or set `UV_NATIVE_TLS=true` to make uv use the system cert store.

## Safety

- **Read-heavy**: 20 of 27 tools are read-only
- **Audit logging**: Write operations logged to `~/.vmware/audit.db` (SQLite WAL, via vmware-policy) with timestamp, user, target, operation, and result
- **Token expiry handling**: vRealizeOpsToken re-acquired automatically 60 seconds before expiry (6-hour sliding validity, extended on each call)
- **Prompt injection defense**: API text values sanitized via `_sanitize()` — strips control characters, truncates to 500 chars
- **Credential safety**: Passwords loaded only from environment variables (`.env` file), never from `config.yaml`
- **Input validation**: resource_id and alert_id validated before API calls; criticality values validated against known enum

## Setup

```bash
uv tool install vmware-aria
mkdir -p ~/.vmware-aria
cp config.example.yaml ~/.vmware-aria/config.yaml
# Edit config.yaml with your Aria Operations host details

# Add to ~/.vmware-aria/.env (create if missing, chmod 600):
# VMWARE_ARIA_PROD_PASSWORD=<your-password>
chmod 600 ~/.vmware-aria/.env

vmware-aria doctor
```

> All tools are automatically audited via vmware-policy. Audit logs: `vmware-audit log --last 20`

> Full setup guide with multi-target config, MCP server setup, and Docker: see `references/setup-guide.md`

## Architecture

```
User (natural language)
  |
AI Agent (Claude Code / Goose / Cursor)
  | reads SKILL.md
vmware-aria CLI or MCP server (stdio transport)
  | Aria Operations Suite API (REST/JSON over HTTPS)
  | POST /suite-api/api/auth/token/acquire → vRealizeOpsToken
Aria Operations Manager
  |
VMs / Hosts / Clusters / Datastores / Alerts / Capacity
```

The MCP server uses stdio transport (local only, no network listener). Connections to Aria Ops use HTTPS on port 443 with vRealizeOpsToken authentication (6-hour sliding token validity, auto-refreshed).

## Audit & Safety

All operations are automatically audited via vmware-policy (`@vmware_tool` decorator):
- Every tool call logged to `~/.vmware/audit.db` (SQLite, framework-agnostic)
- Policy rules enforced via `~/.vmware/rules.yaml` (deny rules, maintenance windows, risk levels)
- Risk classification: each tool tagged as low/medium/high/critical
- View recent operations: `vmware-audit log --last 20`
- View denied operations: `vmware-audit log --status denied`

vmware-policy is automatically installed as a dependency — no manual setup needed.

## License

MIT — [github.com/zw008/VMware-Aria](https://github.com/zw008/VMware-Aria)
