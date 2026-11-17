---
title: "Remote Control WebSocket abuse limits: review follow-ups"
status: open
priority: P2
owner: Hardening Cody
repo: wip-ldm-os-private
created: 2026-05-12
source_review: 2026-05-12 Hardening CC review of wip-ldm-os-private#908
parent_ticket: 2026-05-05--codex--remote-control-websocket-frame-abuse-limits.md
parent_pr: wipcomputer/wip-ldm-os-private#908
---

# Remote Control WebSocket Abuse Limits: Review Follow-Ups

PR #908 shipped the browser-side WebSocket abuse limits and passed Hardening CC review with `PASS WITH NITS`. Eight findings were surfaced. Two (tumbling-window behavior, idle-close bound) are getting documented in the same PR's TECHNICAL.md. Two roll into existing master-plan items. The remaining four are tracked here.

This ticket exists so PR #908 can merge + alpha-22 + hosted deploy + smoke without holding the parent ticket open on follow-up-grade items.

## Background

- Parent ticket: `2026-05-05--codex--remote-control-websocket-frame-abuse-limits.md`
- Parent PR: `wipcomputer/wip-ldm-os-private#908` (Hardening Cody)
- Review: 2026-05-12 Hardening CC PASS WITH NITS
- Master plan reference: item #9 (security gate, invite-list dogfood blocker)

Once parent ticket #9 lands + deploys + smokes, this follow-up ticket inherits the post-deploy hardening work. Each item below is independently shippable.

## Follow-up items

### F1. Kill-switch agents set is frozen at process start (LOW)

`createCodexWsAbuseLimitConfig(process.env)` reads `LDM_CODEX_WS_KILL_SWITCH_AGENTS` once at boot (`server.mjs:58`). Adding an agent to the env requires a PM2 restart to take effect. Slow for live incident response.

**Fix shape:**

- File-watch a JSON file (e.g., `/etc/ldm-codex-ws-killswitch.json`) and reload the agent set on change, or
- Trap `SIGHUP` and re-read the env, or
- Add a privileged operator endpoint (passkey-gated) that pushes the kill list into a runtime-mutable store.

**Acceptance:**

- Operator can add an agentId to the kill-switch without restarting the relay process.
- Newly-added agents are blocked on the next browser frame (4405) and at next upgrade (HTTP 503) within seconds, not at next deploy.
- Removal works symmetrically.

### F2. Cap-check race on simultaneous upgrades (LOW)

`server.mjs:3288-3299` checks `openCodexWebClientsForKey(webKey).length >= maxBrowserSocketsPerThread` before calling `handleUpgrade` and `addCodexWebClient`. Two upgrade requests arriving within microseconds both see the same count and both pass, exceeding the cap by O(concurrent connections).

Bounded and not exploitable for serious abuse, but the cap should be hard.

**Fix shape:**

- Reserve a slot in `codexWebClients` for the (agentId, threadId) key BEFORE handleUpgrade resolves, or
- Make the check + increment atomic via a small reservation counter Map keyed by webKey, or
- Move the cap check inside the handleUpgrade callback so it runs after the new socket is reserved.

**Acceptance:**

- Behavioral test simulates N+1 concurrent upgrades and asserts at most N succeed (no over-cap).
- Existing single-connection happy path unchanged.

### F3. Daemon-side has no abuse limits (LOW)

PR #908 locks down the browser surface only. Daemon WS auth is Bearer `ck-` (single token). A stolen `ck-` attacker can open repeated daemon WS connections to flood the relay's upgrade + identity + policy + close cycle. Items #10 (PR #895) and #7 (PR #893) close fast on a misbehaving daemon, but each cycle still costs CPU.

Different threat model from browser side: the daemon is supposed to be the user's own paired machine. But token theft is the exact scenario items #7 and #10 already model.

**Fix shape:**

- Per-agentId daemon-WS connection-open rate limit (e.g., max N opens per minute), enforced at upgrade.
- Per-agentId `daemon.identity` frequency cap (catches the rapid-reconnect loop pattern).
- Reuse `LDM_CODEX_WS_KILL_SWITCH_AGENTS` for the daemon side (operator can disable a tenant's daemon path too).

**Acceptance:**

- Repeated stolen-`ck-` daemon WS opens at high rate get HTTP 429 / 503 from the upgrade path.
- Legitimate daemon reconnect (single open after backoff) still succeeds.
- Tests cover both shapes.

### F4. `lastActivityMs` is not updated by `observePendingBytes` (NIT)

`codex-relay-ws-abuse-limits.mjs:109-114`: `observePendingBytes` returns a decision but does not touch `lastActivityMs`, while `observeFrame` and `observeMalformed` both do. Doesn't change behavior today because pending-byte rejection closes the WS immediately, but it's an inconsistent contract that could bite a future change.

**Fix shape:**

Update `lastActivityMs = nowMs` (or pass `nowMs` parameter) inside `observePendingBytes`. Symmetrical with the other observers.

**Acceptance:**

- Unit test asserts all four observers refresh `lastActivityMs` on call.

## Folded into other tickets

### F5: behavioral test depth for cap check, upgrade-time kill switch, and pending-byte close

The current test asserts source strings + tests the pure module exhaustively. No behavioral test wires a mock WS through the upgrade handler. Specifically:

- Cap check at the (n+1)th simultaneous upgrade returns HTTP 429.
- Operator kill switch returns HTTP 503 at upgrade.
- Pending byte threshold closes WS with code 4406 before forwarding.

Roll into existing master-plan item #14 (behavioral test depth) rather than a standalone ticket.

### F6: browser-side handling of close codes 4400-4406

When the relay closes a browser WS with an abuse close code, the user sees a silent disconnect with no actionable cause. Same UX shape as the silent-fail gap that master-plan item #11 is already scoped for. Browser should branch on close codes and surface "rate limit triggered" / "session ended" / "temporarily disconnected" in the transcript or presence dot, without violating the plaintext-after-ready guard.

Expand master-plan item #11 scope to include close-code handling for the 4400-4406 range when it's worked.

## Non-goals

- Do not add per-IP rate limiting at this layer. nginx or the front proxy is the right place if needed.
- Do not change the close code numbering once these ship (4400-4406 are now operator-known).
- Do not weaken the existing limits while adding finer-grained controls.

## Closure

This ticket can close when F1, F2, F3, F4 land in private main. F5 and F6 close under their parent master-plan items.
