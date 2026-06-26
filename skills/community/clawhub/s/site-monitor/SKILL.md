---
name: website-monitor
description: Monitor websites for changes, downtime, or specific content. Get notified when a page changes, goes down, or matches/stops matching a pattern. Lightweight — no database needed.
author: zacjiang
version: 1.0.0
tags: monitor, website, uptime, change detection, alert, scraping, automation
---

# Website Monitor

Lightweight website monitoring — detect changes, downtime, or content patterns without external services.

## Usage

### Check if a site is up
```bash
python3 {baseDir}/scripts/monitor.py check https://example.com
```

### Monitor for changes (compare to last snapshot)
```bash
python3 {baseDir}/scripts/monitor.py watch https://example.com --state-dir /tmp/monitor-state
```
Returns exit code 0 if unchanged, 1 if changed (with diff), 2 if down.

### Check for specific content
```bash
python3 {baseDir}/scripts/monitor.py match https://example.com/pricing --pattern "Enterprise plan"
```
Returns exit code 0 if pattern found, 1 if not found.

### Batch monitor from file
```bash
# sites.txt: one URL per line
python3 {baseDir}/scripts/monitor.py batch sites.txt --state-dir /tmp/monitor-state
```

## Integration with OpenClaw

### Heartbeat check
Add to your HEARTBEAT.md:
```
Run website monitor batch check on sites.txt.
If any site is down or changed, notify me.
```

### Cron job
```bash
# Check every 30 minutes
openclaw cron add --every 30m --task "Run website monitor on my sites list and alert me if anything changed"
```

## Features

- 🔍 Change detection with text diff
- ⬆️ Uptime checking (HTTP status + response time)
- 🎯 Pattern matching (regex supported)
- 📁 File-based state (no database needed)
- 📋 Batch monitoring from URL list
- 🪶 Zero dependencies beyond Python stdlib + requests

## Dependencies

```bash
pip3 install requests
```

## How State Works

When using `watch` mode, the script saves a hash of each page's text content in `--state-dir`. On the next run, it compares the current hash to the saved one. If different, it reports the change and shows a text diff.

State files are named by URL hash, so you can monitor hundreds of sites without collision.
