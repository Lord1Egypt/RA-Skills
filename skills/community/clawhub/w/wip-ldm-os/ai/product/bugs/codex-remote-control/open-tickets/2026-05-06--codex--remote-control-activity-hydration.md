---
title: "Remote Control activity rows should survive refresh"
status: open
priority: P1
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-06
---

# Remote Control Activity Hydration

## Problem

During a live Codex turn, the Remote Control browser can show activity rows that match the TUI's working state:

```text
Explored
Search SlashCommand.*model|/model|model in tui
Read slash_command.rs
Ran codex --version
```

After refreshing the browser, those activity rows disappear. The durable transcript remains:

```text
you
Wait, what about like/model like I can do that

codex
I'll check the local Codex CLI surface instead of guessing...

turn complete
```

That proves there are two separate hydration layers:

- durable transcript hydration: working;
- activity/status hydration: missing.

The live view and refreshed view should not disagree accidentally.

## Expected Behavior

Remote Control web should preserve the user-visible shape of a Codex turn across refresh.

The browser should hydrate both:

- durable transcript messages: user messages, Codex messages, turn completion;
- activity/status rows: explored, search, read, ran, tool status, interruption, and meaningful slash-command related activity, when that history is available.

The activity rows should stay visually distinct from chat messages. They should look compact and secondary, similar to the TUI's activity rows, not like primary chat bubbles and not like raw protocol debug cards.

## Product Decision Needed

The implementation should first determine whether Codex App Server history includes historical activity events.

If App Server history includes activity:

- normalize historical activity into the same web activity-row model used for live events;
- render it during `session.history` hydration;
- dedupe any live events that arrive during the hydration handoff.

If App Server history does not include activity:

- make an explicit product choice instead of relying on accidental behavior;
- either show only the durable transcript after refresh and document activity as live-only;
- or persist/cache recent per-thread or per-turn activity in the daemon and include it in `session.history`.

Do not recreate fake activity rows from assistant prose.

## Likely Implementation

Check the daemon attach and hydration path:

- `thread/read`;
- `thread/turns/list`;
- any App Server event history or turn detail surface already available.

Then update the browser-side event normalization so live activity rows and hydrated activity rows share one UI model.

The UI should keep three lanes conceptually separate:

- chat transcript: durable user and Codex messages;
- activity rows: compact work/status events;
- diagnostics: connection, E2EE, attach, reconnect, and error state.

## Acceptance

- Start a Codex turn that performs searches, file reads, or shell commands.
- Browser shows live activity rows while the turn is running.
- Refresh the browser after the turn.
- User and Codex transcript messages still render.
- Activity rows from the turn still render if the backend has them.
- If historical activity is unavailable, the browser behavior is intentional and documented, not accidental.
- Activity rows are compact and secondary.
- Raw protocol JSON remains hidden in normal mode.
- Hydration and live events do not duplicate the same activity row.
- Existing co-presence remains green:
  - browser to TUI;
  - TUI to browser;
  - multi-browser fanout;
  - refresh/rejoin;
  - Stop scoped to the attached thread.

## Related

- `2026-05-05--codex--remote-control-refresh-hydration.md`
- `2026-05-05--codex--remote-control-app-server-event-rendering.md`
- `2026-05-05--codex--remote-control-web-transcript-fidelity.md`
- `2026-05-06--codex--remote-control-chat-ui-baseline.md`

## Non-Goals

- Do not render raw App Server protocol envelopes.
- Do not make the browser imitate terminal pixels exactly.
- Do not change relay fanout.
- Do not solve slash-command controls here.
