# Remote Control Web Activity Terminology Parity

Status: Open
Priority: P1
Owner: Coder
Area: Codex Remote Control, Kaleidoscope web transcript

## Problem

Remote Control web currently exposes some Codex activity using terminology that does not match the visible Codex TUI.

Parker observed a live Remote Control session where the TUI presents the state as normal Codex activity, but the web view uses wording such as `reasoning` for what the TUI user experience presents as `thinking`.

This makes the browser feel like a protocol or debug view instead of a peer view of the same Codex session.

## Observed

- The visible Codex TUI shows user-facing activity terms and compact work rows.
- The web Remote Control transcript can show different terms for the same state.
- Example mismatch: web says `reasoning`; TUI-facing language should say `thinking` for that same state.
- Related activity rows such as explored, search, read, ran, tool status, interruption, or slash-command related work should feel like Codex activity, not raw protocol labels.

## Expected

Remote Control web should map App Server and daemon events into the same user-facing activity vocabulary as the Codex TUI wherever possible.

Specifically:

- Use `thinking` for the user-facing thinking state if that is the TUI label.
- Do not show `reasoning` as a default transcript label when the equivalent TUI state is `thinking`.
- Render tool and work events as compact activity rows.
- Keep raw event names out of the default transcript.
- Reserve raw protocol labels for an explicit debug view, if one exists later.

## Scope

This is a presentation and normalization bug.

Do not change:

- relay protocol;
- daemon protocol;
- Codex App Server behavior;
- E2EE;
- auth;
- pair or relink behavior.

## Relationship To Existing Tickets

This is narrower than:

- `2026-05-05--codex--remote-control-web-transcript-fidelity.md`
- `2026-05-05--codex--remote-control-app-server-event-rendering.md`
- `2026-05-06--codex--remote-control-activity-hydration.md`

Those tickets cover broader transcript semantics and hydration. This ticket specifically tracks label and terminology parity between the visible TUI and the web Remote Control surface.

## Implementation Notes

Add or tighten the browser-side event normalization layer so activity labels are semantic UI labels, not direct protocol strings.

Suggested mapping examples:

```text
reasoning -> thinking
tool/search -> search
tool/read -> read
tool/run -> ran
interrupt/error -> interrupted or failed, depending on event semantics
```

Do not infer fake activity from assistant prose. Only map real activity, status, or App Server events.

## Acceptance

- During a live turn, the web view uses `thinking` where the TUI user experience uses `thinking`.
- The web view does not show `reasoning` as the default user-facing label for the thinking state.
- Compact work events render as activity rows rather than raw protocol labels.
- Hydrated activity, if available, uses the same labels as live activity.
- Browser refresh does not reintroduce raw event labels for the same thread.
- Existing Remote Control co-presence still works:
  - browser to TUI;
  - TUI to browser;
  - multi-browser fanout.

## Validation

- Add or update a focused browser normalization test for the `reasoning` to `thinking` label mapping.
- Add or update snapshot or component tests for activity row labels if the Kaleidoscope test setup supports it.
- Run the existing Remote Control web validation for transcript rendering.
