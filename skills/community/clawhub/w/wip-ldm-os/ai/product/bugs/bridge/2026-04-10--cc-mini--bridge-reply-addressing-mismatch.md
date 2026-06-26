# Bug: Bridge replies addressed to "cc-mini" are invisible to CC sessions

**Date:** 2026-04-10
**Filed by:** cc-mini (with Parker)
**Component:** bridge (src/bridge/core.ts, `drainInbox` + `messageMatchesSession`)
**Severity:** High (bridge replies silently dropped; breaks CC<->Lēsa round-trip)
**Related:** 2026-04-06--cc-mini--bridge-async-inbox-plan.md (parent plan)

## Description

When Lēsa sends a reply to CC via the bridge file inbox at `~/.ldm/messages/`, CC's `lesa_check_inbox` returns "No pending messages" even though the file exists and is addressed to CC. The message is silently dropped.

## Reproduction

1. CC sends a message to Lēsa via `lesa_send_message`
2. Lēsa replies by writing a JSON file to `~/.ldm/messages/`
3. CC calls `lesa_check_inbox`
4. Expected: CC sees Lēsa's reply
5. Actual: "No pending messages" returned. File still sits in the inbox unprocessed.

## Concrete example from Apr 10 bridge test

**CC's outbound (written by CC):**
```json
{
  "id": "1588d669-6d25-4bf4-90f6-3c355732492b",
  "type": "chat",
  "from": "cc-mini:default",
  "to": "lesa",
  "body": "Bridge test from CC. ...",
  "timestamp": "2026-04-10T19:17:41.678Z",
  "read": false
}
```

**Lēsa's reply (written by Lēsa):**
```json
{
  "from": "lesa",
  "to": "cc-mini",
  "body": "Bridge confirmed working on my end. ...",
  "type": "chat"
}
```

Both files exist in `~/.ldm/messages/`. Neither was picked up by `lesa_check_inbox`.

## Root cause

`src/bridge/core.ts:270-284` ... `messageMatchesSession()`:

```typescript
function messageMatchesSession(msgTo: string, agentId: string, sessionName: string): boolean {
  if (msgTo === "*" || msgTo === "all") return true;
  const target = parseTarget(msgTo);
  if (target.agent !== "*" && target.agent !== agentId) return false;
  if (target.session === "*") return true;
  return target.session === sessionName;  // <-- fails here
}
```

When `msgTo === "cc-mini"` (no session qualifier), `parseTarget()` likely returns `{ agent: "cc-mini", session: undefined }` or similar. The check `target.session === sessionName` fails because `sessionName` is `"default"` (or the actual session name like `"ldmos03"`).

There are two addressing conventions in use:

| Who writes | Format | Works? |
|---|---|---|
| CC via `pushInbox` | `cc-mini:default` (agent + session) | Yes, matches `cc-mini:default` |
| Lēsa (bridge convention from TOOLS.md) | `cc-mini` (agent only) | **No, missing session** |

The TOOLS.md bridge reply convention documented on Apr 6 says to use `"to": "cc-mini"` with agent only. That format has never matched CC's session filter.

## Impact

- CC<->Lēsa round-trip is broken
- All of Lēsa's bridge replies are silently dropped by CC
- No error, no warning, no metric
- Parker can see both messages in `~/.ldm/messages/` but CC acts as if nothing was received
- Wasted CC turns retrying, wasted Lēsa turns responding to messages CC never received
- Breaks the "bridge works" assertion, undermines the async inbox plan from 2026-04-06

## Fix options

### Option 1: Relax matching for agent-only addresses (recommended)

In `messageMatchesSession`, treat agent-only addresses as broadcasts to all sessions of that agent:

```typescript
function messageMatchesSession(msgTo: string, agentId: string, sessionName: string): boolean {
  if (msgTo === "*" || msgTo === "all") return true;
  const target = parseTarget(msgTo);
  if (target.agent !== "*" && target.agent !== agentId) return false;
  // Agent-only address (no session) = deliver to any session of that agent
  if (!target.session || target.session === "*") return true;
  return target.session === sessionName;
}
```

Pro: backwards compatible, catches all existing Lēsa replies.
Con: if Parker has multiple CC sessions open, they'd all receive the same message.

### Option 2: Require fully-qualified addresses

Enforce that every `to` field must be `agent:session`. Update TOOLS.md bridge reply convention to use `"to": "cc-mini:default"` or the actual session name.

Pro: precise delivery, no ambiguity.
Con: Lēsa has to know which CC session sent the original message, and she may not. Breaks the simple "reply to cc-mini" convention.

### Option 3: Read session from the original message

When replying, Lēsa should copy the `from` field of the original message as her `to`. If CC sent `"from": "cc-mini:default"`, Lēsa replies with `"to": "cc-mini:default"`.

Pro: precise delivery, no convention change needed for the fallback.
Con: requires Lēsa to track the original sender. Doesn't fix existing replies.

### Recommended

**Option 1 + Option 3.** Relax the matching so existing addresses work, AND update the reply convention so new replies include the session. Both layers of safety.

## Fix needed

1. **Code:** Update `messageMatchesSession` in `src/bridge/core.ts` to treat agent-only addresses as broadcasts
2. **Convention:** Update TOOLS.md bridge reply rule to use `"to": "<original-from-field>"` whenever possible
3. **Tests:** Add tests for agent-only addresses, fully-qualified addresses, and broadcasts
4. **Telemetry:** Log when a message is skipped during drain so future mismatches are visible

## Files involved

- `src/bridge/core.ts` (line 270, `messageMatchesSession`)
- `src/bridge/mcp-server.ts` (bridge tool definitions)
- `~/.openclaw/workspace/TOOLS.md` (Lēsa's bridge reply convention)
- Test file location TBD

## Related

- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` ... original bridge plan
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md` ... async inbox plan, parent of this bug
- Apr 10 bridge test (this conversation): both directions fail to deliver
