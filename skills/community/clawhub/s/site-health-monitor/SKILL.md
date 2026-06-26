---
name: site-health-monitor
description: Monitor websites for uptime, SSL certificate expiry, response time, HTTP errors, and content changes. Generate health reports and send alerts when issues are detected. Use when asked to monitor a website, check site health, track uptime, verify SSL certificates, detect downtime, set up website monitoring, check if a site is up, or audit website performance. Triggers on "monitor site", "check uptime", "SSL expiry", "is my site up", "website health", "site status", "monitor URL", "check website".
---

# Site Health Monitor

Monitor one or more websites for health issues. Detect downtime, expiring SSL certs, slow responses, and content changes — then report or alert.

## Quick Check (Single URL)

When user asks to check a single URL right now:

1. Run `scripts/check_site.sh <url>`
2. Parse the JSON output
3. Present a formatted health report

## Monitored Sites Config

For ongoing monitoring, maintain a config at user's chosen location (default: `~/.openclaw/workspace/site-monitor.json`):

```json
{
  "sites": [
    {
      "url": "https://example.com",
      "name": "Main Site",
      "checks": ["uptime", "ssl", "response_time", "content"],
      "alert_threshold_ms": 3000,
      "ssl_warn_days": 14,
      "content_selector": "title"
    }
  ],
  "defaults": {
    "checks": ["uptime", "ssl", "response_time"],
    "alert_threshold_ms": 5000,
    "ssl_warn_days": 30
  }
}
```

## Health Checks

### 1. Uptime
- HTTP GET to URL
- **Pass:** 2xx/3xx status
- **Warning:** 4xx status
- **Fail:** 5xx, connection refused, timeout (>10s)

### 2. SSL Certificate
- Run `scripts/check_ssl.sh <domain>`
- **Pass:** Valid, >30 days to expiry
- **Warning:** <30 days to expiry (configurable)
- **Fail:** Expired, self-signed, or missing

### 3. Response Time
- Measure TTFB + transfer via `scripts/check_site.sh`
- **Pass:** Under threshold (default 5000ms)
- **Warning:** 1-2x threshold
- **Fail:** >2x threshold or timeout

### 4. Content Changes (Planned)
- Fetch page, extract text, hash it
- Compare against stored hash
- Report if content changed since last check
- *Note: This feature is planned for v1.1*

## Reports

### Single Site
```
## 🟢 example.com — Healthy
| Check         | Status | Detail                    |
|---------------|--------|---------------------------|
| Uptime        | ✅ UP  | 200 OK (143ms)            |
| SSL           | ✅ OK  | Expires in 87 days        |
| Response Time | ✅ OK  | 342ms (threshold: 5000ms) |
| Content       | — Same | No changes detected       |
```

### Multi-Site Summary
```
## Site Health — 2026-03-26
| Site       | Status | Issues         |
|------------|--------|----------------|
| example.com| 🟢 OK | —              |
| api.foo.io | 🟡 WARN| SSL: 12 days  |
| shop.bar   | 🔴 DOWN| 503 error     |
```

### Alerts
Alert when: site DOWN, SSL within warning window, response >2x threshold, 2+ consecutive failures.

Format: `⚠️ [site] — [issue]. [detail]. Checked at [time].`

## Scheduled Monitoring

Suggest cron job for recurring checks (30-60 min interval for production). Store last 100 results per site in `~/.openclaw/workspace/.site-monitor-history.json`.

## Scripts

- `scripts/check_site.sh <url>` — HTTP health check, outputs JSON (status, timing, headers)
- `scripts/check_ssl.sh <domain>` — SSL cert check, outputs JSON (issuer, expiry, days remaining)
