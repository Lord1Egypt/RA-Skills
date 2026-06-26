# LDM OS v0.3.0

LDM OS evolves from an installer/boot system into a full agent operating system. Five new core features plus WIP Bridge absorbed as a core module.

## WIP Bridge Absorption

WIP Bridge (wip-bridge-private) is now a core module at `src/bridge/`. Bridge is always installed with LDM OS, not optional. The standalone wip-bridge-private repo is deprecated.

- Bridge source (core.ts, mcp-server.ts, cli.ts) lives in `src/bridge/`
- Built with tsup into `dist/bridge/`
- `lesa` CLI stays as alias in LDM OS bin
- All existing MCP tools preserved (`lesa_*`, `oc_skill_*`)

## Agent Register

Named session tracking. Parker runs multiple CC sessions simultaneously. Now they can discover each other.

- `lib/sessions.mjs` ... register/deregister/list sessions (pure ESM, zero deps)
- File-based at `~/.ldm/sessions/{name}.json` with PID liveness validation
- Boot hook registers on SessionStart
- Stop hook (`src/hooks/stop-hook.mjs`) deregisters on session end
- CLI: `ldm sessions`

## Message Bus

File-based inter-session messaging. One CC session can message another, or broadcast to all.

- `lib/messages.mjs` ... send/read/broadcast/acknowledge (pure ESM, zero deps)
- File-based at `~/.ldm/messages/{uuid}.json`
- Message types: chat, system, update-available
- Boot hook reads pending messages on session start
- CLI: `ldm msg send/list/broadcast`

## Update Checker

Cron job checks npm for newer versions of installed extensions. Surfaces updates in boot output.

- `lib/updates.mjs` ... check npm, write manifest (pure ESM, zero deps)
- Cron job every 6 hours (`src/cron/update-check.mjs`)
- Boot hook surfaces "Updates Available" section
- CLI: `ldm updates`

## ACP Compatibility Docs

Agent Client Protocol (ACP-Client) and Agent Communication Protocol (ACP-Comm) documented at `docs/acp-compatibility.md`. Both Apache 2.0, compatible with MIT + AGPL.

## Init and Doctor Updates

- `ldm init` creates: `sessions/`, `messages/`, `shared/cron/`, `state/`
- `ldm doctor` checks session and message directory health

## Build Pipeline

- `prepublishOnly` script builds bridge TypeScript before npm publish
- `dist/bridge/` ships with the npm package
- `docs/` added to files field
