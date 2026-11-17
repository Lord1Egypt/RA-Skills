---
title: "Remote Control must support multiple browser peers per thread"
status: done
priority: P0
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
completed: 2026-05-05
---

# Remote Control Multi-Browser Fanout

## Problem

One visible Codex TUI plus one browser now works. Opening the same Remote Control URL in a second browser tab or device displaces the first browser.

Observed behavior:

- Browser A opens the URL and turns green.
- Browser B opens or refreshes the same URL.
- Browser B turns green.
- Browser A turns red or disconnects.
- Disconnect can show close code `4000`.

This violates the v1 product contract: every tab opened to the same URL is a peer view of the same session.

## Current Green Baseline

The following is proven for one browser:

- Browser to TUI works.
- TUI to browser works.
- Same thread id is used.
- App Server backend is the right path.
- The old split-brain SDK runner problem is fixed.

Do not regress that.

## Expected Behavior

Multiple browsers should attach as subscribers to one shared backend.

Desired shape:

```text
threadId
  backend: one TUI App Server client
  browsers: Set<WebSocket>
```

Not:

```text
browser socket
  owns backend
```

A new browser subscriber must not replace the existing browser subscriber or recreate the backend unnecessarily.

## Likely Implementation

Replace any effective `threadId -> one web socket` ownership with `threadId -> set of web sockets`.

Broadcast session events to all browser sockets in the set.

On browser close:

- remove only that socket,
- keep other browser sockets connected,
- keep the shared App Server/TUI backend alive,
- do not kill or detach the TUI.

If the last browser closes, the daemon may detach browser-side subscriptions, but it must not stop the visible TUI session.

## Acceptance

- [x] Open the same Remote Control URL in two browser tabs.
- [x] Both stay connected and green.
- [x] Browser A sends a message. Browser B and the TUI both show it.
- [x] Browser B sends a message. Browser A and the TUI both show it.
- [x] The TUI sends a message. Both browser tabs show it.
- [x] Closing Browser B does not disconnect Browser A.
- [x] Refreshing Browser B reattaches successfully.
- [ ] Stop from either browser interrupts the shared App Server turn and both browsers reflect the state. Tracked separately in `2026-05-05--codex--remote-control-stop-shared-state.md`.

## Completion Evidence

Live dogfood on 2026-05-05 completed the multi-browser fanout slice:

- Browser A sent `BROWSER_A_TO_ALL`. The TUI received it.
- Browser B sent `BROWSER_B_TO_ALL`. The TUI received it.
- TUI sent `TUI_TO_BOTH_BROWSERS`. Both attached browser views received the shared thread output.
- Closing Browser B did not kill Browser A.
- Refreshing Browser B reattached successfully.
- Relink completed after hosted reload: paired as `parker-smoke-test`, relay key saved.

The Stop behavior remains the next isolated slice, not part of this ticket's completion.

## Non-Goals

- Do not touch Codex for this bug.
- Do not change passkey login.
- Do not redesign the UI.
- Do not solve multiple simultaneous Codex TUI sessions here. That belongs to the per-session socket or broker ticket.
