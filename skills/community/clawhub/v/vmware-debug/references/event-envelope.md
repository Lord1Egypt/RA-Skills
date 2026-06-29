# The Unified Event Envelope

This is the contract between `vmware-debug` and every data-source skill. The
orchestrating agent fetches events with each skill's own read tools, normalises
each into this shape, and passes the list to `incident_timeline`. Debug has **no
runtime dependency** on the other packages (no version lockstep, no heavy install).

## Shape

```json
{
  "ts":       "2026-06-23T10:15:30Z",
  "source":   "monitor",
  "severity": "error",
  "entity":   "vm-web01",
  "text":     "Device naa.600... performance has deteriorated",
  "fields":   { "host": "esxi-03", "datastore": "ds1" }
}
```

| Field | Type | Notes |
|---|---|---|
| `ts` | string \| number | ISO-8601, epoch **seconds**, or epoch **millis** (auto-detected). Required. |
| `source` | string | `monitor` \| `aria` \| `loginsight` \| `nsx` \| `nsx-security` \| `storage` \| ... |
| `severity` | string | Free text; normalised to `critical`/`error`/`warning`/`info`/`unknown`. |
| `entity` | string | The object the event is about (VM/host/datastore). May be empty. |
| `text` | string | Human-readable message — this is what the symptom classifier matches on. |
| `fields` | object | Any source-specific extras; preserved, never dropped. |

The normaliser is tolerant of common field-name variants (e.g. `timestamp`,
`createTime`, `startTimeUTC` for `ts`; `criticality`, `level` for `severity`;
`resourceName`, `vm_name`, `fullFormattedMessage` for entity/text), so most
sources map with little or no adaptation.

## Mapping cheatsheet per source

| Source tool (example) | ts | severity | entity | text |
|---|---|---|---|---|
| vmware-monitor `event_list` | `createdTime` | `severity` | `vm`/`host` | `fullFormattedMessage` |
| vmware-aria `alert_query` | `startTimeUTC` | `criticality` | `resourceName` | `alertDefinitionName` |
| vmware-aria `anomaly` | `timestamp` | (derive) | `resourceName` | stat + value |
| vmware-log-insight `log_search` | `timestamp` | `severity`/derive | `hostname` | `text` |
| vmware-nsx (firewall/traceflow) | `time` | (derive) | src/dst | rule/verdict |

## Why this design

- **Decoupling** — debug never imports monitor/aria/log-insight (CLAUDE.md 踩坑 #21/#32).
- **Testability** — correlation is pure functions over `Event`; unit tests feed synthetic events.
- **Transparency** — the cross-skill "联动" happens at the agent layer, visibly, not hidden inside debug.
