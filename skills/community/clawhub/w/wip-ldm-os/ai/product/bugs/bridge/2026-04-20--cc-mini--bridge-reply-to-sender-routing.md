# Bridge: Reply routing defaults to broadcast; specific-session replies need a helper

**Date:** 2026-04-20
**Filed by:** cc-mini (with Parker)
**Component:** bridge (`src/bridge/core.ts`, `src/bridge/mcp-server.ts`) + TOOLS.md convention
**Severity:** Medium (ambiguous routing; not lost messages, but visible confusion and wasted turns)
**Related:** 2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md (parent; shipped Option 1), 2026-04-06--cc-mini--bridge-async-inbox-plan.md (parent plan)

## Description

After the Apr 10 fix shipped Option 1 (agent-only address = broadcast), Lēsa's replies addressed `to: "cc-mini"` now reach cc-mini sessions ... but ALL of them, not the specific one that originally messaged her. Parker observed this live on 2026-04-20: he sent a thanks to Lēsa, she replied, and BOTH `cc-mini:lesa-code` (the session that actually shipped the work) AND `cc-mini:default` (a separate idle session) saw the reply and acknowledged. The default session politely declined credit, which worked out socially, but the bridge semantics are:

> Agent-only `to:` = broadcast. Specific-session `to:` = unicast. No mechanism for "reply to whoever sent this" other than Lēsa manually constructing the right string.

## Reproduction

1. cc-mini session `lesa-code` calls `lesa_send_message(body)`.
2. MCP server writes inbox record with `from: "cc-mini:lesa-code"`, `to: "lesa"`. Also fires to gateway. ✓
3. Lēsa's agent replies. Her agent (or her TOOLS.md convention) writes `to: "cc-mini"` (agent-only).
4. `parseTarget("cc-mini")` → `{agent:"cc-mini", session:"*"}` (broadcast) per Apr 10 Option 1 fix.
5. Every cc-mini session's inbox-rewake hook fires on the new file.
6. `drainInbox` is first-come-first-served on the file (it's `renameSync`'d to `_processed/`), but the HOOKS fire in parallel so every session SEES the wake event.
7. Each session reasons about whether to respond; multiple end up replying, confusion ensues.

Race detail: the FILE is claimed by whichever session's `drainInbox` reaches `renameSync` first. But the hooks already pushed the raw text into each session's context. Even the session that "loses" the drain race has already started reasoning about the message.

## Impact

- **Wasted compute.** Each idle cc-mini session burns at least one turn reading + reasoning about messages not intended for it.
- **Ambiguous authorship.** Lēsa sees multiple replies from "cc-mini" without knowing which session is which.
- **Conversation fragmentation.** A thread logically scoped to one session becomes noise across all of them.
- **Not lost, just confused.** Messages are delivered; the problem is routing precision.

## Root cause

Two layered issues, both reply-routing:

1. **No "reply to sender" MCP helper.** Neither `lesa_send_message` nor `lesa_check_inbox` exposes an easy way to say "write my next message addressed to whoever sent me this one." Lēsa's agent (and cc-mini) have to manually parse the sender's `from` and construct the `to` string. When they forget, they use the agent-only default → broadcast.

2. **TOOLS.md convention is agent-only.** Lēsa's workspace `TOOLS.md` documents `to: "cc-mini"` as the reply form. That was the original Apr 6 plan before multi-session cc-mini was a thing. It was patched by Apr 10's Option 1 (agent-only = broadcast) so replies at least reached somewhere, but nothing updated the convention to target specific sessions.

## Fix

Three layers, each standalone valuable:

### Layer A (bridge code): `inReplyTo` routing + `lesa_reply_to_sender` MCP tool

Add an optional `inReplyTo: <messageId>` field to the inbox schema and to `pushInbox()`. When present:

- `pushInbox` looks up the referenced message (in `~/.ldm/messages/_processed/` if already drained, or the current inbox).
- If found, auto-resolves `to: <original.from>`.
- Caller's explicit `to` wins; `inReplyTo` only fills in when `to` is missing or agent-only.

Add a new MCP tool `lesa_reply_to_sender({ messageId, body })` that wraps the above. Callers can bypass manual string construction entirely.

### Layer B (MCP surface): expose message IDs in `lesa_check_inbox` output

Today `lesa_check_inbox` returns a formatted block without the underlying message `id`. The agent can't call `lesa_reply_to_sender(id, ...)` without knowing IDs. Include `[id: <uuid>]` in the rendered output so the agent has the key at hand.

### Layer C (convention): dev-guide update

Shared-doc update: the agent-to-agent reply convention is "use `lesa_reply_to_sender` when available, else copy the inbound `from` verbatim into `to`." Replace any `to: "cc-mini"` guidance with the reply-to-sender pattern. Propagates to both agents on next `ldm install`.

## Non-goals

- **Not removing broadcast semantics.** Explicit `to: "cc-mini:*"` broadcasts still work. Parker or an agent can still intentionally hit every session of an agent if that's the intent.
- **Not enforcing reply routing.** Broadcast-by-default stays the fallback when nothing else resolves. The change is that reply-to-sender is now CHEAP and OBVIOUS, so correct usage becomes the default when an agent actually wants to reply.

## Tests

- `lesa_reply_to_sender` with a known `inReplyTo` routes to the original sender's session.
- `inReplyTo` referencing a non-existent message: falls through to broadcast behavior (no-op on routing).
- Existing broadcast tests (`to: "cc-mini"`) still pass unchanged.
- `lesa_check_inbox` output now includes `[id: <uuid>]` per message.

## Version bumps

- bridge package version in `src/bridge/package.json`: patch.
- wip-ldm-os root patch on release.

## Release notes + rollout

Release notes on the branch. After merge: `wip-release patch` on wip-ldm-os-private, `ldm install` to propagate.

## Related files

- `src/bridge/core.ts` (pushInbox, parseTarget, messageMatchesSession, drainInbox)
- `src/bridge/mcp-server.ts` (lesa_send_message, lesa_check_inbox, + new lesa_reply_to_sender)
- `shared/docs/dev-guide-wipcomputerinc.md.tmpl` (bridge convention section)

## Related prior bugs

- `2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md` — Option 1 shipped, Option 3 did not. This doc is Option 3.
- `2026-04-06--cc-mini--bridge-async-inbox-plan.md` — parent plan.
- `2026-04-05--cc-mini--bridge-master-plan.md` — umbrella.
