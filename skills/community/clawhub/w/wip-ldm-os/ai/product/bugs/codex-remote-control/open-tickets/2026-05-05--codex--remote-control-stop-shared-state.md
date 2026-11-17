---
title: "Remote Control Stop must interrupt shared App Server turn and update all peers"
status: open
priority: P0
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Stop Shared State

## Problem

The App Server backend now supports one-browser co-presence and multi-browser fanout. Stop is now the next isolated product slice.

Stop must interrupt the same live Codex turn that the visible TUI is running. It must not interrupt a parallel runner, and it must not only update the browser state locally.

## Current Green Baseline

Do not regress the proven Remote Control behavior:

- Browser A to TUI works.
- Browser B to TUI works.
- TUI to both browsers works.
- Closing one browser does not kill the other browser.
- Refreshing a browser can reattach successfully.
- Relink completed after hosted reload, but E2EE key persistence is tracked separately.

## Expected Behavior

When a turn is active:

- Stop is enabled in the browser.
- Clicking Stop sends encrypted `session.interrupt`.
- The daemon maps it to App Server `turn/interrupt`.
- The visible Codex TUI turn stops.
- The browser shows interrupted/stopped state.
- Other browser peers, once multi-browser fanout is fixed, show the same state.

When no turn is active:

- Stop is disabled or returns a clear no-active-turn result.
- It must not close the session.
- It must not disconnect the browser.
- It must not require relinking or reloading the page.

## Acceptance

One-browser smoke:

- Start a long-running Codex response from the browser.
- Click Stop in the browser.
- The visible TUI stops the same active turn.
- The browser shows the turn as interrupted or stopped.
- The session remains attached afterward.
- A follow-up browser prompt still works.
- A follow-up TUI prompt still appears in the browser.

After multi-browser fanout:

- Clicking Stop from Browser A updates Browser B.
- Clicking Stop from Browser B updates Browser A.
- Closing one browser does not affect Stop availability in the other browser.

Regression check:

- Browser A can still send after Stop.
- Browser B can still send after Stop.
- The TUI can still send after Stop.
- Refreshing a browser after Stop reattaches to the same live thread.

## Non-Goals

- Do not touch login or pair flow.
- Do not solve raw event rendering here.
- Do not solve transcript hydration here.
