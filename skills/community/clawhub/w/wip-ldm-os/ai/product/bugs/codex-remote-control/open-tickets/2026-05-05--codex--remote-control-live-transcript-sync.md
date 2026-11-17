---
title: "Remote Control live transcript sync and hydration"
status: open
priority: P1
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Live Transcript Sync

## Confirmed Green

The alpha.8 install and Codex entrypoint are green. Do not keep working on install registration.

Confirmed working:
- Fresh Codex session recognizes `start remote control`.
- Skill loads.
- MCP tool is called.
- Correct current-session URL is printed.
- Browser opens and attaches to thread `019df4cd-a4f2-7751-be82-9300381f69a2`.
- Browser can send a prompt and get a Codex response.

## Problem

Live sync is incomplete.

Browser and terminal are attached to the same thread, but they are not live-mirroring each other.

The next implementation should not start with JSONL tailing. OpenAI's documented rich-client surface for conversation history, turn control, approvals, and streamed agent events is Codex App Server. MCP remains the URL-launch tool, not the live session transport.

Product requirement: co-presence, not handoff.

Co-presence means:
- The Codex TUI remains live.
- Remote Control remains live.
- Both observe the same messages, turns, status, and Stop state.
- Either side can send input without kicking the other side off the live stream.

Handoff is explicitly insufficient for v1. If App Server lets the phone take over but causes the TUI to stop receiving live events, the sync bug is not fixed.

## Acceptance

- If Parker types in terminal Codex, the browser Remote Control view shows the user message and Codex response without refresh.
- If Parker types in the browser, other open browser tabs for the same Remote Control URL show the same message and response.
- If Parker types in the browser, the terminal Codex TUI live-renders the user message and Codex response.
- If terminal Codex cannot live-render browser-originated turns because stock Codex only supports handoff, this ticket remains open. Patch `openai/codex` for multi-listener co-presence or carry a fork.
- Refreshing the browser should hydrate the current transcript, not start as an empty debug screen.

## Likely Fix Area

The stock App Server spike in `2026-05-05--codex--remote-control-app-server-spike.md` has run.

Spike result:
- App Server can read, resume, hydrate, start a turn, stream its own turn, and persist the result.
- App Server sees enough shared state to reject concurrent turns while the TUI thread is active.
- The existing WIP Remote Control path can show TUI assistant output in the browser.
- The Remote Control browser tab did not live-render the App Server-started turn.
- Browser-originated sends did not render into the TUI as peer live events.
- A clean App Server observer did not receive a normal TUI-originated prompt live.
- The Remote Control browser disconnected with code 1006 during the observer test.

Therefore this ticket is blocked on the OpenAI Codex co-presence primitive. The next fix area is `openai/codex`, not WIP's hosted relay, Kaleidoscope UI, PTY automation, or JSONL tailing.

The Codex patch must stay generic and upstreamable:
- Add multi-subscriber live thread behavior to App Server.
- Do not depend on WIP hosted relay, WIP passkeys, Kaleidoscope, `codex-daemon`, or LDM install.
- Keep `ai/**` and WIP-private planning out of any upstream PR.
- Dogfood through `wipcomputer/openai-codex-private` while upstream review is pending.

If an upstream or carried Codex patch makes App Server drive and observe the same live thread as the Codex TUI:
- Replace the daemon's SDK-runner path with a local `codex app-server` client.
- Use `thread/resume` for the URL thread id.
- Use `thread/read` or `thread/turns/list` to hydrate.
- Use `turn/start` for browser prompts.
- Use `turn/interrupt` for Stop.
- Forward App Server notifications to every browser client attached to that thread over the existing E2EE relay.

Until then:
- Do not make JSONL tailing the primary architecture.
- Do not implement PTY typing as a product transport.
- Do not downgrade v1 to browser-only sync without changing the product requirement.
- Inspect `openai/codex` and make the smallest upstreamable patch so the TUI and App Server clients can share live thread events.
- Treat JSONL tailing as diagnostic infrastructure only.

The current source-code finding is tracked in `ai/product/plans-prds/codex-remote-control/2026-04-28--cc-mini--app-server-pivot-phase-7.md`:
- TUI uses App Server client primitives.
- `thread_state.rs` has a singular listener path that may kick prior listeners.
- v1 requires co-presence anyway.
- If stock Codex cannot deliver it, the plan is a generic upstreamable multi-listener ThreadState patch carried in WIP's private Codex fork until upstream accepts or replaces it.

## Out Of Scope

Remote Control visual cleanup belongs to `2026-05-05--codex--remote-control-ui-cleanup.md`.

Account/passkey identity clarity belongs to `2026-05-05--codex--remote-control-account-passkey-clarity.md`.

The App Server architecture gate belongs to `2026-05-05--codex--remote-control-app-server-spike.md`.
