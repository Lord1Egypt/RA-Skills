---
title: "Codex Remote Control Master Ticket"
status: in-flight
priority: P0
owner: Remote Control K Partner (coordination) + Hardening Cody / WIP Codex Cody / Installer Cody (work) + Remote Control CC Partner (review)
repo: wip-ldm-os-private / wip-codex-remote-control-private / openai-codex-private / kaleidoscope-private
created: 2026-05-27
---

# Codex Remote Control Master Ticket

This is the rolling index for Codex Remote Control work. It is **append-only**: tickets get added here, status moves here, and short editorial notes about ordering live here. The individual ticket files in `open-tickets/`, `closed-tickets/`, and `archive/` remain the source of truth for their own scope. This master is the source of truth for **ordering, ownership, and rolling context** across the folder.

The existing hardening plan remains authoritative for the numbered security and reliability sequence:

[`open-tickets/2026-05-12--cc-mini--remote-control-hardening-followups.md`](open-tickets/2026-05-12--cc-mini--remote-control-hardening-followups.md)

This file does not replace that plan. This file sits above it and organizes the entire Remote Control queue by lane: hardening, WIP Codex fork compatibility, co-presence behavior, hosted auth, UI, installer, docs, and launch readiness.

## Folder Standard

Codex Remote Control bugs use this structure:

```text
ai/product/bugs/codex-remote-control/
  ldmos-bugs-masterticket--codex-remote-control.md
  open-tickets/
  closed-tickets/
  archive/
```

- `open-tickets/` contains active bugs that still need implementation, review, verification, or explicit disposition.
- `closed-tickets/` contains bugs that were fixed and should remain easy to find.
- `archive/` contains stale, superseded, or historical bug artifacts.

Do not leave loose bug tickets in the root. The root should contain only the master ticket and folders.

## Why this exists

Remote Control has become a cross-repo product surface. The work now spans:

- `wip-codex-remote-control-private`: daemon, local server, MCP tool, E2EE session handling, TECHNICAL.md.
- `wip-ldm-os-private`: hosted relay, pairing, WebAuthn, OAuth, install rules, tracker docs.
- `openai-codex-private`: patched Codex fork, App Server co-presence, socket lifecycle, upstream rebase work.
- `kaleidoscope-private`: browser UI, login handoff, transcript rendering, mobile layout.

The folder already has many individual tickets and one hardening master plan. What was missing was a folder-level index that answers: what is active, what is blocked, what belongs to which repo, and what should not be conflated.

### 2026-05-27 state

The Parker-only dogfood path is still viable, but the product is not production-secure yet.

The P0/P1 hardening boundary through item 10 in the hardening plan is done. Production-launch hardening items 36-39 remain open. WIP Codex fork compatibility item 40 remains open and is active again because stock Codex moved to `0.134.0` and the WIP fork still needs upstream tracking, socket lifecycle guards, and attached-thread hydration compatibility.

Current implementation signal:

- `wipcomputer/openai-codex-private#17` exists for app-server socket ownership guard work.
- That PR is only part of item 40. It does not by itself close upstream `0.134.0` protocol drift or history hydration failures.
- No direct public repo edits are allowed. Public parity work flows through private repos and `deploy-public`.

## Operating principles

1. **Append-only.** Add rows, move status, and add short editorial notes. Do not rewrite history out of this file.
2. **Keep lanes separate.** Relay/E2EE security, WIP Codex fork compatibility, browser UI, installer behavior, and public mirror parity are different lanes.
3. **One slice per PR.** Combine only when two tickets are mechanically inseparable, and say so in the PR body.
4. **No public repo edits.** Fix private source or release/deploy-public pipeline. Public repos are published output.
5. **Tracker-only changes do not release.** This file and other `ai/` tracker edits merge to private `main` and stop unless Merge/Deploy K explicitly assigns release work.
6. **TECHNICAL.md follows shipped behavior.** Filing a ticket does not require `TECHNICAL.md`. Closing a runtime behavior change usually does.
7. **Alpha validation is allowed when the slice needs an installed artifact.** Beta/stable promotion and deploy-public are separate decisions.

---

## Execution order

### Phase 0: Master indexes and source-of-truth docs

| Ticket | Status | Notes |
|---|---|---|
| `ldmos-bugs-masterticket--codex-remote-control.md` (this file) | in-flight | Folder-level index. Update when lanes move or new tickets are filed. |
| `open-tickets/2026-05-12--cc-mini--remote-control-hardening-followups.md` | open / active source of truth for hardening sequence | Existing ordered list of security, reliability, and production-launch hardening. Do not duplicate its detailed item matrix here. |
| `open-tickets/2026-05-05--codex--remote-control-security-review-lanes.md` | open / P0 | Defines security-review lanes across relay, browser, daemon, fork, and hosted auth. Keep reviewer ownership explicit. |
| `open-tickets/2026-05-05--codex--remote-control-regression-contract.md` | open / P0 | Durable regression contract across daemon, relay, browser, and patched Codex. Pull forward whenever a behavior fix lacks a real test bar. |
| `open-tickets/2026-05-05--codex--remote-control-automated-regression-tests.md` | open / P0 | Cross-repo regression harness. Related to, but broader than, individual item tests in the hardening plan. |

### Phase 1: WIP Codex fork compatibility and upstream drift

**Goal:** `codex-wip` and stock `codex` can coexist on the same machine across upstream Codex updates without breaking app-server bootstrap, attached-thread hydration, or resume behavior.

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/wip-codex-fork/2026-05-19--codex--wip-codex-upstream-update-and-socket-guard.md` | open / P0 | Active. Covers upstream version tracking plus app-server socket ownership. Current evidence after stock Codex `0.134.0`: socket guard alone is not enough; WIP fork also needs upstream protocol and history hydration compatibility. |
| `open-tickets/2026-05-05--codex--wip-codex-fork-upstream-hygiene.md` | open / P0 | Broader fork hygiene. Should either feed into the active item 40 work or be updated after the `0.134.0` rebase decision. |
| `open-tickets/2026-05-05--codex--remote-control-single-global-socket.md` | open / P1 | Older App Server socket limitation. Reassess after item 40's socket guard and upstream rebase work land. |
| `open-tickets/2026-05-05--codex--remote-control-patched-codex-install-path.md` | open / P1 | Clean install path for patched Codex. Depends on deciding how WIP Codex versions advertise upstream base and compatibility. |
| `open-tickets/wip-codex-fork/2026-05-12--codex--wip-codex-exit-resume-hint.md` | open / P1 | UX fix: WIP Codex exit footer should say `codex-wip resume`, not `codex resume`. Keep with fork work. |
| `closed-tickets/2026-05-06--codex--remote-control-codex-only-upstream-branch.md` | done / reference | Clean upstream branch or diff summary exists. Use as reference for future upstream contribution packets. |

### Phase 2: Hardening gate and Parker-only reliability

**Goal:** keep the current dogfood path safe and reliable before expanding beyond Parker. The ordered source of truth is the hardening plan.

| Ticket | Status | Notes |
|---|---|---|
| Hardening plan items 1-10 and 27 | done | Boundary intact for Parker-only dogfood. See the hardening master plan for PRs, releases, and test bars. |
| `open-tickets/2026-05-12--cc-mini--remote-control-browser-plaintext-followups.md` | open / P1 | Next hardening gate before wider invite-list dogfood. |
| `open-tickets/2026-05-13--cc-mini--remote-control-daemon-stale-online-socket.md` | open / P1 | Build before `start remote control` readiness. Hosted relay stale daemon socket can block legitimate reconnects. |
| `open-tickets/2026-05-13--cc-mini--remote-control-start-ensures-daemon-readiness.md` | open / P1 | Build after stale daemon socket fix. `start remote control` should preflight daemon running, paired, relay-connected, and E2EE-ready. |
| `open-tickets/2026-05-12--cc-mini--remote-control-browser-auto-reconnect-after-tui-restart.md` | open / P1 | Browser should auto-reattach after TUI/App Server restart. |
| `open-tickets/2026-05-12--cc-mini--remote-control-ws-abuse-limits-followups.md` | open / P2 | Follow-up hardening after WebSocket abuse limits shipped. |
| `open-tickets/2026-05-11--codex--remote-control-two-browser-cross-thread-regression.md` | open / P1 | Missing end-to-end no-cross-talk regression. |
| `open-tickets/2026-05-11--codex--remote-control-thread-authority-interrupt-error-parity.md` | open / P2 | Error parity follow-up to avoid session-existence side channel. |
| `open-tickets/2026-05-11--codex--remote-control-e2ee-session-rehello-collision-dos.md` | open / P2 | Browser-chosen session id collision/re-hello DoS hardening. |

### Phase 3: Production-launch hardening

**Goal:** close or explicitly disposition the security findings from the 2026-05-18 review before describing Remote Control as production-secure.

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-05-18--codex--remote-control-oauth-token-mint-session-proof.md` | open / P0 | Hosted OAuth token mint path must prove server-side session and PKCE. This is production-launch critical. |
| `open-tickets/2026-05-18--codex--remote-control-daemon-token-redaction.md` | open / P1 | Daemon CLI must not print local control tokens by default. |
| `open-tickets/2026-05-18--codex--remote-control-public-mirror-hardening-parity.md` | open / P1 | Public mirror must reflect hardened relay claims, or release policy must explain intentional lag. No direct public edits. |
| `open-tickets/2026-05-18--codex--remote-control-dependency-audit-cleanup.md` | open / P1 | Clean or disposition dependency advisories before broader launch. |

### Phase 4: Pairing, auth, identity, and browser E2EE follow-ups

**Goal:** make account, passkey, pair/relink, and E2EE trust boundaries understandable and resilient.

| Ticket | Status | Notes |
|---|---|---|
| `closed-tickets/2026-05-06--codex--remote-control-pair-status-poll-token.md` | done | P0 pair-status authority fix shipped. |
| `closed-tickets/2026-05-05--codex--remote-control-pair-relink-audit-and-rotation.md` | done | Pair/relink audit and rotation shipped. |
| `closed-tickets/2026-05-06--codex--remote-control-browser-plaintext-after-e2ee.md` | done | Browser rejects plaintext after E2EE ready. |
| `open-tickets/2026-05-05--codex--remote-control-account-passkey-clarity.md` | open / P2 | User-facing account/passkey clarity. |
| `open-tickets/2026-05-03--codex--pair-mode-login-choice-clarity.md` | ticketed | Clarify existing-key vs new-key pair-mode login. Normalize status when next touched. |
| `open-tickets/2026-05-06--codex--remote-control-safari-handoff-bearer-token.md` | open / P1 | Safari handoff must not expose long-lived bearer token to same-origin JavaScript. |
| `open-tickets/2026-05-06--codex--remote-control-daemon-pubkey-pinning.md` | open / P2 | Browser should pin daemon public key after first trusted E2EE session. |
| `open-tickets/2026-05-05--codex--remote-control-local-e2ee-key-file-hardening.md` | open / P2 | Local E2EE key file hardening. |
| `open-tickets/2026-05-06--codex--remote-control-e2ee-forward-secrecy.md` | open / P3 | Forward secrecy upgrade. |
| `closed-tickets/2026-05-11--codex--remote-control-e2ee-restart-regression-test.md` | done | Regression evidence for restart/reconnect key availability. |

### Phase 5: Co-presence behavior and transcript fidelity

**Goal:** make the browser and phone feel like true peers of the active TUI thread, not a debug viewer or second runner.

| Ticket | Status | Notes |
|---|---|---|
| `closed-tickets/2026-05-05--codex--remote-control-multi-browser-fanout.md` | done | Multi-browser peer support shipped. |
| `closed-tickets/2026-05-05--codex--remote-control-daemon-thread-authority-binding.md` | done | Daemon commands are bound to ticket thread. |
| `open-tickets/2026-05-05--codex--remote-control-stop-shared-state.md` | open / P0 | Stop must interrupt the shared App Server turn and update all peers. |
| `open-tickets/2026-05-05--codex--remote-control-refresh-hydration.md` | open / P0 | Browser refresh must hydrate existing thread history. Related to new stock Codex hydration drift, but not identical to WIP fork item 40. |
| `open-tickets/2026-05-05--codex--remote-control-live-transcript-sync.md` | open / P1 | Live transcript sync and hydration. |
| `open-tickets/2026-05-06--codex--remote-control-activity-hydration.md` | open / P1 | Activity rows should survive refresh. |
| `open-tickets/2026-05-05--codex--remote-control-web-transcript-fidelity.md` | open / P1 | Web transcript should match Codex TUI output. |
| `open-tickets/2026-05-05--codex--remote-control-app-server-event-rendering.md` | open / P1 | Render App Server events as chat, not raw debug payloads. |
| `open-tickets/2026-05-05--codex--remote-control-web-status-line.md` | open / P1 | Browser should show Codex TUI status line metadata. |
| `open-tickets/2026-05-05--codex--remote-control-session-title-freshness.md` | open / P1 | Show current Codex session title and UUID. |
| `open-tickets/2026-05-06--codex--remote-control-send-races-attach-steer.md` | open / P1 | Browser send can race attach and call steer without active turn. |

### Phase 6: UI, mobile, and Kaleidoscope browser surface

**Goal:** make the Remote Control browser surface usable on phone and aligned with the rest of Kaleidoscope without changing security lanes accidentally.

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-05-06--codex--remote-control-mobile-composer-safe-area.md` | open / P0 | Mobile composer must stay above browser chrome. High user-impact polish. |
| `open-tickets/2026-05-05--codex--remote-control-ui-cleanup.md` | open / P1 | `/demo` chat-style cleanup without footer. |
| `open-tickets/2026-05-06--codex--remote-control-chat-ui-baseline.md` | open / P1 | Chat UI baseline from assistant UI patterns. |
| `open-tickets/2026-05-06--codex--remote-control-slash-command-controls.md` | open / P1 | Expose Codex slash commands as controls. |
| `open-tickets/2026-05-07--codex--remote-control-activity-terminology-parity.md` | open / needs frontmatter cleanup | Activity terminology parity ticket has no frontmatter in the first lines. Normalize when next touched. |
| `open-tickets/2026-05-06--codex--kaleidoscope-shadcn-radix-foundation-audit.md` | open / P0 | Kaleidoscope foundation audit. Related UI infrastructure, not Remote Control runtime. |

### Phase 7: Installer, daemon identity, and local OS integration

**Goal:** make the installed product clean on macOS and coherent through the install prompt.

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-05-12--codex--remote-control-daemon-macos-node-background-identity.md` | open / P1 | macOS attributes background prompts to Homebrew `node`. Process-title labeling is not enough. Needs executable-identity fix or LDM OS service-management direction. |
| `open-tickets/2026-05-06--codex--remote-control-tui-relink-readiness.md` | open / P1 | Start flow should handle relink readiness from inside the TUI. |
| `open-tickets/2026-05-05--codex--remote-control-patched-codex-install-path.md` | open / P1 | Also appears in Phase 1 because it intersects WIP Codex fork packaging. |

### Phase 8: Upstream, public packet, and architecture docs

**Goal:** keep the OpenAI-facing and public-facing story accurate without overclaiming or moving runtime code unnecessarily.

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-05-05--codex--remote-control-app-server-spike.md` | blocked-upstream / P0 | Architecture spike is blocked by upstream direction. Keep watching `app-server-daemon`, `remote_control`, queued turns, state sync, and public PRs. |
| `closed-tickets/2026-05-06--codex--remote-control-upstream-architecture-diagram.md` | done | OpenAI-facing architecture diagram exists. |
| `open-tickets/2026-05-18--codex--remote-control-public-mirror-hardening-parity.md` | open / P1 | Also appears in Phase 3 because public trust and production security overlap. |

---

## Done / shipped reference

These are the main completed items that explain why the current dogfood path works:

| Ticket | Status | Notes |
|---|---|---|
| `closed-tickets/2026-05-06--codex--remote-control-agentid-tenant-boundary.md` | done | Tenant boundary no longer depends on user-entered display label. |
| `closed-tickets/2026-05-06--codex--remote-control-pair-status-poll-token.md` | done | Pair-status no longer returns `apiKey` to pairing-id-only callers. |
| `closed-tickets/2026-05-05--codex--remote-control-e2ee-key-persistence.md` | done | E2EE daemon key registration survives hosted reloads. |
| `closed-tickets/2026-05-11--codex--remote-control-e2ee-restart-regression-test.md` | done | Restart regression test captured. |
| `closed-tickets/2026-05-05--codex--remote-control-daemon-thread-authority-binding.md` | done | E2EE browser session is bound to one thread. |
| `closed-tickets/2026-05-05--codex--remote-control-pair-relink-audit-and-rotation.md` | done | Pair and relink audit/rotation shipped. |
| `closed-tickets/2026-05-06--codex--remote-control-daemon-takeover-throttling.md` | done | Duplicate daemon takeover throttling shipped. |
| `closed-tickets/2026-05-06--codex--remote-control-browser-plaintext-after-e2ee.md` | done | Browser plaintext rejection after E2EE ready shipped. |
| `closed-tickets/2026-05-05--codex--remote-control-websocket-frame-abuse-limits.md` | done | WebSocket frame abuse limits shipped. |
| `closed-tickets/2026-05-05--codex--remote-control-multi-browser-fanout.md` | done | Multi-browser fanout shipped. |
| `closed-tickets/2026-05-06--codex--remote-control-codex-only-upstream-branch.md` | done | Clean Codex-only upstream branch or diff summary prepared. |
| `closed-tickets/2026-05-06--codex--remote-control-upstream-architecture-diagram.md` | done | OpenAI-facing diagram prepared. |

## Cross-repo dependency map

| Lane | Working repo | Reviewer / owner |
|---|---|---|
| Daemon, E2EE, MCP tool, TECHNICAL.md | `wip-codex-remote-control-private` | Hardening Cody + Remote Control CC Partner |
| Hosted relay, auth, OAuth, pairing, deploy manifest | `wip-ldm-os-private` | Hardening Cody + Merge/Deploy K |
| Browser UI, login handoff, transcript rendering | `kaleidoscope-private` | Remote Control UI / CC Partner |
| Patched Codex fork, app-server socket, upstream rebase | `openai-codex-private` | WIP Codex Cody + K Partner |
| Public mirror parity | private source repo first, then `deploy-public` | Merge/Deploy K |

## How to use this file

When a new Remote Control ticket is filed: add it to the right phase and write one line of context.

When a ticket moves through status: update the row here. Do not rewrite the individual ticket file unless its scope changed.

When deciding what to work on next:

1. Check Phase 1 if stock Codex or `codex-wip` is broken.
2. Check Phase 2 if Parker-only dogfood is unreliable.
3. Check Phase 3 before claiming production security or expanding sign-up.
4. Check Phase 5 and Phase 6 for product fidelity and phone/browser polish.

When a runtime slice ships: update the individual ticket, this master, the hardening plan if applicable, and `wip-codex-remote-control-private/TECHNICAL.md` if shipped behavior changed.

---

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
