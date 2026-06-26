# ReefBeat Complete Local HTTP API Reference

All devices: plain HTTP port 80, no authentication. Content-Type: application/json for writes.
Base URL: `http://<device_ip>`

---

## Common Endpoints (ALL Devices)

| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| GET | `/device-info` | — | Model, firmware, serial, hostname |
| GET | `/firmware` | — | Firmware version details |
| GET | `/dashboard` | — | Primary live status data |
| GET | `/mode` | — | Current mode string |
| GET | `/cloud` | — | Cloud link configuration |
| GET | `/wifi` | — | WiFi info |
| POST | `/maintenance` | `{}` | Start maintenance mode |
| DELETE | `/maintenance` | — | End maintenance mode |
| POST | `/emergency` | `{}` | Start emergency mode |
| DELETE | `/emergency` | — | End emergency mode |
| DELETE | `/off` | — | Turn device on (exit "off" mode / resume auto) |
| POST | `/cloud/enable` | `{}` | Enable cloud connection |
| POST | `/cloud/disable` | `{}` | Disable cloud connection |
| POST | `/firmware` | `{}` | Trigger firmware update |
| POST | `/reset` | `{}` | Factory reset device |
| POST | `/identify` | `{}` | Identify device (LED flash) — LED only |

---

## ReefLED G1 (RSLED50 / RSLED90 / RSLED160)

G1 devices use white/blue channel percentages (0–100). Kelvin is derived/virtual.

**Note:** RSLED90 older firmware may not have `/dashboard` — use `/` for device-info.

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/` or `/dashboard` | Live status (depends on firmware) |
| GET `/manual` | Current manual mode (white, blue, enabled, duration) |
| GET `/acclimation` | Acclimation config |
| GET `/moonphase` | Moon phase config (enabled, moon_day) |
| GET `/preset_name` | Current preset name (newer firmware) |
| GET `/preset_name/{1-7}` | Preset name per day 1–7 (older firmware) |
| GET `/auto/{1-7}` | Auto schedule for day 1–7 (1=Mon, 7=Sun) |
| GET `/clouds/{1-7}` | Clouds schedule for day 1–7 |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| POST | `/manual` | `{"white": 60, "blue": 80}` | Set manual mode |
| POST | `/manual` | `{"white": 60, "blue": 80, "duration": 30}` | Manual mode with timer (mins) |
| POST | `/acclimation` | `{"enabled": true, "duration": 50, "start_intensity_factor": 30}` | Set acclimation |
| POST | `/moonphase` | `{"enabled": true, "moon_day": 14}` | Set moon phase |
| POST | `/timer` | `{"duration": 30}` | Set manual duration (mins, 0=indefinite) |
| PUT | `/auto/{day}` | schedule JSON | Update daily auto schedule |
| PUT | `/clouds/{day}` | clouds JSON | Update daily clouds schedule |
| POST | `/identify` | `{}` | Flash LED to identify |

---

## ReefLED G2 (RSLED60 / RSLED115 / RSLED170)

G2 devices use kelvin (10000–20000) + intensity (0–100%). No white/blue direct control.

Same endpoints as G1 but `/manual` payload uses kelvin/intensity:

| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| POST | `/manual` | `{"kelvin": 14000, "intensity": 80}` | Set manual mode |
| POST | `/manual` | `{"kelvin": 14000, "intensity": 80, "duration": 30}` | Manual with timer (mins) |
| POST | `/acclimation` | `{"enabled": true, "duration": 50, "start_intensity_factor": 30}` | Set acclimation |
| POST | `/moonphase` | `{"enabled": true, "moon_day": 14}` | Set moon phase |
| POST | `/timer` | `{"duration": 30}` | Set manual duration (mins) |
| PUT | `/auto/{day}` | schedule JSON | Update daily auto schedule |
| PUT | `/clouds/{day}` | clouds JSON | Update daily clouds schedule |

---

## ReefDose (RSDOSE2 / RSDOSE4)

Heads are 1-indexed. RSDOSE2 has heads 1–2; RSDOSE4 has heads 1–4.

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/dashboard` | All head status, supplement names, daily dose, last dose |
| GET `/device-settings` | Device settings (stock_alert_days, dosing_waiting_period) |
| GET `/dosing-queue` | Pending dose queue |
| GET `/head/{n}/settings` | Per-head config (supplement, schedule, container_volume, slm) |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| POST | `/head/{n}/manual` | `{"volume": 5}` | Manual dose (mL) |
| PUT | `/head/{n}/settings` | settings JSON | Update head settings |
| DELETE | `/head/{n}/settings` | — | Delete/clear head supplement |
| DELETE | `/head/settings` | — | Delete all heads (bundled mode) |
| POST | `/head/{n}/start-calibration` | `{}` | Start calibration sequence |
| POST | `/head/{n}/calibration/start` | `{}` | Calibration start (alt endpoint) |
| POST | `/head/{n}/end-calibration` | `{"volume": 4.0}` | End calibration with measured volume |
| POST | `/head/{n}/calibration-manual` | `{"volume": 4}` | Test calibration (run 4mL test) |
| POST | `/head/{n}/end-setup` | `{}` | End calibration setup |
| POST | `/head/{n}/priming/start` | `{}` | Start priming |
| POST | `/head/{n}/priming/stop` | `{}` | Stop priming |
| POST | `/head/{n}/end-priming` | `{}` | End priming sequence |
| PUT | `/device-settings` | `{"stock_alert_days": 7, "dosing_waiting_period": 60}` | Update device settings |
| PUT | `/bundle/settings` | `{"bundled_heads": true}` | Enable bundle (linked heads) mode |
| POST | `/bundle/setup` | bundle payload | Set up bundle |

### Head settings structure
```json
{
  "supplement": {"uid": "...", "name": "Alk", "display_name": "Alkalinity"},
  "schedule": {"dd": 10.0},
  "container_volume": 1000,
  "schedule_enabled": true,
  "slm": false
}
```

---

## ReefMat (RSMAT250 / RSMAT500 / RSMAT1200)

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/dashboard` | Roll status: meters_left, advance_count, advance_mode |
| GET `/configuration` | Config: auto_advance, schedule_advance, schedule_length, roll model |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| POST | `/advance` | `{}` | Manual advance one step |
| POST | `/new-roll` | `{"external_diameter": 11.1, "name": "New Roll", "thickness": 0.3, "is_partial": false}` | Register new roll (full) |
| POST | `/new-roll` | `{"external_diameter": 8.5, "name": "Started Roll", "thickness": 0.3, "is_partial": true}` | Register started roll |
| PUT | `/configuration` | `{"auto_advance": true}` | Enable auto-advance |
| PUT | `/configuration` | `{"schedule_advance": true}` | Enable scheduled advance |
| PUT | `/configuration` | `{"schedule_length": 15.0}` | Set schedule advance length (cm, 5–45) |
| DELETE | `/emergency` | — | Clear emergency / mat jam |

**Roll max diameters by model:**
- RSMAT250: 11.1 cm
- RSMAT500: 11.1 cm
- RSMAT1200: 11.1 cm
- Thickness constant: 0.3 mm

---

## ReefRun (RSRUN)

Controls up to 2 pumps (return pump + skimmer).

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/dashboard` | Live pump state, intensity, temperature, over-skimming status |
| GET `/pump/settings` | Full pump config: schedule, sensor_controlled, overskimming |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| PUT | `/pump/settings` | `{"pump_1": {...}}` | Update pump 1 settings |
| PUT | `/pump/settings` | `{"pump_2": {...}}` | Update pump 2 settings |
| PUT | `/pump/settings` | `{"fullcup_enabled": true}` | Toggle full-cup detection (skimmer) |
| PUT | `/pump/settings` | `{"overskimming": {"enabled": true, "threshold": 10}}` | Configure over-skimming |
| POST | `/preview` | `{"pump_1": {"pd": 0, "ti": 80}, "pump_2": {"pd": 0, "ti": 50}}` | Preview pump speeds (temporary) |
| DELETE | `/preview` | — | Stop/save preview |

### Pump settings structure
```json
{
  "pump_1": {
    "id": 1,
    "name": "Return pump",
    "type": "return",
    "model": "return-6",
    "sensor_controlled": false,
    "schedule_enabled": true,
    "schedule": [{"st": 0, "ti": 80, "pd": 0}]
  }
}
```
- `schedule_enabled: false` = pump off
- `ti` = intensity (0–100)
- `pd` = pulse duration (0 = constant)
- `st` = start time offset

---

## ReefATO+ (RSATO+)

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/dashboard` | Water level, pump state, temperature, leak sensor, fill history |
| GET `/configuration` | auto_fill setting |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| PUT | `/configuration` | `{"auto_fill": true}` | Enable auto-fill |
| PUT | `/configuration` | `{"auto_fill": false}` | Disable auto-fill |
| POST | `/manual-pump` | `{}` | Start manual fill |
| POST | `/stop` | `{}` | Stop manual fill |
| POST | `/resume` | `{}` | Resume ATO after empty/malfunction latch |
| POST | `/update-volume` | `{"volume": 5000}` | Set reservoir volume remaining (mL) |

### Dashboard key fields
```json
{
  "mode": "auto",               // auto, pump_timeout, malfunction
  "water_level": "above",       // above, below, desired
  "pump_state": "off",          // off, pump_on, malfunction
  "ato_sensor": {
    "current_read": 25.1,       // temperature (°C)
    "current_level": "desired"  // desired, low, high
  },
  "leak_sensor": {
    "status": "dry"             // dry, wet
  },
  "today_fills": 2,
  "today_volume_usage": 2820    // mL
}
```

**Malfunction / pump_timeout:** POST `/resume` to clear the latch and restart ATO.

---

## ReefWave (RSWAVE25 / RSWAVE45)

⚠️ Local changes desync from the ReefBeat mobile app (expected behavior).

### Read
| Endpoint | Description |
|----------|-------------|
| GET `/dashboard` | Wave mode, intensity, direction |
| GET `/configuration` | Wave settings, schedule |
| GET `/preview` | Current preview settings |

### Write / Action
| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| PUT | `/configuration` | settings JSON | Update wave settings |
| POST | `/preview` | `{"type": "st", "frt": 5, "rrt": 5, "fti": 80, "rti": 80, "duration": 300000, "sn": 5, "pd": 10}` | Start preview mode |
| DELETE | `/preview` | — | Stop preview / save as schedule |

### Wave mode types (`type` field)
- `st` — steady (alternating)
- `ra` — random
- `re` — reef (simulated reef surge)
- `su` — surge
- `un` — nutrient (long cycle)

### Preview fields
| Field | Description | Range |
|-------|-------------|-------|
| `frt` | Forward time (min) | 2–60 |
| `rrt` | Backward time (min) | 2–60 |
| `fti` | Forward intensity (%) | 10–100 |
| `rti` | Backward intensity (%) | 10–100 |
| `duration` | Preview duration (ms) | 60000–600000 |
| `sn` | Steps (st mode) | 3–10 |
| `pd` | Wave period (s) | 2–25 |

---

## Cloud API (reference only — not implemented in the CLI script)

Base: `https://cloud.reef-beat.com`
Auth: POST `/oauth/token` with Basic `Z0ZqSHRKcGE6Qzlmb2d3cmpEV09SVDJHWQ==`

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic Z0ZqSHRKcGE6Qzlmb2d3cmpEV09SVDJHWQ==

grant_type=password&username=<your_email>&password=<your_password>
→ {"access_token": "..."}

GET /aquarium   → list of aquariums with uid, name, properties (shortcuts)
GET /device     → list of devices with hw_model, aquarium_uid, ip
```

---

## Device Discovery

Use the auto-discover command to find all ReefBeat devices on your network:
```bash
python3 scripts/reefbeat.py discover <YOUR_SUBNET>/24
```
This will identify each device type automatically from its `hw_model` field.
