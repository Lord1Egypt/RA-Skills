---
title: "Remote Control refresh must hydrate existing thread history"
status: open
priority: P0
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Refresh Hydration

## Problem

Opening or refreshing `/codex-remote-control/<threadId>` attaches to the live thread, but the page can render blank except for connection diagnostics:

```text
connected. running e2ee handshake...
encrypted channel ready (e2ee-v1).
attached to thread 019dfa1e-0c3... (already in memory).
```

That is not acceptable now that one-browser co-presence works. The browser must show the current thread transcript after reload, not only new events that arrive after attach.

## Current Evidence

Known working thread:

```text
019dfa1e-0c3d-7f01-86b9-9a22cd452bde
```

Manual smoke proved:

- Browser to visible TUI works.
- Visible TUI to browser works.
- Both use the same thread id.
- The daemon is using the TUI App Server socket, not the old SDK runner path.

Refresh still fails the product contract because the page can attach cleanly but show no previous chat history.

## Expected Behavior

When the browser opens or refreshes the Remote Control URL:

1. Connect E2EE relay.
2. Attach to the thread.
3. Fetch persisted thread turns through the daemon's App Server client.
4. Render existing user and Codex messages before or alongside live attach state.
5. Continue streaming new live events after hydration.

The page must not silently present an empty chat as if the session had no history.

## Likely Implementation

Use the TUI-owned App Server socket through the daemon.

On `session.attach`, after `initialize` and `thread/resume`, fetch either:

- `thread/read` with full turn history, or
- `thread/turns/list` if that is the preferred paginated surface.

Then emit a daemon protocol message to the browser such as:

```text
session.history
```

or reuse a documented existing event shape if one already exists.

The browser should render hydrated turns once, then append live `session.event` updates.

## Acceptance

- Open a Remote Control URL for a thread that already has visible TUI/browser messages.
- Refresh the browser page.
- Existing user messages render without sending a new prompt.
- Existing Codex assistant messages render without sending a new prompt.
- The thread title and UUID still render in the header.
- Live browser to TUI and TUI to browser still work after hydration.
- If hydration fails but live attach succeeds, show a visible warning instead of a blank transcript.

## Non-Goals

- Do not touch the Codex fork unless App Server lacks a needed history API.
- Do not implement JSONL tailing as the primary history source.
- Do not redesign the chat UI in this ticket.
- Do not solve multi-browser fanout in this ticket.

