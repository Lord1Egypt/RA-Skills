---
title: "Remote Control web transcript should match Codex TUI output"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-05
---

# Remote Control Web Transcript Fidelity

## Problem

The Remote Control web view proves that mobile/browser co-presence works, but the transcript does not yet render like Codex.

Current web output can show protocol internals as visible chat content:

```text
USER_MESSAGE
{
  "type": "user_message",
  "text": "hi!!!"
}
```

The Codex TUI shows the same interaction as normal transcript entries:

```text
› hi!!!

• Hi. Still bridged.
```

The web UI should mirror the Codex thread experience, not expose the raw App Server event envelope.

## Evidence

Parker captured screenshots from the mobile Remote Control page and visible Codex TUI on 2026-05-05.

Observed mobile web:

- user bubble renders `hi!!!`,
- then a second card renders raw `USER_MESSAGE` JSON for the same message,
- assistant response renders separately,
- same pattern repeats for `This is the mobile. This is mobile working.`

Observed TUI:

- user prompts render once,
- assistant messages render as assistant transcript content,
- interruption and turn lifecycle status render as Codex status, not raw event cards.

## Expected Behavior

Remote Control web should render the same semantic transcript as Codex:

- User messages render once as user messages.
- Assistant messages render once as Codex messages.
- Reasoning/tool/status events render only if they are meaningful to the user.
- Raw App Server event type names are hidden by default.
- Raw JSON envelopes are hidden by default.
- Diagnostic status text is small and secondary, not a primary chat card.

The web does not need to clone terminal pixels or every TUI decorative detail. It does need to present the same product transcript in the same order and with the same meaning.

## Likely Implementation

Add or tighten the browser-side normalization layer that maps App Server/daemon events into web transcript items.

Known mappings:

- `user_message` -> one user bubble containing `text`
- assistant message/delta/completed -> assistant bubble or streaming assistant item
- `turn.completed` / `turn complete` -> small muted status separator
- interruption/failure -> small visible status/error line
- raw JSON -> debug-only mode, not default UI

Deduplicate cases where both the web composer and App Server event stream represent the same user message.

## Acceptance

- Sending `hi!!!` from mobile renders exactly one user message in web.
- The raw `USER_MESSAGE` label does not appear in normal mode.
- The raw JSON object does not appear in normal mode.
- Codex assistant output renders as Codex assistant content.
- TUI-originated prompts render in the browser as user messages, not JSON.
- Browser-originated prompts render in the TUI normally.
- Turn lifecycle text remains visible only as small diagnostic/status text where useful.
- Existing one-browser co-presence remains green.

## Non-Goals

- Do not change the App Server backend.
- Do not change relay encryption.
- Do not solve multi-browser fanout here.
- Do not make the browser imitate terminal pixels exactly.

