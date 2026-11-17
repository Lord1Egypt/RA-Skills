---
name: smartclaws-device-thermal-room-sensor
description: >
  Device contract for a telemetry-only room thermal sensor. Defines SmartClaws
  topics, payload fields, and master-agent interpretation rules.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "T"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      config: ["plugins.entries.smartclaws"]
---

# Thermal Room Sensor Device Contract

This is a device contract skill. It does not install SmartClaws, register a
device, publish telemetry, or define an agent role. Use it with
`smartclaws-master-agent`.

## Device Identity

- Device class: room thermal sensor
- Capability: temperature telemetry
- Authority: telemetry-only
- Command support: none

## SmartClaws Channels

The setup must provide channel addresses in `SMARTCLAWS.md`.

- Outgoing telemetry channel: required.
- Incoming command channel: not used by this contract.

Do not invent channel addresses. If a channel is missing, ask for setup.

## Telemetry Topic

Topic: `telemetry.thermal_status`

Normalized payload:

```json
{
  "temperature_c": 23.45,
  "ambient_c": 21.0,
  "relay_state": true,
  "stale_relay_seconds": 12.4,
  "stale_relay": false,
  "ts": "2026-07-01T11:12:13.000Z"
}
```

Fields:

- `temperature_c`: current room temperature in Celsius.
- `ambient_c`: configured ambient/resting temperature in Celsius, when provided.
- `relay_state`: related heating/relay state when known; `true` = ON,
  `false` = OFF, `null` = unknown.
- `stale_relay_seconds`: age of the related relay state in seconds, or `null`
  when unknown.
- `stale_relay`: `true` when the relay correlation is stale or unavailable.
- `ts`: producer timestamp in ISO-8601 format.

## Master-Agent Use

A master may:

- Read `telemetry.thermal_status` from the outgoing channel.
- Use `temperature_c` as the room temperature signal.
- Use `stale_relay` and `stale_relay_seconds` to decide whether relay
  correlation is trustworthy.
- Combine this telemetry with commandable devices listed in `SMARTCLAWS.md`.

A master must not:

- Publish commands to this device.
- Treat `ambient_c` as a measured current temperature.
- Treat `relay_state` as authoritative when `stale_relay` is true.
- Invent missing readings, timestamps, or relay correlation.

## Sanity Rules

- `temperature_c` must be numeric.
- `ambient_c` and `stale_relay_seconds` must be numeric when present and
  non-null.
- `relay_state` must be boolean or null when present.
- `stale_relay` must be boolean when present.
- `ts` should be a timestamp string when present.
- If recent telemetry is missing, report that no fresh thermal reading is
  available rather than guessing.
