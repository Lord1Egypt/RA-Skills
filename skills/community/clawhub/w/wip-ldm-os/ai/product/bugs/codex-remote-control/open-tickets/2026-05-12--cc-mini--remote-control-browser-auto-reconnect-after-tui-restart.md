---
title: "Remote Control browser does not auto-reconnect after TUI/App Server restart"
status: open
priority: P1
owner: Hardening Cody / Remote Control UI
repo: kaleidoscope-private / wip-codex-remote-control-private
created: 2026-05-12
source: 2026-05-12 live observation during PR #908 (WebSocket abuse limits) smoke prep
master_plan_item: 33
---

# Remote Control Browser Does Not Auto-Reconnect After TUI/App Server Restart

Reconnect-resilience bug observed during smoke prep for item #9 (WebSocket abuse limits). Not a #9 regression. Filed separately so #9 can ship.

## Observed

1. Parker exits the Codex TUI and restarts it.
2. The new TUI process responds to input normally (TUI side is fine).
3. Already-open browser Remote Control tabs do NOT show new TUI output.
4. The browser tabs appear connected (no "disconnected" indicator).
5. Manual browser refresh re-bootstraps, re-attaches, and the thread becomes live again.

Parker's words: "if I exit the TUI and restart, it disconnects, but it's not disconnected because when it refreshes, I see it."

## Diagnosis (best guess, to be confirmed)

- Browser WS to relay stays open after TUI restart (relay doesn't close it, since the relay socket is browser-to-relay, not browser-to-TUI).
- Browser's E2EE session keys to the daemon also remain valid.
- But the daemon's internal subscription to the TUI's App Server session breaks when the TUI restarts, so daemon emits no further events from the old session id to the browser.
- New TUI process re-attaches to its own App Server session, but the browser is still bound to the old session id and never re-runs `session.attach` against the new one.
- Result: browser sees no events, no errors, no obvious failure ... just silent inertness until refresh.

## Expected

- Browser detects stale upstream state after daemon/App Server/TUI restart within a short window (seconds, not "until next refresh").
- Browser automatically re-bootstraps and re-attaches without manual refresh.
- Existing thread id in the URL remains usable.
- Composer reflects accurate online/offline state.

## Possible fix surfaces (pick one or combine)

### Option A: daemon-driven session invalidation
When the daemon detects its App Server subscription ended (TUI process gone, session closed), the daemon emits an encrypted `session.invalidated` frame to all subscribed browsers for that session id. Browsers receiving this trigger a full re-bootstrap and re-attach against the URL's thread id.

Pros: explicit signal, fast, no client-side polling.
Cons: requires daemon protocol addition; encrypted frame so it survives plaintext-after-ready guard.

### Option B: browser-side heartbeat/timeout
Browser maintains a "last event received" timer. If no events arrive for N seconds AND the user has activity (focus, typing) OR a periodic ping, browser proactively re-bootstraps.

Pros: client-side only, no daemon protocol change.
Cons: timing trade-off (too aggressive = unnecessary re-bootstraps; too lax = same UX).

### Option C: ping/pong on the encrypted channel
Daemon and browser exchange periodic encrypted pings. Missed pings trigger browser-side re-bootstrap.

Pros: confirms both ends of the E2EE channel are live, not just the relay WS.
Cons: requires daemon protocol addition, more code than A.

**Recommended:** Option A (daemon-driven invalidation) as primary, Option B (browser-side timeout) as a backstop for cases where the daemon itself crashed and can't emit the invalidation.

## Acceptance

- After TUI/App Server restart, a still-open browser tab automatically re-bootstraps and re-attaches within 10 seconds.
- New TUI output appears in the previously-open browser tab without manual refresh.
- Phone client behaves the same way.
- Existing manual-refresh path still works.
- No regression in `WS_ABUSE_LIMITS_BROWSER_TO_TUI` / `WS_ABUSE_LIMITS_TUI_TO_BROWSER` / phone-to-TUI smoke.
- Regression test (behavioral) covers the auto-reattach path.

## Smoke procedure (for the fix)

Pick markers when fixing:

1. Open browser Remote Control tab for thread A; confirm encrypted attach.
2. Send `RECONNECT_BEFORE_RESTART_BROWSER_TO_TUI` from browser; verify in TUI.
3. Send `RECONNECT_BEFORE_RESTART_TUI_TO_BROWSER` from TUI; verify in browser.
4. Exit TUI, restart, attach to the same thread.
5. WITHOUT refreshing the browser tab, send `RECONNECT_AFTER_RESTART_TUI_TO_BROWSER` from the new TUI.
6. Verify the browser tab shows the new message within ~10 seconds.
7. WITHOUT refreshing, send `RECONNECT_AFTER_RESTART_BROWSER_TO_TUI` from the browser; verify in TUI.
8. Repeat from a phone client.

## Non-goals

- Do not change the relay's transport role. The relay should not become a session authority for "did the TUI restart."
- Do not weaken the plaintext-after-ready guard. If Option A is used, the invalidation frame must ride inside `e2ee.frame`.
- Do not auto-reload the browser page. Just re-do the bootstrap + attach within the existing page.

## Related

- Master plan item #17 (Refresh hydration) ... separate but adjacent: that ticket is about what refresh shows; this ticket is about the no-refresh case.
- Master plan item #11 (Browser plaintext follow-ups) ... separate but adjacent: that ticket surfaces silent-fail signals via close codes; this ticket fixes a different silent-fail (stale tab after restart).
- This ticket was first hinted at on 2026-04-24 in earlier dogfood notes ("browsers are disconnecting and having to refresh"). Formal filing happens now because it surfaced during #9 smoke prep.

## Closure

This ticket can close when the auto-reattach behavior is shipped, the smoke markers above pass, and a behavioral regression test pins the auto-reattach path. Master plan tracker item #33 flips to DONE at the same time.
