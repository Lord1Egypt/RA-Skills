# workled MCP Device Setup

This document describes how to connect a workled device so that the workled
skill can control the LED indicator and touch-pad macros, and how to install
the client hooks/plugins that drive `set_agent_state` automatically.

## Prerequisites

- A workled device, powered on.
- Node.js 18+ (for the opencode plugin that communicates with the device).

## First use: connect the device to Wi-Fi

A fresh device broadcasts its own hotspot. Connect your computer to that hotspot:

- A captive portal should open automatically; if not, open `http://192.168.4.1/`
  in a browser.
- Set your home Wi-Fi and enter its password to complete provisioning.
- The device then connects to your home Wi-Fi automatically.

## Device Home page

Open the device's web page in a browser (device status / provisioning):

```
http://<device-name>.local
```

- `<device-name>` is the name configured when connecting the device (e.g.
  `HomeAnt-1234`); it varies per device.
- On the same LAN you can also use the device's IP address directly (e.g.
  `http://192.168.31.146`).

## MCP endpoint

Once the device is on the same network, its MCP endpoint is:

```
http://<device-name>.local:18791/mcp
```

Add the server to your agent config. For opencode, edit `~/.config/opencode/opencode.json`:

```jsonc
{
  "mcp": {
    "workled": {
      "type": "remote",
      "url": "http://<device-name>.local:18791/mcp",
      "enabled": true
    }
  }
}
```

## Bluetooth pairing (required for macro)

The device appears as a BLE HID keyboard. Its name starts with `HomeAnt` or `workled`. Pair it with your computer:

- **Windows**: Settings → Bluetooth & devices → Add device → Bluetooth → select the device whose name starts with `HomeAnt` or `workled`.
- **macOS**: System Settings → Bluetooth → select the device whose name starts with `HomeAnt` or `workled`.
- **Linux**: `bluetoothctl` → `scan on` → look for a device whose name starts with `HomeAnt` or `workled` → `pair <device-name>` → `trust <device-name>` → `connect <device-name>`.

After pairing, the device stays connected while in range. If it disconnects, re-pair or trigger reconnection.

## Installation & Uninstallation

### Install the skill

Install it **through your agent**. Ask the agent
to clone the repository into the skills directory your client scans, then run
the client installer:

```text
git clone https://github.com/git-hub-cloud/workled.git ~/.agents/skills/workled
node ~/.agents/skills/workled/skill-install.mjs install --client <name>
```

- Keep it up to date: `git -C ~/.agents/skills/workled pull`.
- The skill manifest and the state protocol live in
  [SKILL.md](https://github.com/git-hub-cloud/workled/blob/main/SKILL.md).

### Client integration

Every target path is derived from `homedir()`, never from cwd, so
the same command runs from any directory on any shell. Both `install` and
`uninstall` take an **optional** `--client <name>` (opencode, kilo, openclaw,
trae-cn, hermes, dsh, pi, workbuddy): omit it to **auto-detect** the running
client; pass it explicitly when several clients are installed (ambiguous) or to
target a *different* client (e.g. from an opencode chat, "install workled in
kilocode" → `--client kilocode`).
`index.js status` accepts the same optional `--client <name>` filter; default
is **all clients**.

```
node <skill-dir>/skill-install.mjs install|uninstall [--client <name>]
node <skill-dir>/skill-install.mjs --help
node <skill-dir>/index.js status [--client <name>]    # filter optional; default all
```

Examples:

```
node <skill-dir>/skill-install.mjs install --client opencode
node <skill-dir>/skill-install.mjs uninstall --client opencode
node <skill-dir>/index.js status --client opencode
```

What every client's install flow does:

1. **Client-level hook / plugin / entry** — covers the Enter → first-output gap (the window the agent cannot reach): calls `set_agent_state("thinking")` when the user submits a message.
2. **MCP entry** — registers the `workled` server in the client's MCP config (opencode/kilo/openclaw/trae-cn/pi/workbuddy register it; hermes uses a YAML block).
3. **Uninstall** — removes the hook/entry and the MCP entry. Everything else in the config files is preserved verbatim.

After installing, run `node <skill-dir>/index.js status` and surface the JSON
`hint` to the user. A `hint` of "No `workled` server configured" means the
client's MCP is not set up — guide the user through the MCP endpoint
above.

> **Prevent / detect a placeholder URL.** `install` resolves the MCP URL once:
> `WORKLED_MCP_URL` → placeholder `http://<device-name>.local:18791/mcp`. If no
> real URL is known and the
> target config has **no existing `workled` entry** (e.g. after an earlier
> uninstall), the placeholder is written. Fix it by editing the config URL to
> the real device name/IP, or re-run install with
> `WORKLED_MCP_URL=http://<device-name>.local:18791/mcp` set. A config that
> already holds a real URL is never downgraded to the placeholder.

## Verify

After the device is reachable and the opencode plugin is loaded, trigger an LED
state change:

```
set_brightness(128)
```

The LED should respond. If it does not, see Troubleshooting below.

## Troubleshooting

Run the diagnostic command first when the LED does not respond; it prints a
single JSON object describing the first `workled` MCP server found and its
reachability. Exit code is 0 when a workled config exists and is reachable,
1 otherwise:

```
node <skill-dir>/index.js status
```

The command scans the MCP config of every client (opencode,
trae-cn, openclaw, pi, workbuddy, hermes, dsh) and lists every server named
`workled`, checking each reachability with a **stateless** `tools/call get_agent_state`
probe. Fields:

- `bluetooth` — `{ available, powered, devicePaired, deviceNames, error? }`; BLE pairing
  matters for the touch-pad macros (the LED + macro only need Wi-Fi)
- `WORKLED_MCP_URL` — present only when the env var is set
- `clients` — one entry per discovered MCP config. Every functional client
  requires an MCP server (that is how the agent calls the device), so only
  MCP-configured clients appear here; the `WORKLED_MCP_URL` override never
  appears as an entry. Fields per entry:
  - `client` — the client id
  - `mcpPath` — path of the MCP config file that declares the server
  - `mcpUrl` — the configured workled server URL
  - `mcpEnable` — whether the server is enabled (absent `enabled` ⇒ `true`)
  - `mcpUrlReachable` — whether the URL answered a stateless `get_agent_state` probe
  - `mcpConfig` — `true` whenever this client has a workled row in its MCP
    config; the entry is here precisely because it does, so this is equivalent
    to "is this client MCP-configured". Used to gate the `configured but
    disabled` / `no url` diagnostics below
  - `plugin` — the actual installed plugin/hooks artifact path for that client
    (generated entry file, or the config/hooks file carrying the workled
    marker), or `null` when not installed
  - `skill` — the per-client skill directory where SKILL.md is installed
    (e.g. `~/.workbuddy/skills/workled`; openclaw uses
    `~/.openclaw/workspace/skills/workled` since its TUI installs there), or
    `null` when not installed for that client
- `hint` — a concrete next step for the current state
- `ok` / `exitCode` — success flag and process exit code

- **Device not on the network yet** — connect to the device hotspot first and
  complete Wi-Fi provisioning (see "First use" above). After provisioning the
  device joins your home Wi-Fi automatically.
- **Device unreachable** — make sure the device is powered on and that your
  computer is on the same Wi-Fi network as the device.
- **Device dropped off the network** — the device can go offline silently
  (power loss / Wi-Fi sleep). Recheck `index.js status`; if the URL does not
  resolve at all, power-cycle the device and confirm it rejoined the LAN.
- **workled configured but disabled** — `workled.enabled` is `false`; enable it
  in your agent config or set `WORKLED_MCP_URL`.
- **Device reachable but something looks off** — `index.js status` prints a `hint`; follow its ordered checklist (`LED → MCP → trust → hooks → DNS`):
  1. **LED** — brightness may be 0; run `set_brightness(128)`, or use the device's manual on/off switch.
  2. **MCP** — the config was just added/edited; **restart the agent or the session** so it reloads the new MCP server entry.
  3. **trust** — some agents require **manually trusting/allowing** the MCP connection before they will use it. Without approval the server is configured but never connected.
  4. **hooks** — some agents need to **manually enable lifecycle hooks** (e.g. `Settings → Hooks`) for the auto `set_agent_state` to fire.
  5. **DNS** — on Windows mDNS (`.local`) is unstable under load; in the MCP config prefer a **static IP** over the `.local` hostname to avoid intermittent `-32001` timeouts.
- **No MCP config found at all** — neither `WORKLED_MCP_URL` nor any config
  source declares the server. Add it under `mcp` in your agent config (see
  "MCP endpoint" above) or set the environment variable.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `WORKLED_MCP_URL` | | Override the MCP server URL directly. |
