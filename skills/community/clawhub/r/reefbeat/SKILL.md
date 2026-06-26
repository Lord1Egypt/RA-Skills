---
name: reefbeat
description: Control and monitor Red Sea ReefBeat aquarium equipment directly over the local HTTP API — no cloud required. Supports ALL actions on ALL devices — ReefLED G1/G2 (lighting/kelvin/intensity/schedules/acclimation/moonphase), ReefDose (dosing/calibration/priming/supplements), ReefMat (filter roll/advance/new-roll), ReefRun (return pump + skimmer control/overskimming), ReefATO+ (auto top-off/resume/volume), ReefWave (wave modes/preview). Use for ANY reef tank / aquarium request.
---

# ReefBeat Skill

Direct HTTP control for Red Sea ReefBeat devices. Full API reference in `references/api.md`.

## Quick Start

```bash
python3 scripts/reefbeat.py discover <DEVICE_IP>/24   # find all devices
python3 scripts/reefbeat.py <ip> info                   # device info + type
python3 scripts/reefbeat.py <ip> status                 # /dashboard
python3 scripts/reefbeat.py <ip> get /endpoint
python3 scripts/reefbeat.py <ip> post /endpoint '{"key":"value"}'
python3 scripts/reefbeat.py <ip> put /endpoint '{"key":"value"}'
```

## Device Discovery

Run discovery to find all devices on your network automatically:
```bash
python3 scripts/reefbeat.py discover <YOUR_SUBNET>/24
```

---

## Common Actions by Request

### ReefLED — Lighting

```bash
# Check current light status
python3 scripts/reefbeat.py <LED_IP> get /manual

# Set white/blue (G1 — RSLED90)
python3 scripts/reefbeat.py <LED_IP> post /manual '{"white": 60, "blue": 80}'

# Timed manual (30 min then resume schedule)
python3 scripts/reefbeat.py <LED_IP> post /manual '{"white": 60, "blue": 80, "duration": 30}'

# Toggle moonphase
python3 scripts/reefbeat.py <LED_IP> post /moonphase '{"enabled": true, "moon_day": 14}'

# Acclimation
python3 scripts/reefbeat.py <LED_IP> post /acclimation '{"enabled": true, "duration": 50, "start_intensity_factor": 30}'

# View auto schedule for Monday (day 1)
python3 scripts/reefbeat.py <LED_IP> get /auto/1

# Turn LED off / resume schedule
python3 scripts/reefbeat.py <LED_IP> delete /off
```

### ReefRun — Pumps / Skimmer

```bash
# Check pump status
python3 scripts/reefbeat.py <RUN_IP> status
python3 scripts/reefbeat.py <RUN_IP> get /pump/settings

# Turn pump on/off (schedule_enabled controls this)
python3 scripts/reefbeat.py <RUN_IP> put /pump/settings \
  '{"pump_2": {"id":2,"name":"skimmer","type":"skimmer","model":"rsk-300","sensor_controlled":true,"schedule_enabled":false,"schedule":[{"st":0,"ti":0,"pd":0}]}}'

# Change return pump intensity to 70%
python3 scripts/reefbeat.py <RUN_IP> put /pump/settings \
  '{"pump_1": {"id":1,"name":"Return pump","type":"return","model":"return-6","sensor_controlled":false,"schedule_enabled":true,"schedule":[{"st":0,"ti":70,"pd":0}]}}'

# Toggle over-skimming protection
python3 scripts/reefbeat.py <RUN_IP> put /pump/settings \
  '{"overskimming": {"enabled": true, "threshold": 10}}'
```

### ReefATO+ — Auto Top-Off

```bash
# Check ATO status (level, temp, fills)
python3 scripts/reefbeat.py <ATO1_IP> status
python3 scripts/reefbeat.py <ATO2_IP> status

# Resume after malfunction/pump_timeout
python3 scripts/reefbeat.py <ATO1_IP> post /resume

# Enable/disable auto-fill
python3 scripts/reefbeat.py <ATO1_IP> put /configuration '{"auto_fill": true}'

# Manual fill / stop
python3 scripts/reefbeat.py <ATO1_IP> post /manual-pump
python3 scripts/reefbeat.py <ATO1_IP> post /stop

# Set reservoir volume (mL)
python3 scripts/reefbeat.py <ATO1_IP> post /update-volume '{"volume": 10000}'
```

### ReefMat — Filter Roll

```bash
# Check roll status
python3 scripts/reefbeat.py <MAT1_IP> status   # aquarium 1 mat
python3 scripts/reefbeat.py <MAT2_IP> status   # aquarium 2 mat

# Advance roll manually
python3 scripts/reefbeat.py <MAT1_IP> post /advance

# Register new full roll (ReefMat250 — max diameter 11.1cm)
python3 scripts/reefbeat.py <MAT1_IP> post /new-roll \
  '{"external_diameter": 11.1, "name": "New Roll", "thickness": 0.3, "is_partial": false}'

# Register started roll
python3 scripts/reefbeat.py <MAT1_IP> post /new-roll \
  '{"external_diameter": 8.5, "name": "Started Roll", "thickness": 0.3, "is_partial": true}'

# Toggle auto-advance
python3 scripts/reefbeat.py <MAT2_IP> put /configuration '{"auto_advance": true}'
```

### ReefWave — Wave Pump

```bash
# Check wave status
python3 scripts/reefbeat.py <WAVE_IP> status

# Start preview mode (alternating, 5min fwd/5min back, 80% intensity, 5min total)
python3 scripts/reefbeat.py <WAVE_IP> post /preview \
  '{"type":"st","frt":5,"rrt":5,"fti":80,"rti":80,"duration":300000,"sn":5,"pd":10}'

# Stop/save preview
python3 scripts/reefbeat.py <WAVE_IP> delete /preview
```

### Shortcuts (All Devices)

```bash
# Start feeding mode
python3 scripts/reefbeat.py <ip> post /maintenance   # or /emergency

# End maintenance
python3 scripts/reefbeat.py <ip> delete /maintenance
```

---

## Network Behaviour
- **Auto-discovery** (`discover` command) opens a UDP socket to `8.8.8.8` (no data sent — standard technique to detect the local network interface), then actively probes all hosts in the subnet via HTTP `/device-info` and `/description.xml`. This is local-only after the interface detection step.
- No cloud authentication or external API calls are made by this skill.
- All device control is purely local HTTP (port 80, no auth).

## Notes
- G1 LEDs (RSLED50/90/160): white + blue channels (0–100%)
- G2 LEDs (RSLED60/115/170): kelvin (10000–20000) + intensity (0–100%)
- ReefDose config requests can take 7–9s — normal
- ReefWave local changes desync from app — expected
- ATO `pump_timeout` / `malfunction` → POST `/resume` to clear
- Always read `/pump/settings` before writing to preserve unchanged pump fields
