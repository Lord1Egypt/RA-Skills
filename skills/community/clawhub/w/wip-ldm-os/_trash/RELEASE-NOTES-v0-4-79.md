# wip-ldm-os v0.4.79

## Bridge: reply-to-sender routing + `lesa_reply_to_sender` MCP tool

Closes the reply-routing footgun observed on 2026-04-20: Lēsa's replies addressed `to: "cc-mini"` (agent-only) broadcast to every cc-mini session, so multiple idle sessions burned turns reading + reasoning about messages not intended for them. Apr 10 shipped Option 1 (agent-only = broadcast) as a safety net; Option 3 (reply-to-sender) never shipped.

### What ships

- `lesa-bridge 0.4.1` ... new `inReplyTo` field on `InboxMessage`, wired into `pushInbox` + `sendLdmMessage`. When `inReplyTo` is set AND `to` is missing or agent-only, the bridge looks up the referenced message and auto-resolves `to` to the original sender's fully-qualified identity.
- New MCP tool `lesa_reply_to_sender({ messageId, body })` wraps the above. Callers no longer have to manually parse sender strings.
- `lesa_check_inbox` output now includes `[id: <uuid>]` per message so agents have the id at hand when replying.
- `shared/docs/dev-guide-wipcomputerinc.md.tmpl` gets a new "Bridge: Reply Routing" section documenting all three routing modes plus the reply-to-sender convention. Propagates to both agents on next `ldm install`.

### Files

- `src/bridge/core.ts`: +70 lines (InboxMessage.inReplyTo, findMessageById, pushInbox + sendLdmMessage inReplyTo resolution).
- `src/bridge/mcp-server.ts`: +40 lines (lesa_reply_to_sender tool, inbox id surfacing).
- `src/bridge/package.json`: 0.4.0 → 0.4.1.
- `shared/docs/dev-guide-wipcomputerinc.md.tmpl`: +17 lines.
- `ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md`: bug doc.

### Non-goals

- Broadcast semantics preserved. Explicit `to: "cc-mini:*"` still reaches every session.
- No enforcement. The goal is to make correct routing cheap and obvious, not to police agents.

### Rollout

After merge: `wip-release patch` on wip-ldm-os-private → `ldm install` to propagate. Bridge binary rebuilds from source on install so the new MCP tool becomes available next session.

### Related

- PR #632 (bridge reply routing)
- Prior: PR from 2026-04-10 shipping Option 1 (agent-only broadcast fallback)
- Bug: `ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md`
