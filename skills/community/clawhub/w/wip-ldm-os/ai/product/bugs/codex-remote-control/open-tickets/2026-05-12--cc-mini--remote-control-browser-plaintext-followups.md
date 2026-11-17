---
title: "Remote Control browser plaintext follow-ups (UX + defense + close-code handling)"
status: open
priority: P1
owner: Hardening Cody
repo: kaleidoscope-private + wip-codex-remote-control-private (TECHNICAL.md per Rule 6)
created: 2026-05-12
source_reviews:
  - 2026-05-12 Hardening CC review of kaleidoscope-private PR #47 (ticket #6 / master plan item #8 closure)
  - 2026-05-12 Hardening CC review of wip-ldm-os-private PR #908 (master plan item #9 closure)
master_plan_item: 11
parent_tickets:
  - 2026-05-06--codex--remote-control-browser-plaintext-after-e2ee.md
  - 2026-05-12--cc-mini--remote-control-ws-abuse-limits-followups.md (F6)
---

# Remote Control Browser Plaintext Follow-Ups

The browser-side plaintext-after-E2EE guard shipped clean (kaleidoscope PR #47, master plan item #8). The WebSocket abuse limits shipped clean (wip-ldm-os-private PR #908, master plan item #9). The composition of those two surfaces opened five small follow-up items the Hardening CC reviews flagged but that didn't block closing the parent slices.

This is the last security-gate item before invite-list dogfood. Parker-only stays. After this lands + smokes, only item #32 (`ck-` rotation/revocation) blocks public sign-up.

## Background

- Browser-side guard: `kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx` (PR #47, commit `7823935`). Once `e2ee.ready` fires for the current session, plaintext control messages on the outer envelope are dropped by `dropPlaintextAfterE2eeReady`.
- WebSocket abuse limits: hosted relay closes browser sockets with codes `4400-4406` on various abuse signals (PR #908). Browser currently shows a silent disconnect for any of these.
- Master plan item #8: closed 2026-05-12 with live smoke.
- Master plan item #9: closed 2026-05-12 with live smoke and alpha.23 deploy.
- This ticket consolidates: #6-review Findings 1, 3, 4, 5 + #908-review Finding F6 fold-in.

## Scope (five sub-items, one PR per repo)

### S1. Surface terminal `error` after ready (UX regression)

`web/src/app/codex-remote-control/[threadId]/page.tsx:287-291` drops `{type: "error"}` after ready. The relay sends this plaintext when the daemon is offline mid-session and the browser tries to send (`server.mjs:3349-3350`). User sees a silent failed send.

**Fix shape:**
- Carve-out: when `msg.type === "error"` and `msg.session` is absent (matches the existing `e2ee.error` carve-out style), treat as terminal session error and call `fail(...)`.
- OR: in `dropPlaintextAfterE2eeReady`, if `msg.type === "error"`, transition `presence` to `'offline'` so the dot reflects reality.

Either reproduces the pre-fix UX without re-opening the transcript-mutation hole. The carve-out is preferred since it surfaces the message text.

**Acceptance:** With the daemon offline mid-session, attempting a send surfaces a transcript error OR flips presence to offline within one RTT.

### S2. Hoist the post-ready guard above the e2ee branches (defense-in-depth)

`web/src/app/codex-remote-control/[threadId]/page.tsx:241-292`. Today the guard runs as the final fallthrough in `onMessage`. It works because every e2ee branch above it `return`s first. If anyone adds a new branch above without `return`, plaintext leaks through.

**Fix shape:** Restructure `onMessage` so the post-ready check is the outer branch:

```ts
function onMessage(ev) {
  const msg = JSON.parse(ev.data);
  if (e2eeReadyRef.current) {
    if (msg.type === 'e2ee.frame') { /* decrypt + handle */ return; }
    if (msg.type === 'e2ee.error') { /* scoped, fail() if matching session */ return; }
    if (msg.type === 'error' && !msg.session) { /* S1 carve-out */ fail(...); return; }
    dropPlaintextAfterE2eeReady(msg);
    return;
  }
  // pre-ready paths: e2ee.ready / e2ee.error / e2ee.frame guard / handlePlaintextResponse fallback
}
```

**Acceptance:** Behavior unchanged in all existing scenarios. Adding a new branch in the post-ready block defaults to "drop unless explicitly allowlisted."

### S3. Truncate drop-log type to 64 chars

`web/src/app/codex-remote-control/[threadId]/page.tsx:90-95`. `protocolTypeForLog` returns `msg.type` verbatim. Attacker-controlled, unbounded.

**Fix shape:**
```ts
function protocolTypeForLog(msg: Record<string, unknown>): string {
  if (typeof msg.type !== 'string') return '<missing>';
  return msg.type.slice(0, 64);
}
```

**Acceptance:** No log line exceeds 64-char type bound regardless of incoming message.

### S4. Remove redundant `e2eeReadyRef.current = false` in close handler

`page.tsx:540`. Already done by effect cleanup at `:559`. Keep cleanup, drop close-handler reset.

**Acceptance:** Single source of reset; existing reconnect path still works.

### S5. Close-code handling for `4400-4406` (folded from ws-abuse F6)

Relay closes browser WS with one of these codes on abuse:

| Code | Meaning | Browser UX surface |
|---|---|---|
| 4400 | oversized frame | "Connection closed: message too large" |
| 4401 | rate limited (message OR byte rate) | "Connection closed: too many messages or bytes" |
| 4402 | too many sockets for thread | "Too many tabs open for this session" |
| 4403 | idle timeout | "Disconnected (idle). Refresh to reconnect." |
| 4404 | malformed frames | "Connection closed: malformed frames" |
| 4405 | operator disabled | "Remote Control temporarily unavailable" |
| 4406 | pending daemon bytes | "Connection paused: daemon is slow" |

**Fix shape:** In the WS close handler in `page.tsx` (around `:540-541`), branch on `ev.code` and either (a) show a transcript error with the appropriate message, or (b) flip presence to offline with the message as a tooltip. Do NOT auto-reconnect on 4402/4405; do NOT spam reconnects on 4401.

**Acceptance:** Each close code surfaces an actionable UI signal. User can tell why they were disconnected. Logs continue to be metadata-only.

## Paired TECHNICAL.md update (Rule 6)

When this implementation lands, update `wip-codex-remote-control-private/TECHNICAL.md` in the same PR cycle:

- Browser Plaintext Rejection After E2EE section: append a "post-fix UX" paragraph noting that plaintext `error` with no session is now surfaced as a terminal error and that the guard now runs as the outer branch.
- WebSocket Abuse Limits section: append browser-side close-code handling table (codes 4400-4406 with UI surface), and note where the handling lives in `page.tsx`.

## Smoke procedure

Pick markers when implementing:

1. **S1**: kill the daemon mid-session, attempt a send from the browser, verify `RECONNECT_DAEMON_OFFLINE_SURFACED` appears in the transcript or presence flips to offline within 2 seconds.
2. **S2**: regression — existing browser-to-TUI and TUI-to-browser plaintext-after-ready smoke from item #8 still passes (`PLAINTEXT_AFTER_E2EE_BROWSER_TO_TUI`, `PLAINTEXT_AFTER_E2EE_TUI_TO_BROWSER`).
3. **S3**: send a malformed frame with a 200-char `type` field, verify log line is truncated to 64 chars.
4. **S5**: trigger each close code in turn:
   - 4400: send a >256KB frame, verify "message too large" UI.
   - 4401: send 121 frames in a 10s window, verify "too many messages" UI.
   - 4402: open 9 tabs to same thread, verify "too many tabs" on the 9th.
   - 4403: leave a tab idle for >30 min, verify "idle disconnect" UI.
   - 4404: send 4 malformed frames, verify "malformed frames" UI.
   - 4406: induce daemon backpressure (e.g., slow daemon), verify "daemon is slow" UI.

## Test bar

- **A** (automated): regression script in `kaleidoscope-private/web/scripts/` that exercises the new code paths via shape-asserts.
- **B** (behavioral): new test that builds a `MessageEvent`-shaped object, dispatches through the handler, and asserts:
  - plaintext `error` with no session → `fail` is called (S1).
  - plaintext non-error after ready → transcript NOT mutated (existing item #8 contract; S2 hoist preserves this).
  - WS close event with code 4401 → UI signal surfaced.
- **C** (manual three-way smoke): with markers above.

## Non-goals

- Do not weaken the plaintext-after-ready guard.
- Do not auto-reload the page on any close code.
- Do not introduce new outgoing-traffic abuse limits client-side (that's relay-side).

## Closure

This ticket can close when:
- S1-S5 land in `kaleidoscope-private`.
- Paired TECHNICAL.md update lands in `wip-codex-remote-control-private`.
- `A + B + C` test bar met.
- Parker live smoke with the markers above passes.
- Master plan tracker item 11 flips to DONE.

After closure, master plan user-expansion gate clears: invite-list dogfood is unblocked (item #32 is the remaining slice before public sign-up).
