---
name: smart-home-assistant
description: >
  Monitor and analyze Home Assistant energy consumption. Use when the user asks about power usage,
  energy monitoring, consumption by room/area, or wants to generate Home Assistant automations
  based on power thresholds. Do NOT use for device control, scene management, or general
  Home Assistant configuration tasks outside energy analysis.
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: ["python3"]
      config: ["home_assistant.url", "home_assistant.token"]
---

# Smart Home & Automation

Analyze real-time energy consumption from your Home Assistant instance. Identifies the highest consumers, groups usage by room/area, and generates actionable automations.

## When to Use

- "What's drawing the most power right now?"
- "Show me energy usage by room"
- "Generate an automation to turn off high-draw devices"
- "Which device is consuming the most electricity?"
- "Create a power threshold alert for my laundry room"

## When NOT to Use

- Turning devices on/off directly (use HA automations for that)
- Managing HA scenes, scripts, or dashboards
- Setting up new HA integrations or devices
- Non-energy Home Assistant queries (temperature, locks, cameras)

## Prerequisites

- A running Home Assistant instance accessible via network
- A long-lived access token (Settings > People > your user > Security > Long-Lived Access Tokens)
- Power monitoring entities with `unit_of_measurement` set to `W` or `kW`
- Areas configured in Home Assistant for room-level grouping

## Configuration

Set the environment variable before running:

```bash
export HA_TOKEN="your-home-assistant-long-lived-access-token"
```

The skill reads `smart_home/skill.yaml` for all other settings:

```yaml
home_assistant:
  url: "http://homeassistant.local:8123"   # Your HA URL
  token: "${HA_TOKEN}"                      # Resolved from env var

units:
  power: ["W", "kW"]
  energy: ["Wh", "kWh"]

rules:
  - name: "High Power Shutoff"
    threshold_watts: 2000                    # Trigger above this
    time_window: { after: "06:00", before: "22:00" }
    require_occupancy: "off"                 # Only trigger when unoccupied
    action: "turn_off"                       # turn_off, turn_on, or notify

outputs:
  default: ["summary", "table"]             # Formats produced when none specified
```

### Config Options

| Field | Default | Description |
|-------|---------|-------------|
| `home_assistant.url` | Required | HA instance URL |
| `home_assistant.token` | Required | Long-lived access token (use `${HA_TOKEN}` env var) |
| `rules[].threshold_watts` | 2000 | Power threshold for automation triggers |
| `rules[].time_window.after` | "06:00" | Automation active after this time |
| `rules[].time_window.before` | "22:00" | Automation active before this time |
| `rules[].require_occupancy` | "off" | Occupancy state required for trigger |
| `rules[].action` | "turn_off" | Action: `turn_off`, `turn_on`, or `notify` |
| `outputs.default` | ["summary", "table"] | Output formats when none specified |

## Output Formats

Three formats, selectable per request. Request by name: `summary`, `table`, `automation`.

### `summary` — Text Insight

A 2-3 sentence human-readable energy snapshot:

> Laundry is drawing 2,200W — 57% of your total 3,842W. The Dryer is the single highest consumer at 2,200W. No anomalies detected.

### `table` — Markdown Comparison

| Area | Device | Consumption (W) |
|------|--------|-----------------|
| Laundry | Dryer | 2,200.0 |
| Kitchen | Fridge | 180.5 |
| Unassigned | Smart Plug 3 | 45.0 |

Sorted by consumption descending, grouped by area.

### `automation` — HA Automation JSON

Generates a JSON payload ready for Home Assistant's `automation.create` service:

```json
[
  {
    "alias": "High Power Alert - Laundry",
    "trigger": {
      "platform": "numeric_state",
      "entity_id": "sensor.dryer_power",
      "above": 2000
    },
    "condition": [
      {
        "condition": "time",
        "after": "06:00:00",
        "before": "22:00:00"
      },
      {
        "condition": "state",
        "entity_id": "binary_sensor.laundry_occupancy",
        "state": "off"
      }
    ],
    "action": {
      "service": "switch.turn_off",
      "target": { "entity_id": "switch.dryer" }
    }
  }
]
```

Conditions are generated based on your config rules:
- **Power threshold** — only devices exceeding `threshold_watts` get automations
- **Time window** — always included from `time_window` config
- **Occupancy** — auto-detected: looks for `binary_sensor.<area>_occupancy` in your entities. Omitted if no occupancy sensor exists for that area.

## How It Works

The skill runs a three-stage pipeline:

```
FETCH          ANALYZE              FORMAT
HA REST API →  Filter energy   →   Summary
/api/states    entities            Markdown table
Area registry  Normalize kW→W     Automation JSON
Device reg.    Group by area
               Rank consumers
```

**Entity detection:** The skill identifies energy entities by checking for a numeric `state` value and a `unit_of_measurement` of `W`, `kW`, `kWh`, or `Wh`. Power values are auto-detected from the entity state, falling back to `power`, `current_power`, or `power_consumption` attributes.

**Area mapping:** Entities are mapped to rooms using the Home Assistant device and area registries. Entities without an area assignment appear under "Unassigned".

**Read-only:** This skill never modifies Home Assistant state. The automation JSON is a draft payload for you to review and apply manually.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "HA_URL is not configured" | Missing `home_assistant.url` in skill.yaml | Add your HA URL to `smart_home/skill.yaml` |
| "HA_TOKEN is not configured" | Env var not set | Run `export HA_TOKEN="your-token"` |
| "Cannot reach Home Assistant" | Network or URL issue | Verify HA is running and URL is correct |
| "No energy data available" | No matching entities | Ensure devices report `unit_of_measurement: W` or `kW` |
| All devices show "Unassigned" | No area registry data | Assign devices to areas in HA Settings > Areas |
| Automation JSON is empty | No devices exceed threshold | Lower `threshold_watts` in config |
