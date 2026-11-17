---
name: smartclaws-device-novapm-sds011
description: >
  Device contract for a NovaPM/SDS011 air-quality bridge. Defines SmartClaws
  telemetry topics, payloads, local serial behavior, and safety rules.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "📡"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      config: ["plugins.entries.smartclaws"]
---

# NovaPM SDS011 Device Contract

This is a device contract skill. It does not install SmartClaws or define an
agent role. Use it with `smartclaws-bridge-agent` for publishing telemetry and
with `smartclaws-master-agent` for reading/auditing air-quality data.

## Device Identity

- Device family: NovaPM using the SDS011 particulate matter sensor.
- Capability: read PM2.5 and PM10 concentrations.
- Local protocol: SDS011 serial protocol over USB serial.
- Default port in existing setups: `/dev/ttyUSB0`.
- Default warmup in existing setups: `30` seconds; never below `15` seconds.
- Actuation: none. This is telemetry-only hardware.

## SmartClaws Channels

The setup must provide channel addresses in `SMARTCLAWS.md`.

- Outgoing telemetry channel: required.
- Incoming command channel: must be null/absent. SDS011 receives no SmartClaws commands.

Do not invent channel addresses.

## Telemetry Topic

Topic: `telemetry.air_quality`

Payload:

```json
{
  "pm25_ug_m3": 12.3,
  "pm10_ug_m3": 28.1,
  "sensor": "sds011",
  "port": "/dev/ttyUSB0",
  "ts": "<current ISO 8601 UTC>"
}
```

Fields:

- `pm25_ug_m3`: PM2.5 concentration in micrograms per cubic meter.
- `pm10_ug_m3`: PM10 concentration in micrograms per cubic meter.
- `sensor`: should be `sds011` for this contract.
- `port`: serial port used for the reading.
- `ts`: ISO 8601 UTC timestamp for the reading.

## Command Topics

None. This device is read-only.

If a setup provides an incoming channel or command topic for this device, treat
it as a setup error unless an operator explicitly changes the device contract.

## Bridge-Agent Use

A bridge should:

1. Wake the sensor.
2. Wait the configured warmup duration.
3. Read one valid measurement frame.
4. Put the sensor back to sleep.
5. Validate the values.
6. Publish `telemetry.air_quality` to the outgoing channel with `smartclaws_publish`.
7. Log failures instead of publishing bad data.

The bridge should preserve sensor life. Avoid unnecessarily short polling
intervals; existing setup guidance used a 5-minute cadence with a 30-second
warmup.

## Master-Agent Use

A master may:

- Read `telemetry.air_quality` from the outgoing channel.
- Answer air-quality/status questions.
- Use readings as context for broader decisions.
- Log threshold or stale-data decisions to its own decision channel.

A master must not publish commands to this device.

## Sanity Rules

Reject a reading and publish no telemetry when:

- `pm25_ug_m3 < 0` or `pm25_ug_m3 > 1000`.
- `pm10_ug_m3 < 0` or `pm10_ug_m3 > 1000`.
- `pm25_ug_m3 > pm10_ug_m3`, which is physically inconsistent for this sensor.
- The sensor returns no valid frame after warmup.

Do not repair, smooth, or invent readings. Bad data is worse than no data.

## Human Interpretation

When reporting readings to a person, include raw values and a plain label.

The bands and thresholds below are **non-authoritative display reference** (drawn
from common EU/EPA/WHO levels) — they help you label a reading, not decide policy.
**Actual alert thresholds and what to do about them are the owner's call** and
belong in `AGENTS.md`, not this device contract. Reference only:

- PM2.5 high (EU/EPA alert ≈ `35` µg/m³; WHO 24h guideline is `15`).
- PM10 high (EU/EPA alert ≈ `50` µg/m³; WHO 24h guideline is `45`).

Useful context labels:

- Good: PM2.5 `0-5`, PM10 `0-20`.
- Moderate: PM2.5 `5-15`, PM10 `20-45`.
- Elevated: PM2.5 `15-35`, PM10 `45-50`.
- High: PM2.5 `>35`, PM10 `>50`.

Always check the timestamp. If the latest reading is older than the expected
publish cadence, say the data may be stale.
