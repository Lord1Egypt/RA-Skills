# vmware-log-insight Capabilities

VMware Aria Operations for Logs (vRealize Log Insight) public REST API v2,
base `https://<host>:9543/api/v2`, session auth (Bearer). All tools read-only.

| Tool | Endpoint | What it returns | Typical response tokens |
|---|---|---|---|
| `search_logs` | GET /events/{constraints} | `{count, complete, constraints, events:[{timestamp_ms, text, fields}]}` (+ `note` when `limit` was lowered) | ~160 per event: ~8000 at the default 50, ~32000 at the 200 cap |
| `aggregate_logs` | GET /aggregated-events/{constraints} | `{aggregation, field, bin_width_ms, bins:[{timestamp_ms, end_ms, value}], spikes:[...]}` | ~1100 for 1h of 1-minute bins |
| `list_log_fields` | GET /fields (+ GET /content/contentpack when a field belongs to a pack) | envelope of `[{name, internal_name, type[, display_name, content_pack]}]` | ~500 filtered; ~15000 unfiltered (~340 fields) |
| `get_log_insight_version` | GET /version | `{version, release_name, build}` | ~40 |
| `list_log_alerts` | GET /alerts | envelope of `[{id, name, enabled, info}]` | 100–1500 |
| `get_log_alert` | GET /alerts/{id} | `{id, name, enabled, info, raw_keys}` | 100–400 |
| `get_log_alert_history` | GET /alerts/{id}/history?limit= | envelope of `[{timestamp_ms, acknowledged, message_count, messages:[{timestamp_ms, text}]}]` (≤3 messages per record) | ~150 per record |

## List envelope

`list_log_fields`, `list_log_alerts` and `get_log_alert_history` return the family list envelope
rather than a bare list — read the rows from `items`:

```json
{
  "items": [{"id": "a1", "name": "Disk full", "enabled": true, "info": ""}],
  "returned": 50,
  "limit": 50,
  "total": 213,
  "truncated": true,
  "hint": "Showing 50 of 213. Raise limit or narrow the query with a filter to see the rest."
}
```

For `list_log_fields` and `list_log_alerts`, `total` is a **real** count, never an
estimate: the appliance returns the whole collection in one GET and this package
applies `limit` client-side. Two consequences worth relying on —

- `truncated: true` means rows were genuinely left behind; raise `limit` or
  narrow `name_filter`.
- A page that exactly fills `limit` is still reported `truncated: false` when it
  is genuinely the whole set, so no redundant follow-up query is needed.
- `list_log_fields` takes no `limit` at all, so it is always `truncated: false` —
  that is the complete field list, not a page of it.

`get_log_alert_history` is different: the appliance pages history itself (`limit`
up to 50; a larger value is lowered and `note` says so). A page shorter than
`limit` is the whole history and carries a real `total`; a full page has
`total: null` and `truncated: true`.

## High-signal design

- **Search over list**: `search_logs` defaults to `limit=50` and a 1-hour window,
  and returns at most 200 events (a larger `limit` is lowered and `note` says so;
  the appliance would send 20000, which on 8.18.7 was 16 MB and 31 s). Narrow with
  `text` or the window rather than raising the limit. `complete=False` signals
  server-side truncation.
- **Spike detection in-tool**: `aggregate_logs` returns z-score-flagged `spikes[]`
  so the agent gets "where did logs burst?" without scanning raw events.
- **Field flattening**: Log Insight's `fields` list is flattened to a `{name: value}`
  dict. Most entries carry `content`; on 8.18.7 the syslog header fields
  (`hostname`, `appname`, `procid`) instead carry `startPosition` + `length` into
  the event text, and the value is sliced from it. All text is `sanitize()`d
  (truncated + control-char stripped).

## Verified response shapes (8.18.7)

Captured read-only from a live 8.18.7-25423541 appliance on 2026-10-17; the
regression tests replay them (`tests/fixtures/li_8_18_7.json`).

| Endpoint | Top level | Notes |
|---|---|---|
| `GET /fields` | JSON array | items `{displayName, internalName, fieldType, isStatic, extracted[, displayNamespace]}`; some fields appear twice, identically (`source`, `facility`) — listed once |
| `GET /alerts` | JSON array | items carry `id` (UUID), `name`, `enabled`, `info`, `query`, `recipients`, `stats` |
| `GET /alerts/{id}` | object | unknown UUID → HTTP 404; a non-UUID id → HTTP 500 |
| `GET /alerts/{id}/history` | JSON array | records `{alertId, triggerTimestamp, acknowledged, resultUrl, messages}`, each with up to 10 messages `{text, timestamp, staticFields, extractedFields}` — captured from a temporary alert that fired twice, then deleted. No `triggerTimestampString`, though the API docs list one. `[]` for an alert that never fired. |
| `GET /events/{c}` | object | `{complete, duration, numResults, events}` |
| `GET /aggregated-events/{c}` | object | `bins: [{minTimestamp, maxTimestamp, *String, value}]`, newest first, empty bins omitted (the tool zero-fills them for COUNT/UCOUNT); `value` is an event for SAMPLE |
| `GET /version` | object | `{releaseName, version}` — the build is the version's suffix |
| `GET /content/contentpack` | object | `{contentPackMetadataList: [{name, namespace, ...}]}` — maps a field's `displayNamespace` (the pack's display name) to its namespace |

**Content-pack fields** are queried as `<pack namespace>:<displayName>`, e.g.
`com.vmware.vsphere:vmw_esxi_auth_failed_user`. Verified with one synthetic hostd
event: UCOUNT on the qualified name counted it; the bare display name and the
encoded `internalName` matched nothing. `list_log_fields` returns the qualified
name. Events only carry such fields when the query passes `content-pack-fields`,
which `search_logs` does not, so its `fields` hold static fields only.

Aggregation functions: COUNT and SAMPLE answer HTTP 400 with an
`aggregation-field`; UCOUNT, AVG, MIN, MAX, SUM, STDDEV and VARIANCE answer
HTTP 400 without one. An unknown field name returns an empty series, not an error.

## Auth & connection

- Session: `POST /api/v2/sessions {username, password, provider}` → `{sessionId, ttl}`;
  carried as `Authorization: Bearer <sessionId>`, re-acquired near TTL expiry.
- Errors are translated centrally to teaching `LogInsightApiError` (status + path +
  fix hint); transient 502/503/504 and transport errors get one retry, 401 triggers
  one re-auth, 4xx are not retried.

## Known limitations

- Exact v2 response schemas are parsed defensively across documented wire variants;
  they need confirmation against a live appliance's `/rest-api` reference (tracked in
  BACKLOG, same status as VKS `/wcp/login`).
- No ingest/write tools by design. Alert management (create/edit/delete) is out of scope.

## Maintenance safety boundary

Automatic transient transport/gateway retries apply only to GET reads. Do not replay a write after a lost response without checking the target; explicit authentication recovery is separate.
