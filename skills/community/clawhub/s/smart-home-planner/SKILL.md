---
name: smart-home-planner
description: >
  Use when users want help with smart home planning, device selection,
  automation design, platform comparison, or configuration for Home Assistant,
  米家/小米, or Apple HomeKit. Triggers on smart home, 智能家居, home
  automation, device recommendation, 自动化场景, and home assistant setup.
---

# Smart Home Planner

## Overview

Guide users through smart-home planning and configuration with safe defaults and clear handoffs between planning, setup, and local automation. Supports Home Assistant, 米家/小米, and Apple HomeKit.

## When to Use

- User wants to plan a new smart home system
- User wants device recommendations for specific rooms
- User wants automation scene design
- User has bought devices and needs configuration help
- User asks about smart home platform comparison

## Safety Rules

- Treat door locks, cameras, and alarm-like scenes as opt-in and require explicit confirmation.
- Prefer manual override and fail-safe defaults when power loss, network loss, or cloud outage would create risk.
- For motion-based automations, use conservative defaults and keep false-trigger handling visible.
- Do not assume a risky automation is acceptable just because it is technically possible.

## Phase 1: Information Collection

### First Trigger — Full Collection

Ask one question at a time. Collect:

**Required (3):**
1. Layout — how many rooms, living rooms, bathrooms
2. Target platform — Home Assistant / 米家 / HomeKit / multiple
3. Budget — total budget range

**Optional (with defaults):**
4. Area → estimate from layout
5. Family members → normal adults (note: elderly, children, pets affect device choice)
6. Existing devices → none
7. Tech level → medium (affects platform recommendation)
8. Priority rooms → all rooms
9. Desired scenes → 5 base scenes (home/away/sleep/wake/security)
10. Special needs → voice control, remote control, energy monitoring

If the user does not provide a required field, ask only for the missing field. If the user declines profile persistence, continue with an ephemeral session and do not write `profile.yaml`. If the user changes layout, budget, or platform later, recalculate the plan from that new baseline instead of patching the old one.

### Save User Profile

After collection, save to `~/.config/smart-home-planner/profile.yaml`:

```yaml
household:
  layout: "..."
  floor: N
  members: [...]
  tech_level: "..."
platform:
  primary: "..."
  secondary: "..."
  server: "..."
api_access:
  home_assistant: { granted: false }
  mijia: { granted: false }
  homekit: { granted: false }
existing_devices: [...]
budget: "..."
priorities: { rooms: [...], scenarios: [...], special: [...] }
```

### Subsequent Triggers — Incremental

1. Read profile from `~/.config/smart-home-planner/profile.yaml`
2. Only ask about changes or new requirements
3. Update profile after each trigger

## Phase 2: Output (Split Delivery)

### First Output — Plan + Scene Effects

Generate and output:

1. **Device list & layout** — organized by room, each device with:
   - Recommended brand + model
   - Installation location
   - Why this device (reasoning)
   - Estimated price

2. **Automation scene effects** — plain language descriptions, NO technical details:
   - Scene name
   - What happens (user experience narrative)
   - Trigger condition (in user terms)
   - Devices involved

Present to user and ask: "Does this plan look good? Any adjustments?"

**Output contract:** use a stable device table, scene table, and purchase-guide table. Prices should be in CNY and clearly marked as estimated when they are not exact. Compatibility warnings should only flag protocol, hub, wiring, platform, or safety issues that materially affect deployment.

### Second Output — Purchase Guide

After user confirms:

1. **Priority ranking** — which devices to buy first
2. **Phased purchasing** — split into stages by budget and priority
3. **Compatibility warnings** — ⚠️ flag any cross-platform issues
4. **Purchase channels** — JD/Tmall/official store recommendations

## Phase 3: Configuration (User-Triggered)

Triggered when user says they've bought devices and want to configure.

### Step 1: Detect API Access

Check user profile `api_access` field for each platform.

```
If granted AND token valid → direct config mode
If granted BUT token expired → guide token refresh
If not granted → ask if user wants to grant access
```

If API access fails, is rate-limited, or a device cannot be found, stop and explain the failure path instead of guessing. If generated YAML does not validate, fix the config or hand back a manual guide.

### Step 2: If User Grants Access — Guide API Setup

**Home Assistant:**
- Guide to Settings → Long-Lived Access Tokens
- Save URL and token to profile
- Test connection with a simple API call

**米家 — Use mijia-api:**
- Guide install: `pip install mijiaAPI`
- Run `api.login()` → QR code appears
- User scans with Mi Home app
- Token auto-saves to `~/.config/mijia-api/auth.json`
- Update profile `api_access.mijia.granted: true`
- See `knowledge/mijia-api-guide.md` for detailed guide

**Apple HomeKit — Use homebridge-mcp-server:**
- Check if Homebridge is installed and running
- If not: guide install (Docker recommended, or npm)
- Install MCP server: `npm install -g @mp-consulting/homebridge-mcp-server`
- Configure MCP connection (URL, username, password)
- Devices already paired to Homebridge are automatically available
- Update profile `api_access.homekit.granted: true`
- See `knowledge/homekit-guide.md` for detailed guide
- **No re-pairing needed** — works with devices already in Homebridge

### Step 3: Execute Configuration

**If API available:**
- Discover existing devices (sync to profile)
- Create automation scenes per the plan
- Ask user to verify and adjust

**If API not available:**
- Output step-by-step manual guide for the platform
- Include config code snippets from `templates/config-snippets.md`
- Suggest using the platform's own agent if available

## Local Automation Fit

Recommend local automation only when the user has always-on hardware and wants local control, lower latency, or polling-based rules that cloud scenes cannot handle well. If the user has no always-on device or only needs simple cloud scenes, prefer Mi Home App automation or the platform-native automation UI instead.

## Phase 4: Local Automation (Optional)

When user wants automations that run locally (not in Mi Home cloud):

> **Who is this for:** Local automation requires a 24/7 always-on device (NAS, Raspberry Pi, old PC, server) to run the polling engine. Best suited for users who have local hardware running at home (e.g., NAS owners, Raspberry Pi enthusiasts, home server hobbyists). If the user has no always-on device, recommend using Mi Home App cloud automation instead.

### Step 1: Ask Automation Location

```
"Where do you want the automation to run?"
  → A) Mi Home App cloud automation (simplest, no extra hardware)
  → B) Local automation (needs a 24/7 device like NAS/Raspberry Pi/old PC)
  → C) Both
```

If user chooses B but has no always-on device, prompt:
"Local automation needs a device that runs 24/7. Do you have any of these?"
  → NAS (Synology/QNAP/etc.)
  → Raspberry Pi
  → Old PC/Mac mini
  → Other always-on server
  → None → recommend Mi Home App cloud automation

If the household mixes ecosystems, treat Home Assistant as the coordinator when possible instead of forcing everything through mijia-api.

### Step 2: If Local Automation Chosen

**Setup flow:**
1. Ensure mijia-api is installed and authenticated (`~/.config/mijia-api/auth.json` exists)
2. Run `scripts/automation_setup.sh` to install deps + copy configs
3. Run `--discover` to list all devices with DIDs
4. Generate `devices.yaml` — map DIDs to HA-style entity_ids
5. Generate `automations.yaml` — YAML rules matching user's scenes
6. Test: run engine, verify sensor polling and rule triggers

**Two execution modes:**

| Mode | Command | RAM | Use case |
|------|---------|-----|----------|
| Standalone | `python3 automation/run_automations.py` | ~20-50MB | Simple, no extra deps |
| AppDaemon | `appdaemon -c automation/conf/` | ~50-150MB | Web UI, complex logic |

**Standalone mode** (recommended for most users):
- Single Python script, no framework dependency
- Uses same `mijia_client.py` as AppDaemon plugin
- Smart polling built-in
- `--discover` flag for device listing

**AppDaemon mode:**
- Plugin file MUST be named `mijiaplugin.py` (not `mijia_plugin.py`)
- Class MUST be named `MijiaPlugin`
- Required methods: `get_namespace()`, `get_updates()`, `stop()`, `get_complete_state()`, `get_metadata()`, `utility()`
- Config uses `devices_file: devices.yaml` (NOT `!include` YAML tag)
- Plugin must be copied to AppDaemon's plugins directory

**Smart polling:**
- Occupancy sensors → 10s interval (someone home)
- No occupancy → 60s interval (save API calls)
- Based on occupancy sensor DIDs in config

**Running as background service:**
```bash
nohup python3 automation/run_automations.py --config ~/.config/smart-home-planner/automation/conf &
```

### Step 3: Generate Automations

Based on user's planned scenes, generate YAML rules (HA-compatible format):

```yaml
- id: living_room_music
  alias: "客厅有人就播放音乐"
  trigger:
    - platform: state
      entity_id: "sensor.occupy_living_room"
      to: "on"
  condition:
    - condition: time
      after: "08:00:00"
      before: "23:00:00"
  action:
    - service: scene.turn_on
      target:
        entity_id: "scene.music_mode"
  mode: single
```

Supported: `state`/`numeric_state`/`time` triggers, `state`/`time`/`and`/`or`/`not` conditions, `scene.turn_on`/`light.turn_on`/`mijia.*` actions.

See `templates/automations-template.yaml` for common patterns.
See `knowledge/automation-guide.md` for full documentation.

## Verification Checklist

Before giving the final recommendation, check:

- Hub and protocol compatibility for every recommended device.
- Power, wiring, and mounting requirements.
- Risky scenes have explicit manual override or fallback behavior.
- Cross-platform conflicts are called out.
- Config output has been validated or clearly marked as manual-only.

## Knowledge References

Load as needed:
- `knowledge/platforms.md` — platform architecture, API details, auth methods
- `knowledge/devices.md` — device categories, protocols, brands, compatibility
- `knowledge/automation-patterns.md` — scene templates and triggers
- `knowledge/mijia-api-guide.md` — mijia-api installation, auth, device control
- `knowledge/homekit-guide.md` — homebridge-mcp-server installation, MCP config, device control
- `knowledge/automation-guide.md` — local automation setup, YAML format, smart polling
- `templates/plan-template.md` — planning document structure
- `templates/config-snippets.md` — platform-specific config code
- `templates/mijia-control-examples.md` — mijia-api code examples
- `templates/automations-template.yaml` — common automation rule templates

## Capability Detection

When configuring, detect agent capabilities:

1. **API connectivity** — can agent reach the platform API?
2. **File system** — can agent write config files to the target server?
3. **Combined result:**
   - API accessible + writable → full auto-config
    - API accessible + read-only → generate config + guide deployment
    - API not accessible → pure guidance mode
    - Not authorized → ask + guide API setup

## Common Failure Paths

- Expired token → refresh or re-authenticate.
- Device not discovered → re-run discovery and verify DID/entity mapping.
- YAML validation failure → correct the config before claiming success.
- Permission denied / read-only target → generate files and provide deployment steps.

## Common Scenarios

### "Help me plan my new apartment"
→ Full Phase 1 + Phase 2 flow

### "I bought a Xiaomi light, help me set it up"
→ Skip to Phase 3, detect mijia API access, configure or guide

### "What's the difference between HA and HomeKit?"
→ Reference `knowledge/platforms.md`, answer comparison

### "I want a security system"
→ Focus on sensors + cameras + security scene from `knowledge/automation-patterns.md`

### "Set up my bedroom automation"
→ Phase 3 only, use bedroom-specific devices and scenes
