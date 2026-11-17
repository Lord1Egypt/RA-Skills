---
title: "Remote Control should expose Codex slash commands as controls"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-06
---

# Remote Control Slash Command Controls

## Problem

The Codex TUI supports slash commands such as:

```text
/model
```

In the TUI, `/model` opens the model and reasoning-effort selection path. In the Remote Control browser today, sending `/model` behaves like an ordinary chat message. Codex may explain what `/model` does, but the web client does not actually trigger the TUI's command path.

That is confusing during dogfood because the browser looks like a peer client of the live TUI session, but important TUI controls are still terminal-only.

## Current Behavior

Observed flow:

- user asks about `/model`;
- Codex checks the local CLI and TUI source;
- TUI activity rows show search/read/run work live;
- user sends `/model`;
- Codex replies with an explanation;
- no model picker opens in the browser;
- no active model switch is performed through the web client.

This is correct for plain text chat transport, but it is not the product behavior we want long term.

## Expected Behavior

Remote Control should expose common Codex slash-command capabilities as first-class web controls.

For `/model`, the web client should eventually provide a model control that:

- shows the current model and reasoning effort;
- lets the user choose a supported model and effort;
- sends the request through the same authoritative Codex/App Server path as the TUI command;
- updates the web status line after the switch;
- preserves the TUI as the active local runtime authority.

Until this exists, the web UI should not pretend that sending `/model` as a normal chat message will switch the active session model.

## Near-Term Behavior

Before a full model selector exists, the browser can handle known slash-command input conservatively:

- detect `/model` entered into the composer;
- show a small inline notice that model switching is not available in web yet;
- tell the user to run `/model` in the local TUI or start a new `codex-wip -m <model>` session;
- do not send `/model` as a normal chat message unless the user explicitly chooses "send as text" or debug mode is enabled.

This avoids confusing transcript entries while the real UI is being built.

## Likely Implementation

Do not implement slash commands by scraping terminal UI.

Preferred path:

- identify whether Codex App Server exposes model/session configuration mutation today;
- if available, route web model changes through the daemon to App Server;
- if unavailable, treat this as a Codex-side feature request or fork patch;
- keep the browser protocol explicit, for example `session.model.set`, rather than overloading chat text.

The browser should use normal UI components for the eventual selector:

- status-line model/effort display under the title row;
- tap/click opens a compact selector;
- mobile uses a sheet or dialog pattern;
- desktop can use a popover or dialog;
- no raw slash-command text is required for the common path.

## Acceptance

- Typing `/model` in Remote Control does not silently send a normal chat message by default.
- The browser gives clear current behavior:
  - model switching is TUI-only for now; or
  - model switching is available through the web selector once implemented.
- The current model and reasoning effort are visible in the web status line when available.
- If a model switch is supported, the web change updates the same live Codex session, not a separate runner.
- If a model switch is unsupported, the UI fails closed and explains the TUI fallback.
- The transcript is not polluted with accidental slash-command attempts.
- Existing chat send behavior remains unchanged for ordinary messages.

## Related

- `2026-05-05--codex--remote-control-web-status-line.md`
- `2026-05-06--codex--remote-control-activity-hydration.md`
- `2026-05-06--codex--remote-control-chat-ui-baseline.md`
- `2026-05-05--codex--remote-control-patched-codex-install-path.md`

## Non-Goals

- Do not implement every Codex slash command in this ticket.
- Do not send slash-command strings as a control protocol.
- Do not create a second web-side Codex runner.
- Do not change model selection for stock Codex sessions that are not running through the WIP-compatible runtime path.
