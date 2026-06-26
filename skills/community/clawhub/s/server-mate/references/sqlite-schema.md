# SQLite schema

## Purpose

Persist 10-minute and hourly rollup metrics so later report generators can read historical data without re-parsing old logs.

## Tables

### `agent_runs`

One row per collection cycle.

- `run_started_at`, `run_finished_at`: lifecycle timing for the agent cycle
- `host_id`, `site`, `mode`: who collected the data and whether it ran in `once` or `daemon`
- `access_lines_read`, `error_lines_read`: how many new lines were ingested this cycle
- `access_lines_dropped`, `error_lines_dropped`: parser failures
- `rollups_upserted`: how many rollup buckets were written or refreshed

### `metric_rollups`

One row per `(host_id, site, bucket_start, bucket_minutes)`.

- `bucket_start`, `bucket_end`: local-time bucket boundaries stored as ISO strings with timezone offsets
- `bucket_minutes`: rollup granularity such as `10` or `60`
- `request_count`, `pv`, `uv`, `unique_ips`, `active_users`, `qps`
- `avg_response_ms`, `slow_request_count`
- `bandwidth_out_bytes`, `bandwidth_in_bytes`
- `total_errors`
- `avg_cpu_pct`, `max_cpu_pct`, `avg_memory_pct`, `max_memory_pct`, `min_disk_free_bytes`

The table uses a unique constraint on `(host_id, site, bucket_start, bucket_minutes)` so the agent can safely rerun and refresh recently closed buckets with `UPSERT`.

### `status_code_rollups`

Status-code breakdown per rollup bucket.

- Primary key: `(rollup_id, status_code)`
- Stores counts for exact status codes such as `200`, `404`, and `502`

### `spider_rollups`

Spider-family traffic per rollup bucket.

- Primary key: `(rollup_id, spider_family)`
- Stores request counts and output bandwidth for each detected crawler family

### `error_category_rollups`

Error category breakdown per rollup bucket.

- Primary key: `(rollup_id, category)`
- Stores counts for categories such as `primary_script_unknown`, `upstream_timeout`, or `permission_denied`

### `error_fingerprint_rollups`

Top error fingerprints per rollup bucket.

- Primary key: `(rollup_id, fingerprint)`
- Stores de-duplicated fingerprint counters so daily reports can rank recurring failures more precisely than category-only aggregation

### `uri_rollups`

Top URI counts per rollup bucket.

- Primary key: `(rollup_id, uri)`
- Stores the top URI counters that later daily or weekly reports can turn into "top pages" sections

### `visitor_rollups`

Distinct visitor signatures per rollup bucket.

- Primary key: `(rollup_id, visitor_hash)`
- Stores hashed `client_ip + user_agent` visitor identities so reports can compute exact cross-bucket UV without persisting raw user-agent strings

### `client_ip_rollups`

Distinct client IPs per rollup bucket.

- Primary key: `(rollup_id, client_ip)`
- Supports exact daily unique-IP counting and leaves room for later GeoIP enrichment

### `slow_request_rollups`

Slow request routes per rollup bucket.

- Primary key: `(rollup_id, uri)`
- Stores slow-request counters so daily reports can rank the slowest endpoints without replaying raw access logs

### `suspicious_ip_rollups`

Suspicious IP activity per rollup bucket.

- Primary key: `(rollup_id, client_ip)`
- Stores the per-bucket request-rate peak for flagged IPs so daily and weekly security sections can surface attack hot spots

## Querying pattern

- Use `metric_rollups` as the fact table for time-series charts and host-health trends.
- Join detail tables by `rollup_id` when a report needs status-code pies, crawler trends, or top URI rankings.
- For daily or weekly reports, aggregate the 10-minute rows when detail matters, or read the hourly rows for lighter queries.
