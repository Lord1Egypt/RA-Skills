---
title: "Remote Control web should show Codex TUI status line metadata"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-05
---

# Remote Control Web Status Line

## Problem

The Codex TUI footer/status line gives critical context about what session the user is controlling.

Example from Parker's visible TUI:

```text
gpt-5.5 high · ~/wipcomputerinc · remote-control--kay--partner
```

The Remote Control web view currently shows title and UUID, but it does not show the equivalent status-line context. On mobile, Parker should still be able to see the model, reasoning effort, working directory, and session title/context that the terminal shows.

## Expected Behavior

Remote Control web should expose the same essential status metadata as the Codex TUI status line.

At minimum:

- model: `gpt-5.5`
- reasoning effort: `high`
- current working directory: `~/wipcomputerinc`
- session title/name: `remote-control--kay--partner`
- thread UUID remains visible

This does not have to be a literal clone of the terminal footer. It should be readable and responsive in the web layout.

## UI Placement

Decision:

- The web status line belongs directly under the session title row.
- On mobile, this means below the tappable title/UUID area where the user can toggle `test` versus the thread id.
- It should sit above the transcript bubbles, not above the bottom composer.
- It should not be a footer/status strip near the input.

Concrete mobile layout:

```text
test
gpt-5.5 high · ~/wipcomputerinc · test-ios-to-macos-cli-codex

[chat transcript starts here]
```

Desktop:

- compact metadata row under the session title and UUID,
- keep the row visually subordinate to the title,
- do not move it to the bottom of the page.

Mobile:

- compact row under the title/UUID toggle,
- allow truncation or tap-to-expand if the line is too long,
- must not collide with the Stop button, browser address bar, or composer safe area,
- must remain visible as session context before the first transcript bubble.

## Data Source

Prefer App Server/session metadata through the daemon rather than guessing in the browser.

Possible sources:

- thread metadata from App Server `thread/read` / loaded thread object,
- model/settings from the active App Server thread/session,
- working directory from thread metadata or daemon attach context,
- session title from `threadName` / Codex thread name.

If a field is unavailable, omit it or show a clear fallback. Do not display stale guessed data.

## Acceptance

- Web Remote Control displays model and reasoning effort for the active session.
- Web Remote Control displays current working directory in compact form.
- Web Remote Control displays session title/name when available.
- UUID remains visible as the stable routing identity.
- Status line appears under the session title/UUID row, above the transcript bubbles.
- Status line does not appear above the bottom composer.
- Refresh preserves the status metadata.
- Mobile layout remains readable and does not overlap Stop or composer controls.
- If status metadata cannot be loaded, the UI shows a small warning or omits the field instead of guessing.

## Non-Goals

- Do not build a session picker.
- Do not replace UUID routing with status-line metadata.
- Do not require exact terminal pixel layout.
- Do not solve title rename freshness here unless the same metadata path makes it trivial.
