---
name: rivian-ls
description: Access Rivian vehicle telemetry (battery, range, charge state, locks, doors, tires, cabin temp, location) using the rivian-ls CLI tool. Use when the user asks about their Rivian's battery level, range, charging status, whether it's locked, door/frunk/liftgate state, tire pressures, odometer, or wants a vehicle status summary. Also use when building dashboards or automations that consume Rivian data. Requires rivian-ls installed and authenticated.
---

# rivian-ls

Fetch and work with Rivian vehicle telemetry via the [rivian-ls](https://github.com/pfrederiksen/rivian-ls) CLI.

> ⚠️ Uses an unofficial Rivian API. May break without notice. Not affiliated with Rivian.

## Installation

```bash
# From source (requires Go 1.21+)
git clone https://github.com/pfrederiksen/rivian-ls.git
cd rivian-ls && make build
cp rivian-ls /usr/local/bin/

# Or via Homebrew
brew install pfrederiksen/tap/rivian-ls
```

## Authentication (Two-Phase MFA)

Rivian requires MFA. Use the two-phase flow for non-interactive / scripted login:

```bash
# Phase 1: Send credentials, triggers SMS code
rivian-ls login --email user@example.com --password secret

# Phase 2: Complete with OTP after receiving SMS (within ~60 seconds)
rivian-ls login --otp 123456
```

Credentials cache to `~/.config/rivian-ls/credentials.json` and auto-refresh. After initial auth, subsequent runs use the cache automatically.

**Non-interactive (single command, if OTP is known in advance):**
```bash
rivian-ls --email user@example.com --password secret --otp 123456 login
```

**Via environment variables:**
```bash
export RIVIAN_EMAIL="user@example.com"
export RIVIAN_PASSWORD="secret"
rivian-ls login  # then provide OTP when prompted
```

## Key Commands

```bash
# Snapshot from cache (fast, no API call)
rivian-ls status --offline --format json

# Live fetch from Rivian API
rivian-ls status --format json

# Stream live updates (WebSocket, auto-falls back to polling)
rivian-ls watch --format json

# Export historical snapshots
rivian-ls export --format json --since 24h

# Multi-vehicle: select by index
rivian-ls status --vehicle 1 --format json
```

## Bundled Script

Use `scripts/rivian_status.py` for clean text or JSON output:

```bash
# Human-readable summary
python3 scripts/rivian_status.py

# JSON (pipe to jq, dashboard APIs, etc.)
python3 scripts/rivian_status.py --format json

# Force live fetch
python3 scripts/rivian_status.py --live
```

## Common Patterns

**Status summary:** Run `python3 scripts/rivian_status.py` — covers all key fields.

**Check if locked:** Parse `IsLocked` from JSON output. Alert if `false` and parked overnight.

**Battery alert:** Check `BatteryLevel` and `RangeStatus`. Alert if below threshold.

**Dashboard API endpoint:** Call `rivian-ls status --offline --format json` from a server-side handler. Use a cron job (`0 * * * *`) to keep the cache fresh.

**Keep cache fresh (cron):**
```bash
0 * * * * /usr/local/bin/rivian-ls status --format json > /dev/null 2>&1
```

## Field Reference

See `references/api-fields.md` for the full JSON schema, all field descriptions, and known limitations.
