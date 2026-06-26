---
name: smartthings-direct
description: Direct SmartThings hub control via the official SmartThings CLI. List devices, read device status, and execute capability commands without going through Home Assistant. Use when the user asks to control a SmartThings device, check device state, run a scene, or when "smartthings" / "ST" is mentioned.
homepage: https://github.com/SmartThingsCommunity/smartthings-cli
metadata:
  clawdbot:
    emoji: "🏠"
    requires:
      bins: ["smartthings"]
---

# SmartThings Direct

Direct control of a SmartThings hub using the official [`@smartthings/cli`](https://github.com/SmartThingsCommunity/smartthings-cli). This is the low-level path — bypasses Home Assistant and Matter bridging. Use this when you want to hit SmartThings devices directly.

For the Home Assistant / Matter setup, see the sibling `smart-home` skill instead.

## Install

```bash
# macOS (recommended)
brew install smartthingscommunity/smartthings/smartthings

# or npm (Node 24.8+)
npm install --global @smartthings/cli
```

Binary: `smartthings` (alias `st`).

Verify: `smartthings --version`.

## Auth

Two options. **Browser login is preferred** for long-lived use because the CLI stores a refresh token.

### Browser (preferred)

Run any command — the CLI opens a browser for Samsung account OAuth on first use.

```bash
smartthings locations      # first call triggers login
```

### Personal Access Token (PAT)

1. Create a PAT at https://account.smartthings.com/tokens
2. Required scopes: `r:devices:*`, `w:devices:*`, `x:devices:*`, `r:locations:*`, `r:scenes:*`, `x:scenes:*`
3. Either pass per command:
   ```bash
   smartthings devices --token <uuid>
   ```
   or add to the config file:
   - macOS: `~/Library/Preferences/@smartthings/cli/config.yaml`
   - Linux: `~/.config/@smartthings/cli/config.yaml`
   ```yaml
   default:
     token: your-pat-uuid-here
   ```

**Heads up:** PATs created after 2024-12-30 expire in **24 hours**. For durable agent use, prefer browser auth or expect to reissue the token.

Confirm config path any time with `smartthings config`.

## Core commands

### Devices

```bash
smartthings devices                              # list all devices
smartthings devices --json                       # JSON output
smartthings devices <id>                         # device detail + capabilities
smartthings devices:status <id>                  # current attribute values
smartthings devices:health <id>                  # online/offline
smartthings devices:capability-status <id> <component> <capability>
```

### Execute commands

Format: `[component:]<capability>:<command>[(args)]` — `component` defaults to `main`.

```bash
# Switch on/off
smartthings devices:commands <id> switch:switch:on
smartthings devices:commands <id> switch:switch:off

# Dimmer to 50 %
smartthings devices:commands <id> main:switchLevel:setLevel\(50\)

# Thermostat cool setpoint to 24 °C
smartthings devices:commands <id> main:thermostatCoolingSetpoint:setCoolingSetpoint\(24\)

# Color temperature
smartthings devices:commands <id> main:colorTemperature:setColorTemperature\(3000\)
```

Parentheses need escaping in bash/zsh. Running `devices:commands` with no args starts an interactive guided prompt — handy for discovering the right capability call.

### Locations, rooms, scenes, capabilities

```bash
smartthings locations
smartthings rooms --location-id <loc-id>
smartthings scenes
smartthings scenes:execute <scene-id>
smartthings capabilities                         # catalog of standard capabilities
```

### Output flags

| Flag | Effect |
|------|--------|
| `-j`, `--json` | JSON to stdout |
| `-y`, `--yaml` | YAML |
| `-o <file>` | write to file (extension sets format) |

No built-in field picker — pipe JSON through `jq`.

## Typical agent workflow

When the user says something like "turn off the living room light":

1. Resolve name → device id:
   ```bash
   scripts/st-find.sh "living room"
   ```
   or directly:
   ```bash
   smartthings devices --json | jq '.[] | select(.label | test("living room"; "i")) | {deviceId, label}'
   ```
2. Check current status before acting (optional but safer):
   ```bash
   smartthings devices:status <id>
   ```
3. Send the command:
   ```bash
   smartthings devices:commands <id> switch:switch:off
   ```
4. Confirm result by re-reading status if the action is consequential (HVAC setpoint, scene execute).

## Rate limits

- Device commands: **12/min per device**, max 10 commands per request
- Locations: 100/min read, 20/hr write
- Rooms: 50/hr all ops
- Scenes: 50/min execute, 50/min list
- `HTTP 429` = rate limited, `HTTP 422` = guardrail violation

Back off rather than retrying tight.

## Notes

- Flags come **after** the subcommand: `smartthings devices -j`, not `smartthings -j devices`.
- `SMARTTHINGS_PROFILE` env var switches config profiles; there is no `SMARTTHINGS_TOKEN` env var.
- This skill is intentionally thin. Prefer invoking the CLI directly over adding wrapper scripts.
