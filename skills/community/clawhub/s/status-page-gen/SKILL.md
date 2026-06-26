---
name: status-page-gen
description: Generate a lightweight static HTML status page for self-hosted services. Checks health endpoints, ping, SSL certificates, and uptime history. Outputs a self-contained dark-theme HTML file (Upptime/Cachet-style) that can be served locally or pushed to a GitHub Gist. Triggers on: status page, service status, uptime, are my services up, health check, service monitor, generate status page, check my services.
---

# status-page-gen

Generate a static HTML status page for all your self-hosted services.

## Skill Location

`~/.openclaw/workspace/skills/status-page-gen/`

## Quick Start

### 1. Configure services

Copy the example config and edit it:

```bash
cp ~/.openclaw/workspace/skills/status-page-gen/assets/services.example.json \
   ~/.openclaw/workspace/skills/status-page-gen/assets/services.json
```

Edit `services.json` with your actual service names, URLs, and health endpoints.

### 2. Run a full check and generate the page

```bash
cd ~/.openclaw/workspace/skills/status-page-gen

python3 scripts/check_services.py --config assets/services.json --output /tmp/status_check.json
python3 scripts/check_certs.py --config assets/services.json --output /tmp/cert_check.json
python3 scripts/history.py --append /tmp/status_check.json --db assets/history.json
python3 scripts/generate_page.py \
  --services /tmp/status_check.json \
  --certs /tmp/cert_check.json \
  --history assets/history.json \
  --output ~/status.html
```

Open `~/status.html` in a browser.

### 3. Schedule updates (cron)

Add to crontab (`crontab -e`):

```
*/5 * * * * cd ~/.openclaw/workspace/skills/status-page-gen && \
  python3 scripts/check_services.py --config assets/services.json --output /tmp/status_check.json && \
  python3 scripts/check_certs.py --config assets/services.json --output /tmp/cert_check.json && \
  python3 scripts/history.py --append /tmp/status_check.json --db assets/history.json && \
  python3 scripts/generate_page.py --services /tmp/status_check.json --certs /tmp/cert_check.json --history assets/history.json --output ~/status.html
```

## Scripts

| Script | Purpose |
|---|---|
| `check_services.py` | HTTP health checks + ping + response time |
| `check_certs.py` | SSL certificate expiry validation |
| `history.py` | Append results to log, compute uptime % |
| `generate_page.py` | Render self-contained HTML status page |

## Config Format (`services.json`)

See `assets/services.example.json` for a full example. Each service entry:

```json
{
  "name": "Grafana",
  "url": "https://grafana.example.com",
  "health_endpoint": "/api/health",
  "expected_status": 200,
  "ping_host": "grafana.example.com",
  "tags": ["monitoring"]
}
```

- `health_endpoint` — path appended to `url` for health check (default: `/`)
- `expected_status` — HTTP status code to consider "up" (default: `200`)
- `ping_host` — hostname for ICMP ping (optional, derived from `url` if omitted)

## References

See `references/setup-guide.md` for detailed configuration, GitHub Gist publishing, and advanced scheduling.
