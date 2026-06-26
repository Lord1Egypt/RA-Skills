---
name: shelly_sync
description: Monitor real-time power consumption from Shelly Pro 3EM and control local appliances/automation based on solar yield or grid usage.
version: 1.0.1
license: MIT
capabilities:
  - "Read current power consumption and grid injection (W)"
  - "Trigger smart plugs/appliances based on power thresholds"
  - "Provide power stats summary"
inputs:
  action:
    type: string
    description: "The operation: 'get_status' or 'optimize_load'"
    required: true
  target_load:
    type: string
    description: "Optional: Specific appliance to toggle (e.g. 'heatpump', 'charger')"
    required: false
env:
  - SHELLY_EM_IP
---

# Shelly Sync Skill

Interface between Shelly Pro 3EM energy monitoring and home automation.

## Usage Guidelines
- Power output in **Watts (W)** or **Kilowatts (kW)**
- **Negative** = grid injection (surplus). **Positive** = grid consumption
- If data fetch fails → report connection error immediately, don't hallucinate

## Commands

### get_status
Returns current power consumption across all 3 phases.
```
/shelly get_status
```

### optimize_load
Analyzes surplus and triggers load optimization if excess energy available.
```
/shelly optimize_load
/shelly optimize_load target_load:heatpump
```

## Implementation
- Script: `shelly_client.py`
- Calls Shelly Pro 3EM RPC API (`EMData.GetStatus`)
- Returns clean JSON with total power and phase breakdown