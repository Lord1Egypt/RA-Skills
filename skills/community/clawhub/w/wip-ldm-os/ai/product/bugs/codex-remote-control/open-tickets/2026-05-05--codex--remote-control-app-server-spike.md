---
title: "Remote Control App Server architecture spike"
status: blocked-upstream
priority: P0
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control App Server Architecture Spike

## Decision

Reframe Remote Control around Codex App Server, not the Codex SDK runner.

Current alpha.8 proved:
- Natural-language skill trigger works.
- MCP install works.
- Browser reaches daemon over E2EE.
- Browser can start a parallel turn through the daemon.

But the remaining sync bug is architectural:
- MCP is only the Codex entrypoint tool.
- The browser UI needs a live Codex client protocol.
- Per OpenAI docs, that protocol is Codex App Server.
- Parker's v1 product requirement is co-presence, not handoff.

MCP should stay small. It should create or return the Remote Control URL for the current thread. It should not be the live session event transport.

## Docs Basis

OpenAI's Codex App Server docs expose the primitives Remote Control needs:
- `initialize`
- `thread/resume`
- `thread/read`
- `thread/turns/list`
- `turn/start`
- `turn/interrupt`
- `turn/steer`
- streamed thread, turn, and item notifications

OpenAI's Codex MCP and slash-command docs frame MCP as a tool surface exposed to Codex, while slash commands are built-in Codex control-plane commands. Remote Control should keep using natural-language skill invocation for the URL launcher, then use App Server for the live rich-client layer.

Source-code finding to verify in the spike:
- `codex-rs/tui/src/app_server_session.rs` uses `codex_app_server_client::AppServerClient` and `AppServerEvent`. The TUI already speaks App Server.
- `codex-rs/app-server/src/thread_state.rs` keeps a singular `listener_thread` and `set_listener` cancels the previous listener through `cancel_tx.replace(cancel_tx)`.
- The spike must distinguish handoff from co-presence. A successful `thread/resume` is not enough if it kicks the active TUI off the live stream.

Sources:
- https://developers.openai.com/codex/app-server
- https://developers.openai.com/codex/mcp
- https://developers.openai.com/codex/cli/features#model-context-protocol-mcp
- https://developers.openai.com/codex/cli/slash-commands

## Stock Codex Spike First

Before patching Remote Control transport further, run a stock Codex App Server spike.

Goal:
Verify whether `codex app-server` can drive and observe the same live thread as the Codex TUI without kicking the TUI off the live stream.

Test:
1. Open Codex TUI.
2. Start Remote Control from that session to get the thread id.
3. Separately start `codex app-server`.
4. Initialize the client with client metadata for WIP Remote Control.
5. Call `thread/resume` with the TUI thread id.
6. Call `thread/read` or `thread/turns/list` to hydrate.
7. Call `turn/start` with `hello from app-server`.
8. Observe whether the already-open Codex TUI renders that turn live.
9. Type `hello from terminal` in the TUI.
10. Observe whether App Server emits notifications or can read the new terminal turn immediately.
11. Call `turn/interrupt` during an active App Server-started turn and verify Stop behavior.
12. Confirm whether both clients remained subscribed throughout the test.

Decision:
- If stock App Server supports co-presence, implement Remote Control daemon on App Server.
- If stock App Server supports handoff only, open the multi-listener ThreadState track in `openai/codex`.
- If Codex needs a patch, make the smallest upstreamable change so TUI and App Server clients can share live thread events.

Do not build the core product on PTY typing or JSONL tailing. Those can be debug tools, but co-presence requires shared live thread events through App Server.

## Implementation Direction If Stock App Server Works

Keep the MCP tool small:
- Return the current thread URL.
- Do not use MCP as the session event transport.

In `codex-daemon`, start or connect to `codex app-server` locally:
- Prefer stdio transport first.
- Initialize once with client info for WIP Remote Control.
- Use `thread/resume` for the URL thread id.
- Use `thread/read` or `thread/turns/list` to hydrate history.
- Use `turn/start` for browser prompts.
- Use `turn/interrupt` for Stop.
- Forward streamed App Server notifications to browser clients over the existing E2EE relay.

Browser Remote Control becomes an App Server client via daemon relay:
- On attach, hydrate transcript.
- During turns, render streamed item and turn notifications.
- Multiple browser tabs and devices subscribe to the same daemon/App Server session.

## Open Question

Can the stock Codex TUI and a separate App Server client both stay subscribed to the same live thread at the same time?

If yes:
- Wire it.

If no:
- Do not fake it with JSONL tailing.
- Record that stock Codex supports handoff but not co-presence.
- Open an `openai/codex` discussion issue for ThreadState multi-listener support.
- Build the smallest upstreamable patch, or carry a fork if v1 cannot wait for upstream.

## Acceptance

- Fresh Codex session starts.
- Parker types `start remote control`.
- Remote Control URL opens.
- Browser hydrates the existing transcript through App Server.
- Browser sends a prompt through App Server and receives streamed Codex events.
- Refresh rehydrates the same transcript.
- Stop maps to `turn/interrupt`.
- The spike records whether the stock Codex TUI live-renders App Server-started turns.
- The spike records whether App Server can observe TUI-originated terminal turns without JSONL tailing.
- The spike records whether the TUI and Remote Control client remain subscribed simultaneously.
- The spike states one of two outcomes: `stock co-presence works` or `stock handoff only, multi-listener patch required`.

## Out Of Scope

Remote Control visual cleanup belongs to `2026-05-05--codex--remote-control-ui-cleanup.md`.

Account/passkey identity clarity belongs to `2026-05-05--codex--remote-control-account-passkey-clarity.md`.

## Spike Result: 2026-05-05

Outcome: full co-presence was not observed in the tested Codex build. The current WIP Remote Control path can show Codex TUI assistant output in the browser, but browser-originated input does not appear back in the TUI, App Server-started turns did not live-render through the browser/TUI path, and a clean App Server observer did not receive a normal TUI-originated prompt live.

What worked:
- `codex app-server` initialized.
- `thread/read` on `019df4cd-a4f2-7751-be82-9300381f69a2` resolved title `remote-control--cody--coder`.
- `thread/read` hydrated the current transcript.
- Running the probe outside the Codex tool sandbox allowed `thread/resume` to succeed.
- App Server `turn/start` succeeded while the TUI thread was idle.
- App Server streamed its own turn through `turn/started`, `item/agentMessage/delta`, and `turn/completed`.
- The App Server-started turn persisted and later hydrated through `thread/read` / `thread/turns/list`.
- Parker observed Codex TUI assistant output streaming into the open Remote Control browser tab through the existing WIP daemon/browser path.

Exact App Server-started turn:
- Thread: `019df4cd-a4f2-7751-be82-9300381f69a2`
- Turn: `019df8c8-bc00-79c3-b180-2548b74014aa`
- Prompt: `Reply exactly: APP_SERVER_COPRESENCE_SPIKE_OK`
- Response: `APP_SERVER_COPRESENCE_SPIKE_OK`

What did not work:
- The open Remote Control browser tab did not live-render the App Server-started turn. Parker reported the last visible browser content was the earlier sandbox-blocked result, not `APP_SERVER_COPRESENCE_SPIKE_OK`.
- A separate App Server observer connection resumed the thread successfully. During the attempted observer window it saw startup/status notifications and `skills/changed`, but no live turn stream.
- Parker's test inputs during that window were browser-originated, not TUI-originated.
- Browser-originated input did not appear in the Codex TUI as a peer live event.
- A browser-originated prompt while the TUI turn was active returned `sessionId 019df4cd-a4f2-7751-be82-9300381f69a2 is already running a turn`.
- Clean observer test: an App Server observer resumed the thread, Parker sent `OBSERVER_TEST_FROM_TUI` as a normal TUI prompt, and the observer received no `turn/started`, `item/*`, or `turn/completed` notifications. It only saw `remoteControl/status/changed`, MCP startup status, and `thread/status/changed`.
- During the clean observer test, the Remote Control browser disconnected with `code 1006`.
- Stop is not reliable enough yet to use as an App Server co-presence signal.

Interpretation:
- Stock App Server sees the same persisted thread and enough live state to reject concurrent turns.
- Stock App Server can run and stream an App Server-owned turn.
- Existing WIP Remote Control appears to mirror TUI assistant output into the browser.
- Existing WIP Remote Control does not provide symmetric browser-to-TUI live mirroring.
- Stock App Server does not automatically bridge its own turn stream into the existing browser/TUI live path.
- Stock App Server observer did not receive a normal TUI-originated prompt live.
- Attaching/running the observer correlates with Remote Control browser disconnects, which is consistent with the single-listener/listener-replacement risk.
- Full co-presence, meaning TUI plus browser/App Server clients all live-rendering the same turn stream and accepting peer input, was not observed.

Three planes are visible in the dogfood run:
1. Local Codex TUI/runtime plane: the active Codex turn, tool calls, command output, internal status, and the terminal transcript Parker sees in the TUI.
2. WIP Remote Control browser plane: the hosted browser receives selected daemon/relay events, including some Codex assistant output from the active TUI turn.
3. Codex App Server plane: a separate App Server client can hydrate and append turns to the same thread, but its live stream is not automatically unified with the WIP browser plane or the active TUI plane.

The product requirement is not merely that all three planes touch the same thread id. The v1 requirement is one shared live event bus where TUI and browser are peer subscribers.

Co-presence does not mean the browser must clone every TUI implementation detail. The browser does not need every internal processing event, local tool bookkeeping line, or terminal-only debug trace. It does need the shared product events: user messages, Codex assistant output, relevant command output/errors, approval requests, turn lifecycle status, and Stop state.

Next engineering move:
- Open an `openai/codex` discussion issue with the spike evidence.
- Inspect the App Server listener/subscription path.
- Build the smallest upstreamable multi-listener ThreadState/event-broadcast patch if stock Codex still has singular live listener behavior.
- Keep the Codex patch generic: no WIP hosted relay, no WIP passkey auth, no Kaleidoscope, no `codex-daemon`, no LDM install behavior, and no `ai/**` files in the upstream PR.
- Dogfood the patch from `wipcomputer/openai-codex-private` while upstream review is pending.
- Do not ship JSONL tailing, PTY typing, or browser-only sync as the product architecture.
