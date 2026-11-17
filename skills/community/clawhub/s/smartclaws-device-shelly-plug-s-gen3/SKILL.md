---
name: smartclaws-device-shelly-plug-s-gen3
description: >
  Device contract for Shelly Plug S Gen3. Defines SmartClaws topics, payloads,
  local Shelly RPC methods, and safety rules for bridge and master agents.
license: LGPL-3.0-or-later
metadata:
  openclaw:
    emoji: "🔌"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      config: ["plugins.entries.smartclaws"]
---

# Shelly Plug S Gen3 Device Contract

This is a device contract skill. It does not install SmartClaws, register a
device, or define an agent role. Use it with `smartclaws-master-agent` or
`smartclaws-bridge-agent`.

## Device Identity

- Vendor: Shelly
- Device: Shelly Plug S Gen3, Type F variant
- Capability: one relay switch channel with built-in power metering
- Local protocol: Shelly Gen2+/Gen3 JSON-RPC over HTTP
- Controllable component: `switch:0`

## SmartClaws Channels

The setup must provide channel addresses in `SMARTCLAWS.md`.

- Outgoing telemetry channel: required.
- Incoming command channel: required only for commandable setups.

Do not invent channel addresses. If a channel is missing, ask for setup.

## Telemetry Topic

Topic: `telemetry.switch_status`

Normalized payload:

```json
{
  "output": true,
  "apower_w": 852.3,
  "voltage_v": 230.1,
  "current_a": 3.7,
  "energy_total": 142.4,
  "temperature_c": 41.5
}
```

Fields:

- `output`: relay state, `true` = ON, `false` = OFF.
- `apower_w`: active power in watts.
- `voltage_v`: mains voltage.
- `current_a`: current draw in amps.
- `energy_total`: cumulative energy value reported by Shelly.
- `temperature_c`: plug internal temperature in Celsius; not room temperature.

Shelly RPC source mapping:

- `output` <- `Switch.GetStatus?id=0.output`
- `apower_w` <- `apower`
- `voltage_v` <- `voltage`
- `current_a` <- `current`
- `energy_total` <- `aenergy.total`
- `temperature_c` <- `temperature.tC`

## Command Topic

Topic: `command.switch.set`

Payload:

```json
{
  "on": true,
  "toggle_after": 0
}
```

Validation:

- `on` is required boolean.
- `toggle_after` is optional non-negative integer seconds.
- `toggle_after: 0` means no auto-revert.
- Reject strings, floats, negative values, null, and unknown command topics.

Effect:

- `on: true` maps to relay ON.
- `on: false` maps to relay OFF.

## Local RPC Methods

Read device info:

```text
GET /rpc/Shelly.GetDeviceInfo
```

Read relay/power state:

```text
GET /rpc/Switch.GetStatus?id=0
```

Set relay state:

```text
GET /rpc/Switch.Set?id=0&on=true
GET /rpc/Switch.Set?id=0&on=false
```

If authentication is enabled, the bridge setup must provide the credential path
or mechanism. Do not print credentials.

## Master-Agent Use

A master may:

- Read `telemetry.switch_status` from the outgoing channel.
- Decide whether a command is needed.
- Publish `command.switch.set` only when setup authority allows it. With the
  SmartClaws plugin, use `smartclaws_publish` with the registered device `name`
  and `deviceChannel: "command"` so the write goes through
  `SmartClawsDevice.publishCommand`.

A master must not:

- Call Shelly RPC directly.
- Treat plug internal temperature as room temperature.
- Re-send commands repeatedly without checking recent telemetry/decision state.

## Bridge-Agent Use

A bridge may:

- Read Shelly RPC status and publish `telemetry.switch_status`.
- In command-enabled modes, read `command.switch.set` from the incoming channel and call `Switch.Set`.
- Persist the last handled command offset in its setup state file.

A bridge must not:

- Execute unknown command topics.
- Reprocess already-handled command offsets.
- Publish fake telemetry unless explicitly running a labelled simulation.

## Sanity Rules

- `output` must be boolean.
- Power, voltage, current, energy, and temperature must be numeric when present.
- Missing optional numeric fields may be omitted; do not invent values.
- If Shelly is unreachable, publish no telemetry for that cycle and log/fail loud.

## References

- Shelly Plug S Gen3 docs: https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen3/ShellyPlugSG3
- Shelly Switch component RPC: https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch/
- Shelly RPC protocol: https://shelly-api-docs.shelly.cloud/gen2/General/RPCProtocol
