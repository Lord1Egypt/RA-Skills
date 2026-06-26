---
name: uptimecheck
description: Check if URLs and API endpoints are up or down with response times and status codes. Use when asked to monitor uptime, check if a website is down, measure HTTP response times, track endpoint health over time, or verify that services are responding. Supports batch checking from files, history tracking with JSONL storage, and configurable timeouts. Zero dependencies — pure Python stdlib.
---

# uptimecheck ✅

Lightweight URL uptime monitor with response time measurement and history tracking.

## Commands

### Check endpoints
```bash
# Check one or more URLs
python3 scripts/uptimecheck.py check https://github.com https://api.example.com

# Check from a file (one URL per line, # comments supported)
python3 scripts/uptimecheck.py check -f urls.txt

# Save results to history for trend analysis
python3 scripts/uptimecheck.py check https://myapi.com --save

# Custom timeout (default 10s)
python3 scripts/uptimecheck.py check https://slow-api.com -t 30
```

### View history
```bash
# Recent checks
python3 scripts/uptimecheck.py history

# Filter by URL
python3 scripts/uptimecheck.py history --url github.com

# Last N entries
python3 scripts/uptimecheck.py history -n 100
```

## Output
- ✅ for 2xx-4xx responses (client errors count as "up")
- ❌ for 5xx, timeouts, DNS failures, connection refused
- Response time in milliseconds
- Summary with count of down endpoints

## History Storage
Results saved to `~/.uptimecheck/checks.jsonl` — one JSON object per line with url, status, ms, ok, timestamp.

## Exit Codes
- 0: All endpoints responding
- 1: One or more endpoints down (useful for CI/cron alerting)
