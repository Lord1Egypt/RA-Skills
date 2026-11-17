---
title: "Remote Control browser send can race attach and call turn/steer without an active turn"
status: open
priority: P1
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-06
---

# Remote Control Send Races Attach And Steer

## Problem

After a live relink during the pair-status poll-token validation, the browser attached to the Remote Control session, but the first browser-originated send surfaced:

```text
error: no active turn to steer
```

After the session settled, later browser and TUI sends worked normally in the same thread.

This points to a startup or attach race in the daemon send path:

- browser connects,
- daemon is paired,
- thread attach is still settling or active-turn state is stale,
- first browser send calls `turn/steer`,
- Codex has no active turn to steer,
- user sees an error before normal sends recover.

## Current Evidence

Observed during pair-status poll-token live validation on 2026-05-06:

- installed daemon was `wip-codex-remote-control@0.0.2-alpha.15`,
- `codex-daemon status` reported running and paired,
- no stray `codex-daemon link` process was running,
- first browser send after reconnect showed `error: no active turn to steer`,
- subsequent browser sends worked,
- TUI to browser and browser to TUI co-presence recovered after the session settled.

## Expected Behavior

The first browser send after fresh attach or reconnect should not produce `no active turn to steer`.

The daemon should either:

- wait until attach readiness and active-turn state are known, or
- use `turn/start` when no active turn is known.

`turn/steer` should only be used when the daemon has a specific active turn id that is still valid for the attached thread.

## Acceptance

- Sending immediately after a fresh browser attach does not produce `no active turn to steer`.
- Sending immediately after relink/reconnect does not produce `no active turn to steer`.
- Browser sends still use `turn/steer` only when there is a known active turn to steer.
- Normal browser to TUI and TUI to browser co-presence still works.
- Stop behavior is unchanged.

## Non-Goals

- Do not change pair-status poll-token behavior here.
- Do not change hosted relay tenancy here.
- Do not redesign Remote Control frontend state here.
