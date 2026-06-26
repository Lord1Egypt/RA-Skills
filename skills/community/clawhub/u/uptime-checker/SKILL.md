---
name: uptime-checker
description: Lightweight URL uptime checker and response time monitor. Check if websites and APIs are up, measure response times, track history, and detect SSL issues. Use when checking if a site is down, monitoring API endpoints, measuring response times, checking SSL certificates, or building uptime reports. Triggers on "is this site up", "check uptime", "website down", "response time", "monitor URL", "endpoint health check", "site status".
---

# Uptime Checker

Zero-dependency URL uptime checker with response time monitoring, history tracking, and multi-URL support.

## Quick Start

```bash
# Check a single URL
python3 scripts/uptime_check.py https://example.com

# Check multiple URLs
python3 scripts/uptime_check.py https://api.example.com https://example.com https://status.example.com

# JSON output for scripting
python3 scripts/uptime_check.py https://example.com --format json

# Check with custom expected status
python3 scripts/uptime_check.py https://example.com/old-page --expected-status 301

# Load URLs from file
python3 scripts/uptime_check.py --urls-file urls.txt

# Save results and view history
python3 scripts/uptime_check.py https://example.com --save --history-file checks.json
python3 scripts/uptime_check.py --history --history-file checks.json

# Skip SSL verification (self-signed certs)
python3 scripts/uptime_check.py https://internal.example.com --no-verify-ssl

# Custom timeout and method
python3 scripts/uptime_check.py https://example.com --timeout 5 --method HEAD

# Add custom headers (auth, etc.)
python3 scripts/uptime_check.py https://api.example.com --header "Authorization:Bearer token123"
```

## Features

- Check single or multiple URLs in one command
- Response time measurement in milliseconds
- SSL certificate validation
- Redirect detection and following
- History tracking with uptime percentage summaries
- Configurable expected HTTP status codes
- Custom headers, methods, and timeouts
- JSON and text output formats
- Exit code 1 if any endpoint is down (for scripting/cron)
- No external dependencies — pure Python stdlib
