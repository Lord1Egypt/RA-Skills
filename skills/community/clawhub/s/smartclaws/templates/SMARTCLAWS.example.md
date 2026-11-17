# SMARTCLAWS.md — deployment facts (example)

Copy this to your workspace root as `SMARTCLAWS.md`. This file is **off-chain
wiring**: job, which device skill to load, labels, local command policy, bridge
hardware, and the owner's **goal** (what this agent is trying to achieve).
**Never put private keys or secrets here.**

The chain is source of truth for addresses, channels, encrypted kind, and
roles. Join on registered **`name`**. Look those up with the plugin
(`smartclaws_list_local`, `smartclaws_discover`). Optional `address` / channel
fields below are hints only — if they disagree with the plugin, **trust the
plugin**.

Plugin calls: pass device `name` (not the YAML map key) or a channel `0x`
address; pass agent `id` or `address`, not display `name`.

`role` is the job: `user-proxy` | `group-master` | `device-master` | `device-bridge`.

`goal` is the owner's standing purpose — not a job name, not a device list.
Write it in the owner's words during setup. Honor it on every cycle. When the
owner changes how this agent should operate, update `goal` here (confirm first;
do not invent a mission). Session authority still lives in `AGENTS.md`.

```yaml
# user-proxy | group-master | device-master | device-bridge
role: group-master

# Optional: defaults to SMARTCLAWS_HOME or ~/.smartclaws.
smartclawsHome: ~/.smartclaws

# Optional hint. Prefer plugin lookup by registered name.
# group:
#   name: home
#   # address: 0x...

# Owner-stated purpose. Free-form. Required for anyone who decides or acts
# unsupervised; still ask for every job. Blank means "no standing mission" —
# ask before acting autonomously; do not invent one.
goal: |
  Keep the living room comfortable while saving energy. Prefer cheaper tariff
  windows when comfort can still be met; in expensive windows keep the load
  off if the room will stay in band. Act ahead of the trend so limits are not
  crossed while waiting for the next cycle.

# Omit this whole block for a user proxy (no agent contract).
agent:
  # Plugin `agent` targets: use `id` or `address`, not display `name`.
  id: main
  name: Home Controller          # display only
  # address: 0x...               # optional hint; prefer plugin lookup by id/name
  encrypted: false               # must match registration; kind is for life
  # outgoingChannel / incomingChannel: optional hints; prefer plugin

# Agents you may notify. Needs SENDER_ROLE on-chain. Omit if none.
notifiable:
  worker-1:
    id: worker-1                 # registered agent id (plugin lookup)
    name: Air-Quality Worker     # display only

# Map keys are labels. Plugin `device` parameter = `name` below.
devices:
  shelly-plug:
    skill: smartclaws-device-shelly-plug-s-gen3
    name: shelly-plug-s          # registered on-chain name — the join key
    label: Living Room Plug
    encrypted: false             # must match registration; kind is for life
    authority: commandable       # local policy: commandable | telemetry-only
                                 # (on-chain `master` is separate; you need both to command)
    # outgoingChannel / incomingChannel: optional hints

  novapm:
    skill: smartclaws-device-novapm-sds011
    name: novapm-sds011-1
    label: Air Quality Sensor
    encrypted: false
    authority: telemetry-only    # do not command; incoming is unused

  thermal-sensor-1:
    skill: smartclaws-device-thermal-room-sensor
    name: thermal-sensor-1
    label: Room Temperature
    encrypted: false
    authority: telemetry-only
```

## Bridge variant

A bridge owns **one** device. Use this shape when `role: device-bridge`.

`bridge.mode`:

- `telemetry-only` — publish readings. Do not apply commands.
- `chain-commanded` — also apply commands from the device incoming channel.
- `operator-assisted` — that, plus commands from a human allowed by `AGENTS.md`.

Missing or unclear → fail closed to `telemetry-only`.

```yaml
role: device-bridge

smartclawsHome: ~/.smartclaws

# telemetry-only | chain-commanded | operator-assisted
bridge:
  mode: telemetry-only
  device: novapm           # YAML key of the one device below
  stateFile: state.json    # last-handled command offset, etc.

goal: |
  Publish accurate readings from this device on a steady cadence. Never invent
  data. Do not apply commands (telemetry-only). Flag implausible readings
  instead of publishing them.

agent:
  id: bridge-1
  name: Sensor Bridge      # display only
  encrypted: false

devices:
  novapm:
    skill: smartclaws-device-novapm-sds011
    name: novapm-sds011-1  # registered name — plugin join key
    label: Air Quality Sensor
    encrypted: false
    authority: telemetry-only
    local:                 # hardware/API; device-skill specific
      sensorPort: /dev/ttyUSB0
      warmupSeconds: 30
```

## Notes

- `encrypted` must match how the device/agent was registered. Kind cannot
  change; a new entity is required.
- `authority: telemetry-only` is local policy (this agent must not command).
  `commandable` still requires on-chain device `master` for the wallet.
- User proxy: `role: user-proxy`, no `agent` block, attach names the wallet
  already belongs to. `goal` is still worth writing (e.g. "only act when
  asked; summarize status").
- `goal` is the mission. Numeric knobs (comfort band, cooldowns) and extra
  standing instructions may live in `AGENTS.md` guidelines — they must not
  contradict `goal`. If they disagree, stop and ask.
- Extra local sources the goal needs (for example a `tariff:` block from
  `smartclaws-tariff-file-source`) are added when that skill is installed —
  not invented here.
- A name you cannot resolve with the plugin is a setup gap — stop and ask.
- Session authority (who may make you act or change `goal`) lives in
  `AGENTS.md`, not here.
