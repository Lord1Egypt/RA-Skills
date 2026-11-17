---
title: "Remote Control stale daemon socket blocks legitimate reconnect"
status: open
priority: P1
owner: Hardening Cody
repo: wip-ldm-os-private
created: 2026-05-13
source: 2026-05-13 live dogfood observation by Parker
master_plan_item: 34
related:
  - 2026-05-06--codex--remote-control-daemon-takeover-throttling.md (item 10, regression vector)
  - 2026-05-12--cc-mini--remote-control-browser-auto-reconnect-after-tui-restart.md (item 33, adjacent reliability)
---

# Remote Control Stale Daemon Socket Blocks Legitimate Reconnect

P1 reliability/hardening follow-up. Regression introduced by item #10 (daemon takeover throttling, `wip-ldm-os-private` PR #895 / alpha-19). Closing item #10 was the right security move; this ticket adds the missing liveness cleanup half so legitimate daemon reconnects are not blocked by stale presence state.

This ticket is **not** master plan item #11 (browser plaintext follow-ups), which remains the user-expansion gate item before invite-list dogfood. This ticket is item #34 in the matrix, P1 reliability, adjacent to items #10 and #33.

## Background

Before item #10, when a new daemon connected with the same `ck-` account token, the relay would replace the old daemon socket. That made restarts forgiving, but it also meant a stolen `ck-` could repeatedly kick the real daemon offline (DoS amplified by impersonation in earlier reviews).

Item #10 (PR #895, `server.mjs:3132-3144` `activateCodexDaemonWs`) fixed that by saying: do not let a new daemon evict an already-online daemon until the new daemon proves `daemon.identity`. The duplicate-online guard checks `previous.readyState === previous.OPEN` and rejects the new connection with close code `4004 "daemon already online"` if that's true.

The relay assumes `readyState === OPEN` is sufficient proof that the existing socket is usable. It is not. A daemon socket can sit in `codexDaemons` with `OPEN` state but be effectively dead at the transport layer (TCP half-open, network blip, suspended VM, broken intermediary). The relay has no liveness check that confirms the peer is actually reachable.

## Observed (2026-05-13)

- `start remote control` returned the correct thread URL.
- Browser login succeeded; the Remote Control page kept spinning at bootstrap.
- `https://wip.computer/health` returned healthy with Postgres.
- `codex-daemon status` initially showed not running.
- Starting `codex-daemon` made it dial `wss://wip.computer/api/codex-relay/daemon`.
- Relay accepted the upgrade, then immediately closed the new connection with `4004 "daemon already online"`.
- Daemon reconnected after backoff; relay rejected again. Loop.
- Stopping/restarting `codex-daemon` did not clear the stale entry.
- Re-logging the browser did not clear it.
- This pattern is new since item #10 / alpha-19.

## Root cause

Hosted relay daemon presence has no liveness detection.

- `codexDaemons` is populated only by `activateCodexDaemonWs` (post-`daemon.identity`).
- It is cleared only by the WS close handler (`server.mjs` near `:3203`).
- If the close handler never fires (because the TCP connection wedged silently), the map entry stays forever.
- The duplicate-online guard at `server.mjs:3132-3140` then permanently rejects every reconnect with `4004`.

`readyState === OPEN` is local-side state about the WS API. It does not confirm that the remote peer is still there.

## Expected

- Duplicate **real** online daemons still get rejected with `4004` (item #10's guarantee preserved).
- Stale daemon sockets are detected by an application-layer heartbeat and terminated.
- Terminated stale sockets are removed from `codexDaemons` via the existing close cleanup path.
- A legitimate `codex-daemon` restart can reconnect within seconds, not requiring a hosted MCP restart.
- Browser bootstrap/attach does not spin forever because of stale daemon presence.

## Fix shape

Add hosted relay daemon WebSocket heartbeat/liveness:

1. On daemon activation in `activateCodexDaemonWs`:
   - Start an interval (e.g., 30s) that sends a WS ping to this daemon.
   - Track a `lastPongAt` timestamp; initialize at activation.
2. On `pong` event from the daemon: update `lastPongAt`.
3. In the interval, if `now - lastPongAt > 2 * pingInterval` (one missed pong + grace): call `ws.terminate()` (not `ws.close()`, since `close()` requires a working transport for the close frame).
4. In the existing close handler:
   - Clear the heartbeat interval.
   - Continue removing the entry from `codexDaemons` only if `codexDaemons.get(agentId) === ws` (already in place).
5. Daemon side (`wip-codex-remote-control-private/src/relay-client.ts`): the `ws` library auto-responds to pings with pongs by default; verify no special handling required.
6. Keep `4004 "daemon already online"` for true duplicate live daemons.

Tunable via env:
- `LDM_CODEX_DAEMON_HEARTBEAT_MS` (default 30000)
- `LDM_CODEX_DAEMON_HEARTBEAT_GRACE_MS` (default 60000)

## Acceptance

- Pure-function unit test for the heartbeat decision: given `lastPongAt` older than grace, returns "terminate."
- Integration source-shape test asserts `server.mjs` registers a ping interval per daemon WS and clears it on close.
- Existing duplicate-online guard regression still passes (real duplicate live daemon still gets `4004`).
- New behavioral test: stale daemon WS that never pongs is terminated and removed from `codexDaemons`; a subsequent legitimate reconnect succeeds.
- `node --check src/hosted-mcp/server.mjs` passes.
- Existing Remote Control hardening tests still pass:
  - `npm run test:crc-pair-relink-audit-and-rotation`
  - `npm run test:crc-e2ee-key-persistence`
  - `npm run test:crc-e2ee-session-route`
  - `npm run test:crc-pair-status-poll-token`
  - `npm run test:crc-agentid-tenant-boundary`
  - `npm run test:crc-websocket-abuse-limits`

## Paired TECHNICAL.md update (Rule 6)

When this implementation lands, update `wip-codex-remote-control-private/TECHNICAL.md`:

- In the Pair and Relink Fresh Presence section's "Duplicate reconnect guard" paragraph, add a sentence noting that stale daemon presence is detected via a heartbeat and terminated via `ws.terminate()`, after which a legitimate reconnect succeeds without manual intervention.
- Document the env knobs `LDM_CODEX_DAEMON_HEARTBEAT_MS` and `LDM_CODEX_DAEMON_HEARTBEAT_GRACE_MS`.

## Smoke procedure

Pick marker `STALE_DAEMON_RECOVERY` when implementing:

1. Start `codex-daemon`; verify connected to relay via `codex-daemon status`.
2. Open Remote Control URL; verify `STALE_DAEMON_RECOVERY_BROWSER_TO_TUI` arrives in TUI.
3. Kill `codex-daemon` via `kill -STOP <pid>` (suspended, not SIGKILL — to simulate stale socket).
4. Wait for heartbeat grace window (~60s default).
5. Verify relay PM2 logs show `terminated stale daemon for tenant <id>` or similar.
6. `kill -CONT <pid>` to resume the daemon process.
7. Daemon reconnects within backoff; verify activation succeeds (no `4004`).
8. Browser shows live thread within 10s of daemon reconnect.
9. Send `STALE_DAEMON_RECOVERY_TUI_TO_BROWSER`; verify in browser.

## Test bar

- **A** automated regression: heartbeat decision unit test + source-shape integration test.
- **B** behavioral: mock WS that never pongs, advance fake clock past grace, assert `terminate()` called + map entry removed.
- **C** manual smoke with the markers above.
- **D** hosted deploy verification: `/health` healthy, deploy manifest matches, PM2 logs show heartbeat interval started.

## Non-goals

- Do not weaken the duplicate-online guard from item #10.
- Do not auto-reconnect daemons that are intentionally stopped by the user.
- Do not change `start remote control` behavior. This is a hosted-relay-side fix, not an MCP tool change.
- Do not ping on the browser WS path. That path has its own idle TTL via the WS abuse limits (item #9); daemon and browser sockets have different liveness needs.

## Note on `start remote control`

This is not a `start remote control` bug. `start remote control` only creates or returns the browser URL for the current Codex thread. The architecture:

- `start remote control`: gives browser URL for thread.
- Browser: logs in, bootstraps, opens WebSocket.
- `codex-daemon`: must already be connected to the hosted relay.
- Hosted relay: routes browser frames to the daemon.

The broken layer is hosted relay daemon presence/liveness, between the daemon and the relay. `start remote control` cannot fix this because it does not own the relay's `codexDaemons` map.

## Closure

This ticket can close when:
- Heartbeat lands in `wip-ldm-os-private` `server.mjs`.
- Paired TECHNICAL.md update lands.
- A + B + C + D test bar met.
- Parker live smoke with `STALE_DAEMON_RECOVERY_*` markers passes after deploy.
- Master plan tracker item 34 flips to DONE.

## Matrix placement

- Section: `READY (product polish + reliability)` (same section as #33).
- Severity: P1 (reliability blocker for dogfood).
- Not a user-expansion gate item.
- After this lands, the only gate before invite-list dogfood remains item #11. After both #11 and this land, invite-list dogfood is unblocked from a reliability standpoint.
