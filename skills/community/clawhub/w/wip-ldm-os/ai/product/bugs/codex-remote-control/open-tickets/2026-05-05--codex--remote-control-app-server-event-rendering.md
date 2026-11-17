---
title: "Remote Control should render App Server events as chat, not raw debug payloads"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-05
---

# Remote Control App Server Event Rendering

## Problem

After the App Server backend started working, the browser UI began showing raw App Server payloads as chat content.

Observed browser content:

```text
USER_MESSAGE
{
  "type": "user_message",
  "text": "does it mirror?"
}
REASONING
```

The product should show user and Codex messages as normal chat bubbles. Raw event names and JSON payloads are useful diagnostics, but they should not be the primary chat UI.

## Current Green Baseline

Do not treat this as a transport failure. Co-presence is working for one browser:

- Browser input lands in the visible TUI.
- TUI input lands in the browser.
- The shared thread id is correct.

This ticket is about rendering the App Server event stream correctly.

## Expected Behavior

Render product-level chat events:

- Browser-originated user messages as user bubbles.
- TUI-originated user messages as user bubbles.
- Codex assistant output as assistant bubbles.
- Relevant command output or errors as secondary but readable content.
- Turn completion as small status text, not a large bubble.

Render diagnostics as muted inline separators:

- connected. running e2ee handshake...
- encrypted channel ready (e2ee-v1).
- attached to thread ...
- turn complete
- disconnected (code ...)

Do not show raw JSON payloads by default.

## Likely Implementation

Add a browser-side event normalization layer for App Server notifications and daemon events.

Map known App Server payloads into UI message models before rendering.

Keep an optional debug mode later if needed, but default Remote Control should not look like a protocol console.

## Acceptance

- Browser message `does it mirror?` renders once as a user bubble.
- The raw `USER_MESSAGE` heading does not appear in normal mode.
- The raw JSON object does not appear in normal mode.
- Codex response renders as an assistant bubble.
- `REASONING` does not appear as a giant empty chat item.
- `turn complete` renders as a small muted diagnostic separator or disappears after a newer meaningful event.
- Existing one-browser co-presence still works.

## Related

This overlaps visually with:

`2026-05-05--codex--remote-control-ui-cleanup.md`

Keep this ticket focused on event normalization and message rendering after the App Server backend change.

