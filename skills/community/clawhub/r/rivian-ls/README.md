# rivian-ls — OpenClaw Skill

An [OpenClaw](https://openclaw.ai) agent skill for accessing Rivian vehicle telemetry using the [`rivian-ls`](https://github.com/pfrederiksen/rivian-ls) CLI.

Get battery level, range, charge state, lock status, door/frunk state, tire pressures, cabin temp, and location — from your terminal, your dashboard, or any automation.

> ⚠️ Uses an unofficial Rivian API. Not affiliated with Rivian Automotive.

## What It Does

- **Status summaries** — battery %, range, charge state, odometer, ready score
- **Security checks** — lock state, door/frunk/liftgate status
- **Telemetry** — cabin temp, tire pressures, GPS location
- **Dashboard integration** — JSON API endpoint pattern for live panels
- **Automation** — cron-friendly cache refresh, alert triggers

## Installation

### Install the skill via ClawHub

```bash
clawhub install rivian-ls
```

### Install the `rivian-ls` CLI (required)

```bash
# From source (Go 1.21+)
git clone https://github.com/pfrederiksen/rivian-ls.git
cd rivian-ls && make build && cp rivian-ls /usr/local/bin/

# Or Homebrew
brew install pfrederiksen/tap/rivian-ls
```

### Authenticate (two-phase MFA)

Rivian requires MFA. Use the two-phase flow:

```bash
# Phase 1: Send credentials, triggers SMS code
rivian-ls login --email user@example.com --password secret

# Phase 2: Complete with OTP after receiving SMS (within ~60 seconds)
rivian-ls login --otp 123456
```

Credentials are cached automatically at `~/.config/rivian-ls/credentials.json` and auto-refresh. Subsequent runs use the cache — no re-auth needed unless tokens expire.

## Usage

Once the skill is installed and `rivian-ls` is authenticated, just ask OpenClaw:

- *"What's my Rivian's battery at?"*
- *"Is my truck locked?"*
- *"Show me the Rivian status"*
- *"Are any doors open on the Rivian?"*
- *"What are my tire pressures?"*

## Bundled Script

```bash
# Human-readable summary
python3 scripts/rivian_status.py

# JSON output (for piping, dashboards, etc.)
python3 scripts/rivian_status.py --format json

# Force live fetch from Rivian API
python3 scripts/rivian_status.py --live
```

## Dashboard Integration

Add a live Rivian panel to any web dashboard:

```typescript
// Server-side API endpoint
import { execSync } from 'child_process';

export async function GET() {
  const output = execSync('rivian-ls status --format json --offline');
  return json({ data: JSON.parse(output) });
}
```

Keep the cache fresh with a cron job:

```bash
# /etc/cron.d/rivian-refresh
0 * * * * /usr/local/bin/rivian-ls status --format json > /dev/null 2>&1
```

## Field Reference

See [`references/api-fields.md`](references/api-fields.md) for the full JSON schema.

Key fields:

| Field | Description |
|-------|-------------|
| `BatteryLevel` | State of charge (0–100%) |
| `RangeEstimate` | Estimated range in miles |
| `ChargeState` | "charging", "complete", "disconnected" |
| `IsLocked` | True if all doors locked |
| `CabinTemp` | Interior temperature °F |
| `Doors.*` | Per-door open/closed state |
| `TirePressures.*` | Per-tire PSI + status |
| `ReadyScore` | Rivian's vehicle readiness score |
| `Odometer` | Total miles driven |

## Security

- No credentials hardcoded — uses `rivian-ls` secure credential cache
- Script uses `shell=False`, specific exception types, type hints
- 0/61 VirusTotal detections

## License

MIT
