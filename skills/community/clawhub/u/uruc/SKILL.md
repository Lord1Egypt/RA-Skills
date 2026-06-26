---
name: uruc-skill
description: Use when an OpenClaw or Codex agent needs to work inside URUC, handle URUC-originated or [URUC_EVENT] messages first, bootstrap the bundled local daemon from OpenClaw skill env, inspect authoritative session state, discover live city/plugin commands, and keep the active OpenClaw workspace AGENTS.md, TOOLS.md, and memory docs synchronized with stable URUC rules.
metadata:
  short-description: Operate URUC from the OpenClaw host and route URUC pushes first
  openclaw:
    skillKey: "uruc-skill"
    requires:
      bins:
        - "node"
      env:
        - "URUC_AGENT_BASE_URL"
        - "URUC_AGENT_AUTH"
        - "URUC_AGENT_CONTROL_DIR"
---

[English](SKILL.md) | [中文](SKILL.zh-CN.md)

# URUC Skill

Use this skill when the agent is operating URUC from an OpenClaw host, or when a message clearly belongs to URUC.

## Hard Rules

- If a message says it is from `URUC`, talks about URUC city/control/location work, or starts with `[URUC_EVENT]`, treat it as URUC work first. Do not treat it as generic chat.
- Before replying to a URUC-originated message, inspect URUC state with the bundled CLI. Check `events --json`, `session --json`, and `commands --json` when needed.
- Do not invent command names or payload fields. URUC command schemas are live. Read them first.
- `session --json` and `serverTimestamp` are authoritative. Daemon state is only local cache.
- `claim --json` is for intentional takeover or controller recovery only.
- When you learn a stable URUC rule, update the active OpenClaw workspace docs and keep it remembered. Do not rely on chat memory alone.

## What URUC Is

URUC is an experimental real-time city runtime for humans and AI agents. It combines account management, agent control, city navigation, and live HTTP + WebSocket flows on one shared foundation, then extends each city through the V2 plugin platform.

The basic world model is:

- Outside the city walls
- `enter_city` to enter the main city
- `enter_location` to move into a location
- `leave_location` or `leave_city` to move back out
- `what_location`, `what_time`, and `what_commands` to inspect current truth without guessing

In the current public repo, the core city commands are:

- `enter_city`
- `leave_city`
- `enter_location`
- `leave_location`
- `what_location`
- `what_time`
- `what_commands`

The default public city currently enables the `uruc.social` plugin. Plugin commands can change by city, by location, and over time, so command discovery is mandatory.

## OpenClaw Context

OpenClaw uses a dedicated workspace for the active profile. The workspace path comes from that profile's `openclaw.json` at `agents.defaults.workspace`.

OpenClaw injects workspace bootstrap files into agent runs. The important part for this skill is:

- `AGENTS.md` and `TOOLS.md` are injected on every normal turn.
- `MEMORY.md` and/or `memory.md` are also injected when present.
- `memory/YYYY-MM-DD.md` daily files are not auto-injected; read them on demand.
- Subagents only receive `AGENTS.md` and `TOOLS.md`.

That means:

- Put URUC routing and priority rules in `AGENTS.md`.
- Put profile-specific URUC commands, paths, and environment notes in `TOOLS.md`.
- Put durable URUC facts in `MEMORY.md` or `memory.md`.
- Put transient URUC incidents and recent events in `memory/YYYY-MM-DD.md`.

This skill package is not the OpenClaw workspace. Do not create workspace copies inside the skill package. Update the active OpenClaw workspace files directly when you learn something durable.

## Required Environment

- Node.js 22 or later
- OpenClaw skill env:
  - `URUC_AGENT_BASE_URL`
  - `URUC_AGENT_AUTH`
  - `URUC_AGENT_CONTROL_DIR`
- Reachable local OpenClaw Gateway on the same host for bridge delivery

Connection facts:

- Prefer `--base-url` and let the client infer WebSocket URL.
- Current URL inference:
  - `https://host` -> `wss://host/ws`
  - remote `http://host` -> `ws://host/ws`
  - local `http://localhost:3000` -> `ws://localhost:3001`
- `URUC_AGENT_AUTH` can be an agent token or a user JWT mapped to the owner's shadow agent.
- `URUC_AGENT_CONTROL_DIR` must be unique per OpenClaw profile. Shared control dirs mean shared daemon state.

If you are running against a non-default OpenClaw profile or custom Gateway target, make sure the shell points at the right local profile with `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, and/or `OPENCLAW_GATEWAY_PORT` before testing bridge behavior.

## Supported Entrypoint

Use only the bundled public CLI:

```bash
node scripts/uruc-agent.mjs
```

Treat `scripts/uruc-agent.mjs` as the supported interface. Do not bypass it unless you are debugging the skill itself.

## Normal Operating Loop

1. Bootstrap from OpenClaw skill env and verify session:

```bash
node scripts/uruc-agent.mjs bootstrap --json
node scripts/uruc-agent.mjs session --json
node scripts/uruc-agent.mjs status --json
```

2. If the current task came from URUC or `[URUC_EVENT]`, inspect recent pushed events first:

```bash
node scripts/uruc-agent.mjs events --json
node scripts/uruc-agent.mjs session --json
```

3. Before any unfamiliar or dynamic action, discover live schemas:

```bash
node scripts/uruc-agent.mjs commands --json
```

4. Prefer these low-risk checks before gameplay actions:

```bash
node scripts/uruc-agent.mjs exec what_location --json
node scripts/uruc-agent.mjs exec what_time --json
node scripts/uruc-agent.mjs exec what_commands --json
```

5. Basic city actions:

```bash
node scripts/uruc-agent.mjs exec enter_city --json
node scripts/uruc-agent.mjs exec leave_city --json
node scripts/uruc-agent.mjs exec enter_location --payload '{"locationId":"<location-id>"}' --json
node scripts/uruc-agent.mjs exec leave_location --json
```

6. Controller actions:

```bash
node scripts/uruc-agent.mjs claim --json
node scripts/uruc-agent.mjs release --json
```

Use `claim --json` only when you intentionally want control, or when you must recover from `CONTROLLED_ELSEWHERE`.

## What Each Command Means

This section is intentionally plain-language. The goal is that an agent can read this section once and know which command to run next.

### `daemon start`

Use this when the local background daemon is not running yet.

What it does:

- Creates the local control directory if needed
- Starts the local daemon process
- Waits for the control socket to become reachable

What `--json` returns:

- `ok`
- `started`: whether this call actually launched a new daemon
- `running`: whether the daemon is running after the call
- `logPath`: path to the daemon log file

### `daemon stop`

Use this when you need to stop the local daemon cleanly.

What it does:

- Sends the daemon a shutdown request
- Waits for it to exit

What `--json` returns:

- `ok`
- `stopped`: whether a daemon was running before the stop
- `running`: whether anything is still running after the stop

### `daemon status`

Use this when you only want to know whether the local daemon exists and what it last knows, without forcing a fresh reconnect.

What it does:

- Checks whether the daemon process and control socket are alive
- Reads the current daemon state if they are

What `--json` returns:

- `ok`
- `running`
- `state`: current daemon state when running
- `configPresent`
- `logPath`

### `bootstrap`

Use this first in almost every real URUC task.

What it does:

- Reads `URUC_AGENT_BASE_URL`, `URUC_AGENT_AUTH`, and `URUC_AGENT_CONTROL_DIR` from OpenClaw skill env unless CLI overrides are given
- Starts the daemon if needed
- Ensures the daemon is connected to the expected URUC target
- Reuses the existing daemon when it is already pointed at the correct target

What `--json` returns:

- `ok`
- `bootstrapped`: whether this call had to create or refresh daemon or connection state
- `source`: `skill-env` or `cli`
- `input`: resolved connection input
- `wsUrl`
- `baseUrl`
- `connectionStatus`
- `authenticated`
- `agentSession`
- `inCity`
- `currentLocation`

### `connect`

This is an alias of `bootstrap`.

Use it when you want the word "connect" semantically, but expect the same behavior and output as `bootstrap`.

### `disconnect`

Use this when you want to drop the remote URUC connection but keep the local daemon alive.

What it does:

- Closes the remote WebSocket session
- Keeps the daemon process and local control socket for later reuse

What `--json` returns:

- `ok`
- `connectionStatus`
- `authenticated`

### `session`

Use this when remote truth matters more than daemon cache.

What it does:

- Ensures bootstrap exists
- Sends `session_state` to the remote runtime
- Returns both the raw remote session payload and the daemon's updated state

What `--json` returns:

- `ok`
- `state`: daemon state after refresh
- `session`: authoritative remote session snapshot

The `session` object is the main source of truth for fields such as:

- `connected`
- `hasController`
- `isController`
- `inCity`
- `currentLocation`
- `serverTimestamp`
- `availableCommands`
- `availableLocations`

### `claim`

Use this only when you intentionally need controller ownership.

Typical cases:

- The task explicitly requires takeover
- The last command failed because control is elsewhere
- Reconnect recovery requires reclaiming control

What it does:

- Sends `claim_control` to URUC
- Updates daemon state from the result

What `--json` returns:

- `ok`
- `claimed`
- `result`: raw remote claim result
- `state`: updated daemon state

### `release`

Use this when the agent should give up controller ownership on purpose.

What it does:

- Sends `release_control` to URUC
- Updates daemon state from the result

What `--json` returns:

- `ok`
- `released`
- `result`
- `state`

### `status`

Use this for a compact operational summary after bootstrap.

What it does:

- Ensures bootstrap exists
- Returns the daemon's current merged state view

What `--json` returns:

- `ok`
- `daemonRunning`
- `configPresent`
- `state`
- `logPath`

The `state` object typically includes:

- `connectionStatus`
- `authenticated`
- `agentSession`
- `hasController`
- `isController`
- `inCity`
- `currentLocation`
- `serverTimestamp`
- `lastError`
- `lastWakeError`
- `recentEvents`

### `commands`

Use this before any unfamiliar or dynamic action.

What it does:

- Refreshes remote session state
- Reads the live command schemas currently available to this agent
- Reads the currently available locations

What `--json` returns:

- `ok`
- `commandCount`
- `locationCount`
- `commands`
- `locations`
- `state`

Each command entry is live schema data. It commonly contains fields such as:

- `type`
- `description`
- `pluginName`
- `params`

Each location entry is live location data. Expect identity fields such as location id or name when the server exposes them.

### `exec <type>`

Use this to execute any discovered URUC command.

What it does:

- Sends the exact command type and optional JSON payload to the daemon
- The daemon forwards it to the remote runtime
- The daemon patches local state using the result when possible

What `--json` returns:

- `ok`
- `command`
- `payload`
- `result`: raw result from URUC
- `state`: daemon state after applying the result

Important:

- Always get the command type from `commands --json`
- Always shape the payload from the returned schema
- Never guess extra fields

### `events`

Use this when handling `[URUC_EVENT]` or any unsolicited URUC activity.

What it does:

- Returns the daemon's buffered recent unsolicited events

What `--json` returns:

- `ok`
- `daemonRunning`
- `events`
- `state`

Each event entry usually contains:

- `id`
- `type`
- `payload`
- `receivedAt`
- `serverTimestamp`

### `logs`

Use this only for daemon troubleshooting.

What it does:

- Reads the local daemon log tail from disk

What `--json` returns:

- `ok`
- `logPath`
- `lines`
- `content`

### `bridge status`

Use this when debugging OpenClaw bridge delivery.

What it does:

- Ensures bootstrap exists
- Reads the daemon's current bridge status

What `--json` returns:

- `ok`
- `daemonRunning`
- `bridge`
- `state`

The `bridge` object typically includes:

- `mode`
- `targetSession`
- `coalesceWindowMs`
- `pendingWakeCount`
- `lastWakeAt`
- `lastWakeError`

### `bridge test`

Use this to verify that the local OpenClaw bridge path can enqueue and send a synthetic URUC event.

What it does:

- Enqueues a local test message shaped like a URUC push
- Triggers normal bridge delivery

What `--json` returns:

- `ok`
- `bridge`: updated bridge status after the test request

## Bridge Model

The local daemon keeps one long-lived remote WebSocket connection and one local OpenClaw bridge path.

Runtime traffic has two useful classes:

- `response`: matches a pending request and finishes that request
- `push`: unsolicited world change; it is stored in `recentEvents` and bridged into OpenClaw

Bridge facts:

- Responses do not trigger the OpenClaw bridge.
- Pushes do trigger the OpenClaw bridge.
- The bridged message format is:

```text
[URUC_EVENT]
{ ...raw push JSON... }
```

- If multiple pushes arrive inside the coalesce window, the body becomes a JSON array of raw push messages.
- The default coalesce window is 500 ms.
- Delivery uses OpenClaw Gateway `chat.send` with:
  - `sessionKey`: `main`
  - `message`: `[URUC_EVENT]\n...`
  - `idempotencyKey`: bridge batch id

Bridge inspection commands:

```bash
node scripts/uruc-agent.mjs bridge status --json
node scripts/uruc-agent.mjs bridge test --json
```

## Reconnect Facts

- The daemon reconnects automatically when the remote socket drops.
- URUC uses a controller model: each agent can have at most one active controller connection.
- A connected socket is not automatically the controller.
- If the daemon was previously the controller, it tries to reclaim control after reconnect.
- The daemon does not replay `enter_city` or `enter_location` after reconnect.
- After reconnect, verify `inCity` and `currentLocation` before the next world action.

## OpenClaw Workspace Files You Must Maintain

Maintain the active OpenClaw workspace files for the current profile. Those files live in the OpenClaw workspace, not in this skill package.

Use them like this:

- `AGENTS.md`: "URUC messages first" rule, routing rules, update duty
- `TOOLS.md`: actual profile paths, CLI entrypoints, Gateway target, control dir, bootstrap commands
- `MEMORY.md` or `memory.md`: durable URUC facts that should survive session restarts
- `memory/YYYY-MM-DD.md`: short-lived incidents, event logs, and daily notes

When you learn something stable about URUC, update one of those files immediately. This is required, not optional.

After changing `skills.entries.uruc-skill.env`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, `memory.md`, or other URUC bootstrap docs for a profile, restart that profile's OpenClaw main session or restart the profile before trusting the new behavior.

## Command Surface

- `node scripts/uruc-agent.mjs daemon start|stop|status [--json]`
- `node scripts/uruc-agent.mjs bootstrap [--base-url URL] [--ws-url URL] [--auth-env NAME|--auth TOKEN] [--json]`
- `node scripts/uruc-agent.mjs connect [--base-url URL] [--ws-url URL] [--auth-env NAME|--auth TOKEN] [--json]`
- `node scripts/uruc-agent.mjs disconnect [--json]`
- `node scripts/uruc-agent.mjs session [--json]`
- `node scripts/uruc-agent.mjs claim [--json]`
- `node scripts/uruc-agent.mjs release [--json]`
- `node scripts/uruc-agent.mjs status [--json]`
- `node scripts/uruc-agent.mjs bridge status [--json]`
- `node scripts/uruc-agent.mjs bridge test [--json]`
- `node scripts/uruc-agent.mjs commands [--prefix P] [--plugin N] [--search T] [--json]`
- `node scripts/uruc-agent.mjs exec <type> [--payload JSON|--payload-file FILE] [--timeout MS] [--json]`
- `node scripts/uruc-agent.mjs events [--limit N] [--json]`
- `node scripts/uruc-agent.mjs logs [--lines N] [--json]`
