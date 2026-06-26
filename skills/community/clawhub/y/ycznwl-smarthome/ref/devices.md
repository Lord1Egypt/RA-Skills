# Device Reference

## API

```
GET /api/v1/devices              — list all devices
GET /api/v1/devices/:id          — get single device (by numeric ID)
POST /api/v1/devices/:id/control — control a device
```

The control endpoint accepts:
```json
{ "action": "<action_name>", "params": { ... } }
```

## Device Types

| Type | Description | Common Subtypes |
|------|-------------|-----------------|
| `light` | Lighting | `light`, `light_dimmer`, `light_tunable`, `light_rgb` |
| `switch` | On/off switching | `switch`, `outlet`, `pulse` |
| `sensor` | Environmental/security sensors | See sensor subtypes below |
| `curtain` | Curtains and blinds | `curtain`, `blind`, `pulse_curtain` |
| `thermostat` | Temperature controllers | — |
| `ac` | Air conditioners | `ac`, `heater` |
| `fan` | Fans | `fan` |
| `garage` | Garage doors | `garage`, `pulse_garage` |
| `window` | Windows | `window`, `pulse_window` |
| `scene` |  scene controllers **and** virtual scenes | `scene` (check `protocol` to distinguish) |
| `lock` | Door locks | `lock` |
| `air_purifier` | Air purifiers | `air_purifier` |
| `player` | Media players | `player` |

### Sensor Subtypes

| Subtype | Measures | Status Property | Unit |
|---------|----------|-----------------|------|
| `sensor_temperature` | Temperature | `temperature` | °C |
| `sensor_humidity` | Humidity | `humidity` | % |
| `sensor_illuminance` | Light level | `illuminance` | lux |
| `sensor_co2` | CO₂ | `co2` | ppm |
| `sensor_co` | CO | `co` | ppm |
| `sensor_pm25` | PM2.5 | `pm25` | µg/m³ |
| `sensor_pm10` | PM10 | `pm10` | µg/m³ |
| `sensor_tvoc` | TVOC | `tvoc` | — |
| `sensor_air_quality` | Air quality index | `air_quality` | — |
| `sensor_motion` | Motion detected | `motion` | bool |
| `sensor_presence` | Presence detected | `presence` | bool |
| `sensor_smoke` | Smoke detected | `smoke` | bool |
| `sensor_leak` | Water leak | `leak` | bool |
| `sensor_contact` | Door/window contact | `contact` | bool |

## Capabilities, Actions, and Parameters

### on_off — Power control

**Applies to**: light, switch, outlet, ac, fan, air_purifier

| Action | Params | Description |
|--------|--------|-------------|
| `turn_on` | none | Turn the device on |
| `turn_off` | none | Turn the device off |
| `toggle` | none | Toggle current power state |

**Status property**: `power` (boolean)

**Example — turn on a light**:
```json
{ "action": "turn_on", "params": {} }
```

**Example — turn off a switch**:
```json
{ "action": "turn_off", "params": {} }
```

### brightness — Dimming

**Applies to**: light_dimmer, light_tunable, light_rgb

| Action | Params | Description |
|--------|--------|-------------|
| `set_brightness` | `{ "brightness": <0-100> }` | Set brightness percentage |

**Status property**: `brightness` (int, 0–100, unit: %)

**Example**:
```json
{ "action": "set_brightness", "params": { "brightness": 75 } }
```

### color_temperature — Color temperature

**Applies to**: light_tunable

| Action | Params | Description |
|--------|--------|-------------|
| `set_color_temperature` | `{ "color_temperature": <K> }` | Set color temp in Kelvin |

**Configurable per-device range**: any window within `1000–10000 K` (default `2700–6500 K`),
with a configurable step (default `100`). Out-of-range values are clamped and step-aligned
by the backend, but stay within the user's configured range when authoring scenes.

**Status property**: `color_temperature` (int, unit: K)

**Example**:
```json
{ "action": "set_color_temperature", "params": { "color_temperature": 4000 } }
```

### color — RGB color

**Applies to**: light_rgb

| Action | Params | Description |
|--------|--------|-------------|
| `set_color` | `{ "color": "#RRGGBB" }` | Set color as a hex string (preferred) |

**Examples**:
```json
{ "action": "set_color", "params": { "color": "#FF8800" } }
```

**Status properties**: `color` (string, e.g. `"#FF8800"`), `hue` (int, 0–360, read-only),
`saturation` (int, 0–100, read-only)

**Important — what `set_color` does NOT accept**:
- `hue` / `saturation` are **status properties only**. There is no `set_hue` or
  `set_saturation` action and they cannot be passed as params to `set_color`.
- HSV input is not supported. Convert HSV → hex before sending.

### open_close — Open/close control

**Applies to**: curtain, blind, garage, window, pulse_curtain, pulse_garage, pulse_window

| Action | Params | Description |
|--------|--------|-------------|
| `open` | none | Open the device |
| `close` | none | Close the device |
| `stop` | none | Stop current movement |

**Status properties**: `open_state` (bool), `is_opening` (bool), `is_closing` (bool)

**Example — open a curtain**:
```json
{ "action": "open", "params": {} }
```

### position — Position control

**Applies to**: curtain, blind

| Action | Params | Description |
|--------|--------|-------------|
| `set_position` | `{ "position": <0-100> }` | Set position percentage (0=closed, 100=open) |

**Status property**: `position` (int, 0–100, unit: %)

**Example — set curtain to 50%**:
```json
{ "action": "set_position", "params": { "position": 50 } }
```

### slat_position — Blind slat angle

**Applies to**: blind

| Action | Params | Description |
|--------|--------|-------------|
| `set_slat_position` | `{ "slat_position": <0-100> }` | Set slat angle percentage |

**Status property**: `slat_position` (int, 0–100, unit: %)

### target_temperature — Temperature setpoint

**Applies to**: thermostat, ac, heater

| Action | Params | Description |
|--------|--------|-------------|
| `set_target_temperature` | `{ "target_temperature": <0-100> }` | Set target temperature in °C |

**Status property**: `target_temperature` (float, 0–100, step: 0.5, unit: °C)

**Example — set AC to 24°C**:
```json
{ "action": "set_target_temperature", "params": { "target_temperature": 24 } }
```

### mode — Operation mode

**Applies to**: ac

| Action | Params | Description |
|--------|--------|-------------|
| `set_mode` | `{ "mode": "<mode>" }` | Set operation mode |

**Mode values**: `auto`, `cool`, `dry`, `fan_only`, `heat`

**Status property**: `mode` (enum)

**Example — set AC to cooling**:
```json
{ "action": "set_mode", "params": { "mode": "cool" } }
```

### fan_speed — Fan speed control

**Applies to**: ac, fan, air_purifier

| Action | Params | Description |
|--------|--------|-------------|
| `set_fan_speed` | `{ "fan_speed": <0-100> }` | Set fan speed percentage |
| `set_fan_speed_mode` | `{ "fan_speed_mode": "<mode>" }` | Set fan speed preset (enum value depends on device type) |

**`fan_speed_mode` enum values are NOT universal — they differ by device type:**

| Device type | Default enum | Notes |
|-------------|--------------|-------|
| `ac` | `auto`, `low`, `medium`, `high` | Can be customized per device via `fan_speed_mapping` |
| `fan` | depends on `speed_level_mapping` (typical defaults: `level1`, `level2`, `level3`) | Fans usually do NOT accept `auto`/`low`/`medium`/`high` directly |
| `air_purifier` | depends on `speed_level_mapping` | Same as fan — read device capability before sending |

> ⚠ Always read the target device's capability `fan_speed_mode` enum (via `GET /devices/:uuid` → `capabilities[].properties[name=fan_speed_mode].options`) before issuing `set_fan_speed_mode`. Sending an enum value that the device doesn't expose will be rejected by the backend (`unsupported fan_speed_mode: ...`).

**Status properties**: `fan_speed` (int, 0–100), `fan_speed_mode` (enum, varies per device)

### swing_mode — Swing/oscillation

**Applies to**: ac

| Action | Params | Description |
|--------|--------|-------------|
| `set_swing_mode` | `{ "swing_mode": true/false }` | Enable/disable swing |

**Status property**: `swing_mode` (bool)

### lock_unlock — Lock control

**Applies to**: lock

| Action | Params | Description |
|--------|--------|-------------|
| `lock` | none | Lock the device |
| `unlock` | none | Unlock the device |

**Status property**: `lock_state` (bool)

### scene — Scene activation

**Applies to**: scene (KNX physical scene controllers and gateway virtual scene devices)

| Action | Params | Description |
|--------|--------|-------------|
| `activate_scene` | none | Activate the scene (the scene number is fixed by device configuration; you don't pass it) |

### playback — Media playback

**Applies to**: player

| Action | Params | Description |
|--------|--------|-------------|
| `play` | none | Start playback |
| `pause` | none | Pause playback |
| `play_pause` | none | Toggle play/pause |
| `next_track` | none | Skip to next track (only if supported) |

**Status property**: `playing` (boolean)

### volume — Volume control

**Applies to**: player

| Action | Params | Description |
|--------|--------|-------------|
| `set_volume` | `{ "volume": <0-100> }` | Set volume percentage |
| `mute` | none | Mute (only if supported) |
| `unmute` | none | Unmute (only if supported) |
| `toggle_mute` | none | Toggle mute (only if supported) |

**Status properties**: `volume` (int, 0–100, unit: %), `muted` (boolean)

### playback_mode — Playback mode

**Applies to**: player (KNX only)

| Action | Params | Description |
|--------|--------|-------------|
| `set_playback_mode` | `{ "playback_mode": "<mode>" }` | Set playback mode |

**Mode values**: `sequential`, `repeat`, `repeat_one`, `shuffle`, `single`

### media_source — Media source selection

**Applies to**: player (KNX only)

| Action | Params | Description |
|--------|--------|-------------|
| `set_media_source` | `{ "media_source": "<source>" }` | Select media source |

**Source values**: `local`, `bluetooth`, `aux`, `usb`, `network`, `optical`, `hdmi`

## Read-only Capabilities (sensors)

These capabilities produce status properties but have no controllable actions:

| Capability | Property | Type | Unit | Range |
|------------|----------|------|------|-------|
| `temperature` | `temperature` | float | °C | -50 to 100 |
| `humidity` | `humidity` | float | % | 0 to 100 |
| `illuminance` | `illuminance` | float | lux | 0 to 100000 |
| `co2` | `co2` | float | ppm | 0 to 10000 |
| `co` | `co` | float | ppm | 0 to 10000 |
| `pm25` | `pm25` | float | µg/m³ | 0 to 1000 |
| `pm10` | `pm10` | float | µg/m³ | 0 to 1000 |
| `tvoc` | `tvoc` | float | — | 0 to 1000 |
| `air_quality` | `air_quality` | float | — | 0 to 1000 |
| `motion` | `motion` | bool | — | — |
| `presence` | `presence` | bool | — | — |
| `smoke` | `smoke` | bool | — | — |
| `leak` | `leak` | bool | — | — |
| `contact` | `contact` | bool | — | — |
| `battery` | `battery` (int), `low_battery` (bool) | int/bool | % | 0–100 |
| `running` | `running` | bool | — | — |
| `filter` | `filter` | int | % | 0–100 |

## Device Response Format

Each device in the API response looks like:

```json
{
  "id": "42",
  "uuid": "a1b2c3d4-...",
  "name": "Living Room Light",
  "type": "light",
  "sub_type": "light_dimmer",
  "protocol": "knx",
  "instance_name": "knx-main",
  "room_id": "3",
  "status": {
    "power": true,
    "brightness": 75
  },
  "is_online": true,
  "capabilities": ["on_off", "brightness"],
  "supported_actions": ["turn_on", "turn_off", "toggle", "set_brightness"],
  "properties": { ... },
  "config": { ... }
}
```

- `capabilities`: capability names (e.g. `["playback", "volume"]`)
- `supported_actions`: the actual actions this device supports — use this to determine which controls to show. Actions may vary even within the same device type depending on the underlying protocol and hardware.

Use `uuid` for automation trigger/node device references.
Use numeric `id` for the control API endpoint path.
