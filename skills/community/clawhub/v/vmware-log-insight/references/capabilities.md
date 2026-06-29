# vmware-log-insight Capabilities

VMware Aria Operations for Logs (vRealize Log Insight) public REST API v2,
base `https://<host>:9543/api/v2`, session auth (Bearer). All tools read-only.

| Tool | Endpoint | What it returns | Typical response tokens |
|---|---|---|---|
| `log_search` | GET /events/{constraints} | `{count, complete, constraints, events:[{timestamp_ms, text, fields}]}` | 400–4000 (scales with limit) |
| `log_aggregate` | GET /aggregated-events/{constraints} | `{aggregation, bin_width_ms, bins:[...], spikes:[...]}` | 200–1500 |
| `log_fields` | GET /fields | `[{name}]` | 100–800 |
| `log_version` | GET /version | `{version, release_name, build}` | ~40 |
| `alert_list` | GET /alerts | `[{id, name, enabled, info}]` | 100–1500 |
| `alert_get` | GET /alerts/{id} | `{id, name, enabled, info, raw_keys}` | 100–400 |
| `alert_history` | GET /alerts/{id}/history | `[{timestamp_ms, info}]` | 100–1500 |

## High-signal design

- **Search over list**: `log_search` defaults to `limit=50` and a 1-hour window;
  narrow with `text`/filters rather than raising the limit. `complete=False`
  signals server-side truncation.
- **Spike detection in-tool**: `log_aggregate` returns z-score-flagged `spikes[]`
  so the agent gets "where did logs burst?" without scanning raw events.
- **Field flattening**: Log Insight's `fields: [{name, content}]` is flattened to
  a `{name: content}` dict; all text is `sanitize()`d (truncated + control-char stripped).

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
