---
name: vmware-log-insight
description: >
  Use this skill whenever the user needs to search, aggregate, or investigate
  centralized logs in VMware Aria Operations for Logs (formerly vRealize Log
  Insight) — the appliance that collects syslog from ESXi hosts, vCenter, and
  VMs. It is the log data source of the VMware family: full-text event search
  over a time window, aggregation with spike detection, field discovery, and
  alert queries. Always use this skill for "search the logs", "what did the host
  log", "find errors in Log Insight", "show me a log spike", "query vRealize Log
  Insight", "Aria Operations for Logs" when the context is explicitly
  VMware/vSphere/ESXi. It is strictly READ-ONLY — it never ingests, edits, or
  deletes anything. Do NOT use it for vCenter events/alarms (use vmware-monitor)
  or for performance metrics and anomalies (use vmware-aria). To correlate logs
  with events from other sources into one root-cause timeline, hand results to
  vmware-debug.
installer:
  kind: uv
  package: vmware-log-insight
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["VMWARE_LOG_INSIGHT_CONFIG"],"bins":["vmware-log-insight"],"config":["~/.vmware-log-insight/config.yaml"]},"primaryEnv":"VMWARE_LOG_INSIGHT_CONFIG"}}
---

# VMware Log Insight

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware", "vSphere",
> and "Aria" are trademarks of Broadcom. Source is publicly auditable under the MIT license.

Read-only log search and aggregation for **VMware Aria Operations for Logs**
(vRealize Log Insight) — the centralized-log data source for the VMware skill
family. Strictly non-destructive: it queries, it never writes.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|---|---|:--:|:--:|
| Log search | `log_search` | 1 | Read |
| Aggregation / spikes | `log_aggregate` | 1 | Read |
| Metadata | `log_fields`, `log_version` | 2 | Read |
| Alerts | `alert_list`, `alert_get`, `alert_history` | 3 | Read |

**7 tools, all read-only.** No ingest, no alert creation/edit/delete — zero write surface.

## Quick Install

```bash
uv tool install vmware-log-insight
cp config.example.yaml ~/.vmware-log-insight/config.yaml   # then edit
vmware-log-insight doctor       # verify connectivity
```

## When to Use This Skill

Use it to read the **actual log lines** behind an incident — what an ESXi host's
vmkernel logged, vCenter vpxd errors, a login storm in VM syslog — and to find
**when** log volume spiked.

- vCenter events/alarms (not raw syslog)? → **vmware-monitor**
- Performance metrics / anomalies / capacity? → **vmware-aria**
- Correlate logs + events + metrics into one root-cause view? → **vmware-debug**

**Do NOT use when** there is no Log Insight appliance, or the user wants vCenter
alarms (monitor) or metric anomalies (aria). This skill only reads the log store.

## Related Skills — Skill Routing

| Need | Skill |
|---|---|
| Raw centralized logs + spikes | **vmware-log-insight** (this) |
| vCenter events & alarms | vmware-monitor |
| Metrics, anomalies, capacity | vmware-aria |
| Incident correlation / root cause | vmware-debug (feed it `log_search` output) |
| Network logs / DFW / traceflow | vmware-nsx, vmware-nsx-security |

## Common Workflows

### 1. "Find the errors on a host in the last hour"
1. `log_search(text="error", last="1h", filters via CLI hostname=...)` — or CLI: `vmware-log-insight search -q error -l 1h`.
2. Read the `events[]` (timestamp + text + fields). Narrow with a more specific `text` if `complete=False` (result was truncated).
3. **Failure branch — auth/connection error:** the teaching message names the cause (e.g. "503: appliance starting up"); run `vmware-log-insight doctor`. A 503 is a *status*, not a crash.

### 2. "Was there a log spike, and when?"
1. `log_aggregate(text="...", last="6h", bin_width_ms=300000)` — counts per 5-minute bin + `spikes[]` (z-score flagged).
2. Take a spike's `timestamp_ms`, then `log_search(begin_ms=..., end_ms=...)` around it to read what burst.
3. **Failure branch — empty bins:** widen `last` or drop the `text` filter; confirm the appliance actually receives logs from the source.

### 3. Correlate logs into a root-cause timeline
1. `log_search` / `log_aggregate` here for the log signal.
2. Pull vCenter events (vmware-monitor) and metrics/anomalies (vmware-aria) for the same window/entity.
3. Hand all of them to **vmware-debug** `incident_timeline` (normalise to its event envelope) to rank root causes.

## Usage Mode

- **MCP** (in an agent): call `log_search`/`log_aggregate`, then pass results to vmware-debug. Primary mode.
- **CLI** (humans): `vmware-log-insight search -q "apd" -l 2h`.

## MCP Tools (7 — 7 read, 0 write)

| Category | Tools |
|---|---|
| Logs | `log_search` (time window + text + filters), `log_aggregate` (COUNT/etc + spike detection), `log_fields`, `log_version` |
| Alerts | `alert_list`, `alert_get`, `alert_history` |

**Query model**: time windows use a relative `last` ("1h", "30m", "7d") or an
absolute `begin_ms`/`end_ms` (epoch ms); `text` is a CONTAINS search. See
`references/cli-reference.md` for the full constraint grammar.

## CLI Quick Reference

```bash
vmware-log-insight search -q "scsi apd" -l 2h          # search events
vmware-log-insight search -q error -l 1h --json        # raw JSON
vmware-log-insight aggregate -q error -l 6h --bin-ms 300000   # spikes
vmware-log-insight fields --name host                  # discover fields
vmware-log-insight alert list                          # defined alerts
vmware-log-insight doctor                              # diagnostics
vmware-log-insight mcp                                  # start MCP server (proxy-safe)
```

## Troubleshooting

- **`POST /sessions returned HTTP 401`** — wrong username/password/provider. Check `config.yaml` (`provider: Local | ActiveDirectory`) and the `VMWARE_LOG_INSIGHT_<TARGET>_PASSWORD` env var.
- **`HTTP 503` on every call** — the appliance is starting or a service isn't ready; the error says so. Wait and retry; `doctor` reports it as a status, not a crash.
- **`HTTP 400` on a search** — a malformed constraint. Time/field filters are path-encoded as `field/OPERATOR/value`; let the CLI/tool build them rather than hand-crafting.
- **Empty results but logs exist** — check the time window (`last`) and that the appliance actually ingests from that source; widen the window.
- **Default port is 9543**, not 443 — set `port` in `config.yaml` if your appliance differs.

## Audit & Safety

Read-only by construction (no write tools). MCP tools run through
`@vmware_tool(risk_level="low")`, which records each call to the shared audit DB
(`~/.vmware/audit.db`). Credentials load from `~/.vmware-log-insight/.env`
(`chmod 600`); plaintext passwords there are auto-rewritten to a grep-safe
`b64:` form on first load (obfuscation, not encryption — inject from a secret
manager for real at-rest secrecy). All API text passes through `sanitize()`
(prompt-injection defence). TLS verification is on by default; disable only for
self-signed lab appliances. See `references/setup-guide.md`.

## License

MIT.
