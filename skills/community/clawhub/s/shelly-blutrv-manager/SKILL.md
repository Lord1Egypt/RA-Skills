---
name: Shelly BluTRV Manager
slug: shelly-blutrv-manager
homepage: https://github.com/wolf128058/openclaw-skill-shelly-blutrv-manager
description: Control Shelly BluTRV thermostats and H&T sensors via local RPC with cloud fallback. Use when: (1) checking room temperatures, (2) setting thermostat targets, (3) controlling heating in Schlafzimmer/Wohnzimmer/Flur, (4) reading sensor data from Shelly devices. Triggers on phrases like "heizung", "temperatur setzen", "thermostat", "raumtemperatur", "BluTRV", "Shelly TRV".
changelog: Conservative ClawHub release with explicit runtime requirements, dedicated secret file, local RPC control, and cloud fallback for supported devices.
metadata: {"clawdbot":{"emoji":"T","requires":{"bins":["bash","curl","jq"],"env":["SHELLY_GATEWAYS","SHELLY_TARGETS","SHELLY_CLOUD_SERVER_URI","SHELLY_CLOUD_TOKEN"],"config":["~/.openclaw/skills/.shelly-blutrv-manager.env"]},"primaryEnv":"SHELLY_CLOUD_TOKEN","os":["linux","darwin"]}}
---

# Shelly BluTRV Manager

Local-first control of Shelly BluTRV thermostats via RPC with automatic cloud fallback.

## Repository

GitHub: `https://github.com/wolf128058/openclaw-skill-shelly-blutrv-manager`

## Setup

Bei Erstnutzung zuerst `references/setup.md` lesen und Gateway-Zuordnung, Cloud-Fallback und Schreibgrenzen festlegen, bevor Befehle ausgeführt werden.

## Access

Siehe `references/auth-and-access.md` für Credential-Handling, lokale vs. Cloud-Nutzung und Sicherheitsgrenzen.

## Quick Reference

### BluTRV Thermostate

| Raum | Gateway | TRV # | Device ID |
|------|---------|-------|-----------|
| Schlafzimmer | `192.168.0.101` | 200 | `cafebabefeed` |
| Wohnzimmer | `192.168.0.102` | 201 | `bad0ff1ce123` |
| Flur | `192.168.0.102` | 202 | `f00dbabecafe` |

### H&T Sensoren (WiFi, nur Cloud)

| Raum | Device ID | Typ |
|------|-----------|-----|
| Schlafzimmer | `bad0ff1ce321` | H&T (Temp + Feuchtigkeit) |

**H&T Sensoren liefern:** Temperatur, relative Feuchtigkeit, Batterie, RSSI

## Status abfragen

### BluTRV Thermostate

```bash
# Via Alias
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/blutrv-status.sh schlafzimmer

# Via IP + TRV-ID
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/blutrv-status.sh 192.168.0.101 200

# Output-Fields: room_temperature_C, current_C, target_C, battery_percent, source, rssi
```

### H&T Sensoren (nur Cloud)

```bash
# Status mit Temperatur + Feuchtigkeit
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/ht-status.sh schlafzimmer

# Alternativ via Device-ID
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/ht-status.sh decafbadf00d

# Rohes JSON
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh status decafbadf00d
```

**H&T Output-Fields:** `temperature_C`, `humidity_percent`, `battery_percent`, `rssi`

### Alle Geräte auf einmal

```bash
# Alle Status abrufen
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh list | jq '.data.devices_status'
```

## Temperatur setzen

```bash
# Via Helper-Script (empfohlen)
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/blutrv-control.sh <gateway_ip> <trv_id> <temp>

# Beispiel: Schlafzimmer auf 20°C
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/blutrv-control.sh 192.168.0.101 200 20

# Via Alias
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/blutrv-control.sh schlafzimmer 20

# Direkt via RPC (für Debugging)
curl -s -X POST "http://192.168.0.101/rpc" \
  -H "Content-Type: application/json" \
  -d '{"method":"BluTrv.Call","params":{"id":200,"method":"TRV.SetTarget","params":{"id":0,"target_C":20}}}'
```

**Wichtig:** BluTRVs sind Bluetooth-Battery-Geräte — Befehle brauchen ein paar Sekunden.

## Cloud API

```bash
# Geräte auflisten
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh list

# Device-Status
~/.openclaw/workspace/skills/shelly-blutrv-manager/scripts/shelly-cloud.sh status <device_id>
```

**Limitation:** Cloud-API kann KEINE BluTRV-Status lesen — nur WiFi-Geräte (H&T, Shelly Plug, etc.). Für TRVs immer lokale Gateways nutzen.

## Device-Registry

Siehe `references/devices.md` für vollständige Geräteliste und Gateway-Zuordnung.

## Ziel-Aliase

Die Helper-Scripts akzeptieren neben `gateway_ip` und `trv_id` auch frei definierbare Ziel-Aliase aus `SHELLY_TARGETS`.
Ein Ziel wird intern eindeutig über `gateway_key + trv_id + trv_device_id` beschrieben, damit mehrere `BluTrv (200)` an unterschiedlichen Gateways nicht verwechselt werden.

## Best Practices

1. **Immer Helper-Scripts nutzen** — nicht nacktes `curl` ohne Timeout
2. **Lokales RPC bevorzugen** — Cloud hat striktes Rate-Limit
3. **Write verifizieren** — `blutrv-control.sh` prüft nach dem Setzen das resultierende `target_C`
4. **Timeout-Handling** — `blutrv-status.sh` hat bereits integriertes Timeout + Fallback
5. **Fehler offen kommunizieren** — Bei Timeout/Hänger: "Laufzeitprüfung fehlgeschlagen" sagen, nicht still hängen

## Scope

Das veröffentlichte Paket ist bewusst auf lokale RPC-Steuerung, verifizierte Writes und Cloud-Fallback begrenzt.
Experimentelle WebSocket-Schreib- oder Debug-Helfer sind nicht Teil dieses ClawHub-Releases.

## Troubleshooting

Siehe `references/troubleshooting.md` für typische Fehlerbilder und Recovery-Schritte.