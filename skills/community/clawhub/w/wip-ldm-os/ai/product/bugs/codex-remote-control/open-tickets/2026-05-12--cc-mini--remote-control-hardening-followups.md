---
title: "Remote Control hardening master plan (single ordered list)"
status: open
priority: P0
owner: cc-mini partner / Cody
repo: wip-ldm-os-private / wip-codex-remote-control-private / kaleidoscope-private
created: 2026-05-12
supersedes:
  - "the original implementation-order brief sent to Cody (slices 1-15)"
  - "the previous version of this tracker (sections A-F)"
---

# Remote Control Hardening: Master Plan

One ordered list. Everything we have to do, top to bottom. Each item has a test bar so "working" actually means "tested."

## Status legend

- `DONE` ... landed, regression test passing, manual smoke confirmed
- `TESTING` ... landed, test bar in progress
- `READY` ... can be started now
- `BLOCKED` ... waiting on something else in this list
- `DEFERRED` ... own slice, separate sequence

## Test bar legend

Each item lists what "green" means before it moves to `DONE`:

- `A` ... named automated regression script passes (`npm run test:crc-*` or equivalent)
- `B` ... behavioral test (mocked handler dispatch, asserts state change, not just source strings)
- `C` ... manual three-way co-presence smoke: TUI <-> browser <-> phone, both directions, with the named marker
- `D` ... deploy verification: `/health` healthy + deploy manifest matches

Most security-boundary items need `A + C + D`. Defense-in-depth and tests need `A` or `A + B`. Product polish needs visual smoke.

## User expansion gate

- Items 1-10 + 27 = boundary intact for Parker-only dogfood.
- Item 11 (browser plaintext UX) remains before invite-list dogfood beyond Parker.
- Item 32 (`ck-` rotation) blocks public sign-up.
- Items 36-39 are production-launch hardening from the 2026-05-18 security triage. They do not reopen Parker-only alpha dogfood, but they must be resolved or explicitly dispositioned before calling Remote Control production-secure.
- Item 40 is WIP Codex fork reliability from the 2026-05-19 stock Codex update incident. It does not reopen the relay/E2EE security gate, but it is a P0 dogfood reliability gate for keeping `codex-wip` and stock `codex` compatible on the same machine.

## Recent updates

- **2026-05-19 stock Codex update incident** ... filed item 40. After updating stock Codex to `0.131.0`, a stale unmanaged `codex-wip resume ...` process held the shared app-server control socket and caused stock `codex` bootstrap to fail with `missing field sessionId`. Fix shape: WIP Codex upstream-version tracking plus app-server socket ownership/cleanup guard.
- **2026-05-18 security triage** ... filed items 36-39. Verdict from the private architecture review: current Remote Control is much stronger than the older public relay snapshot, but still alpha-secure rather than production-secure. New tickets capture daemon token redaction, OAuth token-mint session proof, public mirror hardening parity, and dependency audit cleanup.
- **2026-05-13** ... filed item 35: `start remote control` should ensure daemon readiness. UX gap surfaced by the live dogfood that found item #34. Today the command returns a URL but doesn't preflight daemon-up, relay-paired, or E2EE-ready states. Fix shape is a bounded preflight in the MCP tool. Build after item #34 so the 4004 retry path has somewhere to recover to.
- **2026-05-13** ... filed item 34: stale daemon socket blocks legitimate reconnect. Regression from item #10's duplicate-online guard, which checks `readyState === OPEN` but has no liveness detection. Observed in live dogfood: relay rejects real daemon reconnects with `4004` while the stale entry sits forever. Fix shape is daemon WS ping/pong heartbeat.
- **2026-05-12 PR #915** ... filed item 33 as a new reliability bug discovered during PR #908 smoke prep: browser tabs do not auto-reattach after TUI/App Server restart. Not a #908 regression. Separate fix surface.
- **2026-05-12 live smoke** ... closed item 8. Browser plaintext rejection after E2EE ready stayed compatible with normal encrypted Remote Control traffic. Parker verified browser to TUI, TUI to browser, and phone to TUI markers in the same live thread with no relogin loop, stuck composer, or raw plaintext event in transcript.
- **2026-05-12 PR #908 / alpha.23 / hosted deploy** ... closed item 9. WebSocket abuse limits shipped to hosted relay, deploy manifest verified `25 ok, 0 mismatched` including `codex-relay-ws-abuse-limits.mjs`, `/health` returned Postgres healthy, and Parker live smoke passed after deploy.
- **2026-05-12 PR #895 / alpha.19** ... closed items 10 and 27. Daemon activation deferred behind accepted `daemon.identity` via `activateCodexDaemonWs()`; duplicate daemon on an online tenant rejected with 4004; daemon frames pre-identity rejected with 1008; oversized pubkeys rejected at policy layer.
- **2026-05-12 PR #893 / alpha.18** ... closed item 7 (Finding A) and item H (recovery key log prefix).

---

## The list

### DONE (security boundary)

| # | Title | Source | Closed by | Test bar reached |
|---|---|---|---|---|
| 1 | AgentId tenant boundary | brief #1 | `wip-ldm-os-private` PR #835, #856 / `@wipcomputer/wip-ldm-os@0.4.85-alpha.7` | A + C + D |
| 2 | Pair-status poll token | brief #2 | `wip-codex-remote-control-private` PR #56 (alpha.15) + `wip-ldm-os-private` PR #860 (alpha.8) | A + C + D |
| 3 | E2EE key persistence + reconnect | brief #3 | `wip-codex-remote-control-private` PR #62 (alpha.20) + `wip-ldm-os-private` PR #867 (alpha.10) | A + C + D |
| 4 | E2EE restart regression test | brief #3.2 | `wip-ldm-os-private` PR #871 | A |
| 5 | Daemon thread authority binding | brief #4 | `wip-codex-remote-control-private` PR #68, #69 + `wip-ldm-os-private` PR #881 | A + C |
| 6 | Pair/relink fresh presence | brief #5 | `wip-codex-remote-control-private` + `wip-ldm-os-private` PR #885 + hotfix PR #889 (alpha.17) | A + C + D |
| 7 | Daemon-reconnect pubkey change rejection (Finding A) | review 2026-05-11 | `wip-ldm-os-private` PR #893 / `@wipcomputer/wip-ldm-os@0.4.85-alpha.18` | A + C + D |
| 8 | Browser plaintext rejection after E2EE ready | brief #6 | `kaleidoscope-private` PR #47 + `wip-codex-remote-control@0.0.4-alpha.9`. Live smoke passed on 2026-05-12 with browser to TUI, TUI to browser, and phone to TUI markers in the same encrypted thread. | A + C |
| 9 | WebSocket abuse limits | brief #7 | `wip-ldm-os-private` PR #908 / `@wipcomputer/wip-ldm-os@0.4.85-alpha.23`. Hosted deploy completed, `/health` returned Postgres healthy, deploy manifest verified `25 ok, 0 mismatched`, and Parker live smoke passed after deploy. | A + C + D |
| 10 | Daemon takeover throttling | review 2026-05-12 PR #893 Finding 1 | `wip-ldm-os-private` PR #895 / `@wipcomputer/wip-ldm-os@0.4.85-alpha.19`. Defers daemon activation behind accepted `daemon.identity` via `activateCodexDaemonWs()`; new connection rejected with 4004 when an online daemon already exists; daemon frames before identity rejected with 1008. | A + D |
| 27 | Oversized pubkey policy bound | review 2026-05-12 PR #893 Finding 5 | `wip-ldm-os-private` PR #895 / `@wipcomputer/wip-ldm-os@0.4.85-alpha.19`. `evaluateCodexDaemonReconnectPubkey` rejects `incomingPubkey.length > 1024` with `reason: "invalid_daemon_pubkey"`. | A |

### TESTING

No items currently in `TESTING`.

### READY (in order)

| # | Title | Severity | Test bar required | Ticket / fix shape |
|---|---|---|---|---|
| 11 | **Browser plaintext follow-ups** | P1 (UX + defense) | A + B + C | [`2026-05-12--cc-mini--remote-control-browser-plaintext-followups.md`](2026-05-12--cc-mini--remote-control-browser-plaintext-followups.md). Five sub-items: surface terminal `error` after ready; hoist post-ready guard above e2ee branches; truncate drop-log type to 64 chars; remove redundant ref reset; handle WS close codes 4400-4406 in the browser. |
| 12 | **Daemon UX on 4003 close** | LOW (UX) | A + manual | NEW. Branch on `code === 4003` in `relay-client.ts:281-285`; print user-actionable "run `codex-daemon link` to re-pair"; stop or extend reconnect backoff. File `2026-05-12--cc-mini--remote-control-daemon-4003-rerepair-ux.md` |
| 13 | **Audit table records rejected reconnects + source IP** | LOW (forensics) | A | NEW. Add `rejected`, `reject_reason`, `source_ip` columns to `codex_daemon_e2ee_key_audit`. Write rejection row from `server.mjs:3160-3186`. File `2026-05-12--cc-mini--remote-control-daemon-reconnect-audit-rejections.md` |
| 14 | **Behavioral test depth for three guards** | LOW (test) | A + B | NEW. Behavioral tests for (a) plaintext-after-ready guard, (b) daemon.identity policy server integration, (c) browser invalidation on pair-complete replacement. File `2026-05-12--cc-mini--remote-control-behavioral-test-depth.md` |

### READY (product polish + reliability, after items 11-14)

| # | Title | Severity | Test bar | Ticket |
|---|---|---|---|---|
| 15 | Mobile composer safe area | P0 | manual | [`2026-05-06--codex--remote-control-mobile-composer-safe-area.md`](2026-05-06--codex--remote-control-mobile-composer-safe-area.md) |
| 16 | Stop shared state | P0 | A + C | [`2026-05-05--codex--remote-control-stop-shared-state.md`](2026-05-05--codex--remote-control-stop-shared-state.md) |
| 17 | Refresh hydration | P0 | A + C | [`2026-05-05--codex--remote-control-refresh-hydration.md`](2026-05-05--codex--remote-control-refresh-hydration.md) |
| 18 | Web transcript fidelity + event rendering | P1 | manual | [`2026-05-05--codex--remote-control-web-transcript-fidelity.md`](2026-05-05--codex--remote-control-web-transcript-fidelity.md) + [`2026-05-05--codex--remote-control-app-server-event-rendering.md`](2026-05-05--codex--remote-control-app-server-event-rendering.md) |
| 19 | Status line metadata | P1 | manual | [`2026-05-05--codex--remote-control-web-status-line.md`](2026-05-05--codex--remote-control-web-status-line.md) |
| 20 | Session title freshness | P1 | manual | [`2026-05-05--codex--remote-control-session-title-freshness.md`](2026-05-05--codex--remote-control-session-title-freshness.md) |
| 21 | Patched Codex install path | P1 | manual | [`2026-05-05--codex--remote-control-patched-codex-install-path.md`](2026-05-05--codex--remote-control-patched-codex-install-path.md) |
| 33 | **Browser auto-reconnect after TUI/App Server restart** | P1 (reliability) | A + B + C | [`2026-05-12--cc-mini--remote-control-browser-auto-reconnect-after-tui-restart.md`](2026-05-12--cc-mini--remote-control-browser-auto-reconnect-after-tui-restart.md). After TUI restart, the browser WS stays open and E2EE keys remain valid, but the tab is silently inert until manual refresh because it never re-runs `session.attach` against the new TUI session id. Recommended fix: daemon-driven encrypted `session.invalidated` frame + browser-side reattach, with a browser timeout as backstop. |
| 34 | **Stale daemon socket blocks legitimate reconnect** | P1 (reliability) | A + B + C + D | [`2026-05-13--cc-mini--remote-control-daemon-stale-online-socket.md`](2026-05-13--cc-mini--remote-control-daemon-stale-online-socket.md). Regression from item #10. Relay's duplicate-online guard checks `previous.readyState === OPEN` but has no liveness detection; a stale daemon WS keeps rejecting legitimate reconnect with `4004 "daemon already online"` until hosted MCP restart. Fix: ping/pong heartbeat on daemon WS, terminate stale sockets, preserve the `4004` for real duplicates. **Build before #35.** |
| 35 | **`start remote control` should ensure daemon readiness** | P1 (UX) | A + B + C | [`2026-05-13--cc-mini--remote-control-start-ensures-daemon-readiness.md`](2026-05-13--cc-mini--remote-control-start-ensures-daemon-readiness.md). Today the command returns a URL but does not verify the daemon path is healthy: daemon may be stopped, unpaired, or rejected by relay. Fix: preflight that starts daemon if needed, waits for relay-connected + E2EE-ready, instructs `codex-daemon link` when unpaired, surfaces 4003 (re-pair needed). Build **after #34** so the 4004 retry path can recover via heartbeat cleanup. |

### READY (P2 defense-in-depth + thread-authority test gaps)

| # | Title | Severity | Test bar | Ticket / fix shape |
|---|---|---|---|---|
| 22 | **Browser daemon-key pinning** (Finding D, re-prioritize) | P1 (suggest) | A + B + manual | [`2026-05-06--codex--remote-control-daemon-pubkey-pinning.md`](2026-05-06--codex--remote-control-daemon-pubkey-pinning.md). Include short fingerprint in bootstrap; browser stores prior in `localStorage` keyed by agentId; on change show "daemon identity changed" prompt before opening E2EE. |
| 23 | Two-browser cross-thread no-cross-talk regression | P1 | A + B | [`2026-05-11--codex--remote-control-two-browser-cross-thread-regression.md`](2026-05-11--codex--remote-control-two-browser-cross-thread-regression.md) |
| 24 | Cross-thread interrupt error parity | P2 | A | [`2026-05-11--codex--remote-control-thread-authority-interrupt-error-parity.md`](2026-05-11--codex--remote-control-thread-authority-interrupt-error-parity.md) |
| 25 | E2EE re-hello session-id collision DoS | P2 | A | [`2026-05-11--codex--remote-control-e2ee-session-rehello-collision-dos.md`](2026-05-11--codex--remote-control-e2ee-session-rehello-collision-dos.md) |
| 26 | Persistence ordering + audit-write decoupling | LOW | A + B | NEW. Swap order in `register()` (persist first, then in-memory). Differentiate primary-table failure (1011) from audit-row failure (log + continue). File `2026-05-12--cc-mini--remote-control-daemon-pubkey-persistence-ordering.md` |
| 28 | First-pair fresh-presence comment + fingerprint truncation defense | NIT | source review | NEW. One-line comment at `server.mjs:2872`; align relay and daemon fingerprint format. File `2026-05-12--cc-mini--remote-control-fingerprint-and-first-pair-doc.md` |
| 29 | Local E2EE key file hardening | P2 | A | [`2026-05-05--codex--remote-control-local-e2ee-key-file-hardening.md`](2026-05-05--codex--remote-control-local-e2ee-key-file-hardening.md) |
| 30 | E2EE forward secrecy | P3 | A | [`2026-05-06--codex--remote-control-e2ee-forward-secrecy.md`](2026-05-06--codex--remote-control-e2ee-forward-secrecy.md) |
| 31 | Pair-status real device binding (design call) | LOW/MED | discussion + A | NEW. Either implement signature-over-`pairing_id+timestamp` with daemon E2EE key, or update ticket #2 wording to "single-use poll token." File `2026-05-12--cc-mini--remote-control-pair-status-device-binding.md` |

### READY (production-launch hardening from 2026-05-18 review)

| # | Title | Severity | Test bar | Ticket / fix shape |
|---|---|---|---|---|
| 36 | Daemon CLI token redaction | P1 | A + manual | [`2026-05-18--codex--remote-control-daemon-token-redaction.md`](2026-05-18--codex--remote-control-daemon-token-redaction.md). `codex-daemon status` and foreground start must not print full local control tokens by default. Use fingerprints or redaction instead. |
| 37 | OAuth token mint server-side session + PKCE proof | P0 | A + B | [`2026-05-18--codex--remote-control-oauth-token-mint-session-proof.md`](2026-05-18--codex--remote-control-oauth-token-mint-session-proof.md). Any `ck-` bearer mint path must prove server-side authenticated session and fail closed on missing, mismatched, expired, or replayed PKCE state. |
| 38 | Public mirror hardening parity | P1 | source + deploy audit | [`2026-05-18--codex--remote-control-public-mirror-hardening-parity.md`](2026-05-18--codex--remote-control-public-mirror-hardening-parity.md). Public `wip-ldm-os` relay source must match the hardened hosted relay claims, or release-track policy must explicitly explain intentional lag. No direct public mirror edits. |
| 39 | Dependency audit cleanup | P1 | audit + tests | [`2026-05-18--codex--remote-control-dependency-audit-cleanup.md`](2026-05-18--codex--remote-control-dependency-audit-cleanup.md). Clean or disposition Remote Control dependency advisories before broader launch, including the high `fast-uri` advisory path. |

### READY (WIP Codex fork compatibility + local app-server lifecycle)

| # | Title | Severity | Test bar | Ticket / fix shape |
|---|---|---|---|---|
| 40 | WIP Codex upstream update + app-server socket guard | P0 | A + B + manual | [`wip-codex-fork/2026-05-19--codex--wip-codex-upstream-update-and-socket-guard.md`](wip-codex-fork/2026-05-19--codex--wip-codex-upstream-update-and-socket-guard.md). Track stock Codex updates against the WIP Codex fork, warn on incompatible versions, and ensure `codex-wip` does not leave stale unmanaged app-server socket state that breaks stock `codex` bootstrap. |

### DEFERRED (own slice)

| # | Title | Severity | Why deferred |
|---|---|---|---|
| 32 | `ck-` apiKey rotation / revocation | MED | Broader scope (schema + UI + auth-verify recovery). Must land before public sign-up. File `2026-05-12--cc-mini--ck-apikey-rotation-and-revocation.md` |

---

## Working rules

1. **One PR per numbered item** unless two are mechanically inseparable. State the link if combined.
2. **Test bar must be reached before status flips to DONE.** Mark `TESTING` in this doc when the PR lands; flip to `DONE` only after the named bar is met.
3. **Never combine security-boundary changes with UI polish.** Item 11 (browser plaintext follow-ups) and items 15-21 (polish) stay separate.
4. **Smoke after every slice.** TUI <-> browser <-> phone with the named marker for that slice. Update SHARED-CONTEXT.md with the marker + result.
5. **No new user expansion past Parker** until item 11 lands. No public sign-up until item 32 lands.
6. **Every matrix update has a paired `TECHNICAL.md` update in `wip-codex-remote-control-private`.** This matrix tracks process state. `wip-codex-remote-control-private/TECHNICAL.md` is the source of truth for shipped behavior. Whenever an item in this matrix flips status (especially to `DONE`), or its shipped runtime behavior changes, the matching section in `TECHNICAL.md` gets updated in the same PR cycle or immediately after. The two land together: matrix row + closure evidence + ticket `status: done` + `TECHNICAL.md` section reflecting what now ships. Filing a new ticket does NOT require a `TECHNICAL.md` change; only items moving through the matrix toward `DONE` do. If the implementation PR lives in `wip-ldm-os-private` or `kaleidoscope-private`, the `TECHNICAL.md` update PR in `wip-codex-remote-control-private` is paired and references the implementation PR. Hardening CC review verifies the `TECHNICAL.md` update accuracy as part of closure review, not separately.

## When this doc is done

When items 9-31 are all `DONE` (item 32 has its own ticket and may be in progress), this tracker can be archived. Set `status: done` in frontmatter and add a one-line closure block summarizing what shipped together.

## Quick stats

- Done: 11 (items 1-10, 27)
- Testing: 0
- Ready (security gate, items 11-14): 4
- Ready (product polish + reliability, items 15-21, 33, 34, 35): 10
- Ready (defense-in-depth + nits, items 22-26, 28-31): 9
- Ready (production-launch hardening, items 36-39): 4
- Ready (WIP Codex fork compatibility, item 40): 1
- Deferred: 1 (item 32)
- **Total to land: 29** before this tracker can close.

New tickets to file from this plan: 7 (items 12, 13, 14, 26, 28, 31, 32). Item 27's file is no longer needed (closed without one). Items 11, 33, 34, and 35 were filed by 2026-05-13. Items 36-39 were filed by 2026-05-18. Item 40 was filed by 2026-05-19.
