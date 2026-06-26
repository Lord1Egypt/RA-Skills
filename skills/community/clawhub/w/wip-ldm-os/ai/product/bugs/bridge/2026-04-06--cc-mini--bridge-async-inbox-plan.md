# Bridge: Async Inbox + CC-to-CC Communication

**Date:** 2026-04-06
**Filed by:** cc-mini (with Parker)
**Priority:** high
**Status:** plan approved, implementation next
**Depends on:** March 30 bridge messaging architecture at `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md`

## What this plan fixes

Three bugs that are all the same problem:

### Bug 1: Bridge blocks CC while waiting for Lēsa's reply

The current `lesa_send_message` calls the gateway synchronously and waits up to 120s for Lēsa to respond. If she's busy, CC is stuck. Can't do anything else. The client aborts at 120s, the server keeps processing, the reply goes to iMessage, CC never sees it, retries, each retry burns another full Opus turn.

Increasing the timeout from 120s to 300s was the wrong fix. It just makes CC stuck for longer.

**The real fix:** async send. CC sends the message, gets an immediate "sent" acknowledgment, and picks up Lēsa's reply from the inbox when it arrives.

### Bug 2: Parker can't see both sides of the CC-Lēsa conversation

When CC sends to Lēsa via HTTP, Parker should see CC's outbound message and Lēsa's reply in the TUI. Currently the inbound from CC doesn't display as a visible turn in the TUI. When Lēsa replies, CC gets it via HTTP but Parker doesn't see it printed in CC's terminal.

**The real fix:** CC prints what it sent and what it received. Lēsa's reply goes through her normal session pipeline (visible in TUI). Messages are file-based so Parker can read them directly too.

### Bug 3: CC sessions can't talk to each other

Parker has ldmos03 (this session) and lesa01 (another tab). They can't communicate. Parker wants to open CC on his MacBook Air and have it talk to CC on the Mac Mini. The bridge currently only knows how to talk to OpenClaw (Lēsa's gateway), not to other CC sessions.

**The real fix:** shared file-based inbox at `~/.ldm/messages/`. Any agent writes there. Any agent reads from there. CC-to-CC, CC-to-Lēsa, Lēsa-to-CC. All the same mechanism.

## Why these are the same problem

All three bugs exist because the bridge uses two different communication paths:

1. **CC to Lēsa:** synchronous HTTP to the OpenClaw gateway (port 18789). Blocks. Can't target sessions. Only reaches Lēsa.
2. **Lēsa to CC:** writes a file to `~/.ldm/messages/`. Async. CC polls via UserPromptSubmit hook.

Path 1 is the broken one. Path 2 already works. The fix is: **make everything use path 2.** One inbox. One format. One read mechanism. All directions.

## The architecture (already designed, half built)

From the March 30 bridge messaging architecture doc:

```
LOCAL (same machine):
  Lesa  --> file: ~/.ldm/messages/{uuid}.json <-- check_inbox -- CC session
  CC    --> file: ~/.ldm/messages/{uuid}.json <-- check_inbox -- Lesa (via gateway inject)
  CC-A  --> file: ~/.ldm/messages/{uuid}.json <-- check_inbox -- CC-B

REMOTE (cross-machine, Phase 5):
  CC-Air  --encrypt--> R2 relay --poller--> file: ~/.ldm/messages/{uuid}.json
```

One inbox. Multiple delivery mechanisms. All land in `~/.ldm/messages/`.

## What is already built

| Component | Location | Status |
|---|---|---|
| Session registry | `lib/sessions.mjs` | SHIPPED |
| Message bus (file-based JSON) | `lib/messages.mjs` | SHIPPED |
| Message CLI | `ldm msg send/list/broadcast` | SHIPPED |
| Session CLI | `ldm sessions` | SHIPPED |
| Inbox directory | `~/.ldm/messages/` | EXISTS |
| Session directory | `~/.ldm/sessions/` | EXISTS |
| Bridge MCP server | `src/bridge/mcp-server.ts` | SHIPPED (uses in-memory queue, needs fix) |
| Bridge HTTP 18790 | `src/bridge/mcp-server.ts` | SHIPPED (needs filesystem backend) |
| Gateway HTTP 18789 | OpenClaw gateway | SHIPPED |
| CC inbox polling | UserPromptSubmit hook | SHIPPED |
| Message format spec | `lib/messages.mjs` | SHIPPED |

The libs exist. The format exists. The directories exist. The polling exists. It's a wiring job.

## Implementation plan

### Step 1: Wire `lesa_send_message` to use async send + file inbox for reply

**What changes:**

Currently `lesa_send_message` in the bridge MCP tool does:
1. POST to gateway 18789 (synchronous, blocks up to 120s)
2. Wait for HTTP response with Lēsa's reply
3. Return the reply to CC

Change to:
1. POST to gateway 18789 with fire-and-forget (the `fireAndForget` flag at line 510 of `core.ts` already exists)
2. Write a "pending reply" marker to `~/.ldm/messages/` so CC knows it's waiting
3. Return immediately: "Message sent to Lēsa. Her reply will arrive in your inbox."
4. Lēsa processes the message through her full pipeline (visible in Parker's TUI)
5. Lēsa's reply gets written to `~/.ldm/messages/` (she already does this)
6. CC's `check_inbox` (UserPromptSubmit hook or a new MCP tool) picks up the reply
7. CC prints both what it sent and what Lēsa replied

**Files:**
- `src/bridge/mcp-server.ts`: modify `lesa_send_message` tool handler to use fire-and-forget + return immediately
- `src/bridge/core.ts`: the `fireAndForget` path at line 510 already does the right thing

**What Parker sees:**
- In CC's terminal: "Sent: [message text]" then later "Lēsa replied: [reply text]"
- In Lēsa's TUI: CC's inbound message + Lēsa's reply (both visible as normal turns)

**What does NOT change:**
- The gateway endpoint. No server-side changes. The gateway works fine.
- Lēsa's session pipeline. Messages still go through her full agent pipeline.
- The steer-backlog queue path for mid-stream messages. Still in place.

### Step 2: Wire `check_inbox` as an MCP tool

**What changes:**

Add a `check_inbox` MCP tool to the bridge that reads `~/.ldm/messages/` for messages addressed to this CC session.

Currently CC polls via the UserPromptSubmit hook. That works but only fires when Parker types something. Adding it as an MCP tool means CC can check proactively.

**Files:**
- `src/bridge/mcp-server.ts`: new `lesa_check_inbox` tool (or rename existing if there's a stub)
- Uses `lib/messages.mjs` readMessages() filtered by agent + session name

### Step 3: Add `ldm_send_message` for CC-to-CC

**What changes:**

New MCP tool `ldm_send_message` (or extend the existing one) that writes a message to `~/.ldm/messages/` with a `to` field targeting any agent or session:

```
ldm_send_message({ to: "lesa", message: "hey" })
ldm_send_message({ to: "cc-mini:lesa01", message: "hey" })
ldm_send_message({ to: "cc-mini:ldmos03", message: "hey" })
ldm_send_message({ to: "*", message: "gateway restarting" })
```

This is the CC-to-CC feature Parker asked for. ldmos03 writes a file. lesa01 picks it up via check_inbox.

**Files:**
- `src/bridge/mcp-server.ts`: new tool or extend existing
- Uses `lib/messages.mjs` sendMessage() with targeting

### Step 4: Session registration on boot

**What changes:**

When CC boots, register in `~/.ldm/sessions/` with the session name (from `LDM_SESSION_NAME` env var or the `/rename` label Parker gives it).

This is how other sessions discover each other. "Who can I talk to?" = read `~/.ldm/sessions/`.

**Files:**
- `src/bridge/mcp-server.ts` or `src/hooks/session-start.mjs`: register on boot
- Uses `lib/sessions.mjs` registerSession()

### Step 5: Boot hook reads inbox

**What changes:**

On SessionStart, check `~/.ldm/messages/` for pending messages addressed to this session. Display them at the top of the session: "You have 2 messages from Lēsa."

This is how messages that arrived while CC was offline get delivered.

**Files:**
- `src/hooks/session-start.mjs` or wire into the existing boot hook
- Uses `lib/messages.mjs` readMessages()

## Message format (already defined)

From `lib/messages.mjs`:

```json
{
  "id": "uuid",
  "type": "chat",
  "from": "cc-mini:ldmos03",
  "to": "lesa",
  "body": "Hey Lēsa, quick question about the bridge.",
  "timestamp": "2026-04-06T08:00:00.000Z",
  "read": false,
  "readBy": []
}
```

The `to` field supports:
- `"lesa"` ... Lēsa's default session
- `"cc-mini:lesa01"` ... specific CC session by name
- `"cc-mini:*"` ... broadcast to all CC sessions
- `"*"` ... broadcast to all agents

## What Parker sees (the visibility requirement)

Parker's rule: "whatever you say, I see. Whatever she says, I see. Nothing hidden."

After this plan ships:

1. **CC sends to Lēsa:** CC prints "Sent to Lēsa: [message]" in its terminal. The message hits the gateway, enters Lēsa's session pipeline, Parker sees it in TUI as a normal inbound turn.
2. **Lēsa replies:** Lēsa's reply appears in TUI (normal). She also writes to `~/.ldm/messages/`. CC picks it up and prints "Lēsa replied: [reply]" in its terminal.
3. **CC sends to another CC:** CC prints "Sent to cc-mini:lesa01: [message]". The file lands in `~/.ldm/messages/`. The target session picks it up on its next check_inbox and prints it.
4. **All messages are files in `~/.ldm/messages/`.** Parker can `ls` them, `cat` them, or read them in any tool. Nothing is hidden in HTTP responses or in-memory queues.

## What this does NOT include (future phases)

- **Cross-machine communication** (MacBook Air to Mac Mini). That's the Cloud Relay (Phase 5 of the March 30 architecture). Designed but not started. Needs Cloudflare Worker + R2 + device pairing. Separate plan.
- **Automatic reply routing back through gateway.** Lēsa's reply currently goes to iMessage AND gets written to the file inbox. If we later want her reply to ONLY go to the file inbox (not iMessage) when the sender is CC, that's a gateway-side change. Not in scope for this plan.
- **Message persistence / history.** Read messages go to `_read/` or get deleted. Conversation history stays in daily logs and Crystal. Not a message bus concern.

## Verification

After all 5 steps ship:

1. CC sends a message to Lēsa. CC is NOT blocked. Returns immediately.
2. Lēsa processes and replies. Parker sees both sides in TUI.
3. CC picks up the reply from the inbox. Prints it in terminal. Parker sees it.
4. CC (ldmos03) sends a message to CC (lesa01). lesa01 picks it up on next check_inbox.
5. `ls ~/.ldm/messages/` shows the message files. Parker can read them.
6. On session boot, pending messages display: "You have N messages from [sender]."
7. `ldm msg list` shows pending messages from CLI.

## Scope boundary

**In scope:** Steps 1-5 above. All local, same machine, file-based.

**Out of scope:** Cloud Relay (cross-machine), automatic Lēsa reply routing, message encryption, device pairing. Those are separate plans that build on top of this inbox.

## Files to modify

| File | Step | Change |
|---|---|---|
| `src/bridge/mcp-server.ts` | 1 | `lesa_send_message` uses fire-and-forget, returns immediately |
| `src/bridge/core.ts` | 1 | Already has `fireAndForget` path; may need minor adjustments |
| `src/bridge/mcp-server.ts` | 2 | New `check_inbox` MCP tool |
| `src/bridge/mcp-server.ts` | 3 | New `ldm_send_message` MCP tool |
| `src/bridge/mcp-server.ts` or `src/hooks/` | 4 | Session registration on boot |
| `src/hooks/session-start.mjs` or boot hook | 5 | Read inbox on boot, display pending messages |
| `lib/messages.mjs` | all | Already shipped; may need minor format adjustments |
| `lib/sessions.mjs` | 4 | Already shipped; may need session-name-from-env support |

## Cross-references

- `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md` ... the full 240-line architecture doc this plan implements
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` ... the prior bridge bug plan (cost amplification focus)
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md` ... the 2-5x cost trace
- `ai/product/bugs/master-plans/session-recap-04-05-2026.md` ... what broke and what shipped on Apr 5

## Open questions for Parker

1. When Lēsa replies to CC via the file inbox, should her reply ALSO go to iMessage (current behavior) or ONLY to the inbox? Current plan: both (no server changes). Future option: inbox-only for CC-originated messages.
2. Session names: should CC auto-register with the `/rename` label (e.g., "ldmos03") or require `LDM_SESSION_NAME` env var? I'd prefer auto-register from the label if available.
3. Should `check_inbox` run on a timer (every 30s?) or only when CC explicitly calls it / on UserPromptSubmit? Timer adds background cost. Manual is free but means CC doesn't see replies until it checks.
