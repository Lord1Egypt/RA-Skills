# Architecture

## Goal

Build a lightweight monitoring stack for CentOS servers that can live next to Baota/BT panel instead of replacing it. Split responsibilities cleanly:
- Server agent: collect host metrics, parse access and error logs, emit structured events
- OpenClaw-side analyzer: aggregate, answer questions, enrich errors, trigger alerts, and manage guarded automation

## Deployment assumptions

- Expect CentOS or another RHEL-like host.
- Expect Nginx, Apache, or both behind Baota/BT panel.
- Do not assume any vendor-specific log tree. Always verify the actual `access_log` and `error_log` directives or set explicit paths in `config.yaml`.
- Expect PHP-FPM for many PHP sites, but do not assume a single service name. Some environments use `php-fpm`, others use versioned units or init scripts.
- Expect webhook targets such as WeCom, DingTalk, or ServerChan to be configured outside the core parser.

## Component layout

1. Agent process
   - Sample `cpu`, memory, disk, load, and network I/O with `psutil`
   - Tail `access.log` and `error.log`
   - Convert lines to normalized JSON
   - Push batches through stdout, file drop, HTTP POST, or websocket transport
2. Ingestion layer
   - Accept event batches
   - Attach host metadata and ingestion timestamps
   - Reject malformed payloads without losing the raw line reference
3. Storage layer
   - Keep append-only raw events for replay
   - Keep rollup tables or cached counters for fast natural-language answers
4. Analysis layer
   - Compute traffic, performance, security, spider, and error metrics
   - Detect threshold breaches and burst patterns
   - Generate summaries for reports and chat answers
5. Notification and action layer
   - Format webhook messages
   - Gate auto-ban and auto-heal behind policy checks
   - Write audit events for every action

## Recommended rollout

1. Deliver read-only collection first.
   - System snapshots
   - Access event parsing
   - Error event parsing
2. Deliver rollups next.
   - PV, UV, IP counts
   - Status breakdown
   - QPS and response time
   - Top URIs and sources
   - Error categories and fingerprints
3. Deliver notifications next.
   - CPU, memory, disk
   - 5xx burst
   - suspicious IP and 404 burst
   - latency degradation
4. Deliver automation last.
   - auto-ban with TTL and allowlists
   - auto-heal with cooldowns and health checks

## Logging requirements

- Prefer an access log that exposes:
  - remote IP
  - timestamp
  - request line
  - status code
  - response bytes
  - referer
  - user-agent
  - response time
  - request length or another upload-size proxy if upload metrics matter
- If the current log format does not include response time or request length, treat those metrics as unavailable until the log format is extended.
- Keep raw log excerpts on normalized events so an analyst can still inspect parser edge cases.

## Failure domains

- Parser failure: count and surface it; never hide it.
- Transport failure: queue or retry without duplicating parsed offsets.
- Alert failure: preserve the alert event even if the webhook is down.
- Action failure: write the command, target, outcome, and rollback guidance to the audit trail.
