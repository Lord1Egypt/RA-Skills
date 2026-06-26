---
name: ratgdo32-disco
description: Control a ratgdo32 disco garage door opener via its local web API. Use when the user asks to open/close the garage, check garage status, toggle the garage light, check if a car is parked, enable/disable remotes, or anything involving the garage door. Supports door control, light, obstruction detection, vehicle presence (laser sensor), parking assist, motion, and remote lockout. Uses local network trust model (LAN-only, no internet exposure).
---

# ratgdo32 disco — Garage Door Controller

Control a ratgdo32 disco (HomeKit firmware) garage door opener via its local REST API.

## Security Model

The ratgdo32 disco uses a **local network trust model**. The device's web API is only accessible from your LAN — it does not expose any ports to the internet and has no cloud dependency.

**Your responsibilities:**
- Keep the device on a trusted, password-protected network (WPA2/WPA3)
- Do not port-forward the device's HTTP port to the internet
- Use your router's client isolation or VLAN features if you want extra segmentation
- The agent should always confirm door state before acting (built into the helper script)

This is the same trust model used by most local smart home devices (Hue bridges, Shelly relays, ESPHome, etc.).

## Setup

Set the `RATGDO_HOST` environment variable to your device's IP or mDNS hostname:

```bash
export RATGDO_HOST="192.168.1.XXX"  # or your-device.local
```

If unset, the helper script defaults to `192.168.1.XXX` — you must update it.

Find your device IP via your router's DHCP table, or use mDNS:

```bash
dns-sd -B _hap._tcp  # Browse HomeKit devices
```

## Device Info

Configure these for your setup:

| Field | How to Find |
|-------|-------------|
| **IP** | Router DHCP table or mDNS browse |
| **mDNS** | Usually `Garage-Door-XXXXXX.local` (based on MAC) |
| **MAC** | Printed on the ratgdo32 board or in your router's client list |
| **Protocol** | Check your garage opener's learn button color (yellow = Security+ 2.0, purple = Security+ 1.0) |
| **Web UI** | `http://<your-ip>/` |

## Quick Reference

| Action | Command |
|--------|---------|
| Get full status | `curl -s http://$RATGDO_HOST/status.json` |
| Open door | `curl -s -X POST -F "garageDoorState=1" http://$RATGDO_HOST/setgdo` |
| Close door | `curl -s -X POST -F "garageDoorState=0" http://$RATGDO_HOST/setgdo` |
| Light on | `curl -s -X POST -F "garageLightOn=1" http://$RATGDO_HOST/setgdo` |
| Light off | `curl -s -X POST -F "garageLightOn=0" http://$RATGDO_HOST/setgdo` |
| Disable remotes | `curl -s -X POST -F "garageLockState=1" http://$RATGDO_HOST/setgdo` |
| Enable remotes | `curl -s -X POST -F "garageLockState=0" http://$RATGDO_HOST/setgdo` |

## Status API

`GET http://<host>/status.json` returns JSON:

```json
{
  "garageDoorState": "open|closed|opening|closing|stopped",
  "garageLightOn": true|false,
  "garageObstructed": true|false,
  "garageLockState": "locked|unlocked",
  "vehicleState": "present|absent|arriving|departing",
  "vehicleDistance": 42,
  "motionDetected": true|false
}
```

### Key fields
- **garageDoorState** — current door position
- **garageLightOn** — ceiling light status
- **garageObstructed** — safety sensor triggered (do NOT close if true)
- **garageLockState** — "locked" means physical remotes are disabled
- **vehicleState** — laser sensor detects parked car
- **vehicleDistance** — distance to vehicle in cm (laser)
- **motionDetected** — PIR motion sensor

## Control API

`POST http://<host>/setgdo` with form data:

| Field | Values | Effect |
|-------|--------|--------|
| `garageDoorState` | `1` = open, `0` = close | Opens or closes the door |
| `garageLightOn` | `1` = on, `0` = off | Toggles ceiling light |
| `garageLockState` | `1` = lock, `0` = unlock | Disables/enables physical remotes |

## Safety Rules

1. **Never close the door if `garageObstructed` is true.** Report the obstruction and stop.
2. **Always check status before opening/closing** to confirm current state and avoid unnecessary operations.
3. **Confirm with the user before disabling remotes** — this temporarily locks out all physical remotes (wall button, car remotes). Re-enable with `garageLockState=0`.

## Helper Script

Use `scripts/garage.sh` for common operations:

```bash
# Status (human-readable)
bash scripts/garage.sh status

# Control
bash scripts/garage.sh open
bash scripts/garage.sh close
bash scripts/garage.sh light-on
bash scripts/garage.sh light-off
bash scripts/garage.sh lock-remotes
bash scripts/garage.sh unlock-remotes
```

The helper script includes safety checks: it verifies obstruction status before closing and confirms current state before toggling.

## Compatibility

- **Firmware:** HomeKit firmware v3.x+ (tested on v3.4.4)
- **Protocols:** Security+ 2.0 (yellow learn button), Security+ 1.0 (purple learn button)
- **Platforms:** Works alongside HomeKit/Apple Home. Not compatible with Home Assistant simultaneously (HomeKit single-pair limitation). Use web API for agent control, Apple Home for Siri/manual control.
- **Vehicle sensor:** Requires the optional laser parking sensor. Distance reading varies by vehicle position.

## Notes

- HomeKit pairing is separate from the web API. Both can operate simultaneously.
- The device broadcasts mDNS as `Garage-Door-XXXXXX.local` where XXXXXX is derived from the MAC address.
