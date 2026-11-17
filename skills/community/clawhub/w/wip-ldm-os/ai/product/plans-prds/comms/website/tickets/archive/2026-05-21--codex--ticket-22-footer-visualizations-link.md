# Ticket 22: Add Visualizations link to all footers

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** archived, implemented. Website PR #63 and hosted-mcp PR #1061 added the same-tab `Visualizations` footer link.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 17 footer export, Ticket 20 footer brand home link, Ticket 21 login footer brand link, future shared footer template ticket
**Surface:** all current WIP Computer website and hosted footer instances

## Problem

Archived 2026-05-21: the same-tab `Visualizations` footer link landed in the website and hosted-mcp footer lanes.

The Kaleidoscope live wall is useful during the sprint, but the URL is currently easy to forget:

```text
https://wip.computer/visualizations/kaleidoscope/onboarding/live/
```

Parker wants a quiet footer link so the live wall is discoverable without promoting it as a main CTA.

## Scope

Add a `Visualizations` link under the footer `Tools` group everywhere the current grouped footer appears.

Link target:

```text
https://wip.computer/visualizations/kaleidoscope/onboarding/live/
```

Open behavior:

```text
Open in the same tab.
```

For plain HTML anchors, do not add `target="_blank"` or `rel="noopener"` for this link.

```html
<a href="https://wip.computer/visualizations/kaleidoscope/onboarding/live/">Visualizations</a>
```

Pages in scope:

- homepage footer
- Kaleidoscope live wall footer
- `/login` footer
- Privacy Policy footer
- Website Terms footer
- Kaleidoscope Terms footer
- any other current public page using the same grouped footer markup

## Requirements

- Add exactly one `Visualizations` link under `Tools`.
- The link points to `https://wip.computer/visualizations/kaleidoscope/onboarding/live/`.
- The link opens in the same tab.
- Keep `Are you an AI agent?` unchanged.
- Keep Local passkeys footer behavior unchanged.
- Keep footer taxonomy unchanged except for adding this one `Visualizations` link under `Tools`.
- Preserve existing footer visual layout.
- Preserve all other footer links and copy.

## Explicitly Out Of Scope

- Do not change the header.
- Do not change the blue `Demo Kaleidoscope` CTA.
- Do not redesign the footer.
- Do not start the shared footer/template refactor in this ticket.
- Do not change Local passkeys behavior.
- Do not change `Are you an AI agent?`.
- Do not change login, demo chat, WebAuthn, QR, wallet, image generation, live-wall data, legal body copy, server behavior, nginx, Remote Control, relay, daemon, E2EE, API keys, or unrelated CSS/JS.
- Do not deploy.

## Acceptance Criteria

- Every current in-scope footer has a `Visualizations` link under `Tools`.
- Every `Visualizations` link points to `https://wip.computer/visualizations/kaleidoscope/onboarding/live/`.
- Every `Visualizations` link opens in the same tab.
- No other footer links or footer taxonomy change.
- Local passkeys footer state and toggle behavior are unchanged.
- `Are you an AI agent?` remains unchanged.
- Login/auth, demo chat, live-wall data, and legal body copy are unchanged.

## Validation

Minimum expected checks:

- `git diff --check` in every repo touched
- parser or grep check that every in-scope footer contains `Visualizations`
- parser or grep check that every `Visualizations` link uses the live-wall URL
- parser or grep check that every plain HTML `Visualizations` link does not include `target="_blank"` or `rel="noopener"`
- changed-file check proving no login/auth behavior, demo chat behavior, live-wall data/feed/stats/images, legal body copy, server behavior, nginx, wallet, WebAuthn, QR, API-key, or unrelated CSS/JS files changed

## Review Notes For Coder

Use fresh worktrees for every repo touched.

Stop at PR. Do not deploy.

Report:

- exact files changed in each repo
- every footer/page updated
- confirmation that `Visualizations` opens in the same tab
- confirmation that footer taxonomy changed only by adding the one `Visualizations` link under `Tools`
- confirmation that behavior surfaces were not changed
