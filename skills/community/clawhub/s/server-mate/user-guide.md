# Server-Mate User Guide

Version: `1.3.1`

## 1. What This Guide Covers

This guide is for operators who want to deploy `Server-Mate` on CentOS, Ubuntu, Debian, or other mainstream Linux servers.

It covers:

- Python and system dependencies
- GeoIP / MaxMind provisioning for province-level reports
- multi-site `config.yaml` setup
- SSH brute-force monitoring and SSL expiry checks
- Daily / weekly / monthly report generation
- Guarded Automation safety rules and audit workflow
- Cron and systemd scheduling
- Nginx or Apache download-link exposure for generated PDF reports

## 2. Prerequisites

### 2.1 Python Packages

Install the base runtime:

```bash
python3 -m pip install psutil
```

Install YAML support if you want native YAML parsing instead of JSON-compatible syntax:

```bash
python3 -m pip install pyyaml
```

Install report-generation packages:

```bash
python3 -m pip install matplotlib
```

Optional but recommended:

- `requests` is not required right now because webhook delivery uses the Python standard library.
- `sqlite3` is built into standard Python on most Linux distributions.
- Install `geoip2` if you want real province distribution in PDF reports:

```bash
python3 -m pip install geoip2 maxminddb aiohttp
```

- Install `geoipupdate` if you want to refresh GeoLite2 databases from MaxMind with your own account:

```bash
# CentOS / Rocky / AlmaLinux
sudo yum install geoipupdate

# Ubuntu / Debian
sudo apt-get update
sudo apt-get install geoipupdate
```

### 2.2 Linux Fonts for Chinese PDF Rendering

If `report_language: zh`, install at least one Chinese font package so matplotlib can render Chinese correctly.

Recommended packages:

- CentOS / Rocky / AlmaLinux:

```bash
sudo yum install google-noto-sans-cjk-ttc-fonts
```

- Ubuntu / Debian:

```bash
sudo apt-get update
sudo apt-get install fonts-noto-cjk
```

After installing fonts, refresh the font cache if needed:

```bash
fc-cache -fv
```

### 2.3 Log Paths

Server-Mate does not hardcode a single BT Panel layout. Always set log paths explicitly in `config.yaml`.

Typical examples:

- Nginx:
  - `/var/log/nginx/site-access.log`
  - `/var/log/nginx/site-error.log`
- Apache:
  - `/var/log/httpd/site-access.log`
  - `/var/log/httpd/site-error.log`
  - `/var/log/apache2/site-access.log`
  - `/var/log/apache2/site-error.log`
- Custom layout:
  - `/path/to/logs/site-a.access.log`
  - `/path/to/logs/site-a.error.log`

### 2.4 GeoIP / MaxMind Setup

Server-Mate 1.3.1 supports two GeoIP provisioning modes:

- Official MaxMind mode
  - Put your MaxMind `GeoIP.conf` at `./data/GeoIP.conf`.
  - Keep it out of Git. This file contains your `AccountID` and `LicenseKey`.
  - If `geoipupdate` is installed, the report generator will try this path first when `geoip_city_db` is missing.
- Public mirror fallback
  - If `geoipupdate` is not installed or `./data/GeoIP.conf` is absent, Server-Mate falls back to the built-in public `.mmdb` mirror download.

Recommended workflow:

1. Register a free MaxMind GeoLite2 account.
   - Sign-up page: [GeoLite sign up](https://www.maxmind.com/en/geolite2/signup)
2. Create a GeoLite2 license key in the MaxMind account portal.
   - License key guide: [Generate a License Key](https://support.maxmind.com/hc/en-us/articles/4407111582235-Generate-a-License-Key)
3. Create `./data/GeoIP.conf` manually.
4. Fill in your real `AccountID` and `LicenseKey`.
5. Keep `notifications.reports.geoip_city_db` pointing at `./data/GeoLite2-City.mmdb`.

Important:

- Do not commit `./data/GeoIP.conf` to GitHub.
- Do not paste real MaxMind credentials into `config.example.yaml`.
- If a key has already been shared in plaintext, rotate it in MaxMind before production use.

## 3. Configuration Overview

Main config file:

- `config.yaml`
- Copy [`config.example.yaml`](config.example.yaml) to `config.yaml` and then adjust paths, webhooks, and automation switches for your environment.

If the file is missing, the agent can generate a default one automatically.

### 3.1 Full Example

```yaml
agent:
  host_id: web-01
  timezone: Asia/Shanghai
  mode: once
  state_file: ./server_agent_state.json

system_metrics:
  enabled: true
  disk_root: /
  collect_network_io: true

logs:
  auth_log: ""

sites:
  - domain: site-a.example.com
    site_host: site-a.example.com
    access_log: /path/to/logs/site-a.access.log
    error_log: /path/to/logs/site-a.error.log
  - domain: api.example.com
    site_host: api.example.com
    access_log: /var/log/nginx/api.example.com.access.log
    error_log: /var/log/nginx/api.example.com.error.log

storage:
  database_file: ./metrics.db
  rollup_minutes: [10, 60]

thresholds:
  ssh_bruteforce_window_minutes: 5
  ssh_bruteforce_failures: 10

notifications:
  webhooks:
    telegram:
      enabled: false
      bot_token: ""
      chat_id: ""
      timeout_seconds: 10
      disable_web_page_preview: true
    dingtalk:
      enabled: true
      url: https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
  reports:
    report_language: zh
    report_export_dir: ./public/reports
    public_base_url: https://ops.example.com/reports
    geoip_city_db: ./data/GeoLite2-City.mmdb
    geoip_update_config: ./data/GeoIP.conf
    ai_analysis:
      enabled: true
      simulate: false
      endpoint: https://api.openai.com/v1
      model: gpt-4o-mini
      api_key_env: OPENAI_API_KEY
      timeout_seconds: 20
    daily:
      enabled: true
      push_time: "08:30"
      output_dir: ./reports
      channels: [dingtalk, telegram]
    weekly:
      enabled: true
      push_weekday: 1
      push_time: "09:00"
      output_dir: ./reports
      channels: [dingtalk]
    monthly:
      enabled: true
      push_day: 1
      push_time: "09:30"
      output_dir: ./reports
      channels: [dingtalk]
automation:
  dry_run: true
  auto_ban:
    enabled: false
    whitelist_ips: [127.0.0.1, "::1", 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16]
    whitelist_spiders: [googlebot, baiduspider, bingbot]
    ban_ttl_seconds: 86400
  auto_heal:
    enabled: false
    services: [php-fpm]
    cooldown_seconds: 3600
```

For a production-ready template, start from [`config.example.yaml`](config.example.yaml).

## 4. Parameter Reference

### 4.1 `agent`

- `host_id`
  - Logical host name shown in alerts and reports.
- `timezone`
  - Local timezone used for bucket closing, scheduling, and reports.
- `mode`
  - `once` or `daemon`.
- `poll_interval_seconds`
  - Agent loop interval in daemon mode.
- `state_file`
  - JSON cursor/state file for incremental log reads.

Legacy note:

- Older single-site keys such as `agent.site`, `agent.site_host`, and top-level `logs.*` are still normalized for compatibility, but new deployments should use `sites[]`.

### 4.2 `system_metrics`

- `enabled`
  - Whether host-global CPU, memory, disk, load, and network metrics are collected.
- `disk_root`
  - Filesystem mount point used by `psutil.disk_usage()`.
- `collect_network_io`
  - Whether to sample host-level RX or TX counters.

### 4.3 `sites`

Each item in `sites` is an independent business target:

- `domain`
  - Primary site identifier used in SQLite rollups, reports, and webhook notifications.
- `site_host`
  - Hostname used for referer/source classification.
- `enabled`
  - Whether this site participates in collection and report generation.
- `access_log`
  - Site-specific access log path.
- `error_log`
  - Site-specific error log path.

Important behavior:

- Server-Mate collects host metrics once per cycle, not once per site.
- Access and error logs are parsed independently for each configured site.
- `report_generator.py` will generate one report per site unless you pass `--site`.

### 4.4 `storage`

- `database_file`
  - SQLite database path.
- `rollup_minutes`
  - Bucket granularities to persist, for example `[10, 60]`.

### 4.5 `thresholds`

Examples:

- `slow_ms`
  - Slow-request threshold in milliseconds.
- `attack_rpm_threshold`
  - Requests per minute threshold for suspicious IP detection.
- `cpu_pct`
  - CPU alert threshold.
- `memory_pct`
  - Memory alert threshold.
- `disk_free_ratio`
  - Disk free space threshold, for example `0.10`.
- `ssh_bruteforce_window_minutes`
  - Rolling window used for SSH brute-force detection.
- `ssh_bruteforce_failures`
  - Failed SSH login threshold per source IP inside the rolling window.

### 4.6 `logs`

- `auth_log`
  - Optional SSH/authentication log path.
  - Leave it empty to auto-detect `/var/log/auth.log` on Ubuntu/Debian or `/var/log/secure` on CentOS/RHEL-family systems.

### 4.7 `notifications.webhooks`

Each channel supports:

- `enabled`
  - Whether the channel is active.
- `url`
  - Incoming webhook URL.
- `timeout_seconds`
  - HTTP timeout.

Additional DingTalk option:

- `at_all`
  - Whether the robot should mention everyone.

Telegram-specific options:

- `bot_token`
  - Telegram bot token. If empty, Server-Mate falls back to `TELEGRAM_BOT_TOKEN`.
- `chat_id`
  - Telegram target chat id. If empty, Server-Mate falls back to `TELEGRAM_CHAT_ID`.
- `disable_web_page_preview`
  - Whether Telegram should hide URL previews in push messages.

### 4.8 `notifications.reports`

Global report options:

- `report_language`
  - `zh` or `en`.
- `report_export_dir`
  - Optional externally exposed directory for copied PDF/Markdown files.
- `public_base_url`
  - Optional URL prefix used to build direct download links.
- `geoip_city_db`
  - Optional GeoIP City database path. When configured with `geoip2`, province-distribution charts use real IP geolocation. If omitted, Server-Mate falls back to `Unknown Region` / `未知地区`.
  - If the configured file is missing, the report generator first tries `geoipupdate` with `geoip_update_config`, then falls back to a public mirror download.
- `geoip_update_config`
  - Optional path to MaxMind `GeoIP.conf`.
  - Recommended value: `./data/GeoIP.conf`.
  - Use this when you want Server-Mate to refresh GeoLite2 databases from your own MaxMind account instead of relying only on the public mirror.
  - Report generation also checks the configured site certificate and surfaces SSL remaining days in PDF headers and webhook summaries.

Per-schedule options:

- `output_dir`
  - Local report directory. This is always used first.
- `report_export_dir`
  - Optional override for the global export directory.
- `public_base_url`
  - Optional override for the global public URL.
- `channels`
  - Webhook channels used for report notifications.

Daily-specific:

- `push_time`
  - Example: `"08:30"`.
- `send_on_startup_if_missed`
  - Whether to backfill a missed report on process startup.

Weekly-specific:

- `push_weekday`
  - `1-7`, usually `1` for Monday.

Monthly-specific:

- `push_day`
  - `1-28`.

### 4.9 `notifications.reports.ai_analysis`

- `enabled`
  - Enables AI health commentary for daily / weekly / monthly PDF reports.
- `simulate`
  - When `true`, the generator uses a built-in fallback summary instead of calling a real LLM API.
- `endpoint`
  - Base OpenAI-compatible API endpoint. Example: `https://api.openai.com/v1`.
- `model`
  - Chat model name, for example `gpt-4o-mini`.
- `api_key_env`
  - Environment variable name that stores the API key. Default: `OPENAI_API_KEY`.
- `timeout_seconds`
  - HTTP timeout for the AI request.

In OpenClaw, `OPENAI_API_KEY` is injected by the runtime automatically. Do not add a manual `export OPENAI_API_KEY=...` step in normal OpenClaw deployments.

### 4.10 `automation`

Global switch:

- `dry_run`
  - Master safety switch for Guarded Automation.
  - When `true`, Server-Mate sends the automation notice and writes SQLite audit records, but never runs the real `iptables` or `systemctl` command.
  - Recommended default for first deployment: keep `dry_run: true` for several days.

`automation.auto_ban`:

- `enabled`
  - Enables auto-ban logic for suspicious IP bursts.
- `channels`
  - Webhook channels used for the automatic intervention notice.
- `whitelist_ips`
  - Absolute allowlist checked before any ban command.
- `whitelist_spiders`
  - Trusted crawler families that should never be auto-banned.
- `ban_ttl_seconds`
  - Ban lifetime before automatic release.
- `max_active_bans`
  - Hard cap to stop unbounded firewall growth.
- `command_template`
  - Shell template for the actual ban action.
- `unban_command_template`
  - Shell template used when TTL expires.

`automation.auto_heal`:

- `enabled`
  - Enables restart-based self-heal attempts.
- `services`
  - Service list that can be restarted.
- `trigger_kinds`
  - Alert kinds that are allowed to trigger self-heal.
- `cooldown_seconds`
  - Restart anti-flap lock. The same service is only allowed once per cooldown window.
- `command_template`
  - Shell template used for the restart command.

## 5. Multi-Site Configuration Guide

Use `sites[]` when one host serves multiple domains or applications.

Recommended pattern:

- Put only host-global settings in `agent`, `system_metrics`, `storage`, and shared webhook blocks.
- Put domain-specific log paths in `sites[]`.
- Keep `domain` stable over time because it becomes part of SQLite rollup keys and report filenames.

Example:

```yaml
sites:
  - domain: app.example.com
    access_log: /path/to/logs/app.access.log
    error_log: /path/to/logs/app.error.log
  - domain: api.example.com
    access_log: /var/log/nginx/api.example.com.access.log
    error_log: /var/log/nginx/api.example.com.error.log
```

Operational notes:

- One `server_agent.py --once` run will loop over every enabled site.
- One scheduled PDF generation run will emit one file per site automatically.
- For manual single-site inspection, use `--site`:

```bash
python3 scripts/report_generator.py --config config.yaml pdf --range daily --site site-a.example.com --json
```

## 6. Guarded Automation Guide

### 6.1 Start in Dry-Run

Strong recommendation:

- Keep `automation.dry_run: true` during initial deployment.
- Watch the webhook notifications and SQLite audit tables for several days.
- Only switch to `false` after you trust the trigger thresholds, whitelist coverage, and operational blast radius.

With `dry_run: true`, Server-Mate will:

- evaluate the same auto-ban and auto-heal conditions
- send a high-priority automation notice to DingTalk, WeCom, or Feishu
- write audit rows into SQLite
- skip the real shell execution

### 6.2 Auto-Ban Rules

Auto-ban is designed for suspicious IP bursts such as CC-style request spikes.

Rules to follow:

- Treat `whitelist_ips` as mandatory, not optional.
- Keep loopback, RFC1918 private ranges, and trusted office VPN ranges in the whitelist.
- Keep trusted crawlers in `whitelist_spiders`.
- Do not disable the TTL release path unless an external controller such as fail2ban is managing expiry for you.
- Review `max_active_bans` before turning on production bans.

### 6.3 Auto-Heal Rules

Auto-heal is intentionally conservative.

Rules to follow:

- Only allow restartable services that your team is comfortable bouncing automatically.
- Keep `trigger_kinds` narrow. Start with `server_error_burst` only.
- Do not reduce `cooldown_seconds` aggressively. The default one-hour lock exists to prevent restart storms.
- If the same service continues failing after one restart window, prefer human intervention and incident escalation.

## 7. Generating Reports Manually

### 7.1 Daily Markdown Snapshot

```bash
python3 scripts/report_generator.py --config config.yaml daily --date 2026-03-26 --json
```

### 7.2 Daily PDF + Webhook Push

```bash
python3 scripts/report_generator.py --config config.yaml pdf --range daily --end-date 2026-03-26 --send
```

### 7.3 Weekly PDF

```bash
python3 scripts/report_generator.py --config config.yaml pdf --range weekly --end-date 2026-03-26 --json
```

### 7.4 Monthly PDF + Webhook Push

```bash
python3 scripts/report_generator.py --config config.yaml pdf --range monthly --end-date 2026-03-31 --send
```

All three PDF modes now reuse the same final SaaS report layout:

- Daily: 24-hour traffic, hot pages / IPs / referers, spiders, status codes, visitor profile
- Weekly: 7-day trend using the same visual style, real SQLite aggregation, and AI commentary
- Monthly: 30-day trend using the same visual style, real SQLite aggregation, and AI commentary

## 8. Automated Scheduling Guide

This is the recommended production pattern:

- Run the collector in `--once` mode every 10 minutes.
- Run report generation as one-shot PDF jobs.
- Let cron or systemd control timing instead of embedding a complex scheduler into the report process.
- For scheduled daily / weekly / monthly pushes, use `pdf --range ... --send` instead of the lightweight `daily --send` markdown mode.

### 8.1 Open crontab

```bash
crontab -e
```

### 8.2 Data Capture Every 10 Minutes

This parses new access and error logs incrementally, refreshes in-memory state, and writes rollups into SQLite.

```cron
*/10 * * * * /usr/bin/env bash -lc 'cd /path/to/server-mate && python3 ./scripts/server_agent.py --config ./config.yaml --once >> ./logs/server-mate-agent.log 2>&1'
```

### 8.3 Daily PDF Report at 01:00

This generates the previous day daily report and pushes it to the configured webhook channels.
In multi-site mode, this single cron entry will loop over every configured site and emit one report per domain.

```cron
0 1 * * * /usr/bin/env bash -lc 'cd /path/to/server-mate && python3 ./scripts/report_generator.py --config ./config.yaml pdf --range daily --send >> ./logs/server-mate-report.log 2>&1'
```

### 8.4 Weekly PDF Report Every Monday at 01:10

```cron
10 1 * * 1 /usr/bin/env bash -lc 'cd /path/to/server-mate && python3 ./scripts/report_generator.py --config ./config.yaml pdf --range weekly --send >> ./logs/server-mate-report.log 2>&1'
```

### 8.5 Monthly PDF Report on the 1st at 01:20

```cron
20 1 1 * * /usr/bin/env bash -lc 'cd /path/to/server-mate && python3 ./scripts/report_generator.py --config ./config.yaml pdf --range monthly --send >> ./logs/server-mate-report.log 2>&1'
```

### 8.6 Manual Markdown Snapshot (Debug Only)

If you need the lightweight Markdown mode for debugging, run it manually instead of wiring it into cron/systemd report tasks:

```bash
cd /path/to/server-mate
python3 ./scripts/report_generator.py --config ./config.yaml daily --date 2026-03-26 --send
```

### 8.7 Recommended Log Files

```bash
cd /path/to/server-mate
mkdir -p ./logs ./reports
touch ./logs/server-mate-agent.log ./logs/server-mate-report.log
```

## 9. Scheduling with systemd

Recommended when you want stronger process control than cron.

### 9.1 Generate a Workspace-Specific Service Unit

Run this from the Server-Mate workspace root:

```bash
python3 ./scripts/server_agent.py --config ./config.yaml --generate-service
```

If you want to save the generated content first:

```bash
python3 ./scripts/server_agent.py --config ./config.yaml --generate-service > ./server-mate.service.txt
```

The generated output already uses the current absolute workspace path for:

- `WorkingDirectory`
- `ExecStart`
- `config.yaml`

### 9.2 Install the Generated Unit

1. Run `--generate-service`.
2. Copy the printed content into `/etc/systemd/system/server-mate.service`.
3. Reload and enable the service.

One-line install example:

```bash
python3 ./scripts/server_agent.py --config ./config.yaml --generate-service | sudo tee /etc/systemd/system/server-mate.service >/dev/null
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now server-mate.service
sudo systemctl status server-mate.service
```

### 9.3 Manual Template

If you prefer to paste a template manually, replace `<SERVER_MATE_DIR>` with your workspace path and `<PYTHON_BIN>` with the Python interpreter you want systemd to use.

`/etc/systemd/system/server-mate.service`

```ini
[Unit]
Description=Server-Mate Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=<SERVER_MATE_DIR>
Environment=PYTHONUNBUFFERED=1
ExecStart=<PYTHON_BIN> <SERVER_MATE_DIR>/scripts/server_agent.py --config <SERVER_MATE_DIR>/config.yaml --daemon
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Example placeholders:

- `<SERVER_MATE_DIR>` -> `/home/opc/server-mate`
- `<PYTHON_BIN>` -> `/usr/bin/python3`

### 9.4 Optional Report Timer Example

You can still keep report generation as one-shot timers while the agent itself runs as a daemon.

`/etc/systemd/system/server-mate-weekly-report.service`

```ini
[Unit]
Description=Server-Mate Weekly PDF Report

[Service]
Type=oneshot
WorkingDirectory=<SERVER_MATE_DIR>
ExecStart=<PYTHON_BIN> <SERVER_MATE_DIR>/scripts/report_generator.py --config <SERVER_MATE_DIR>/config.yaml pdf --range weekly --send
```

`/etc/systemd/system/server-mate-weekly-report.timer`

```ini
[Unit]
Description=Run Server-Mate Weekly PDF Report

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now server-mate-weekly-report.timer
```

### 9.5 When to Use Cron vs systemd

- Use `cron` when you want the fastest deployment with simple one-line schedules.
- Use `systemd` when you want a resident collector with restart policy and `journalctl` visibility.
- Use `systemd timers` when you want native service management for scheduled reports.
- For most production installs, `--once` plus cron is still the easiest model to audit and recover.

## 10. Exposing PDF Reports via Nginx

Assume:

- `report_export_dir = /srv/reports/server-mate`
- `public_base_url = https://ops.example.com/reports`

Example Nginx config:

```nginx
server {
    listen 80;
    server_name ops.example.com;

    location /reports/ {
        alias /srv/reports/server-mate/;
        autoindex off;
        add_header Cache-Control "no-cache";
    }
}
```

After reloading Nginx, a generated file such as:

- `/srv/reports/server-mate/server-mate-example-com-weekly-20260326091015-zh.pdf`

becomes:

- `https://ops.example.com/reports/server-mate-example-com-weekly-20260326091015-zh.pdf`

Default naming pattern:

- `server-mate-{site}-{daily|weekly|monthly}-{YYYYMMDDHHMMSS}-{zh|en}.pdf`

## 11. Exposing PDF Reports via Apache

```apache
Alias /reports/ "/srv/reports/server-mate/"

<Directory "/srv/reports/server-mate/">
    Require all granted
    Options -Indexes
</Directory>
```

Reload Apache after changes:

```bash
sudo systemctl reload httpd
```

or:

```bash
sudo systemctl reload apache2
```

## 12. Audit and Troubleshooting

### 12.1 Runtime Logs

Typical places to look first:

- `./logs/server-mate-agent.log`
- `./logs/server-mate-report.log`
- `journalctl -u server-mate.service -f` when the collector is managed by systemd

These are especially useful when:

- a webhook endpoint is temporarily unreachable
- a log file was rotated and you want to confirm the collector recovered
- Guarded Automation sent a dry-run or failed-action notice

### 12.2 SQLite Audit Tables

Guarded Automation history is persisted in:

- `automation_actions`
  - Every dry-run, successful action, skipped cooldown action, unban, and failure.
- `banned_ips`
  - Ban lifetime tracking, expiry, and unban result.

Useful queries:

```bash
cd /path/to/server-mate
sqlite3 ./metrics.db "SELECT created_at, site, action_type, target, status, dry_run, reason FROM automation_actions ORDER BY id DESC LIMIT 20;"
sqlite3 ./metrics.db "SELECT site, ip_address, created_at, expires_at, lifted_at, lift_status FROM banned_ips ORDER BY id DESC LIMIT 20;"
```

### 12.3 Checklist

- If Chinese text shows as squares in PDFs:
  - install `fonts-noto-cjk` or an equivalent CJK font package
  - run `fc-cache -fv`
- If the webhook message contains only a local path:
  - set `report_export_dir`
  - set `public_base_url`
  - expose the export directory via Nginx or Apache
- If no report data appears:
  - verify `database_file`
  - confirm the agent is writing rollups
  - check `site` and `host_id` match the stored data
- If one site is missing from reports:
  - verify the site still exists in `sites[]`
  - confirm that the site's `enabled` flag is `true`
  - check both `access_log` and `error_log` paths for that domain
- If slow routes or abnormal IP sections are empty:
  - make sure the latest agent version has created `slow_request_rollups` and `suspicious_ip_rollups`
- If auto-ban or auto-heal did not run:
  - confirm `automation.dry_run` and `automation.auto_ban.enabled` or `automation.auto_heal.enabled`
  - query `automation_actions` to see whether the action was skipped by whitelist or cooldown
  - verify webhook notifications for `⚠️ 自动化干预通知`

## 13. Next Suggested Steps

- Enable AI diagnosis for complex `error_event` alerts
- Add GeoIP enrichment for country / region reports
- Add signed or expiring report download URLs if the report host is public
