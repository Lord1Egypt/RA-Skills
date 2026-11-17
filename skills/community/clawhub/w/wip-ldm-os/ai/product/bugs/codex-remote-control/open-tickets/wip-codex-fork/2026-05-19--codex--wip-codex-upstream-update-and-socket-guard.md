---
title: "WIP Codex must track upstream Codex updates and avoid stale app-server socket breakage"
status: open
priority: P0
owner: WIP Codex Cody
repo: openai-codex-private / wip-codex-remote-control-private
created: 2026-05-19
surface: WIP Codex fork / Codex App Server / Remote Control co-presence
---

# WIP Codex Upstream Update And App-Server Socket Guard

## Problem

After updating stock Codex to `codex-cli 0.131.0`, starting `codex` failed with:

```text
Error: thread/start failed during TUI bootstrap: thread/start response decode error: missing field `sessionId`
```

Diagnosis showed a stale unmanaged WIP Codex process had been holding the shared Codex app-server control socket:

```text
~/.codex/app-server-control/app-server-control.sock
```

The stale process was:

```text
codex-wip resume 019dfa1e-0c3d-7f01-86b9-9a22cd452bde
```

started on 2026-05-12 at 14:43. Killing that stale `codex-wip` process cleared the owner. A stale socket file could still remain with no process listening, which makes the next Codex startup hit connection refused or decode errors.

This is not a Codex Remote Control package uninstall problem. It is a WIP Codex fork and app-server lifecycle problem.

## Why This Matters

Remote Control co-presence currently depends on the WIP-patched Codex fork. But Parker also updates and runs stock Codex.

That means two things must be true:

1. WIP Codex must stay close enough to upstream Codex that the fork speaks the same app-server protocol shape as the installed stock Codex.
2. WIP Codex must not leave unmanaged app-server state that breaks stock `codex` after an upstream update.

The product contract is: WIP Codex can add co-presence behavior, but it cannot poison the shared Codex local state for normal Codex use.

## Part A: Upstream Version Tracking

When stock Codex updates, the WIP Codex fork needs an explicit rebase/update gate.

### Required behavior

- Detect the locally installed stock Codex version, for example `codex --version`.
- Detect the WIP Codex fork build/version.
- Warn when `codex-wip` is behind the installed stock Codex version or upstream protocol baseline.
- Keep a documented process for rebasing WIP Codex onto the current upstream Codex release.
- Run the WIP co-presence patch tests after every rebase.

### Acceptance

- A documented WIP Codex rebase checklist exists.
- A local diagnostic command or script reports:
  - stock Codex version;
  - WIP Codex version or upstream base commit;
  - whether the WIP fork is known-compatible with that stock version.
- The install or dogfood path tells Parker when WIP Codex needs to be updated after stock Codex changes.
- Remote Control docs stop treating WIP Codex as a static one-time fork.

## Part B: App-Server Socket Ownership And Cleanup Guard

WIP Codex must not leave stale unmanaged app-server sockets that break stock Codex bootstrap.

### Required behavior

- Before `codex-wip` starts or resumes, inspect the app-server control socket path.
- If the socket exists and is owned by a live WIP Codex process, reuse or manage it intentionally.
- If the socket exists and is owned by a stock Codex or Codex.app process, do not steal it silently.
- If the socket exists but has no listener, treat it as stale IPC state and clean it up or surface a precise repair message.
- On clean exit, WIP Codex should release the socket cleanly.
- On crash or stale state, the next start should repair or fail with actionable instructions.

### Acceptance

- Starting stock `codex` after a stale `codex-wip` process no longer fails with `missing field sessionId`.
- `codex-wip` can detect a stale `~/.codex/app-server-control/app-server-control.sock` with no owner and recover safely.
- `codex-wip` does not kill active stock Codex, Codex.app, or unrelated Codex sessions without explicit confirmation.
- Diagnostic output names the owning process and PID before any disruptive action.
- A test or scripted smoke covers:
  - no socket;
  - live WIP-owned socket;
  - live stock-Codex-owned socket;
  - stale socket file with no listener.

## Suggested Fix Shape

Prefer a small guard layer around app-server startup/resume:

1. Check `~/.codex/app-server-control/app-server-control.sock`.
2. Run an owner probe equivalent to:

```bash
lsof -nP ~/.codex/app-server-control/app-server-control.sock
```

3. If no owner exists, remove only the stale socket file, not any package, repo, credentials, sessions, or Remote Control state.
4. If owner exists, classify it:
   - `codex-wip`: WIP-owned, safe to reuse or manage under WIP rules;
   - stock `codex` or `Codex.app`: do not disrupt without explicit user action;
   - unknown: fail with diagnostic instructions.
5. Add a command or diagnostic mode that prints the current app-server socket owner and whether WIP Codex considers it safe.

## Non-Goals

- Do not delete `~/.codex` session history.
- Do not delete `~/.codex-daemon` credentials or E2EE state.
- Do not uninstall Codex Remote Control.
- Do not kill random Codex processes without identifying the PID and socket ownership.
- Do not move WIP Codex logic into the hosted relay.

## Validation Evidence To Capture

- `codex --version` after stock update.
- WIP Codex upstream base or version.
- App-server socket owner before and after the guard:

```bash
lsof -nP ~/.codex/app-server-control/app-server-control.sock
```

- A failed-before, fixed-after startup transcript for stock `codex`.
- A successful `codex-wip resume <thread-id>` transcript after the guard.

