---
name: vmware-log-insight
description: >
  Use this skill whenever the user needs to search, aggregate, or investigate
  centralized logs in VMware VCF Operations for Logs (formerly Aria Operations
  for Logs / vRealize Log Insight) — the appliance that collects syslog from ESXi hosts, vCenter, and
  VMs. It is the log data source of the VMware family: full-text event search
  over a time window, aggregation with spike detection, field discovery, and
  alert queries. Always use this skill for "search the logs", "what did the host
  log", "find errors in Log Insight", "show me a log spike", "query vRealize Log
  Insight", "Aria Operations for Logs", "VCF Operations for Logs" when the context is explicitly
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
metadata: {"openclaw":{"requires":{"anyBins":["vmware-log-insight","uvx"]},"optional":{"env":["VMWARE_LOG_INSIGHT_CONFIG","VMWARE_LOG_INSIGHT_<TARGET>_PASSWORD","VMWARE_LOG_INSIGHT_<TARGET>_USERNAME","VMWARE_AUDIT_APPROVED_BY"]}}}
---

# VMware Log Insight

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware", "vSphere",
> and "Aria" are trademarks of Broadcom. Source is publicly auditable under the MIT license.

Read-only log search and aggregation for **VMware Aria Operations for Logs**
(vRealize Log Insight) — the centralized-log data source for the VMware skill
family. Strictly non-destructive: it queries, it never writes.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|---|---|:--:|:--:|
| Log search | `search_logs` | 1 | Read |
| Aggregation / spikes | `aggregate_logs` | 1 | Read |
| Metadata | `list_log_fields`, `get_log_insight_version` | 2 | Read |
| Alerts | `list_log_alerts`, `get_log_alert`, `get_log_alert_history` | 3 | Read |

**7 tools, all read-only.** No ingest, no alert creation/edit/delete — zero write surface.

## Quick Install

```bash
uv tool install vmware-log-insight==2.4.4
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
| Incident correlation / root cause | vmware-debug (feed it `search_logs` output) |
| Network logs / DFW / traceflow | vmware-nsx, vmware-nsx-security |

## Common Workflows

### 1. "Find the errors on a host in the last hour"
1. `search_logs(text="error", last="1h")` — or CLI: `vmware-log-insight search -q error -l 1h`. There is no host filter parameter: read each event's `fields.hostname` / `fields.source`, or put the host name in `text` (whole words match, and dots split words: `esx01` finds `esx01.lab.local`; `esx0` finds nothing, `esx0*` does).
2. Read the `events[]` (timestamp + text + fields). Narrow with a more specific `text` if `complete=False` (result was truncated).
3. **Failure branch — auth/connection error:** the teaching message names the cause (e.g. "503: appliance starting up"); run `vmware-log-insight doctor`. A 503 is a *status*, not a crash.

### 2. "Was there a log spike, and when?"
1. `aggregate_logs(text="...", last="6h", bin_width_ms=300000)` — counts per 5-minute bin + `spikes[]` (z-score flagged).
2. Take a spike's `timestamp_ms`, then `search_logs(begin_ms=..., end_ms=...)` around it to read what burst.
3. **Failure branch — empty bins:** widen `last` or drop the `text` filter; confirm the appliance actually receives logs from the source. The appliance omits bins with no events; for COUNT and UCOUNT the tool adds them back as 0 (`filled_empty_bins: true`), so a burst after a quiet stretch still shows as a spike.
4. Distinct hosts per bin: `aggregate_logs(aggregation="UCOUNT", field="hostname")`. Only COUNT and SAMPLE take no `field`; the other seven need one (names from `list_log_fields`).

### 3. Correlate logs into a root-cause timeline
1. `search_logs` / `aggregate_logs` here for the log signal.
2. Pull vCenter events (vmware-monitor) and metrics/anomalies (vmware-aria) for the same window/entity.
3. Hand all of them to **vmware-debug** `build_incident_timeline` (normalise to its event envelope) to rank root causes.

## Usage Mode

- **MCP** (in an agent): call `search_logs`/`aggregate_logs`, then pass results to vmware-debug. Primary mode.
- **CLI** (humans): `vmware-log-insight search -q "apd" -l 2h`.

## MCP Tools (7 — 7 read, 0 write)

| Category | Tools |
|---|---|
| Logs | `search_logs` (time window + text), `aggregate_logs` (COUNT/SAMPLE, or UCOUNT/AVG/MIN/MAX/SUM/STDDEV/VARIANCE of a `field`, + spike detection), `list_log_fields`, `get_log_insight_version` |
| Alerts | `list_log_alerts`, `get_log_alert`, `get_log_alert_history` |

**List envelope**: `list_log_fields`, `list_log_alerts` and `get_log_alert_history` return
`{items, returned, limit, total, truncated, hint}` rather than a bare list — read
the rows from `items`, and treat `truncated: true` as "there is more, raise
`limit` or narrow the filter". For fields and alerts `total` is a real count (the
appliance returns the whole collection in one GET and `limit` is applied here). Alert
history is paged by the appliance (at most 50 records), so a full history page has
`total: null` and `truncated: true`.

**Query model**: time windows use a relative `last` ("1h", "30m", "7d") or an
absolute `begin_ms`/`end_ms` (epoch ms — seconds are refused); `text` is a
CONTAINS search that matches whole words, not substrings (`*` is a wildcard). `search_logs`
returns at most 200 events (~650 chars each) and says so when it lowers `limit`. See
`references/cli-reference.md` for the full constraint grammar.

## Read-Only by Design

All 7 tools here are reads — no ingest, no alert creation/edit/delete, zero
write surface. Running with local or small models? See
[`references/agent-guardrails.md`](references/agent-guardrails.md).

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
- **`HTTP 400` on a search** — a malformed constraint. Time/field filters are path-encoded as `field/<OPERATOR value>` (e.g. `timestamp/LAST%203600000`); let the CLI/tool build them rather than hand-crafting.
- **Empty results but logs exist** — check the time window (`last`) and that the appliance actually ingests from that source; widen the window. `text` matches whole words: `localdom` finds nothing, `localdom*` (wildcard) and `localhost.localdomain` find events. A text search that matches nothing says so in `note`.
- **`UCOUNT needs a field` / `COUNT takes no field`** — the appliance answers HTTP 400 otherwise; pass `field=` only with UCOUNT/AVG/MIN/MAX/SUM/STDDEV/VARIANCE.
- **Default port is 9543**, not 443 — set `port` in `config.yaml` if your appliance differs.

## Audit & Safety

Read-only by construction (no write tools). MCP tools run through
`@vmware_tool(risk_level="low")`, which records each call to the shared audit DB
(`~/.vmware/audit.db`). Targets may declare `environment:` (`production` /
`staging` / `lab`) in `config.yaml` to scope policy rules; reads are never gated
by it, so this skill is unaffected either way, but declaring it keeps any future
write tool correctly scoped. Credentials load from `~/.vmware-log-insight/.env`
(`chmod 600`); plaintext passwords there are auto-rewritten to a grep-safe
`b64:` form on first load (obfuscation, not encryption — inject from a secret
manager for real at-rest secrecy). All API text passes through `sanitize()`
(prompt-injection defence). TLS verification is on by default; disable only for
self-signed lab appliances. See `references/setup-guide.md`.

## License

MIT.

## Current evidence boundary

Automatic transient transport/gateway retries apply only to GET reads. Do not replay a write after a lost response without checking the target; explicit authentication recovery is separate. See `references/capabilities.md`.
