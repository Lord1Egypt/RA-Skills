---
name: riverdesk
description: "Connect OpenClaw to the RiverDesk task app: install the openclaw-riverdesk channel plugin, pair with a one-time code from web.riverdesk.ai, and verify the agent is online."
---

# RiverDesk

[RiverDesk](https://riverdesk.ai) is a task/chat app that talks to OpenClaw
agents over an end-to-end-encrypted, dial-out WebSocket. The
`openclaw-riverdesk` channel plugin runs inside the OpenClaw gateway — no
inbound ports, no standalone daemon.

Use this skill when the user asks to connect their agent to RiverDesk, pair a
RiverDesk pairing code, or debug a RiverDesk channel that is offline.

## Install the plugin

```bash
openclaw plugins install openclaw-riverdesk
```

## Pair (one-time code flow)

1. Ask the user to sign in at https://web.riverdesk.ai and generate a pairing
   code from their agent's settings. Codes are single-use and expire after
   ~10 minutes — get the code right before configuring.
2. Merge the channel config into the gateway config
   (`~/.openclaw/openclaw.json`). Never overwrite existing channels; add only
   the `channels.riverdesk` block:

   ```json
   {
     "channels": {
       "riverdesk": {
         "serverUrl": "wss://api.riverdesk.ai/plugin",
         "pairingCode": "<one-time code>",
         "agents": ["youragent"],
         "agentMap": { "youragent": "main" }
       }
     }
   }
   ```

   - `agents`: RiverDesk agent id(s) served by this gateway.
   - `agentMap`: RiverDesk agent id → local gateway agent id (usually `main`).
3. Restart the gateway: `openclaw gateway restart`.

On first boot the plugin mints an E2EE keypair
(`~/.riverdesk/plugin-keypair.json`), exchanges the pairing code for a
persistent token stored in a state file next to the keypair, and reconnects
automatically from then on. The pairing code becomes inert after use and may
be removed from the config.

## Verify

```bash
curl -s https://api.riverdesk.ai/health
```

`agentsOnline` should show the agent as `true`. Also confirm in gateway logs:
look for `[rd-channel]` hello-ok lines. Finally, have the user send the agent
a message from the RiverDesk app.

## Troubleshoot

- **Pairing failed**: code expired (10 min TTL) or already used — generate a
  fresh one and restart the gateway.
- **Was online, now offline**: token persists in the state file; check
  outbound reachability to `api.riverdesk.ai:443` and gateway logs.
- **Reset pairing**: delete
  `~/.riverdesk/plugin-keypair.json.rd-state.json`, set a fresh
  `pairingCode`, restart.
- **Migrating from a standalone connector**: stop the old connector process
  after the plugin connects (two clients per agent fight over the
  connection). Reuse the old keypair via `keyFile` to keep the E2EE identity.

## Conduct

- Treat `pairingCode`, `pluginToken`, keypair, and state files as secrets:
  never print, log, or transmit them.
- Back up the gateway config before editing; merge, never replace.
- Do not restart the gateway while the user has critical sessions running
  without warning them first.
