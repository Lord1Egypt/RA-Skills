# The Unified Event Envelope

This is the contract between `vmware-debug` and every data-source skill. The
orchestrating agent fetches events with each skill's own read tools, normalises
each into this shape, and passes the list to `build_incident_timeline`. Debug has **no
runtime dependency** on the other packages (no version lockstep, no heavy install).

## Shape

```json
{
  "ts":       "2026-06-23T10:15:30Z",
  "source":   "monitor",
  "severity": "error",
  "entity":   "vm-web01",
  "text":     "Device naa.600... performance has deteriorated",
  "fields":   { "event_type": "esx.problem.scsi.device.io.latency.high",
                "host": "esxi-03", "datastore": "ds1" }
}
```

| Field | Type | Notes |
|---|---|---|
| `ts` | string \| number | ISO-8601, epoch **seconds**, or epoch **millis** (auto-detected). Required. |
| `source` | string | `monitor` \| `aria` \| `loginsight` \| `nsx` \| `nsx-security` \| `storage` \| ... The catalogue in `rules/evidence_sources.yaml` spells the same skills `vmware-monitor`, `vmware-aria`, `vmware-log-insight`. Both spellings are understood wherever a skill is named — `get_case_readiness(available_skills=...)`, and the grader's count of independent sources, which treats two spellings of one skill as one source. |
| `severity` | string | Free text; normalised to `critical`/`error`/`warning`/`info`/`unknown`. |
| `entity` | string | The object the event is about (VM/host/datastore). May be empty. |
| `text` | string | Human-readable message. Matched by the symptom classifier. |
| `fields` | object | Any source-specific extras; preserved, never dropped. `event_type` / `eventTypeId` is matched by the classifier too — see below. |

### `fields.event_type` is worth passing

The classifier matches the identifier as well as the prose, with camelCase and
dots split so a two-word keyword can reach it (`HostShutdownEvent` → `host
shutdown`, `esx.problem.cpu.ready` → `cpu ready`).

For a classic vCenter event this changes almost nothing — `VmMigratedEvent` and
its message say the same words. It matters for `EventEx`, which is how modern
vSphere emits most events: the message is generic boilerplate ("Issue detected on
esx01") and the whole identity is in `eventTypeId`. Drop that field and a storage
incident arrives as an unreadable event; keep it and it classifies as storage.

`vmware-monitor`'s `get_events` returns it as `event_type`; passing the row
through unchanged is enough.

The normaliser is tolerant of common field-name variants (e.g. `timestamp`,
`createTime`, `startTimeUTC` for `ts`; `criticality`, `level` for `severity`;
`resourceName`, `vm_name`, `fullFormattedMessage` for entity/text), so most
sources map with little or no adaptation.

## Mapping cheatsheet per source

| Source tool (example) | ts | severity | entity | text |
|---|---|---|---|---|
| vmware-monitor `get_events` | `createdTime` | `severity` | `vm`/`host` | `fullFormattedMessage` |
| vmware-aria `alert_query` | `startTimeUTC` | `criticality` | `resourceName` | `alertDefinitionName` |
| vmware-aria `anomaly` | `timestamp` | (derive) | `resourceName` | stat + value |
| vmware-log-insight `search_logs` | `timestamp` | `severity`/derive | `hostname` | `text` |
| vmware-nsx (firewall/traceflow) | `time` | (derive) | src/dst | rule/verdict |

## Why this design

- **Decoupling** — debug never imports monitor/aria/log-insight (CLAUDE.md 踩坑 #21/#32).
- **Testability** — correlation is pure functions over `Event`; unit tests feed synthetic events.
- **Transparency** — the cross-skill "联动" happens at the agent layer, visibly, not hidden inside debug.
