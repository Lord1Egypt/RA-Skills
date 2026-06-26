# Shelly BluTRV Manager (OpenClaw Skill)

[Deutsch](#deutsch) | [English](#english)

---

<a name="deutsch"></a>
## Deutsch

Dieser OpenClaw-Skill steuert Shelly BluTRV Heizkörperthermostate und liest Temperaturdaten von unterstützten Shelly-Sensoren aus. Der Skill arbeitet lokal bevorzugt über Shelly-Gateways per RPC und kann bei Statusabfragen automatisch auf die Shelly Cloud zurückfallen.

### Repository

Der Quellcode wird auf GitHub veröffentlicht:
[wolf128058/openclaw-skill-shelly-blutrv-manager](https://github.com/wolf128058/openclaw-skill-shelly-blutrv-manager)

### Fähigkeiten

- Raumtemperaturen und Thermostatstatus abfragen
- Zieltemperaturen für BluTRV-Thermostate setzen
- Lokale Shelly-Gateways direkt per RPC ansprechen
- Bei lokalen Fehlern oder Timeouts automatisch auf Cloud-Daten zurückfallen
- Messwerte von unterstützten Shelly H&T Sensoren auslesen
- Statusdaten in ein einheitliches JSON-Format normalisieren

### Typische Anwendungsfälle

- "Wie warm ist es gerade im Raum?"
- "Setze das Thermostat auf 20 Grad."
- "Prüfe, ob ein Thermostat erreichbar ist."
- "Lies die Temperatur eines Shelly-Sensors aus."

### Technischer Ansatz

- Local-first: BluTRV-Status und Steuerbefehle laufen bevorzugt über lokale Shelly-Gateways.
- Cloud-Fallback: Wenn ein lokaler Statusabruf fehlschlägt, kann der Skill auf Shelly-Cloud-Daten zurückgreifen.
- Einheitliche Ausgabe: Das Status-Script liefert normalisierte Felder wie `room_temperature_C`, `current_C`, `target_C`, `battery_percent` und `source`.
- Defensiver Scope: Das veröffentlichte Paket ist bewusst auf lokale RPC-Steuerung und dokumentierten Cloud-Fallback begrenzt.

### Enthaltene Werkzeuge

- `scripts/blutrv-status.sh` für Statusabfragen mit Timeout-Handling, Retry und Cloud-Fallback
- `scripts/blutrv-control.sh` zum Setzen von Zieltemperaturen mit anschließender Verifikation
- `scripts/shelly-cloud.sh` als generischer Wrapper für die Shelly-Cloud-API
- `references/auth-and-access.md` für Credential-Handling und Access-Grenzen
- `references/troubleshooting.md` für typische Fehlerbilder und Recovery-Schritte

### Voraussetzungen

- OpenClaw
- Bash
- `curl`
- `jq`
- Ein Shelly-Setup mit BluTRV-Geräten und mindestens einem passenden Gateway

### Konfiguration

Für Cloud-Funktionen werden Shelly-Zugangsdaten über Umgebungsvariablen geladen, typischerweise aus:

```env
~/.openclaw/skills/.shelly-blutrv-manager.env
```

Benötigte Variablen:

```env
SHELLY_GATEWAYS="bedroom-gateway|192.168.0.101|deadc0debeef"
SHELLY_TARGETS="schlafzimmer,bedroom|bedroom-gateway|200|cafebabefeed"
SHELLY_CLOUD_SERVER_URI=https://example.shelly.cloud
SHELLY_CLOUD_TOKEN=your_token_here
```

Die Datei sollte nur Shelly-bezogene Variablen enthalten und mit restriktiven Rechten gespeichert werden, zum Beispiel `chmod 600 ~/.openclaw/skills/.shelly-blutrv-manager.env`.

### Nutzung

```bash
# BluTRV-Status lesen
scripts/blutrv-status.sh <gateway_ip> <trv_id>

# Oder per Ziel-Alias aus SHELLY_TARGETS
scripts/blutrv-status.sh schlafzimmer

# BluTRV-Zieltemperatur setzen
scripts/blutrv-control.sh <gateway_ip> <trv_id> <target_temp_c>

# Oder per Ziel-Alias aus SHELLY_TARGETS
scripts/blutrv-control.sh wohnzimmer <target_temp_c>

# Alle Cloud-Statusdaten laden
scripts/shelly-cloud.sh list

# Einzelnes Cloud-Gerät lesen
scripts/shelly-cloud.sh status <device_id>
```

### Hinweise

- BluTRV-Geräte sind batteriebetriebene Bluetooth-Geräte und reagieren nicht immer sofort.
- Lokale RPC-Kommunikation ist für Thermostate der bevorzugte Weg.
- Cloud-Zugriff eignet sich vor allem für Fallbacks und unterstützte WiFi-Sensoren.
- Die Helper-Scripts akzeptieren frei definierbare Ziel-Aliase aus `SHELLY_TARGETS`.
- Ein Ziel ist eindeutig über Gateway, TRV-ID und Device-ID modelliert, damit gleiche `BluTrv (200)` Namen an verschiedenen Gateways nicht verwechselt werden.
- Das veröffentlichte ClawHub-Paket enthält bewusst keine experimentellen WebSocket-Schreib- oder Debug-Helfer.
- Für eine öffentliche Veröffentlichung sollten installationsspezifische Daten wie Geräte-IDs, Tokens, interne Hostnamen oder IP-Adressen aus dem Repository entfernt oder ersetzt werden.

---

<a name="english"></a>
## English

This OpenClaw skill controls Shelly BluTRV radiator thermostats and reads temperature data from supported Shelly sensors. It prefers local RPC through Shelly gateways and can automatically fall back to Shelly Cloud data when local status requests fail.

### Repository

The source code is published on GitHub:
[wolf128058/openclaw-skill-shelly-blutrv-manager](https://github.com/wolf128058/openclaw-skill-shelly-blutrv-manager)

### Capabilities

- Read room temperatures and thermostat status
- Set target temperatures for BluTRV thermostats
- Talk directly to local Shelly gateways via RPC
- Fall back to cloud data when local requests time out or fail
- Read measurements from supported Shelly H&T sensors
- Normalize status data into a consistent JSON shape

### Typical Use Cases

- "What is the current room temperature?"
- "Set the thermostat to 20 degrees."
- "Check whether a thermostat is reachable."
- "Read the temperature from a Shelly sensor."

### Technical Approach

- Local-first: BluTRV status checks and control commands are sent through local Shelly gateways whenever possible.
- Cloud fallback: If a local status call fails, the skill can use Shelly Cloud data as a fallback.
- Consistent output: The status script returns normalized fields such as `room_temperature_C`, `current_C`, `target_C`, `battery_percent`, and `source`.
- Defensive scope: The published package is intentionally limited to local RPC control and documented cloud fallback.

### Included Tools

- `scripts/blutrv-status.sh` for status queries with timeout handling, retry logic, and cloud fallback
- `scripts/blutrv-control.sh` for setting thermostat targets with verification
- `scripts/shelly-cloud.sh` as a generic Shelly Cloud API wrapper
- `references/auth-and-access.md` for credential handling and access boundaries
- `references/troubleshooting.md` for common failure modes and recovery steps

### Requirements

- OpenClaw
- Bash
- `curl`
- `jq`
- A Shelly setup with BluTRV devices and at least one compatible gateway

### Configuration

Cloud features load Shelly credentials from environment variables, typically from:

```env
~/.openclaw/skills/.shelly-blutrv-manager.env
```

Required variables:

```env
SHELLY_GATEWAYS="bedroom-gateway|192.168.0.101|deadc0debeef"
SHELLY_TARGETS="bedroom|bedroom-gateway|200|cafebabefeed"
SHELLY_CLOUD_SERVER_URI=https://example.shelly.cloud
SHELLY_CLOUD_TOKEN=your_token_here
```

This file should contain only Shelly-related variables and should be stored with restrictive permissions, for example `chmod 600 ~/.openclaw/skills/.shelly-blutrv-manager.env`.

### Usage

```bash
# Read BluTRV status
scripts/blutrv-status.sh <gateway_ip> <trv_id>

# Or use a target alias from SHELLY_TARGETS
scripts/blutrv-status.sh bedroom

# Set a BluTRV target temperature
scripts/blutrv-control.sh <gateway_ip> <trv_id> <target_temp_c>

# Or use a target alias from SHELLY_TARGETS
scripts/blutrv-control.sh living-room <target_temp_c>

# Load all cloud status data
scripts/shelly-cloud.sh list

# Read a single cloud device
scripts/shelly-cloud.sh status <device_id>
```

### Notes

- BluTRV devices are battery-powered Bluetooth devices and may react with a short delay.
- Local RPC is the preferred path for thermostat interactions.
- Cloud access is mainly useful for fallback behavior and supported WiFi sensors.
- The helper scripts accept user-defined target aliases from `SHELLY_TARGETS`.
- A target is modeled by gateway, TRV id, and device id so repeated `BluTrv (200)` names on different gateways do not get mixed up.
- The published ClawHub package intentionally excludes experimental WebSocket write and debug helpers.
- Before publishing the repository, replace or remove installation-specific data such as device IDs, tokens, internal hostnames, or IP addresses.
