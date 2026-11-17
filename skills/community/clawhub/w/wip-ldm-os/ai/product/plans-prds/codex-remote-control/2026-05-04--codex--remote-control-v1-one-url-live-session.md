---
title: "Codex Remote Control v1: one URL, one live session"
date: 2026-05-04
author: Codex
status: active-spec
surface: codex-remote-control
---

# Codex Remote Control v1: One URL, One Live Session

## Decision

Codex Remote Control v1 is not a dashboard.

It is one URL controlling one Codex session.

No picker. No control panel. No alias registry. No multi-session switcher. No separate DNS layer. Parker already names Codex sessions; v1 must use those session titles as the product-facing name.

## Current Evidence

The transport now works:

- Pairing passes through `codex-daemon link`.
- The daemon connects to the hosted relay.
- E2EE handshake completes.
- The browser attaches to an existing Codex thread.
- A prompt typed in the Remote Control page lands in that thread and receives the Codex response.

Known live proof:

```text
/codex-remote-control/019de489-4e3e-78d3-a5ea-141e17b4e46b
connected. running e2ee handshake...
encrypted channel ready (e2ee-v1).
attached to thread 019de489-4e3... (already in memory).
you
ok hi
codex
Hi Parker.
```

The remaining problem is not whether the relay can carry prompts. The remaining product problem is that the target is unclear and incomplete:

- The page shows only a UUID, not the Codex session title.
- Manual pasted URLs can target an old thread by accident.
- The page does not hydrate the existing scrollback before new messages.
- Multiple browser tabs for the same URL are not yet specified as peers.
- `/remote-control` is not wired in Codex, so the current-session link is not generated from inside the active session.

## Product Contract

When Parker invokes Remote Control from a Codex session:

1. Codex generates a URL for the current session.
2. The URL opens the exact same session on desktop or mobile.
3. The page shows the full existing session history.
4. The page shows the Codex session title and the session id.
5. Any browser tab opened to that URL is a peer view of the same session.
6. Messages sent from any tab appear in Codex TUI and every other tab for that URL.
7. Codex responses stream back to every tab for that URL.
8. Stop interrupts only that one session, and every tab reflects the interrupted state.

This is co-presence, not handoff.

Co-presence means the Codex TUI and every Remote Control browser tab are peers on the same live session. Handoff means the phone takes over and the TUI stops receiving live events. Handoff does not satisfy v1.

## Route Model

Canonical route:

```text
/codex-remote-control/<sessionId>
```

`sessionId` remains the routing key for:

- websocket route binding
- E2EE session attach
- local Codex resume
- audit logs
- Stop and interrupt

The session title is display metadata only. It must never replace the session id as the transport key.

## Invocation Model

Target product invocation:

```text
/remote-control
```

Inside a Codex session, `/remote-control` should return one link:

```text
https://wip.computer/codex-remote-control/<current-session-id>
```

The link must be generated from the current Codex session. It must not use the most recent session, a hard-coded smoke id, or a manually pasted id.

If slash commands cannot be added directly yet, the same behavior may ship first through the installed MCP tool, but the product copy must still call this out as the Remote Control entrypoint.

## Session Identity Display

The Remote Control page header must display:

1. Primary label: Codex session title.
2. Secondary label: Codex session id.

Example:

```text
memory-review--kay--partner
019de489-4e3e-78d3-a5ea-141e17b4e46b
```

If the session has no title:

```text
Untitled Codex session
019de489-4e3e-78d3-a5ea-141e17b4e46b
```

Rename behavior:

- If Parker renames a Codex session, the Remote Control page should show the updated title on next load.
- Live title updates are nice later, but not required for v1.
- Rename does not change the URL.
- Rename does not change routing.

## History Hydration

Opening the URL must show the existing session, not only new events after attach.

Required behavior:

- Load persisted messages/events for `<sessionId>` from local Codex session storage through the daemon.
- Render the existing scrollback before or during attach.
- Preserve the event order from the Codex session.
- Mark the page ready only after it knows whether history loaded or failed.

Failure behavior:

- If history cannot load, show a visible warning and still allow live attach if attach succeeds.
- Do not silently present an empty chat as if the session had no history.

## Multi-Tab And Multi-Device Model

Every tab opened to the same URL is a peer view.

Required behavior:

- Chrome desktop and iPhone Safari can open the same URL.
- Both attach to the same Codex session.
- Both show the same session title and id.
- Both show the same hydrated history.
- A prompt sent from Chrome appears on iPhone Safari.
- A prompt sent from iPhone Safari appears on Chrome.
- Codex responses stream to both tabs.
- Stop state reflects in both tabs.

Server and daemon must treat multiple web clients for the same `(agentId, sessionId)` as subscribers to the same session, not as replacements, unless there is a security reason to allow only one viewer. If v1 keeps one active web socket per session, that limitation must be visible and explicit, because it conflicts with the product contract above.

## Stop Semantics

Stop is scoped to one Codex session.

Required behavior:

- Stop is enabled only while a turn is running.
- Stop sends encrypted `session.interrupt` for the attached session.
- The daemon interrupts the current turn.
- Every connected tab for the same URL sees the stopped or completed state.
- Stop must not affect other Codex sessions.

## Desktop And Mobile Contract

The same URL must work on desktop and mobile:

```text
https://wip.computer/codex-remote-control/<sessionId>
```

Desktop and mobile may differ in auth handoff details, but they must resolve to the same target session after auth.

iPhone Safari still has a separate auth handoff bug. That bug should be diagnosed with evidence, not folded into the v1 session contract.

## Architecture Gate Result: App Server Needs Co-Presence Patch

The stock Codex App Server spike ran on 2026-05-05 and is recorded in:

`ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-app-server-spike.md`

The gate question was narrow:

Can `codex app-server` hydrate, drive, interrupt, and observe the same live Codex TUI thread that the Remote Control URL targets while keeping the TUI subscribed?

Use OpenAI's documented App Server primitives first:

- `thread/resume`
- `thread/read` or `thread/turns/list`
- `turn/start`
- `turn/interrupt`

MCP and the Codex skill remain the URL launcher. App Server is the live rich-client transport candidate. JSONL tailing is diagnostic or fallback infrastructure only, not the primary v1 architecture.

Observed result:

- App Server can hydrate the target thread.
- App Server can `thread/resume` and `turn/start` when run with normal local Codex write access.
- App Server streams its own turn events and persists its turn.
- The existing WIP Remote Control path can show TUI assistant output in the browser.
- The browser Remote Control tab did not live-render the App Server-started turn.
- Browser-originated sends did not render into the TUI as peer live events.
- Browser send while the TUI turn was active returned `sessionId 019df4cd-a4f2-7751-be82-9300381f69a2 is already running a turn`.
- A separate App Server observer did not receive a normal TUI-originated prompt live.
- The Remote Control browser disconnected with `code 1006` during the observer test.

Decision:

- Keep App Server as the correct adapter surface.
- Stop WIP transport patching until the Codex co-presence primitive exists.
- Inspect `openai/codex` and make the smallest upstreamable multi-listener patch needed for shared live events.
- Keep the Codex patch generic: no WIP hosted relay, no WIP passkeys, no Kaleidoscope, no `codex-daemon`, no LDM install behavior, and no `ai/**` files upstream.
- Dogfood the patch from `wipcomputer/openai-codex-private` until upstream accepts or replaces it.
- Do not claim v1 live sync is complete if browser tabs sync but the Codex TUI cannot participate.

The dogfood run exposed three separate planes:

1. Local Codex TUI/runtime plane: what Parker sees in the terminal, including active turn execution, tool calls, command output, and terminal-visible status.
2. WIP Remote Control browser plane: selected daemon/relay events sent to the web UI, including some Codex assistant output from the active TUI turn.
3. Codex App Server plane: a stock App Server client can hydrate and append turns to the same thread, but its stream is not automatically unified with the browser or TUI streams.

The v1 contract requires these planes to collapse into one shared live event model. Same thread id plus partial mirroring is not enough.

This is not a terminal-clone requirement. The Remote Control page should show the semantic product stream: user messages, Codex assistant output, relevant command output/errors, approval prompts, turn lifecycle status, and Stop state. It does not need to expose every internal TUI processing detail.

## Non-Goals

Do not build these in v1:

- session picker
- dashboard
- alias registry
- separate DNS/name system
- multiple remote sessions on one page
- public alpha onboarding
- full App Server adapter swap before the spike proves the primitive set
- new login redesign
- new pair flow redesign

The pair-mode login choice clarity ticket remains valid as a separate P1 UX fix.

## Existing Docs Disposition

Use this file as the active product contract.

Keep the older docs, but stop treating them as current product state:

- `2026-04-28--cc-mini--codex-remote-control-master-plan.md`: original architecture and security gates. Keep as historical architecture.
- `2026-04-28--cody--secure-session-continuity-plan.md`: source material now mostly merged into the master plan. Keep as historical review input.
- `2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md`: keep for privacy, plaintext, attach, and interrupt gate mechanics.
- `2026-04-28--cc-mini--app-server-pivot-phase-7.md`: now the immediate architecture gate for live transcript sync. Run its stock App Server spike before more transport work.
- `2026-04-29--codex--relay-auth-security-ticket.md`: security gate history. Several P0s are now implemented; update separately if preparing public alpha.
- `2026-04-29--codex--public-alpha-relay-abuse-gate.md`: public alpha blocker. Not v1 private dogfood.
- `2026-04-29--codex--overall-security-gate-matrix.md`: gate-status tracker. Needs refresh after private dogfood stabilizes.
- `2026-04-30--cc-mini--pair-via-login-qr-flow.md`: current pair contract. Keep as pair source of truth.
- `2026-05-01--codex--remote-control-recovery-master-plan.md`: recovery packet. Keep for deploy/runbook history, but this file supersedes it for product v1 behavior.
- `2026-05-01--codex--remote-control-smoke-automation.md`: still valid. Extend it with v1 history/fanout smokes.
- `ai/product/bugs/codex-remote-control/2026-05-03--codex--pair-mode-login-choice-clarity.md`: valid P1 UX bug, separate from v1 live-session contract.

## Implementation Slices

### Slice 1: Current-session URL generation

Goal: `/remote-control` or the current MCP equivalent generates the URL for the current Codex session.

Acceptance:

- It uses the active session id.
- It prints exactly one openable URL.
- It does not choose a stale or most-recent unrelated session.
- It clearly says which session title and id the URL targets.

### Slice 2: Session title display

Goal: Remote Control page shows title plus id.

Acceptance:

- Header shows session title as primary label.
- Header shows UUID as secondary label.
- Missing title shows `Untitled Codex session`.
- Renaming a session updates the page on next load.

### Slice 3: History hydration

Blocked until the Codex co-presence patch path above is resolved.

Goal: Remote Control page loads the existing session scrollback.

Acceptance:

- Opening the URL shows previous user and Codex messages.
- It does not start as an empty chat when history exists.
- History load failure is visible.
- New events append after hydrated history without duplication.

### Slice 4: Multi-tab fanout

Blocked until the Codex co-presence patch path above is resolved.

Goal: Same URL on multiple devices stays in sync.

Acceptance:

- Chrome and iPhone Safari opened to the same URL show the same title, id, history, and live events.
- A message sent from one appears in all other tabs.
- Codex response streams to all tabs.

### Slice 5: Stop

Blocked until the Codex co-presence patch path above is resolved, unless `turn/interrupt` is verified independently and can land without creating a second transport path.

Goal: Stop works and is reflected everywhere.

Acceptance:

- Start a long turn.
- Stop from Chrome interrupts it.
- iPhone Safari reflects stopped/completed state.
- Stop from iPhone Safari interrupts it.
- Chrome reflects stopped/completed state.

## Acceptance Test For v1

Do not run this as a completion claim until the Codex co-presence patch exists in the Codex build Parker is using.

1. Rename a Codex session to a recognizable title.
2. In that same Codex session, invoke Remote Control.
3. Open the generated URL in Chrome.
4. Confirm Chrome shows the title, id, and existing scrollback.
5. Open the same URL on iPhone Safari.
6. Confirm iPhone Safari shows the same title, id, and scrollback.
7. Send `hello from chrome` in Chrome.
8. Confirm the message appears in iPhone Safari and the Codex TUI.
9. Send `hello from phone` on iPhone Safari.
10. Confirm the message appears in Chrome and the Codex TUI.
11. Confirm Codex response streams to both browser tabs.
12. Start a long turn and press Stop.
13. Confirm the turn stops and both browser tabs reflect the final state.

## Separate Follow-Ups

Do not let these distract from v1:

- Pair-mode login choice clarity: P1 UI ticket already exists.
- iPhone Safari Remote Control auth handoff: still needs instrumentation.
- Usage display bug: token counts currently show cumulative/unhelpful numbers like `25341420 in / 61427 out`; hide or fix separately.
- App Server adapter swap: no longer a vague future item. It is gated by the stock App Server spike before transcript sync work continues.
- Public alpha relay abuse gate: broader exposure blocker, not v1 private dogfood.

## Next Concrete Step

Slice 1 and Slice 2 are implemented in the alpha.8 dogfood path.

Run the stock Codex App Server spike before starting Slice 3, Slice 4, or the live transcript sync ticket:

- confirm `thread/resume` can attach to the same target thread
- confirm existing transcript hydration through App Server
- confirm browser-originated turns can stream through App Server
- confirm whether the active Codex TUI live-renders those turns
- confirm whether App Server can observe terminal-originated turns without JSONL tailing
- confirm whether the TUI and Remote Control client remain subscribed simultaneously
- record the result in the spike ticket and only then choose the implementation path
