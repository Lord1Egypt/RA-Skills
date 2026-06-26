# Setup - Shelly BluTRV

Read this on first use or whenever the skill is moved to a new Shelly environment.
Keep setup short, practical, and focused on safe control.

## Operating Priorities

- Prefer local RPC for BluTRV status and control.
- Use cloud access for supported WiFi devices and controlled fallback scenarios.
- Default to inspection first, then write only with explicit user intent.
- Keep room mappings, gateway IPs, and cloud identifiers outside the scripts.

## First Activation Flow

1. Confirm control scope:
- Which rooms or devices should this skill operate on?
- Should it only answer questions, or may it also change target temperatures?
- Are there heating-related actions that always require confirmation?

2. Confirm environment model:
- Which Shelly gateway serves which room?
- Is Shelly Cloud available and intended as fallback only or normal operating mode?
- Are WebSocket helpers needed only for debugging, or part of the workflow?

3. Configure environment variables:

```env
SHELLY_DEFAULT_GATEWAY_IP=192.168.0.102

# Format: gateway_key|gateway_ip|gateway_device_id ; ...
SHELLY_GATEWAYS="bedroom-gateway|192.168.0.101|deadc0debeef;main-gateway|192.168.0.102|cafebabec0de"

# Format: alias1,alias2|gateway_key|trv_id|trv_device_id ; ...
# Important: trv_id alone is not globally unique. The safe identity is gateway_key + trv_id + trv_device_id.
SHELLY_TARGETS="schlafzimmer,bedroom,sz|bedroom-gateway|200|cafebabefeed;wohnzimmer,living-room,wz|main-gateway|200|bad0ff1ce123;flur,hallway|main-gateway|202|f00dbabecafe"

SHELLY_CLOUD_SERVER_URI=https://example.shelly.cloud
SHELLY_CLOUD_TOKEN=your_token_here
```

Recommended location:

- `~/.openclaw/skills/.shelly-blutrv-manager.env`

The skill reads only the dedicated `.shelly-blutrv-manager.env` file.
This path is also declared in `SKILL.md` metadata so scanners and installers can see where local config is expected.
Store only Shelly-related variables in that file and restrict permissions:

```bash
chmod 600 ~/.openclaw/skills/.shelly-blutrv-manager.env
```

4. Validate the setup with one read operation before any write:

```bash
scripts/blutrv-status.sh schlafzimmer
```

5. After a write, always verify final state:

```bash
scripts/blutrv-control.sh schlafzimmer 20
scripts/blutrv-status.sh schlafzimmer
```

## Registry Model

- `SHELLY_GATEWAYS` describes reachable Shelly gateways.
- `SHELLY_TARGETS` describes user-facing target names and aliases.
- A target alias resolves to exactly one `gateway_key + trv_id + trv_device_id`.
- This avoids ambiguity when multiple devices are both named `BluTrv (200)` on different gateways.

Example:

- Schlafzimmer radiator: `schlafzimmer|bedroom-gateway|200|cafebabefeed`
- Wohnzimmer radiator: `wohnzimmer|main-gateway|200|bad0ff1ce123`

Both can use `trv_id=200`, but they still remain unambiguous because the gateway and device id differ.

## What to Keep Out of the Repo

- real gateway IPs
- real device IDs
- cloud tokens
- live WebSocket URLs with embedded tokens
- user-specific room mappings if they reveal private context

## Guardrails

- Never assume a target temperature change succeeded without a follow-up read.
- Never treat cloud state as fresher than local state when the gateway is reachable.
- Never store production credentials in skill files.
- Never enable WebSocket write helpers against real devices without explicit intent and `--allow-write`.
