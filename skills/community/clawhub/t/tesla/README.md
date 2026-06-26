# 🚗 Tesla Skill for OpenClaw

Control your Tesla vehicles - lock/unlock, climate, charging, location, and more. Supports multiple cars on one account.

## What it does

- **Vehicle status** - battery level, charge state, odometer, software version
- **Lock/unlock** - secure your car remotely
- **Climate control** - turn AC on/off, set temperature
- **Charging** - start/stop charging, check charge status
- **Location** - find where your car is parked
- **Fun stuff** - honk the horn, flash the lights
- **Multi-vehicle** - target specific cars by name

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-tesla.git ~/.openclaw/skills/tesla
```

### Authenticate (one-time)

```bash
export TESLA_EMAIL="you@email.com"
python3 scripts/tesla.py auth
```

This opens a Tesla login URL. Sign in, authorize, paste the callback URL back. Token caches for ~30 days and auto-refreshes.

### Example chat usage

- "Is my Tesla locked?"
- "Lock Stella"
- "What's Snowflake's battery level?"
- "Where's my Model X?"
- "Turn on the AC in Stella"
- "Honk the horn on Snowflake"

## Commands

```bash
python3 scripts/tesla.py list              # List all vehicles
python3 scripts/tesla.py status            # Vehicle status
python3 scripts/tesla.py lock              # Lock
python3 scripts/tesla.py unlock            # Unlock
python3 scripts/tesla.py climate on        # AC on
python3 scripts/tesla.py climate temp 72   # Set temp
python3 scripts/tesla.py charge status     # Charge info
python3 scripts/tesla.py location          # GPS location
python3 scripts/tesla.py honk              # Honk horn
python3 scripts/tesla.py flash             # Flash lights
python3 scripts/tesla.py --car "Stella" status  # Target specific car
```

## How it works

Uses the unofficial [Tesla Owner API](https://tesla-api.timdorr.com). Credentials stored locally only. Refresh token cached in `~/.tesla_cache.json`. No data sent to third parties.

## License

MIT
