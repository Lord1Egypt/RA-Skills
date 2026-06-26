# Plan: Bridge Messaging Architecture

**Date:** 2026-03-30 (updated)
**Author:** cc-mini (with Parker)
**Depends on:** LDM OS v0.3.0 master plan (Phases 2, 3, 7)
**Save to:** wip-ldm-os-private/ai/product/plans-prds/bridge/

## Context

The bridge connects Claude Code sessions and OpenClaw agents. Three problems today:

1. **In-memory inbox.** Each Claude Code session spawns its own bridge MCP process. Only the first one binds port 18790. Messages posted there go to that process's in-memory queue. Five bridge processes running, only one gets messages.

2. **No session targeting.** Parker wants multiple Claude Code sessions running simultaneously: a working session (Parker + CC), a brainstorm session (Lesa + CC), a task session (Lesa delegates to CC). Same agent, same memory, different conversations. Lesa needs to target which session she's talking to.

3. **Localhost only.** CC on the MacBook Air can't reach Lesa on the Mac mini. The bridge is localhost-bound. Cross-machine communication needs Cloud Relay.

## The principle

Same agent, same memory, different conversations. Like phone lines to the same person. Messages to the brainstorm session don't interrupt the working session. And it works across machines, not just localhost.

## Relationship to the v0.3.0 master plan

This plan extends three phases from the LDM OS v0.3.0 master plan (`ldm-os-v030-master-plan.md`):

| Master plan phase | Status | This plan extends it with |
|---|---|---|
| Phase 2: Agent Register | SHIPPED (`lib/sessions.mjs`) | Session naming, inbox folder per session |
| Phase 3: Message Bus | SHIPPED (`lib/messages.mjs`, `~/.ldm/messages/`) | Replace bridge in-memory queue with the message bus |
| Phase 7: Cloud Relay | NOT STARTED | Remote delivery into the same message bus |

The master plan designed the message bus as file-based JSON at `~/.ldm/messages/`. The session registry is at `~/.ldm/sessions/`. Both exist. The bridge inbox should USE these systems instead of its own in-memory queue.

## Architecture

### Message flow (all directions)

```
LOCAL (same machine):
  Lesa  --POST 18790/message-->  file: ~/.ldm/messages/{uuid}.json  <--check_inbox--  CC session
  CC    --lesa_send_message--->  gateway 18789  ---------------------->  Lesa
  CC-A  --ldm msg send--------->  file: ~/.ldm/messages/{uuid}.json  <--check_inbox--  CC-B

REMOTE (cross-machine, Phase 7):
  CC-Air  --encrypt-->  R2 dead drop  --poller-->  file: ~/.ldm/messages/{uuid}.json  <--check_inbox--  CC-Mini
  CC-Mini --encrypt-->  R2 dead drop  --poller-->  file: ~/.ldm/messages/{uuid}.json  <--check_inbox--  CC-Air
```

One inbox. Multiple delivery mechanisms. Local HTTP, local filesystem, remote relay. All land in the same `~/.ldm/messages/` directory.

### Message format

Using the existing message bus format from the master plan (`lib/messages.mjs`):

```json
{
  "id": "uuid",
  "type": "chat",
  "from": "lesa",
  "to": "cc-mini:brainstorm",
  "body": "What do you think about memory auditability?",
  "timestamp": "2026-03-30T18:30:00.000Z",
  "read": false,
  "readBy": []
}
```

The `to` field supports:
- `"cc-mini"` ... default session for that agent
- `"cc-mini:brainstorm"` ... specific named session
- `"cc-mini:*"` ... broadcast to all sessions of that agent
- `"*"` ... broadcast to all agents, all sessions

### Session registration

Uses the existing `lib/sessions.mjs` (Phase 2, shipped):

```
~/.ldm/sessions/
  cc-mini--work.json          ... Parker's working session
  cc-mini--brainstorm.json    ... Lesa's brainstorm session
  cc-mini--task-abc123.json   ... autonomous task
```

Each session file contains: `name`, `agentId`, `pid`, `startTime`, `cwd`. PID liveness validation on read. Stale entries auto-cleaned.

Session name comes from:
- `LDM_SESSION_NAME=brainstorm claude` (explicit)
- Auto-generated from context (working directory, invocation source)
- Default: `work`

### Reading messages

`check_inbox` MCP tool (and boot hook):
1. Scans `~/.ldm/messages/` for files where `to` matches this agent + session (or broadcast)
2. Returns matching messages sorted by timestamp
3. Marks as read (moves to `~/.ldm/messages/_read/` or deletes)

The boot hook (SessionStart) checks automatically. No polling needed for initial delivery.

### The 18790 HTTP server

Write-only endpoint. First bridge process binds it. Writes to `~/.ldm/messages/`:
- `POST /message` ... creates a message file with targeting
- `GET /status` ... pending counts per session
- `GET /sessions` ... lists active sessions from `~/.ldm/sessions/`

Other bridge processes skip binding 18790 (port taken). They still read via `check_inbox` because it reads the filesystem.

### CLI

Uses the existing `ldm msg` commands (Phase 3, shipped):
```bash
ldm msg send cc-mini:brainstorm "Hey, what about..."
ldm msg send lesa "Quick question"
ldm msg list
ldm msg broadcast "Gateway restarting in 5 min"
```

### Cross-machine (Cloud Relay, Phase 7)

```
CC-Air (MacBook Air)
  -> encrypts message with AES-256-GCM
  -> POSTs to Cloudflare Worker (public internet)
  -> Worker stores encrypted blob in R2 (24h TTL)

Mac Mini (poller, runs every minute)
  -> polls Worker for new blobs
  -> decrypts locally
  -> writes to ~/.ldm/messages/{uuid}.json
  -> target session picks it up via check_inbox
```

Same message format. Same inbox. The relay is just a delivery mechanism. It never sees plaintext. Keys never leave the machines.

Reverse direction (Mini -> Air): same pattern. Air runs its own poller.

Every node has the full `~/.ldm/` tree. Crystal.db, sessions, messages. Search is always local. The relay is just the transport for new messages and memory sync.

## Implementation phases

### Phase 1: File-based inbox (immediate fix)
- Replace `inboxQueue` array in `src/bridge/core.ts` with `lib/messages.mjs` read/write
- `pushInbox` calls `sendMessage()` from `lib/messages.mjs`
- `drainInbox` calls `readMessages()` filtered by agent + session
- 18790 HTTP server writes via `sendMessage()`
- No session targeting yet (everything goes to agent default)
- **Fixes the immediate bug:** all bridge processes can read messages

### Phase 2: Session naming + targeting
- Boot registers with a name via `LDM_SESSION_NAME` env or auto-detect
- `POST /message` accepts `to` field with `agent:session` format
- `check_inbox` filters by session name + broadcast
- `GET /sessions` lists active named sessions
- Lesa's `send-to-claude-code` skill updated to specify target

### Phase 3: Boot hook delivery
- SessionStart hook calls `readMessages()` for this agent + session
- Pending messages displayed at the top of the session
- "You have 3 messages from Lesa" on boot

### Phase 4: Cross-agent inbox
- Same `~/.ldm/messages/` for all agents
- `to: "lesa"` routes to OpenClaw via gateway
- `to: "cc-air"` routes to Air's inbox (local if same machine, relay if remote)
- Bridge skill resolution: if target is local, write to file. If remote, encrypt and relay.

### Phase 5: Cloud Relay integration + device pairing

The relay is a hosted service provided by WIP Computer. Users don't self-host.

**Device pairing model:**
- Your phone pairs to Core (Mac mini) via the relay
- Your phone pairs to Node (MacBook Air) via the relay
- Core and Node pair to each other via the relay
- Each pairing creates a shared encryption key (generated locally, never sent to the relay)
- The relay routes encrypted blobs between paired devices. It can't read them.

**How pairing works:**
1. Device A generates a pairing code (short-lived, displayed on screen)
2. Device B enters the code (or scans QR)
3. Both devices derive a shared AES-256-GCM key via key exchange
4. Both register with the Cloudflare Worker using their agent auth token
5. The Worker knows "Device A and Device B are paired" but has no keys

**The relay service:**
- Cloudflare Worker + R2 bucket (encrypted ephemeral storage, 24h auto-clean)
- WIP Computer hosts the Worker at `relay.wip.computer`
- Free tier: 1 Core + 2 Nodes. Paid tier via Agent Pay for more.
- Self-hostable: the Worker code is open source (AGPL). Run your own if you want.
- Zero-knowledge: encrypted blobs pass through. The relay never sees plaintext.

**Message delivery via relay:**
- CC-Air encrypts message, POSTs to `relay.wip.computer/drop`
- Worker stores blob in R2, tagged with destination device ID
- Mac Mini poller hits `relay.wip.computer/pickup`, gets blob, decrypts
- Writes to `~/.ldm/messages/{uuid}.json`
- Target session picks it up via `check_inbox`
- Same message format. Same inbox. Different transport.

**What flows through the relay:**
- Messages (chat, system, task delegation)
- Memory sync (crystal.db deltas, new chunks)
- Session state (who's active, what they're working on)
- NOT: raw API keys, credentials, or unencrypted identity files

## Existing infrastructure (already built)

| Component | Location | Status |
|---|---|---|
| Session registry | `lib/sessions.mjs` | SHIPPED (Phase 2) |
| Message bus | `lib/messages.mjs` | SHIPPED (Phase 3) |
| Session CLI | `ldm sessions` | SHIPPED |
| Message CLI | `ldm msg send/list/broadcast` | SHIPPED |
| Bridge MCP | `src/bridge/mcp-server.ts` | SHIPPED (needs inbox fix) |
| Bridge HTTP 18790 | `src/bridge/mcp-server.ts` | SHIPPED (needs filesystem backend) |
| Bridge HTTP 18789 | OpenClaw gateway | SHIPPED (fixed in v0.4.66) |
| Session discovery docs | `docs/bridge/README.md` | SHIPPED |
| Cloud Relay design | master plan Phase 7 | DESIGNED, NOT STARTED |

## What NOT to build

- No database for messages. Files are fine for this scale.
- No WebSocket server. HTTP POST + filesystem is simpler and survives restarts.
- No message persistence beyond delivery. Read messages go to `_read/` or get deleted. History is in the daily log.
- No authentication on local inbox. Localhost only. Same trust boundary as the gateway.
- No custom protocol. Use the existing `lib/messages.mjs` format.

## Files to change

| File | Phase | Change |
|------|-------|--------|
| `src/bridge/core.ts` | 1 | Replace in-memory queue with `lib/messages.mjs` |
| `src/bridge/mcp-server.ts` | 1 | HTTP server writes to filesystem |
| `src/bridge/mcp-server.ts` | 2 | Add /sessions endpoint, session-targeted routing |
| `src/boot/boot-hook.mjs` | 3 | Check inbox on SessionStart |
| `skills/send-to-claude-code/SKILL.md` | 2 | Document session targeting |
| `docs/bridge/README.md` | 1-2 | Update inbox description |
| `docs/bridge/TECHNICAL.md` | 1-2 | Update "In-memory queue" to file-based |
