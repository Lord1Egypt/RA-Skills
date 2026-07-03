# SMARTCLAWS.md — deployment facts (example)

Copy this to your workspace root as `SMARTCLAWS.md` and fill it in for *this*
deployment. The SmartClaws role skills read this file to learn which channels,
devices, and authority apply here. Keep it accurate. **Never put private keys or
secrets in this file** — only addresses, names, and roles.

```yaml
# Which role this agent plays. One of: master | bridge.
role: master

# SmartClaws HOME the plugin/CLI use (config + wallet live here).
# Optional: defaults to SMARTCLAWS_HOME or ~/.smartclaws.
smartclawsHome: ~/.smartclaws

# This agent's own on-chain identity (master/bridge agents). Omit for a plain
# controller with no agent contract.
agent:
  id: main
  name: Home Controller
  outgoingChannel: 0x...   # your decision/audit log (you write here, via publishOutbound)
  incomingChannel: 0x...   # your inbox: others notify you here if granted SENDER_ROLE

# Other agents you may notify (publish to their incoming channel). Requires the
# target's owner to have granted you SENDER_ROLE. Omit if you coordinate with none.
notifiable:
  worker-1:
    name: Air-Quality Worker
    incomingChannel: 0x...   # you write here via smartclaws_notify / `agent notify`

# Every device you read or command. Install the named device skill for each.
devices:
  shelly-plug:
    skill: smartclaws-device-shelly-plug-s-gen3
    label: Living Room Plug
    outgoingChannel: 0x...   # telemetry it publishes (you read)
    incomingChannel: 0x...   # commands to it (you write, if commandable)
    authority: commandable   # commandable | telemetry-only

  novapm:
    skill: smartclaws-device-novapm-sds011
    label: Air Quality Sensor
    outgoingChannel: 0x...
    incomingChannel: null    # telemetry-only hardware
    authority: telemetry-only
```

## Bridge variant

A bridge owns **one** device, declares a `mode`, and may need local hardware and
last-handled-offset/state fields. Use this shape instead when `role: bridge`:

```yaml
role: bridge

smartclawsHome: ~/.smartclaws

# How this bridge operates: telemetry-only | chain-commanded | operator-assisted.
# Missing/unclear → the bridge skill fails closed to telemetry-only.
bridge:
  mode: telemetry-only
  device: novapm           # the one device key below this bridge owns
  stateFile: state.json    # where you persist last-handled command offset, etc.

agent:
  outgoingChannel: 0x...   # optional bridge/cycle log

devices:
  novapm:
    skill: smartclaws-device-novapm-sds011
    label: Air Quality Sensor
    outgoingChannel: 0x...   # telemetry you publish
    incomingChannel: null    # commands you read (only in command-enabled modes)
    authority: telemetry-only
    local:                   # local hardware/API details for the bridge
      sensorPort: /dev/ttyUSB0
      warmupSeconds: 30
```

## Notes

- `authority: telemetry-only` means read but never command. `incomingChannel`
  must be null/absent for those devices.
- A device address or channel you can't find here is a setup gap — stop and ask,
  don't guess.
- Operating behaviour, permissions, and any control policy live in your
  owner-owned `AGENTS.md`, not here. This file is just the wiring.
