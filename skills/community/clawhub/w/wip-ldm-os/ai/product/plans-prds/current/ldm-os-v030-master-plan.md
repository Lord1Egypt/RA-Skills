# Plan: LDM OS v0.3.0 ... Five Core Features + Bridge Absorption

**Date:** 2026-03-15
**Authors:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** Approved
**Depends on:** LDM OS v0.2.14 (current), WIP Bridge v0.3.2 (absorbing)
**Issues:** wipcomputer/wip-ldm-os #22-#27

---

## Context

LDM OS (v0.2.14) is currently an installer/boot system: scaffold, state detection, extension deployment, boot hook. Parker wants to evolve it into a full agent operating system with communication, session awareness, and update intelligence.

Parker runs multiple Claude Code (CC) sessions simultaneously (ldmos, test-ldmos, devops-toolkit, test-devops-toolkit). They can't see each other, can't communicate, and don't know when updates are available. The bridge (wip-bridge-private) connects CC to Lesa but is a standalone repo. It should be core OS.

First-class platforms: Claude Code CLI, OpenClaw (macOS), Claude (macOS/iOS/web), GPT (web/iOS/macOS). Architecture must be transport-agnostic: pure core logic wrapped by MCP today, HTTP/cloud tomorrow, whatever GPT needs after that.

## Design Decisions

1. **Bridge stays TypeScript, built as separate module within LDM OS.** Core libs (`lib/*.mjs`) stay zero-dep pure ESM. Bridge lives at `src/bridge/` with its own `package.json` for deps (MCP SDK, better-sqlite3, zod), built with tsup into `dist/bridge/`. Two layers: core (zero deps, runs everywhere) and bridge (TypeScript, npm deps, compiled).

2. **One unified MCP server.** All tools under one `lesa-bridge` server: existing bridge tools + update checker + agent register + message bus. One process, one config entry.

3. **File-based session registration with PID liveness.** Files in `~/.ldm/sessions/`. PID check validates liveness. Stop hook deregisters. Stale entries cleaned on read.

4. **File-based message bus.** JSON files in `~/.ldm/messages/`. Survives crashes/restarts. Sessions check on boot. Cleanup via cron (7-day archive, 30-day delete).

5. **Transport-agnostic core.** All business logic is pure functions. MCP wraps it for CC CLI. HTTP wraps it for cloud/iOS (future). OpenClaw plugin wraps it for Lesa. GPT actions wrap it for GPT (future).

---

## Phase 1: Bridge Absorption (Issue #22)

**Foundation. Everything depends on this.**

- Copy bridge source (core.ts, index.ts, cli.ts) into `src/bridge/`
- Bridge gets own `package.json` for deps (MCP SDK, better-sqlite3, zod)
- Built with tsup into `dist/bridge/`
- Add `LDM_ROOT` constant and `resolveConfigMulti()` to core.ts
- MCP registration path changes to LDM OS location
- `lesa` CLI stays as alias in LDM OS bin
- Standalone wip-bridge-private gets DEPRECATED.md
- Bridge version: 0.3.x standalone freezes, 0.4.0 starts in LDM OS

## Phase 2: Agent Register (Issue #23)

- `lib/sessions.mjs` ... register/deregister/list sessions (pure ESM, zero deps)
- File-based at `~/.ldm/sessions/{name}.json` with PID liveness validation
- Boot hook registers on SessionStart
- Stop hook deregisters on session end (`src/hooks/stop-hook.mjs`)
- MCP tool: `ldm_sessions`
- CLI: `ldm sessions` / `ldm sessions --json` / `ldm sessions --cleanup`

## Phase 3: Message Bus (Issue #24)

- `lib/messages.mjs` ... send/read/broadcast/acknowledge (pure ESM, zero deps)
- File-based at `~/.ldm/messages/{uuid}.json`
- Message types: chat, system, update-available
- Boot hook reads pending messages on session start
- MCP tools: `ldm_send_message`, `ldm_check_messages`
- CLI: `ldm msg send <to> <body>` / `ldm msg list` / `ldm msg broadcast <body>`

## Phase 4: Update Checker (Issue #25)

- `lib/updates.mjs` ... check npm, write manifest (pure ESM, zero deps)
- Cron job every 6 hours (`src/cron/update-check.mjs`)
- LaunchAgent template (`templates/ai.ldm.update-check.plist`)
- Boot hook surfaces "Updates Available" section
- MCP tool: `ldm_check_updates`
- CLI: `ldm updates` / `ldm updates --check` / `ldm updates --json`

## Phase 5: Agent Client Protocol (ACP-Client) Awareness

Research phase only. No code changes.

- Agent Client Protocol (ACP-Client): Zed Industries, Apache 2.0, already in OpenClaw for IDE integration
- Agent Communication Protocol (ACP-Comm): IBM / Linux Foundation, Apache 2.0, agent-to-agent REST (not needed now)
- Both Apache 2.0, compatible with our MIT + AGPL dual license
- Document compatibility in `docs/acp-compatibility.md`

## Phase 6: Init and Doctor Updates

- `ldm init` creates: `sessions/`, `messages/`, `shared/cron/`, `state/`
- `ldm doctor` checks: session dir, message dir, update manifest, bridge MCP, stop hook
- `catalog.json`: bridge status changes to "included" (always installed)

## Phase 7: Cloud Relay (Issue #26)

Follow the Memory Crystal ephemeral relay pattern (production architecture, not the deprecated cloud MCP/D1 demo).

- Cloudflare Workers + R2 bucket (encrypted ephemeral storage, 24h auto-clean)
- AES-256-GCM encryption, zero-knowledge relay
- Per-agent auth tokens
- Two tiers: Sovereign (encrypted only) and Convenience (cloud features)
- Per-user endpoint created on ldm init, eventually gated through Agent Pay
- Local poller on Mac decrypts drops and feeds into local message bus

Cloud MCP tools: `ldm_send_message`, `ldm_check_messages`, `ldm_sessions`, `ldm_check_updates`

Key files to port from Memory Crystal: `src/cloud/relay.ts`, `src/cloud/auth.ts`, `src/crypto.ts`, `src/poller.ts`, `wrangler.toml`

References WIP Cloud spec: `wip-cloud-private/ai/product/2026-03-10--wip-cloud-spec-v0.2.0.md`

---

## Implementation Sequence

```
Phase 1: Bridge Absorption        [foundation]
Phase 2: Agent Register           [depends on Phase 1 MCP server]
Phase 3: Message Bus              [depends on Phase 2 session names]
Phase 4: Update Checker           [depends on Phase 3 broadcasting]
Phase 5: ACP-Client Awareness     [research, no deps]
Phase 6: Init + Doctor            [after all phases]
Phase 7: Cloud Relay              [after local features work, follows MC pattern]
```

## Verification

**Phase 1:** `npm run build:bridge` succeeds. All 5 MCP tools respond. `lesa diagnose` passes.
**Phase 2:** SessionStart creates file. `ldm sessions` shows it. Session end removes it.
**Phase 3:** `ldm msg send test-ldmos "hello"` creates file. Boot shows pending. MCP returns and clears.
**Phase 4:** `ldm updates --check` queries npm. Boot shows "Updates Available". Cron broadcasts.
**Phase 7:** Message drops encrypted to R2. Local poller picks up, decrypts, delivers to local bus.
**Full chain:** CC session 1 messages session 2 locally. Remote agent sends message via cloud relay, CC receives it.

## Renames Tracked

- AI DevOps Toolbox -> **Code** (the dev tools)
- lesa-bridge (standalone) -> **WIP Bridge** (core OS module in LDM OS)
- `wip-` prefix is the brand. Attribution baked into names.

## Naming Convention

Full name first with shorthand in parentheses. Shorthand going forward.
- Agent Client Protocol (ACP-Client)
- Agent Communication Protocol (ACP-Comm)

## Doc Standard

Every tool: README.md (simple) + TECHNICAL.md (deep). No REFERENCE.md, SPEC.md proliferation.

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

*WIP.computer. Learning Dreaming Machines.*
