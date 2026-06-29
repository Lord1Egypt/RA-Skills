---
name: server-mate
version: 1.5.1
description: Build or extend a lightweight server monitoring and AI operations workflow for Linux hosts running Nginx or Apache, with optional centralized remote monitoring through the BT-Panel (Baota) HTTP API. Use when Codex needs to collect psutil metrics, parse access, error, or auth logs (locally OR pulled remotely from BT panels with no probe on the target host), design JSON payloads or APIs, add webhook alerts, generate PDF ops reports with SSL expiry summaries, answer natural-language monitoring questions, or implement guarded auto-ban and auto-heal behaviors.
homepage: https://github.com/tankeito/server-mate
metadata:
  clawdbot:
    files:
      - scripts/*
      - references/*
      - config.example.yaml
      - user-guide.md
      - _meta.json
---

# Server Mate

Version: `1.5.1`

Use this skill to design or implement a two-plane monitoring system:
- a Python agent that tails local logs OR pulls remote logs through the BT-Panel HTTP API (centralized, agentless), and samples host metrics
- an OpenClaw-side analyzer that aggregates data, explains failures, answers questions, and sends alerts

The same Agent serves both layouts: leave `panel_id` empty on a site to keep the legacy local-tail path; set `panel_id` on a site to pull its access / error logs remotely with no probe installed on the target host.

## Start

- Confirm the environment first: Linux distribution, Nginx or Apache, PHP-FPM layout, log paths, webhook target, and whether automated actions may touch a live host.
- Keep collection read-only until the user explicitly asks for automation. Add alerting before any auto-ban or auto-heal behavior.
- In OpenClaw deployments, `OPENAI_API_KEY` is injected by the runtime when AI analysis is enabled. Do not ask the user to export it manually. Treat webhook URLs or tokens in `config.yaml` as secrets and do not commit them.
- Treat `./data/GeoIP.conf` the same way. It may contain MaxMind `AccountID` and `LicenseKey`, so keep it local-only and out of Git.
- Prefer MaxMind's official GeoLite2 workflow through `./data/GeoIP.conf` and `geoipupdate`. Treat the built-in public mirror fallback only as an operator-reviewed bootstrap path when no local `.mmdb` file is present.
- Treat auto-ban and auto-heal as privileged features. They may execute operator-supplied firewall or service restart commands and should stay disabled or `dry_run: true` until reviewed.
- Use the references progressively instead of loading everything at once:
  - Read [references/architecture.md](references/architecture.md) for overall design, component boundaries, and rollout order.
  - Read [references/data-contracts.md](references/data-contracts.md) before defining JSON payloads, storage schemas, metrics, or natural-language query handlers.
  - Read [references/ops-playbook.md](references/ops-playbook.md) before implementing thresholds, webhooks, reports, auto-ban, or self-heal logic.
  - Read [references/sqlite-schema.md](references/sqlite-schema.md) before extending historical storage or report queries.
  - Use [scripts/server_agent.py](scripts/server_agent.py) as the collector, daemon entrypoint, and SQLite rollup writer.

## Delivery workflow

1. Map the request to one or more tracks.
   - Agent collection
   - Aggregation and storage
   - Alerting and reporting
   - AI diagnosis
   - Guarded remediation
2. Implement the smallest safe slice first.
   - Start with structured access, error, and system events.
   - Add rollup metrics and natural-language answers next.
   - Add webhook alerts after the counters are stable.
   - Enable auto-ban or auto-heal only when thresholds, cooldowns, allowlists, and audit logs already exist.
3. **Remote panel connectivity test (mandatory before first collection of any new BT panel).** When `remote_panels` and `sites[].panel_id` are first wired up, do not jump straight into `--once`. First prove the auth handshake works end-to-end with a minimal, side-effect-free probe:
   - Instantiate the panel client (`build_panel_registry` or equivalent).
   - Issue ONE `BTPanelClient.exec_shell("echo server-mate-probe")` per panel and assert the returned stdout equals `server-mate-probe`.
   - On `BTPanelAuthError`: the most common root cause is **NTP clock drift** between the Agent host and the panel host — surface the hint emitted by the client and have the operator run `chronyc tracking` / `timedatectl status` on both ends before re-trying. Also verify `api_key_env` actually resolves to a non-empty string and that the panel URL includes the correct port.
   - On any other `BTPanelError`: confirm the panel URL is reachable from the Agent host, the panel's API access switch is enabled, and that no firewall is blocking the port.
   - Only after the probe succeeds for every configured panel may the agent enter normal cron-driven collection.
4. Validate with real or synthetic logs before changing production services.
5. Explain caveats in plain language.
   - Example: UV is often an approximation based on IP and user-agent unless the site provides a stronger visitor key.
   - Example: upload bandwidth is unavailable unless the access log includes request length or a similar field.

## Agent rules

- Prefer Python, `psutil`, and the standard library for the first implementation.
- Prefer a generated `./config.yaml` plus local SQLite state such as `./metrics.db` before adding external services.
- Keep generated artifacts inside the current skill workspace by default: `./config.yaml`, `./metrics.db`, `./logs/`, and `./reports/`. Do not default to `/opt`, `/var/log`, or other system-wide directories.
- Prefer the `system_metrics + sites[]` matrix layout from [config.example.yaml](config.example.yaml) instead of new single-site keys.
- Support configurable log paths. Do not hardcode site layouts when the vhost config can be read instead.
- Emit structured JSON with timezone-aware timestamps, host or site identifiers, event type, and enough raw context to debug parser mistakes.
- In multi-site mode, collect host CPU or memory metrics once per cycle and keep site log parsing isolated per domain.
- Separate parsing, aggregation, transport, and action execution so that HTTP push, stdout replay, file drop, or websocket transport can be swapped independently.
- Keep unknown lines and parser failures as first-class counters instead of dropping them silently.
- When the user asks to monitor a remote server that already runs BT-Panel (Baota), do **not** instruct them to install Server-Mate, a daemon, or any extra package on that target. Instead, guide them to declare the panel under the global `remote_panels` block in `config.yaml` and bind the relevant `sites[]` entry to it via `panel_id`. The local Agent will pull access / error logs through the BT HTTP API automatically. Always inject the `api_key` via `api_key_env`, never as plaintext, and remind the user that `config.yaml` containing any panel credential must stay out of version control.
- Any code path that builds a remote shell command **must** route every operator-supplied path through the project's `_safe_remote_path` helper (or an equivalent: `shlex.quote` PLUS a structural rejection of NUL / CR / LF / empty input). Never f-string a raw `remote_path`, glob, or filename into an `ExecShell` payload, even when the value "obviously" comes from `config.yaml` — configuration is an attacker-controlled surface in multi-tenant or shared-checkout deployments. The same rule applies to any new BT API helper added later (file move, log rotate, restart command, etc.): validate, then quote, then splice.

## Analyzer rules

- Store raw events separately from derived counters.
- Model traffic, performance, security, spider, and error signals as independent reducers over the same event stream.
- Translate natural-language requests into:
  - a time window
  - filters
  - an aggregation
  - a presentation format
- For AI error explanations, pass the fingerprint, surrounding context, and normalized fields instead of dumping entire logs.

## Safety rules

- Treat auto-ban and auto-heal as opt-in features.
- Default Guarded Automation to `dry_run: true` and keep it there until the user has observed automation notifications and audit history for several days.
- Never flip `dry_run` to `false`, or enable `auto_ban.enabled` / `auto_heal.enabled`, unless the operator explicitly approves the command templates, allowlists, cooldowns, and audit destinations.
- Require cooldowns, max actions per window, and allowlists before running firewall or restart commands.
- Require whitelist checks before any ban command. Never ban loopback, RFC1918 private ranges, or trusted crawler families by default.
- Require TTL-based unban or an equivalent release plan for every ban. Do not create permanent firewall blocks from the first implementation.
- Record an audit event for every alert, dry-run, ban, unban, restart, and failed remediation attempt.
- Store audit history in SQLite tables such as `automation_actions` and `banned_ips`, and expose simple lookup queries in user-facing docs.
- Prefer one-shot remediation followed by escalation. Do not loop restarts.

## Report expectations

- Daily report: prior-day PV, UV, IP, request totals, bandwidth, status mix, top errors, and slow endpoints.
- Weekly report: blocked IP trends, crawler trends, suspicious route clusters, and recurring slow routes.
- Monthly report: bandwidth peak, disk growth, capacity warning, and remediation summary.

## Automation scheduling

Use external scheduling for production unless the user explicitly wants an always-on daemon-only design.

- Recommended ingestion pattern:
  - Run `server_agent.py --once` every 10 minutes from `cron` or a `systemd timer`.
  - This keeps log parsing incremental, writes SQLite rollups, and avoids duplicate resident processes.
- For `systemd` deployments in Clawhub-style packaging:
  - Do not rely on bundling a `.service` file inside the skill package.
  - Generate a host-local unit with `server_agent.py --config ./config.yaml --generate-service`, then paste it into `/etc/systemd/system/server-mate.service`.
- Recommended report pattern:
  - Run `report_generator.py` as one-shot scheduled jobs.
  - Daily PDF push at `01:00`.
  - Weekly PDF push every Monday at `01:10`.
  - Monthly PDF push on day `1` at `01:20`.
- In multi-site mode, a single scheduled `report_generator.py` run should iterate over every configured site unless the user explicitly passes `--site`.

## Release notes for 1.5.1

- **Post-Alert Automatic Diagnostics**: Added `run_alert_diagnostics()` which triggers diagnostic shell commands (e.g., `ps`, `uptime`, `ss`, `free`, `dmesg`, `df`, `systemctl status`) when hardware/service alerts fire, appending commands output directly to webhooks.
- **Alert Recovery Notifications**: Added `track_alert_recovery()` and `deliver_recovery_alerts()` to track currently firing alerts in state and notify webhooks when resolved (e.g. ✅ Server-Mate 已恢复), including human-readable duration statistics and peak values.
- **Diagnostics Configuration**: Added configurable settings under `diagnostics` section (`enabled`, `timeout_seconds`, `max_lines_per_command`, `recovery_notification`, `recovery_min_duration_seconds`).

## Release notes for 1.5.0

- **Deep Linux System Metrics — 4-Layer Expansion**: `collect_system_snapshot()` now collects 28+ metrics across four layers, all via `psutil` + standard library (zero new dependencies).
  - **Layer 1 — CPU detail, memory/swap, disk IOPS, network rate**: `cpu_user_pct`, `cpu_system_pct`, `cpu_iowait_pct`; `swap_used_pct`, `swap_used_bytes`, `memory_used_bytes`, `memory_available_bytes`; per-cycle delta `disk_read_iops`, `disk_write_iops`, `disk_read_bytes_delta`, `disk_write_bytes_delta`; `net_rx_mbps`, `net_tx_mbps`, `net_rx_errs`, `net_tx_errs`, `net_rx_drop`, `net_tx_drop`.
  - **Layer 2 — Process accounting**: `process_count`, `process_running`, `process_sleeping`, `process_zombie`; `top_cpu_procs` and `top_mem_procs` (top 5 each).
  - **Layer 3 — Inode & extra partitions**: `disk_inode_used_pct` on root; configurable `extra_disk_partitions` list with per-mount `used_pct`, `free_bytes`, and `inode_used_pct`.
  - **Layer 4 — TCP states & systemd service health**: `tcp_established`, `tcp_time_wait`, `tcp_close_wait` from `psutil.net_connections`; configurable `service_probes` list checked via `systemctl is-active` (returns `service_failed_units`).
- **Delta I/O tracking via `_io_state`**: a mutable dict passed through `run_cycle` → `collect_system_snapshot` persists previous counter values across calls, enabling accurate per-cycle rate metrics without a resident process.
- **10 new alert kinds** in `evaluate_alerts()`: `iowait_high`, `swap_high`, `memory_critical`, `net_errors`, `high_iops`, `zombie_process`, `inode_low`, `disk_multi_low`, `tcp_timewait_high`, `service_down` — each with a dedicated label, remediation suggestion, and detail block in `render_alert_markdown()`.
- **7 new threshold keys** in `config.yaml` / `normalize_config()`: `iowait_pct` (30%), `swap_pct` (60%), `memory_min_available_mb` (200 MB), `net_error_count` (100), `disk_write_iops` (5 000/s), `inode_used_pct` (90%), `tcp_timewait_count` (5 000).
- **4 new `system_metrics` config options**: `collect_processes`, `collect_tcp_states`, `service_probes`, `extra_disk_partitions` — all default-safe and backwards compatible.
- **Zero-downtime DB migration**: `migrate_schema()` is called from `init_database()` and idempotently `ALTER TABLE metric_rollups ADD COLUMN` for all 11 new columns using `PRAGMA table_info` — existing databases are upgraded in-place without data loss.
- **11 new `metric_rollups` columns**: `avg_cpu_iowait_pct`, `avg_swap_used_pct`, `avg_net_rx_mbps`, `avg_net_tx_mbps`, `avg_disk_read_iops`, `avg_disk_write_iops`, `max_process_count`, `max_zombie_count`, `min_inode_free_pct`, `avg_tcp_established`, `max_tcp_timewait` — all persisted through `upsert_metric_rollup()`.

## Release notes for 1.4.1

- **Centralized Remote Monitoring architecture**: Server-Mate is now formally a single-Agent-many-hosts collector. Local sites (`panel_id` empty) and remote sites (`panel_id` bound to a `remote_panels` entry) coexist in the same `sites[]` matrix and share every downstream pipeline (rollups, AI diagnosis, webhooks, PDF reports). Target servers require **only** that BT-Panel API access is enabled — no Python interpreter, no probe, no daemon, no log shipper.
- **Deep BT-Panel API integration**:
  - Compliant signing scheme — HMAC-like MD5 signature: `request_token = md5(str(request_time) + md5(api_key))`, regenerated on every attempt (including retries).
  - Strict POST-only transport per BT official documentation, with auth and business parameters merged into the same `application/x-www-form-urlencoded` body.
  - `requests.Session()` per panel for TCP/TLS pooling and BT cookie persistence — eliminates handshake overhead in cron-driven, high-frequency workloads.
- **Memory safety — byte-level throughput protection**: each cycle issues a single `tail -c +<offset> | head -c <chunk>` ExecShell call capped at `chunk_bytes` (default 5 MB). When a remote `error_log` explodes by hundreds of MB the Agent's memory footprint stays constant, OOM and HTTP timeout are categorically prevented, and residual bytes roll over to subsequent cron ticks. Backlog is stamped into the persisted cursor (`backlog_bytes`, `status="backlog"`) and emitted as a WARNING.
- **Security hardening**:
  - Command-injection defense via `_safe_remote_path` = `shlex.quote` + structural NUL/CR/LF rejection — applied to every remote path before it is spliced into any ExecShell command. Mandatory for every new BT helper added later.
  - NTP time-drift auto-detection: HTTP 401/403 *and* HTTP 200 + `{"status": false, "msg": "request_token error"}` payloads are recognised (English + Chinese variants) and surfaced with the operator-facing hint *"Authentication failed. Please check if the time on the Agent server and the Remote BT panel are synchronized (NTP Time Drift)."* — both in the raised `BTPanelAuthError` and in the WARNING log.
- **LogReader abstraction** (`scripts/log_reader.py`): `LocalLogReader` (delegates to the existing inode/truncate-aware function) and `BTRemoteLogReader` (maintains `remote_offset` + `remote_size`, treats `remote_size < remote_offset` as logrotate). State persists into the existing `server_agent_state.json` so restarts neither double-read nor lose remote bytes.
- **Per-site fault isolation** in `run_cycle`: a single flaky panel can never crash the cron tick or starve other sites; the failure is captured and stamped into the cursor's `status` field for operator visibility.

## Release notes for 1.3.2

- Multi-site matrix config using `sites[]` plus global `system_metrics`
- Host-global metrics stored separately from site-local business rollups
- Logrotate-tolerant incremental readers with inode or truncate recovery
- Guarded Automation with `dry_run`, whitelist checks, TTL-based unban, cooldown-based auto-heal, and SQLite audit trail
- SSH brute-force detection from `logs.auth_log` with `ssh_brute_force` alerting and optional linked auto-ban
- SSL certificate expiry inspection in report generation and webhook summaries
- Telegram delivery support for alerts and report notices
- GeoIP official refresh support via local `./data/GeoIP.conf` and `geoipupdate`, with an operator-reviewed public mirror bootstrap fallback
- `config.example.yaml` and docs updated for MaxMind GeoLite2 setup in the current workspace

Copyable cron examples:

```cron
*/10 * * * * /usr/bin/env bash -lc 'python3 ./scripts/server_agent.py --config ./config.yaml --once >> ./logs/server-mate-agent.log 2>&1'
0 1 * * * /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range daily --send >> ./logs/server-mate-report.log 2>&1'
10 1 * * 1 /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range weekly --send >> ./logs/server-mate-report.log 2>&1'
20 1 1 * * /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range monthly --send >> ./logs/server-mate-report.log 2>&1'
```

Systemd note:

- If the host already standardizes on `systemd`, prefer `Type=oneshot` services plus timers for reports.
- Use `Restart=always` only for the long-running `--daemon` agent mode.

## Example requests

- "Design the ingestion API for Server-Mate."
- "Add 404 burst detection and webhook alerts."
- "Explain today's top 5xx error in plain language."
- "Plan a safe auto-heal flow for repeated 502 responses."
