---
name: vmware-aria
description: >
  Use this skill whenever the user needs VMware Aria Operations (VMware VCF Operations in VCF 9+) data — metrics, alerts, capacity, anomalies, reports.
  Directly handles: resource metrics plus metric key/property/relationship lookup, list/acknowledge/cancel alerts with notes and recommendations, alert definitions, capacity forecasts, anomalies, reports, resource maintenance mode, Aria's own node health and adapter collection state.
  Always use this skill for "check vSphere capacity", "what Aria Operations alerts are active", "show VMware anomalies", "generate an Aria report", "rightsizing recommendations", "VCF Operations alerts", "put this host in Aria maintenance mode", "is Aria Operations still collecting from vCenter", "what does Aria recommend for this alert", or any Aria Operations / VCF Operations / vRealize Operations task.
  Do NOT use for real-time vCenter alarms/events (use vmware-monitor), VM operations (use vmware-aiops), or NSX networking (use vmware-nsx).
  For load balancing/AVI/AKO use vmware-avi.
installer:
  kind: uv
  package: vmware-aria
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["vmware-aria","uvx"]},"optional":{"env":["VMWARE_ARIA_CONFIG","VMWARE_ARIA_<TARGET>_PASSWORD","VMWARE_ARIA_<TARGET>_USERNAME","VMWARE_AUDIT_APPROVED_BY"],"bins":["vmware-policy"]},"homepage":"https://github.com/vmware-skills/VMware-Aria","emoji":"📊","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All write operations audited to ~/.vmware/audit.db.
  Credentials: Each Aria Operations target requires a per-target password env var in ~/.vmware-aria/.env following the pattern VMWARE_ARIA_<TARGET_NAME_UPPER>_PASSWORD. Passwords are never logged or echoed.
  Read-heavy: 36 of 46 tools are read-only. Write operations limited to alert acknowledge/cancel, alert notes, alert definition management, report management, and resource maintenance start/end.
  No webhooks or guest operations. API calls use the configured Aria endpoint (HTTPS 443); MCP defaults to stdio, with opt-in authenticated HTTPS.
  Transitive dependencies: Only vmware-policy (audit/policy). No post-install scripts or background services.
---

# VMware Aria Operations

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "Aria" are trademarks of Broadcom. Source code is publicly auditable at [github.com/vmware-skills/VMware-Aria](https://github.com/vmware-skills/VMware-Aria) under the MIT license.

VMware Aria Operations (vRealize Operations 8.x, VCF Operations 9.x) AI-assisted monitoring — 46 MCP tools, by category below.

> **Version first**: `get_aria_health` reports product identity. Fleet/findings need 9.0+; PromQL uses 9.1 VODAP; unavailable on 8.x.
> **Versions are not a whitelist**: 9.1.1.0 is VCF Operations 9.x. Judge each API response; retain version floors and indexed-path restrictions. [Compatibility evidence](references/setup-guide.md#product-version-versus-feature-evidence).
> **Companion skills**: vmware-monitor (real-time vSphere), vmware-aiops (VM lifecycle), vmware-nsx (networking), vmware-avi (AVI/ALB/AKO), vmware-harden (compliance), vmware-pilot (approval workflows), vmware-policy (audit/policy).

## What This Skill Does

| Category | Tools | Count |
|----------|-------|:-----:|
| **Resources** | list, get details, metrics, health badge, top consumers, metric keys, properties, relationships | 8 |
| **Alerts** | list, get details, investigate (alert→resource), acknowledge, cancel, list definitions, list/add notes, recommendations | 9 |
| **Alert Definitions** | list symptoms, create definition, enable/disable, delete | 4 |
| **Capacity** | cluster overview, remaining capacity, time remaining, rightsizing | 4 |
| **Reports** | list templates, generate, list, get status+download URL, delete | 5 |
| **Anomaly** | list anomalies, risk badge | 2 |
| **Health** | Aria platform health, collector group status, Aria node memory/swap/heap, adapter collection state | 4 |
| **Maintenance** | start / end resource maintenance, list maintenance schedules | 3 |
| **Fleet / PromQL** (VCF Ops 9.1) | fleet certificates, password accounts, VCF domains, diagnostic findings, real-time PromQL query | 5 |
| **Raw API** | search the API operation index; GET one indexed path (read-only escape hatch) | 2 |

**Total**: 46 tools (36 read-only + 10 write)

Uncertain writes: inspect; GET-only retries.

## Quick Install

```bash
uv tool install vmware-aria==2.4.7
vmware-aria init      # guided setup: writes config + .env (chmod 600, password grep-safe), then verifies
vmware-aria doctor
```

## When to Use This Skill

- **Lookup**: which metric keys a resource reports (name, unit) before querying them, its properties, its parents and children
- **Performance**: VM contention (CPU Ready, balloon, swap), time-series metrics, top consumers, anomaly counts and risk badges
- **Alerts**: list, investigate, acknowledge or cancel alerts; read or add notes (who is handling it); read the alert's prioritized recommendations; list, create, enable/disable or delete alert definitions (post-RCA)
- **Capacity**: cluster headroom, time until full, VM rightsizing
- **Reports**: generate, poll, download and delete reports
- **Maintenance**: put a resource in maintenance before planned work (timed or until ended), end it, list maintenance schedules
- **Anything else the API reads**: when no tool answers, `search_api_operations` then one `get_api_path` (GET of an indexed path only)
- **Platform**: is Aria Operations itself healthy (DEGRADED vs DOWN, which service), which version and product line, collector groups, whether the Aria node is short of memory, which adapter stopped collecting

For VM changes, NSX, vSphere alarms, storage or load balancing, route with the table below.

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

> **Troubleshooting paths**: step-by-step playbooks for a DEGRADED platform, alert triage, VM contention, empty metrics, pre-resize checks and planned maintenance — [`references/ops-playbooks.md`](references/ops-playbooks.md).
>
> **Diagnostic investigations**: before any "why is X slow / failing / down" report, follow [`references/investigation-protocol.md`](references/investigation-protocol.md) — four root-cause criteria and up to three deepening rounds; never stop at a partial conclusion.

### Daily VM Health Check (Proactive Ops)

**Judgment**: don't chase the highest CPU consumer — chase the highest **contention** consumer. A VM at 90% CPU on a quiet host is healthy; a VM at 30% CPU but 15% Ready is starving. Key metrics: CPU Ready, Memory Balloon, Disk Latency.

1. Find top CPU consumers → `vmware-aria resource top --metric 'cpu|usage_average' --top 20` (this is the **starting set**, not the answer)
2. Check CPU Ready on hot VMs → `vmware-aria resource metrics <vm-id> --metrics 'cpu|readyPct' --hours 24`
   - >5% = warning, >10% = problem, >20% = critical
3. Check memory pressure → `vmware-aria resource metrics <vm-id> --metrics 'mem|balloonPct,mem|swapped_average' --hours 24`
   - Balloon >0 = ESXi reclaiming memory; Swap >0 = severe — act immediately
   - If a key comes back under `missing` instead of `metrics`, it is not a zero: `not_collected_for_resource` means a wrong key for this resource (use `similar_keys`), `no_data_in_window` means widen `--hours`
4. List active CRITICAL/IMMEDIATE alerts → `vmware-aria alert list --criticality CRITICAL`
5. Check anomaly counts → `vmware-aria anomaly list`
6. Cross-validate against the [investigation protocol](references/investigation-protocol.md) before reporting any "root cause" — high consumption is rarely the root, usually a downstream symptom

### Capacity Planning

1. List clusters → `vmware-aria resource list --kind ClusterComputeResource`
2. Get remaining capacity → `vmware-aria capacity remaining <cluster-id>`
3. Predict time until full → `vmware-aria capacity time-remaining <cluster-id>`
4. Get capacity overview → `vmware-aria capacity overview <cluster-id>`
5. Find rightsizing candidates → `vmware-aria capacity rightsizing` — act only on rows with `Act. yes`; read each VM's caveats and the vendor minimum size before reducing
   - If a yellow `properties_note` prints under the table, the VM property read failed: power state and current size are unknown and no row is actionable — retry, do not resize from it

### Post-Incident: Create Detection Alert (RCA Follow-up)

After an incident, create an early-warning alert. Alert definition management is **MCP-only**:

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

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | ~2K tokens vs ~8K for MCP |
| Cloud models (Claude, GPT-4o) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | Type-safe parameters, structured output |

Running vmware-aria with a local or small model? See [`references/agent-guardrails.md`](references/agent-guardrails.md) for tool-calling guardrails (alert-to-resource correlation and Aria data fidelity).

Every command accepts `--target <name>` (every MCP tool `target`) to pick the Aria Operations instance.

## MCP Tools (46 — 36 read, 10 write)

All MCP tools accept an optional `target`. The six destructive writes take `confirm`: without `confirm=true` they return a `blast_radius` and change nothing — show it to the user first.

| Category | Tool | Type | Description |
|----------|------|:----:|-------------|
| Resource | `list_resources` | Read | List VMs, hosts, clusters by resource kind (or `all`); `collection_status` finds objects not receiving data |
| | `get_resource` | Read | Get resource details with health, risk, efficiency badges |
| | `get_resource_metrics` | Read | Time-series stats; `interval_type=DAYS` for long windows; `summary=true` gives min/max/avg/p95/latest; `missing` explains absent |
| | `get_resource_health` | Read | Badge scores; service objects add `service.available` (a badge is not service state) |
| | `get_top_consumers` | Read | Rank by last-hour average `value` (`latest_value` = newest point) |
| | `list_metric_keys` | Read | Keys a resource reports with name/unit and `definition`, or a kind's defined keys — look up before querying |
| | `get_resource_properties` | Read | Current property values (power state, parent host, extraConfig) |
| | `get_resource_relationships` | Read | Related resources with `direction`; `relationship_type` ALL / PARENT / CHILD |
| Alerts | `list_alerts` | Read | List active alerts with criticality, resource ID, name and kind (`resource_name: null` = unknown, see `resource_names_note`) |
| | `get_alert` | Read | Alert details: named symptoms, the object each is on (e.g. the down service), ISO-8601 times |
| | `investigate_alert` | Read | Resolve an alert to its confirmed affected resource in one call — returns both UUIDs explicitly labelled plus the vmware-monitor handoff |
| | `acknowledge_alert` | **Write** | Mark an alert as acknowledged (does not close it) |
| | `cancel_alert` | **Write** | Cancel (dismiss) an active alert |
| | `list_alert_definitions` | Read | List alert templates configured in Aria Ops |
| | `list_alert_notes` | Read | Notes on an alert (who is handling it, what was done) |
| | `add_alert_note` | **Write** | Add a note; does not change the alert's status (low risk, not idempotent) |
| | `get_alert_recommendations` | Read | Prioritized recommendations from the alert's definition; `status` found / partial / none_defined / unknown |
| Alert Defs | `list_symptom_definitions` | Read | List symptom definitions — use IDs when creating alert defs |
| | `create_alert_definition` | **Write** | Create new alert definition from symptom definition IDs |
| | `set_alert_definition_state` | **Write** | Enable or disable an alert definition |
| | `delete_alert_definition` | **Write** | Delete an alert definition permanently |
| Capacity | `get_capacity_overview` | Read | Group-level remaining % + per-dimension headroom and days-until-full |
| | `get_remaining_capacity` | Read | Remaining CPU, memory, disk before hitting limits |
| | `get_time_remaining` | Read | Days until cluster capacity is exhausted |
| | `list_rightsizing_recommendations` | Read | Per-VM recommended size (raw MHz/KB/GB; use `recommended_vcpus`), direction, power state, `recommendation_stable` / `recommendation_range` (7-day movement), `actionable`, `caveats`, `properties_note`, `history_note` |
| Reports | `list_report_definitions` | Read | List available report definition templates |
| | `generate_report` | **Write** | Trigger report generation (async; returns report_id) |
| | `list_reports` | Read | List generated reports, optionally by definition |
| | `get_report` | Read | Poll report status + get PDF/CSV download URLs |
| | `delete_report` | **Write** | Delete a generated report |
| Anomaly | `list_anomalies` | Read | Per-resource anomaly counts (System Attributes\|total_alarms metric) |
| | `get_resource_riskbadge` | Read | Risk score (0–100): likelihood of future problems |
| Health | `get_aria_health` | Read | Platform `assessment` (HEALTHY/DEGRADED/DOWN/UNKNOWN), per-service health, product version |
| | `list_collector_groups` | Read | Collector agents status and connectivity |
| | `get_aria_node_resources` | Read | Aria node memory/swap/heap and watchdog restarts; memory pressure NORMAL / ELEVATED / HIGH / UNKNOWN |
| | `list_adapters` | Read | Adapter instances, last collection age, `stale` |
| Maintenance | `start_resource_maintenance` | **Write** | Timed (`duration_minutes` / `end_time_ms`) or manual maintenance; before/after state; undo = end |
| | `end_resource_maintenance` | **Write** | End maintenance; refuses a resource not known to be in maintenance |
| | `list_maintenance_schedules` | Read | Recurring maintenance schedules, optionally for one `resource_id` |
| Fleet / PromQL (VCF Ops 9.1) | `list_fleet_certificates` | Read | Certificate status/expiry across the VCF fleet |
| | `list_fleet_password_accounts` | Read | Managed password-account status (read-only; does not rotate) |
| | `list_fleet_domains` | Read | SDDC/workload domains behind one registered VCF integration |
| | `list_findings` | Read | Operations diagnostic findings (not compliance — see vmware-harden) |
| | `promql_query` | Read | Real-time PromQL instant query via the VODAP service (base path INFERRED, unverified on real hardware) |
| Raw API | `search_api_operations` | Read | Search the shipped 8.6 / 9.1 operation index; marks GET operations |
| | `get_api_path` | Read | GET one indexed path (`{id}` filled in, query in `params`); sanitized, capped at 30,000 chars (`truncated`) |

**Read/write split**: 36 read-only, 10 write. All write operations are audit-logged to `~/.vmware/audit.db` (via vmware-policy).

### List results are envelopes — read `truncated` before you summarise

List tools return `{items, returned, limit, total, truncated, hint}`, not a bare array. Rows are under `items`; `truncated: true` means more rows exist — never call it the complete set; `total: null` means the API gave no size. Full rules, per-tool `total` sources and `list_anomalies`' scan fields: [`references/capabilities.md`](references/capabilities.md#list-result-envelope).

## CLI Quick Reference

```bash
# Resources
vmware-aria resource list [--kind VirtualMachine|HostSystem|ClusterComputeResource|all] [--name <filter>] [--collection-status NO_DATA_RECEIVING]
vmware-aria resource get <resource-id>
vmware-aria resource metrics <resource-id> --metrics 'cpu|usage_average,mem|usage_average' --hours 4
vmware-aria resource metrics <vm-id> --metrics 'cpu|readyPct,mem|balloonPct' --hours 24 --summary
vmware-aria resource health <resource-id>
vmware-aria resource top --metric 'cpu|usage_average' --kind VirtualMachine --top 10
vmware-aria resource keys <resource-id> [--filter 'mem|']   # or --kind VirtualMachine
vmware-aria resource properties <resource-id> [--name 'summary|']
vmware-aria resource relationships <resource-id> [--type PARENT]

# Alerts
vmware-aria alert list [--criticality CRITICAL|IMMEDIATE|WARNING|INFORMATION] [--json]
vmware-aria alert get <alert-id>
vmware-aria alert acknowledge <alert-id>
vmware-aria alert cancel <alert-id>
vmware-aria alert definitions [--name <filter>]
vmware-aria alert notes <alert-id>
vmware-aria alert note-add <alert-id> "Taking this: rebooting esx-03"
vmware-aria alert recommendations <alert-id>

# Alert definitions and symptom lookup are MCP-only (no CLI subcommands).

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
vmware-aria health node [--hours 24]        # Aria node memory pressure, watchdog restarts
vmware-aria health adapters [--kind VMWARE] # stale = last collection older than max(3 x interval, 15 min)

# Maintenance (writes ask once; --yes skips, --dry-run prints the API call without connecting)
vmware-aria maintenance start <resource-id> --duration 60   # neither --duration nor --end = until `maintenance end`
vmware-aria maintenance end <resource-id>
vmware-aria maintenance schedules [--resource-id <id>]

# Raw API (read-only: GET of an indexed path only)
vmware-aria api search "resource properties" [--limit 20]
vmware-aria api get /api/resources/<id>/properties [--param pageSize=20]

# Diagnostics
vmware-aria doctor [--skip-auth]
```

### Key Metric Names (for `resource metrics` command)

| Metric | API Key | Unit | What It Means |
|--------|---------|------|--------------|
| CPU Ready | `cpu\|readyPct` | % | vCPU waiting for a physical core; >5% = warning |
| CPU Usage | `cpu\|usagemhz_average` | MHz | CPU actually used |
| CPU Demand | `cpu\|demandmhz` | MHz | CPU the VM requested |
| Memory Consumed | `mem\|consumed_average` | KB | Footprint on host (capacity) |
| Memory Balloon | `mem\|balloonPct` | % | **>0 = ESXi reclaiming memory** |
| Memory Swapped | `mem\|swapped_average` | KB | **>0 = severe pressure** |
| Memory Contention | `mem\|host_contentionPct` | % | Contention for host memory |
| Disk Throughput | `virtualDisk\|read_average`, `virtualDisk\|write_average` | KBps | Read / write rate |
| Disk Latency | `virtualDisk\|peak_vDisk_readLatency`, `virtualDisk\|peak_vDisk_writeLatency` | ms | Highest across the VM's virtual disks |
| Network | `net\|received_average`, `net\|transmitted_average` | KBps | Receive / transmit rate |

VirtualMachine keys and units as defined on Aria Operations 8.18.7; other resource kinds use different keys. Unreported keys come back under `missing`.

> Full CLI reference with all options and output formats: see `references/cli-reference.md`

## Troubleshooting

### "Token not found" error after setup

Token acquisition failed. Verify:
1. Aria Ops is reachable: `vmware-aria doctor`
2. The `auth_source` in config matches your environment (LOCAL, LDAP, AD)
3. The password env var follows the naming convention: `VMWARE_ARIA_<TARGET>_PASSWORD`

### Resources appear missing from list_resources

A collector may be offline: `list_collector_groups` shows DOWN ones. Restart it in the Aria Ops UI (Administration > Collector Groups).

### Metrics return empty data

Read `missing[].reason`: `not_collected_for_resource` (wrong key for this resource — try `similar_keys`), `no_data_in_window` (widen `--hours`, check collectors), `resource_reports_no_stat_keys`, or `undetermined`. Never report a missing key as zero.

### `health status` says OFFLINE (HTTP 503) but data still flows

The node flag is OFFLINE whenever any one service is not running. Read `assessment`: DEGRADED means some services are OK and others are not — not an outage. Seen on Aria Operations 8.18.7 with only `LOCATOR` not OK; `services_not_ok` names the failed ones.

### "Password not found" error

Set `VMWARE_ARIA_<TARGET_NAME_UPPER>_PASSWORD` (hyphens become underscores; target `prod` → `VMWARE_ARIA_PROD_PASSWORD`) in `~/.vmware-aria/.env`.

### `invalid peer certificate: UnknownIssuer` when running uvx (corporate TLS proxy)

`uvx` re-resolves from PyPI on every launch, and a TLS-intercepting proxy breaks that. Run `vmware-aria mcp` after `uv tool install vmware-aria==2.4.7` (no network on launch), or set `UV_NATIVE_TLS=true` to use the system cert store.

## Audit & Safety

1. **Source code**: [github.com/vmware-skills/VMware-Aria](https://github.com/vmware-skills/VMware-Aria) (MIT).
2. **Config and credentials**: `config.yaml` holds hosts and usernames only; passwords live in `~/.vmware-aria/.env` (chmod 600) as `VMWARE_ARIA_<TARGET>_PASSWORD` and are never logged.
3. **Network**: no webhooks. API calls use configured Aria HTTPS endpoints; MCP defaults to local stdio, with opt-in authenticated HTTPS.
4. **TLS**: verification on by default; for a private CA set `SSL_CERT_FILE` rather than `verify_ssl: false` (isolated labs only).
5. **Prompt-injection defense**: API text is sanitized (control characters stripped, length capped) before it reaches the agent.
6. **Least privilege**: use an Aria Operations account with read-only roles unless the write tools (alert acknowledge/cancel, alert notes, alert definitions, reports, resource maintenance) are needed.

Every tool call goes through vmware-policy (`@vmware_tool`): audited to `~/.vmware/audit.db`, subject to `~/.vmware/rules.yaml` deny rules and maintenance windows, each tool risk-tagged. View with `vmware-audit log --last 20` or `--status denied`. The suite-api token is re-acquired automatically before it expires. Setup, multiple targets, MCP clients and Docker: [`references/setup-guide.md`](references/setup-guide.md).

## License

MIT — [github.com/vmware-skills/VMware-Aria](https://github.com/vmware-skills/VMware-Aria)
