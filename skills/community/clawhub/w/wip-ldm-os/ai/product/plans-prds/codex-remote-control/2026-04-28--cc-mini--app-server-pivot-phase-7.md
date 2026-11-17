---
title: "Remote Control App Server pivot spike gate"
date: 2026-04-28
status: active-gate
priority: P0 before live transcript sync
related:
  - 2026-04-28--cc-mini--codex-remote-control-master-plan.md
  - 2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md
  - ../../../product-ideas/vision-quest-01/cody-phone-as-key-authority-layer.md
authors: [cc-mini, cody, parker]
---

# Remote Control App Server Pivot Spike Gate

## Status: spike complete, upstream primitive needed

This is no longer queued future work. The stock App Server spike ran on 2026-05-05.

As of 2026-05-05, the alpha.8 install path, natural-language Codex skill trigger, MCP URL launcher, passkey pairing, browser attach, E2EE handshake, and browser-originated prompt path have all been dogfooded far enough to expose the real blocker: live transcript sync across Codex TUI, desktop browser, and mobile browser.

The spike showed that stock App Server is the right adapter surface, but stock co-presence was not observed in the tested build. The next move is a narrow upstreamable Codex patch, not a WIP-only fake transport.

## What this addendum is

The current daemon integrates against `@openai/codex-sdk` directly. That was the right choice for getting Phase 1-3 working fast, but it is not the right long-term layer. OpenAI publishes a documented interop layer ... **Codex App Server** ... which is the correct surface for "phone, desktop app, and CLI all driving the same Codex thread."

This addendum captures the pivot, the why, the scope, and the hard rules. It is now also the architecture gate for the current live-sync work.

## What App Server gives us

OpenAI's [Codex App Server docs](https://developers.openai.com/codex/app-server/) document the interop primitives every rich Codex client should be built on:

- `thread/start`
- `thread/resume`
- `thread/list`
- `turn/start`
- `turn/steer`
- `turn/interrupt`

Plus auth, conversation history, approvals, and streamed agent events as first-class concerns. OpenAI's own framing: App Server is for **rich clients** (auth, history, approvals, streamed events); the SDK is for **automation/CI**. We are a rich client. We should be on App Server.

That is the clean path for "phone, desktop app, and CLI all talking to the same Codex thread." The SDK + JSONL path is not.

App Server gives us the right adapter surface. It does not automatically prove co-presence semantics for v1. Co-presence means the active Codex TUI and the phone/browser Remote Control client are subscribed to the same live thread at the same time. That must be proven against stock Codex or added upstream.

## Source Finding: Single Thread Listener Risk

The `openai/codex` source confirms that the Codex TUI already uses App Server as its control surface:

- `codex-rs/tui/src/app_server_session.rs` imports `codex_app_server_client::AppServerClient`.
- The same file imports `codex_app_server_client::AppServerEvent`.

So App Server is not a side channel. It is the canonical surface that the TUI itself uses.

The source also shows the risk for v1 co-presence:

- `codex-rs/app-server/src/thread_state.rs` stores a singular `listener_thread: Option<Weak<CodexThread>>`.
- `ThreadState::set_listener` replaces `cancel_tx` and sends cancellation to the previous listener before installing the next listener.

The inspected shape is:

```rust
if let Some(previous) = self.cancel_tx.replace(cancel_tx) {
    let _ = previous.send(());
}
```

That means the spike must not merely prove `thread/resume` works. Handoff is easy: phone resumes and the previous listener is no longer active. Co-presence is the requirement: phone/browser and TUI both observe the same live turn stream without kicking each other off.

OpenAI App Server also tracks connection subscriptions separately. That means the implementation detail may be more nuanced than "one websocket connection only." The product requirement is still clear: v1 needs simultaneous live subscribers. If stock Codex does not deliver that behavior, the patch belongs in `openai/codex` at the thread listener/event-broadcast layer.

## Why Co-Presence Is The v1 Requirement

Parker's product decision is explicit: Remote Control must work like Anthropic Claude Code remote control.

Anthropic's Claude Code Remote Control docs set the parity bar: the local session keeps running on the user's machine, while terminal, browser, and phone stay synchronized as interchangeable surfaces. The docs describe this as working "from both surfaces at once" and sending messages from terminal, browser, and phone interchangeably.

That means:

- The laptop Codex TUI stays alive as the source-of-truth working session.
- The phone or browser opens the same session as a peer view.
- A prompt typed in the TUI appears in Remote Control.
- A prompt typed in Remote Control appears in the TUI.
- Codex output streams to both.
- Stop state is shared.

Handoff is not enough for v1. Handoff would mean the phone takes over, the TUI stream dies or goes stale, and Parker later resumes locally. That does not meet the product bar.

The v1 promise is co-presence. If stock Codex cannot support co-presence, the work moves to an upstream Codex patch or a carried fork. It does not move to JSONL tailing, PTY typing, or browser-only sync.

## Architecture: WIP layer vs OpenAI layer

Cody's framing of the durable shape (after Phase 7 lands):

```
Codex CLI MCP command
  -> local wip-codex-daemon
  -> codex app-server JSON-RPC
  -> Codex thread/turn APIs

Phone / Kaleidoscope web
  -> WIP auth + phone-as-key + E2EE relay
  -> local wip-codex-daemon
  -> codex app-server JSON-RPC
```

Two entry points (the CLI MCP command and the phone/web), one daemon, one App Server backend. The daemon is where WIP control plane meets OpenAI control plane.

**What WIP owns and keeps owning** (from Cody, on the alpha that already shipped):

- Pairing.
- Phone-as-key.
- Relay (`wip.computer/api/codex-relay/...`).
- End-to-end encryption (ECDH P-256 + HKDF + AES-GCM).
- Install flow (LDM OS, `ldm install --alpha wip-codex-remote-control`, `codex mcp add`, install spec at `wip.computer/install/wip-codex-remote-control.txt`).
- The `/remote-control` user experience inside Codex.

These are our layer. They don't move. App Server doesn't replace them; it sits underneath them.

**What WIP routes to OpenAI** (after Phase 7):

- Codex thread control: start, resume, list, send, interrupt, steer.
- Approvals.
- Conversation history surface.

These currently live as custom code in `apps/wip-codex-remote-control-private/src/codex-manager.ts:1` (SDK calls) and `apps/wip-codex-remote-control-private/src/mcp.ts:51` (`~/.codex/session_index.jsonl` reads via `names.ts`). After Phase 7, they become App Server JSON-RPC calls.

## Why this matters now

Today, when a user opens `https://wip.computer/codex-remote-control/<thread-id>` on their phone, the daemon resumes via `codex.resumeThread(threadId)` against threads it discovered by parsing `~/.codex/session_index.jsonl`. That works for threads created by the CLI. It does **not** work for threads created by the **Codex desktop app**, which uses a separate visibility path (`~/.codex/state_5.sqlite`, per OpenAI Codex issue #16385).

In other words: today, Codex Remote Control is **CLI-only**. The phone can drive a Codex thread your CLI started. It cannot drive a Codex thread your desktop app started.

App Server collapses that divide. Threads, listing, resume, and turn streaming all flow through one server-mediated surface that both CLI and desktop are moving toward as the canonical interop layer.

## Public signal we should not ignore

Multiple OpenAI Codex issues are explicitly asking for the same thing we are building, and several of them are flagging the SQLite/JSONL/sidebar visibility split as a real edge:

- [openai/codex #9224](https://github.com/openai/codex/issues/9224) ... feature request: control `codex` CLI from phone via ChatGPT app / Codex tab.
- [openai/codex #13543](https://github.com/openai/codex/issues/13543) ... feature request: QR-paired local-first remote control with `/remote-control`, view progress, interrupt, send input, keep local terminal as source of truth. (This is essentially our product.)
- [openai/codex #14722](https://github.com/openai/codex/issues/14722) ... request: sync between `codex resume`, Codex app, and third-party app-server systems.
- [openai/codex #16385](https://github.com/openai/codex/issues/16385) ... bug: ACP/OpenClaw-created Codex sessions write JSONL files but do not appear in the desktop app, which uses `~/.codex/state_5.sqlite`.
- [openai/codex #10547](https://github.com/openai/codex/issues/10547) ... bug: local sessions exist and CLI can resume them, but desktop sidebar ignores them.
- [openai/codex #14751](https://github.com/openai/codex/issues/14751) ... bug: desktop sidebar appears to load only a recent subset, while CLI can still see the conversations.
- [openai/codex #16614](https://github.com/openai/codex/issues/16614) ... someone tested a phone-oriented custom client on `codex app-server`. `thread/start`, `thread/resume`, `turn/start`, `thread/list` worked. Desktop visibility/source-kind behavior is confusing and not clearly documented.

#16614 is the most relevant precedent: a phone client built on App Server primitives mostly works today. Desktop sidebar visibility is a separate product edge OpenAI still owes documentation on.

## What changes vs what stays

**Daemon layer (changes):**
- `src/codex-manager.ts` ... currently wraps `@openai/codex-sdk` directly via `Codex().startThread()` / `resumeThread()` / `runStreamed()`. Pivot rewrites this to drive a locally-running `codex app-server` process and route turn events back through the same protocol.
- `src/names.ts` ... currently parses `~/.codex/session_index.jsonl` for `listThreads()` / `resolveThread()`. Pivot replaces this with `thread/list` calls to App Server. The file becomes removable.

**Wire protocol (unchanged):**
- `session.attach` / `session.attached` / `session.attach.failed` ... maps to `thread/resume`.
- `session.start` / `session.started` ... maps to `thread/start`.
- `session.send` / `session.event` ... maps to `turn/start` + streamed agent events.
- `session.interrupt` ... maps to `turn/interrupt`.

**Phone surface (unchanged):**
- The web app at `kaleidoscope-private/web/src/app/codex-remote-control/[threadId]` does not change. It speaks the daemon protocol; the daemon's bottom layer is invisible to it.

**Relay + E2EE (unchanged):**
- `wip-ldm-os-private/src/hosted-mcp/server.mjs` codex-relay endpoints stay as-is.
- ECDH P-256 + HKDF + AES-GCM frame envelope stays as-is.
- Gates 1-4 stay green.

**Install spec (changes minimally):**
- `SKILL.md` already says "Codex CLI" today. The pivot lifts that to "Codex CLI and Codex desktop app."
- Probably pick up an "Approvals" line in the user-facing copy when Phase 4 (approval-needed UX) lands as a free side-effect of App Server's approval primitive.

## Hard rules

1. **No SQLite surgery.** Do not read or write `~/.codex/state_5.sqlite` directly. Cody flagged this as a footgun (issue #16385); we should not invent our way around App Server.
2. **No JSONL parsing as the product transport.** JSONL tailing can be diagnostic only. It cannot deliver real co-presence because it cannot make the TUI and Remote Control share one live event stream.
3. **Don't break the wire.** The phone-side protocol (`session.attach` etc.) stays. The daemon's relay-client stays. We are swapping the bottom layer, not the surface.
4. **Don't fake browser-only success.** If browser tabs sync but the active Codex TUI cannot see browser-originated turns, the product contract is not complete. Record the limitation and patch the Codex integration layer.
5. **Upstream when the primitive is missing.** If stock OpenAI Codex lacks the hook needed for TUI plus App Server live sync, inspect `openai/codex` and make the smallest upstreamable change rather than building a permanent private workaround.

## Immediate Spike Acceptance

Run this before Slice 3 history hydration, Slice 4 multi-tab fanout, or any new live transcript sync transport patch.

Result from 2026-05-05:

- [x] Start a fresh Codex TUI session and note its thread id and title.
- [x] Start stock `codex app-server` locally.
- [x] Use `thread/resume` against the same thread id after running outside the tool sandbox.
- [x] Use `thread/read` or `thread/turns/list` to hydrate existing scrollback.
- [x] Use `turn/start` to send a browser-originated prompt through App Server.
- [x] Confirm whether the active Codex TUI live-renders that App Server-started turn. Result: not observed.
- [x] Confirm whether the current WIP Remote Control browser can show TUI assistant output. Result: observed by Parker.
- [x] Confirm whether browser-originated input appears in the Codex TUI as a peer live event. Result: not observed.
- [x] Type a terminal-originated prompt in the Codex TUI while a separate App Server observer is resumed.
- [x] Confirm whether App Server notifications or reads can observe that terminal-originated turn without JSONL tailing. Result: observer did not receive `turn/started`, `item/*`, or `turn/completed`.
- [x] Record browser side effect during observer test. Result: Remote Control browser disconnected with `code 1006`.
- [ ] Use `turn/interrupt` during an active App Server-started turn and verify Stop semantics.
- [x] Record the result in `ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-app-server-spike.md`.

Decision:

- Stock App Server supports the right thread and turn primitives.
- Stock App Server sees shared active-thread state and rejects concurrent turns.
- Current WIP Remote Control can mirror TUI assistant output into the browser.
- Current WIP Remote Control does not mirror browser-originated input into the TUI as a peer live event.
- Stock App Server-started turns did not render through the current WIP browser/TUI path.
- Stock App Server observer did not receive the TUI-originated prompt live.
- Observer attach correlated with Remote Control browser disconnects.
- Patch `openai/codex` for multi-listener co-presence.
- Do not downgrade v1 to browser-only sync without explicitly changing the product requirement.

Observed plane split:

1. Local Codex TUI/runtime plane: active turn execution, tool calls, command output, terminal-visible status, and the TUI transcript.
2. WIP Remote Control browser plane: selected daemon/relay events sent to the browser, including some Codex assistant output from the active TUI turn.
3. Codex App Server plane: App Server can hydrate and append turns to the same thread, but that stream is not automatically unified with the WIP browser plane or the active TUI plane.

The patch target is the place where these become one live subscription model, not another bridge between two already-partial streams.

Co-presence is not a requirement to clone every local terminal detail into the browser. Remote Control should receive the semantic product event stream: user messages, assistant output, relevant command output/errors, approval prompts, turn lifecycle status, and Stop state. Terminal-only implementation noise can stay terminal-only.

## Upstream Patch: ThreadState Multi-Listener

If the spike confirms the source-level risk, the patch target is `openai/codex`, not WIP's hosted relay.

The patch must be generic Codex infrastructure. It cannot depend on any WIP system.

Allowed upstream patch scope:

- App Server supports multiple subscribers on the same thread.
- Multiple clients receive the same semantic turn stream.
- Disconnecting one subscriber does not cancel or unload the other subscribers.
- Status, approval, interrupt, and turn lifecycle events reach every live subscriber.
- Tests cover the generic App Server behavior without WIP services.

Forbidden upstream patch scope:

- WIP hosted relay.
- WIP passkey auth or phone-as-key assumptions.
- Kaleidoscope UI.
- `codex-daemon`.
- LDM install behavior.
- `ai/**` planning files.
- WIP product names, URLs, screenshots, dogfood transcripts, or private notes.

WIP-specific product layers stay outside upstream:

- Pairing.
- Phone-as-key.
- E2EE relay.
- Remote Control browser UI.
- Daemon packaging.
- Passkey auth.
- LDM install.

The private fork exists so WIP can dogfood the generic Codex patch immediately while keeping WIP planning and product integration out of the upstream PR.

Likely patch shape:

- Replace the singular listener ownership in `codex-rs/app-server/src/thread_state.rs` with a multi-listener collection.
- Do not cancel an existing subscriber when another client resumes or subscribes to the same thread.
- Broadcast thread, turn, item, status, approval, and interrupt events to every live subscriber for that thread.
- Drop a subscriber only when its connection closes, explicitly unsubscribes, or backpressure policy disconnects it.
- Preserve the existing single-client behavior as a degenerate case.

Required upstream tests:

- Two clients subscribe to the same loaded thread and both receive the same streamed turn events.
- A second `thread/resume` does not cancel the first client's active subscription.
- A TUI-originated turn is visible to the second client.
- A second-client `turn/start` is visible to the TUI client.
- `turn/interrupt` state reaches both clients.
- Disconnecting one subscriber does not unload the thread while another subscriber remains.
- When the last subscriber disconnects, existing unload behavior remains intact.

Upstream sequence:

1. Run the local confirmation spike and capture the exact stock behavior.
2. Open a discussion issue on `openai/codex`.
3. Cite the phone-as-second-client use cases: #9224, #13543, #14722, and #16614.
4. Frame the requested primitive as multi-listener ThreadState co-presence for App Server clients.
5. Open the patch PR after the discussion issue has the problem statement and intended shape.

## Ship Decision: Carry The WIP Codex Fork

Co-presence requires the multi-listener primitive.

WIP is not waiting for upstream to design or ship this primitive.

Decision:

- Patch Codex ourselves.
- Dogfood on the WIP Codex build.
- Upstream the patch as a contribution in parallel.
- Treat upstream acceptance as desirable, but not a blocker for WIP Remote Control v1.
- Make the product dependency explicit: WIP Remote Control v1 co-presence requires a WIP Codex build until upstream accepts or replaces the patch.

Fork hygiene:

- The private fork lives at `wipcomputer/openai-codex-private`.
- Local checkout lives under `/Users/lesa/wipcomputerinc/repos/third-party-repos/openai-codex-private`.
- `upstream` remains `openai/codex`.
- `origin` is the private WIP fork.
- `ai/` is allowed only in the private fork.
- Every upstream PR branch must pass an upstream-clean check that excludes `ai/**` and any WIP-private files.
- The upstream PR contains only code, tests, and public docs needed by OpenAI maintainers.

The fork path has real cost:

- WIP must track upstream Codex changes.
- Users must install WIP's patched Codex build instead of stock Codex while the fork is required.
- Release and support docs must be explicit about that dependency.

There is no path that ships true co-presence on unpatched stock Codex if stock Codex keeps one live listener per thread.

## Adapter Swap Acceptance

The eventual adapter swap is **not** a "rewrite everything." It keeps WIP pairing, phone-as-key, E2EE relay, install spec, and MCP trigger; it replaces the daemon's Codex backend from `@openai/codex-sdk` + `session_index` parsing to `codex app-server` JSON-RPC. The cut lands when **all** of these are true:

- [ ] `/remote-control` still works from Codex CLI.
- [ ] Existing thread attach uses `thread/resume`.
- [ ] Session list uses `thread/list`, not `~/.codex/session_index.jsonl`.
- [ ] Sending input uses `turn/start` or `turn/steer` as appropriate.
- [ ] Interrupt uses `turn/interrupt`.
- [ ] Approval/waiting state is surfaced from app-server status/events.
- [ ] No direct writes to Codex SQLite or JSONL indexes.
- [ ] Desktop/sidebar behavior is **tested and documented**, not assumed.

This now blocks claims that v1 live transcript sync is complete. It does not block unrelated UI cleanup, account/passkey clarity, hosted auth fixes, or security hardening.

## Build Plan

Step 1 is the spike. Do it before implementation:

1. Probe `codex app-server` locally on the dogfood Mac. Confirm the immediate spike acceptance list above.
2. Worktree on `wip-codex-remote-control-private`. New branch `cc-mini/phase-7-app-server`.
3. New module `src/app-server-client.ts` ... starts a managed `codex app-server` process (or connects to one), exposes the JSON-RPC primitives.
4. Rewrite `src/codex-manager.ts` to delegate to `app-server-client.ts`. Keep the same exported shape (`start`, `attach`, `runStreamed`, `interrupt`, etc.) so `dispatch.ts` does not change.
5. Delete `src/names.ts`. `listThreads()` and `resolveThread()` callers move to `app-server-client.ts`.
6. Re-run `npm test`. All 20 gate assertions must still pass.
7. Live: walk the acceptance-criteria list above end-to-end, including a desktop-app-created thread URL opened on phone.
8. Cut beta or stable, deploy SKILL.md update lifting "Codex CLI" to "Codex CLI and Codex desktop app."

## Open questions for the pivot itself

1. Does `codex app-server` self-bootstrap, or do we need a managed-child-process supervisor in the daemon?
2. What's the auth path? Does App Server inherit the user's `~/.codex/auth.json`, or does the daemon need to forward credentials?
3. Approval UX (Phase 4): does App Server's approval primitive route to a streamed event the daemon can lift to the phone, or does it require an inline callback the daemon implements?
4. Co-presence: does OpenAI accept a multi-listener ThreadState patch upstream, or do we carry a fork until they do?
5. Versioning: which App Server protocol version does the daemon target, and how do we declare the SDK dependency?
6. Local-only daemon mode: does App Server require any inbound port, or is it stdio-only? Affects the loopback-only contract.

These are not blockers; they are what gets investigated in step 1 of the build plan.

## Non-Approaches

Do not lead with these:

- PTY typing into the Codex terminal as the product transport.
- JSONL tailing as the product transport, even temporarily.
- Direct SQLite reads or writes.
- A browser-only mirror that hides the fact that the live Codex TUI is not participating.
- A custom session registry that competes with Codex's own thread model.

Those may be useful for diagnostics or compatibility notes. They are not the product plan.

## Reference

- [OpenAI Codex App Server docs](https://developers.openai.com/codex/app-server/)
- [Claude Code Remote Control docs](https://code.claude.com/docs/en/remote-control/)
- Cody's "Phone as Key, Apple as Authority Layer": `wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/cody-phone-as-key-authority-layer.md`
- Codex Remote Control master plan: `wip-ldm-os-private/ai/product/plans-prds/codex-remote-control/2026-04-28--cc-mini--codex-remote-control-master-plan.md`
- WIP Codex fork hygiene ticket: `wip-ldm-os-private/ai/product/bugs/codex-remote-control/2026-05-05--codex--wip-codex-fork-upstream-hygiene.md`
- OpenAI Codex issues: #9224, #10547, #13543, #14722, #14751, #16385, #16614

## TL;DR

The CLI build was the right wedge. Alpha.8 proved the URL launcher and browser attach path far enough to expose the real sync problem. App Server is now the immediate architecture gate before live transcript work continues. Parker's v1 requirement is co-presence, not handoff: the Codex TUI and Remote Control must both observe and drive the same live session. App Server is still the correct adapter surface, but stock Codex must prove multi-listener behavior. If it does not, patch OpenAI Codex narrowly or carry a fork. Do not build Remote Control v1 on JSONL, PTY, or browser-only sync.
