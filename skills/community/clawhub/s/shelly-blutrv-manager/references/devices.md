# Shelly Device Registry

## BluTRV Thermostate (Bluetooth)

| Gerät | Device ID | Raum | Gateway IP | TRV # |
|-------|-----------|------|------------|-------|
| TRV 200 (WZ) | `shellyblutrv-bad0ff1ce123` | Wohnzimmer | 192.168.0.102 | 200 |
| TRV 202 (Flur) | `shellyblutrv-f00dbabecafe` | Flur | 192.168.0.102 | 202 |
| TRV 200 (SZ) | `shellyblutrv-deadbeefcafe` | Schlafzimmer | 192.168.0.101 | 200 |

## H&T Sensoren (WiFi)

| Gerät | Device ID | Raum | Typ | Sensoren |
|-------|-----------|------|-----|----------|
| H&T Sensor | `decafbadf00d` | Schlafzimmer | WiFi | **Temperatur + Feuchtigkeit** |

### H&T Sensor Details

Der H&T Sensor liefert über die Cloud-API:
- `temperature:0.tC` — Temperatur in °C
- `humidity:0.rh` — Relative Feuchtigkeit in %
- `devicepower:0.battery.percent` — Batteriestand

```bash
# Temperatur
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh status decafbadf00d | jq '.data.device_status["temperature:0"].tC'

# Feuchtigkeit
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh status decafbadf00d | jq '.data.device_status["humidity:0"].rh'

# Batterie
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh status decafbadf00d | jq '.data.device_status["devicepower:0"].battery.percent'
```

## Gateways

| Name | Key | IP | Device ID | TRVs |
|------|-----|----|-----------|------|
| Wohnzimmer Gateway | `default` | 192.168.0.102 | `cafebabec0de` | TRV 200 (WZ), TRV 202 (Flur) |
| Schlafzimmer Gateway | `sz` | 192.168.0.101 | `deadc0debeef` | TRV 200 (SZ) |

## Aliase

| Alias | Gateway | TRV # |
|-------|---------|-------|
| `wohnzimmer`, `wz`, `living` | default | 200 |
| `flur`, `hallway` | default | 202 |
| `schlafzimmer`, `sz`, `bedroom` | sz | 200 |

## Hinweise

- **BluTRVs**: Lokale RPC-Abfragen bevorzugen, Cloud-Fallback wenn Timeout
- **H&T Sensoren**: Nur über Cloud-API erreichbar (WiFi-Geräte)
- **Rate-Limiting**: Cloud-API hat striktes Rate-Limit — nicht spammen