---
title: "Remote Control UI cleanup: /demo chat style without footer"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-05
---

# Remote Control UI Cleanup

## Scope

Remote Control UI must match the /demo chat style, but without the /demo marketing footer.

Scope:
- Use /demo as the visual reference for the chat: centered narrow column, Kaleidoscope header, message bubbles, bottom composer.
- Do not render the global /demo footer in Remote Control on mobile or desktop.
- Remove footer content from the chat interface entirely:
  - WIP Computer, Inc.
  - Learning Dreaming Machines
  - Copyright / Privacy / Terms
  - Are you an AI Agent?
  - Made in California.
- On mobile, the footer currently appears stuck near the top. Do not reposition it. Remove it from Remote Control.
- Keep the composer fixed/anchored at the bottom with safe-area padding.
- The chat area should scroll independently above the composer.

## Status Diagnostics

Remote Control status events should not look like chat messages.

Status lines:
- connected. running e2ee handshake...
- encrypted channel ready (e2ee-v1).
- attached to existing thread ...
- turn complete (...)
- disconnected (code ...)

Behavior:
- Render these as inline diagnostic/status separators between chat bubbles.
- They should be small, muted, centered, and visually secondary.
- They should not occupy large bubble cards.
- They may auto-fade or collapse after a short delay once the next meaningful chat event appears.
- If they remain visible for now, keep them inline between bubbles, not as primary content.

Chat bubbles only:
- User messages
- Codex assistant messages
- Command output or errors when relevant

So the Remote Control UI rule is: chat is the main surface; connection and turn lifecycle events are lightweight diagnostics between messages.

## Visual Reference

Use `/demo` as the visual reference:
- centered narrow column
- Kaleidoscope header
- message bubbles
- bottom composer
- no debug-console feel

Remove from Remote Control chat entirely:
- WIP Computer footer
- Learning Dreaming Machines
- Copyright / Privacy / Terms
- Are you an AI Agent?
- Made in California.

## Out Of Scope

Separate transport bug:
Remote Control currently attaches and browser-originated turns work, but terminal-originated turns do not live-mirror into the browser. That needs transcript hydration plus live session mirroring, not just UI work.

That belongs to `2026-05-05--codex--remote-control-live-transcript-sync.md`.

Account/passkey identity clarity belongs to `2026-05-05--codex--remote-control-account-passkey-clarity.md`.

## Acceptance

- Remote Control uses the `/demo` chat layout as its reference.
- The global `/demo` footer is absent on desktop and mobile.
- Footer text listed above does not appear anywhere inside the Remote Control chat interface.
- The composer is anchored at the bottom with safe-area padding.
- Messages scroll independently above the composer.
- Status lifecycle text renders as small centered diagnostics between bubbles, not as primary chat cards.
- User messages, Codex assistant messages, and relevant command output/errors remain the only bubble content.
