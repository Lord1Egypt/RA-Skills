# Data contracts

## Core event types

Use four normalized event families as the base contract:

1. `system_snapshot`
   - Host health sampled from `psutil`
   - Use for CPU, memory, disk, load, and network counters
2. `access_event`
   - One parsed request from Nginx or Apache access logs
   - Use for traffic, status, performance, source, and spider analysis
3. `error_event`
   - One parsed error line from Nginx, Apache, PHP-FPM, or adjacent services
   - Use for alerting, de-duplication, AI explanation, and report ranking
4. `action_event`
   - One alert, dry-run, ban, unban, restart, or failed remediation attempt
   - Use for auditability and operator trust

## Shared fields

Every event should include:

```json
{
  "event_type": "access_event",
  "ts": "2026-03-25T10:00:00+08:00",
  "host_id": "web-01",
  "site": "example.com",
  "source": "nginx-access",
  "raw": "original log line or compact excerpt"
}
```

## Suggested payloads

### system_snapshot

```json
{
  "event_type": "system_snapshot",
  "cpu_pct": 71.4,
  "memory_pct": 63.1,
  "disk_used_pct": 54.8,
  "disk_free_bytes": 19434733568,
  "load_1m": 0.77,
  "net_rx_bytes": 1234567890,
  "net_tx_bytes": 987654321
}
```

### access_event

```json
{
  "event_type": "access_event",
  "client_ip": "203.0.113.8",
  "method": "GET",
  "uri": "/api/orders",
  "status": 200,
  "bytes_out": 4281,
  "bytes_in": 512,
  "response_ms": 182.4,
  "referer": "https://www.google.com/search?q=orders",
  "source_channel": "search",
  "source_name": "google",
  "user_agent": "Mozilla/5.0 ...",
  "spider_family": null
}
```

### error_event

```json
{
  "event_type": "error_event",
  "severity": "error",
  "component": "nginx",
  "category": "primary_script_unknown",
  "fingerprint": "primary_script_unknown:fastcgi_sent_in_stderr",
  "client_ip": "203.0.113.8",
  "uri": "/index.php",
  "message": "Primary script unknown"
}
```

### action_event

```json
{
  "event_type": "action_event",
  "action": "auto_ban",
  "target": "203.0.113.8",
  "reason": "cc_attack",
  "dry_run": true,
  "result": "scheduled",
  "ttl_seconds": 86400
}
```

## Metric definitions

- `PV`: total request count in the selected window
- `UV`: unique visitor key in the selected window; prefer app user ID or cookie; otherwise fall back to `client_ip + user_agent`
- `IP count`: unique client IPs in the selected window
- `Active users (10m)`: unique visitor keys in the latest rolling 10-minute window
- `QPS`: `request_count / window_seconds`
- `Average response ms`: mean of requests that actually expose a response-time field
- `Slow request`: request whose `response_ms` is above the configured threshold
- `Bandwidth out`: sum of response bytes
- `Bandwidth in`: sum of request bytes when the log format exposes it; otherwise return `null` and say so

## Status and source groupings

- Keep exact status codes and family buckets such as `2xx`, `3xx`, `4xx`, `5xx`.
- Track important exact codes separately:
  - `403`
  - `404`
  - `500`
  - `502`
  - `504`
- Classify source using the referer:
  - `direct`
  - `search`
  - `external`
  - `internal` when the site host is known and matches the referer host

## Natural-language query mapping

Translate each user question into:

1. Time window
2. Site scope
3. Optional filters
   - country or region
   - URI or route prefix
   - status code or family
   - bot family
   - source channel
4. Aggregation
   - count
   - top N
   - ratio
   - trend delta
   - grouped table
5. Caveat
   - missing GeoIP
   - UV approximation
   - missing request length
