---
title: "Remote Control start command should ensure daemon readiness"
status: open
priority: P1
owner: Hardening Cody
repo: wip-codex-remote-control-private
created: 2026-05-13
source: 2026-05-13 live dogfood observation by Parker
master_plan_item: 35
related:
  - 2026-05-13--cc-mini--remote-control-daemon-stale-online-socket.md (item 34, relay-side fix that this UX depends on)
  - 2026-05-12--cc-mini--remote-control-browser-auto-reconnect-after-tui-restart.md (item 33, adjacent reliability)
build_order: after item 34
---

# Remote Control Start Command Should Ensure Daemon Readiness

P1 product/UX gap. The TUI command `start remote control` returns a browser URL but does not verify the daemon path is healthy. Users get a working URL, click it, and find a spinning page because `codex-daemon` is stopped, unpaired, or rejected by the relay.

This ticket is the UX counterpart to item #34 (relay-side stale daemon heartbeat fix). **Build item #34 first.** Without the relay fix, this UX would have to surface "stale daemon presence on the hosted relay" as a state, which is an awkward thing for the local TUI to explain. With item #34 landed, the local readiness check is straightforward: "is the daemon up + paired + E2EE established?"

## Problem

Today the natural-language entry point `start remote control` does exactly one thing: it calls the Remote Control MCP tool and returns the browser URL for the current Codex thread.

What it does:
- Finds the current Codex thread via `CODEX_THREAD_ID`.
- Calls the MCP tool to mint/return the URL.
- Prints `https://wip.computer/login?next=/codex-remote-control/<threadId>`.

What it does NOT do (and product-wise should):
- Check whether `codex-daemon` is running.
- Start `codex-daemon` if it is stopped.
- Verify the daemon reached `relay-client: e2ee session established`.
- Detect missing pair credentials and instruct `codex-daemon link`.
- Detect relay-side rejection (e.g., `4004 daemon already online`, after item #34 lands this is a stale-presence signal that should clear on its own; before item #34 it required hosted MCP restart).
- Block or annotate the URL until the daemon path is healthy.
- Show progress states like `starting daemon...`, `daemon connected`, or `daemon paired`.

Live evidence today: Parker ran `start remote control`, got a URL, browser spun at bootstrap because `codex-daemon` was stopped. The URL was technically correct; the daemon path was not.

## Expected behavior

`start remote control` performs a daemon-readiness preflight before printing the URL:

1. **Daemon process check.** If `codex-daemon status` shows not running:
   - Start `codex-daemon` (existing `codex-daemon start` path; detached child, no `nohup`).
   - Show progress: `starting daemon...`.
2. **Relay connection check.** After the daemon is running, wait for the daemon's `relay-client: connected` state, bounded (e.g., up to 10 seconds).
3. **Pairing check.** If the daemon reports no pair credentials (no `ck-` token persisted):
   - Stop the preflight.
   - Tell the user: "This daemon is not paired. Run `codex-daemon link` to pair, then run `start remote control` again."
4. **E2EE identity registration check.** Wait for the daemon to register its E2EE pubkey with the relay (the `daemon.identity` accepted state from item #10). Bounded.
5. **Relay rejection handling.** If the relay rejects the daemon's activation with `4003 "daemon key change requires fresh pair"`:
   - Tell the user: "Your daemon E2EE key changed since pairing. Run `codex-daemon link` to re-pair."
   - Stop the preflight.
6. **Output.** Only after the daemon path is healthy:
   - Print the URL as before.
   - Optionally include a one-line `daemon: connected, paired, e2ee ready` status.

If the preflight fails at any step, print the URL with a clearly degraded status (e.g., `URL: <url> (daemon offline: run codex-daemon start)`) OR refuse to print the URL until the user resolves the issue. Pick one based on UX preference; both are defensible. Recommended: print the URL with degraded status so users can still copy/paste it for diagnosis, but make the status line prominent.

## Implementation surface

This lives in the Remote Control MCP tool / skill, in `wip-codex-remote-control-private`. Likely files:

- `src/mcp.ts` or the MCP tool registration that handles the `remote_control` invocation.
- `src/codex-manager.ts` for daemon lifecycle inspection.
- Possibly a new helper in `src/relay-client.ts` to expose "is connected + identity-accepted" state to the calling code.

The MCP tool already has access to local daemon state via `codex-daemon status` and friends. The relay-paired and E2EE-ready signals are observable in the daemon's own logs/state. The preflight is reading existing state, not adding new protocol.

## Acceptance

- Running `start remote control` from the TUI starts `codex-daemon` if it's stopped.
- Preflight reports each state transition (`starting daemon`, `daemon running`, `relay connected`, `e2ee ready`) so the user sees progress.
- URL is only printed as "ready" when the daemon path is healthy.
- If pair credentials are missing, the user gets `codex-daemon link` instructions instead of a misleading URL.
- If the relay rejects with `4003` (changed key), the user gets re-pair instructions.
- If the daemon is rejected with `4004` after item #34 lands, the preflight retries briefly (relay heartbeat will clean up stale presence within the grace window); if still rejected after retry, show "daemon path unhealthy" with a hint.
- No browser spinner caused by a stopped, unpaired, or rejected daemon.
- Preflight does not weaken any relay security (it reads state, does not bypass auth, does not skip pair).
- Preflight is bounded (~10-15s total) so the command doesn't hang.

## Test bar

- **A** automated: unit test the preflight state machine with mocked daemon states (stopped, running but not relay-connected, connected but not pair-registered, fully ready, rejected with 4003, rejected with 4004).
- **B** behavioral: integration test that mocks `codex-daemon status` and the relay-client state, drives the preflight, asserts the right output for each state path.
- **C** manual smoke: with the daemon stopped, run `start remote control`, verify it starts the daemon and prints a healthy URL. Then test the unpaired case and the 4003 case (after manually nuking `~/.codex-daemon/e2ee-key.json`).

## Paired TECHNICAL.md update (Rule 6)

When this lands, update `wip-codex-remote-control-private/TECHNICAL.md`:

- Update the "Runtime Flow" section's "Start Daemon" + "Open Remote Control" sub-sections to reflect the new preflight.
- Add a new section under "Hardening Completed" or "What Is Built" describing the daemon-readiness preflight, its state machine, and the bounded timeout.

## Smoke procedure

Marker prefix: `START_READINESS`.

1. Stop `codex-daemon` if running. Run `start remote control`. Verify:
   - Preflight prints `starting daemon...`.
   - Daemon comes up.
   - URL is printed with healthy status.
   - Browser bootstrap succeeds (no spinner).
   - Send `START_READINESS_BROWSER_TO_TUI`, verify in TUI.
2. Stash `~/.codex-daemon/credentials.json` (or whatever holds the `ck-`). Run `start remote control`. Verify:
   - Preflight detects unpaired state.
   - Output instructs `codex-daemon link`.
   - URL is NOT printed as ready (or printed with degraded status).
   - Restore credentials, re-run, healthy.
3. With daemon running and paired, run `start remote control`. Verify:
   - Preflight passes within a few seconds.
   - URL printed with healthy status.
   - No regression in the normal happy path.
4. (After item #34 lands) Simulate stale daemon presence (`kill -STOP` then `kill -CONT` once heartbeat clears). Run `start remote control`. Verify:
   - Preflight detects the brief `4004` rejection.
   - Retries within the heartbeat grace window.
   - Succeeds without manual intervention.

## Non-goals

- Do not change the relay's auth, pair, or E2EE contracts.
- Do not auto-run `codex-daemon link`. That requires user presence (passkey ceremony). Always instruct, never automate.
- Do not background-restart `codex-daemon` if the user explicitly stopped it via `codex-daemon stop` (would need a sentinel; in v1, just respect the user's stop intent or ignore that case).
- Do not weaken the security boundary by reporting "ready" when E2EE handshake hasn't completed.
- Do not block on item #11 (browser plaintext follow-ups). Different surface.

## Build order

1. **Item #34** (relay-side stale daemon heartbeat fix) — must land first so the `4004` retry path in step 6 above has somewhere to recover to.
2. **Item #35** (this ticket) — start command UX.

After both: `start remote control` in the TUI does the right thing end-to-end. User runs one command, gets a healthy URL with a clear status, no surprises.

## Closure

This ticket can close when:
- Preflight lands in `wip-codex-remote-control-private`.
- Paired TECHNICAL.md update lands.
- A + B + C test bar met.
- Parker live smoke with the markers above passes.
- Master plan tracker item 35 flips to DONE.
