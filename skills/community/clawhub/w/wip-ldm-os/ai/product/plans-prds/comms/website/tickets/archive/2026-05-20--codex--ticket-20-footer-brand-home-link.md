# Ticket 20: Link footer brand line to WIP Computer home

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** archived, implemented. Website PR #62 linked the homepage footer brand; hosted legal PR #1055 linked the three legal footers.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 17 footer export, Ticket 19 V05 header/nav polish
**Surface:** website and legal page footers

## Problem

Archived 2026-05-21: the footer brand link behavior is implemented for homepage and hosted legal pages. Login was intentionally split to Ticket 21.

The bottom footer brand line should consistently point people back to WIP Computer.

Footer instances currently show the company identity:

```text
WIP Computer, Inc.
Learning Dreaming Machines
Made in California.
```

The `WIP Computer, Inc.` text should be linked to the WIP Computer homepage everywhere that footer appears.

## Scope

Make only the footer brand link change.

Target URL:

```text
https://wip.computer/
```

Pages in scope:

- homepage footer
- Kaleidoscope live wall footer: `https://wip.computer/visualizations/kaleidoscope/onboarding/live/`
- Privacy Policy footer
- Website Terms footer
- Kaleidoscope Terms footer

If the implementation discovers other current public website pages using the same footer component or copied footer markup, apply the same brand-link fix there only if it is the same footer instance. Do not redesign or retaxonomize those pages.

## Requirements

- Link only `WIP Computer, Inc.`.
- Keep `Learning Dreaming Machines` as text.
- Keep `Made in California.` as text.
- Link target must be `https://wip.computer/`.
- Preserve the existing footer visual layout.
- Preserve the existing footer taxonomy and all other footer links.
- Preserve all page body copy.

## Explicitly Out Of Scope

- Do not change the header.
- Do not change the blue `Demo Kaleidoscope` CTA.
- Do not change Local passkeys footer behavior.
- Do not change login, demo chat, WebAuthn, QR, wallet, image generation, live-wall data, legal body copy, nginx, Remote Control, relay, daemon, E2EE, or API keys.
- Do not start the shared footer/template refactor in this ticket.
- Do not deploy.

## Acceptance Criteria

- On every in-scope footer, `WIP Computer, Inc.` links to `https://wip.computer/`.
- `Learning Dreaming Machines` remains unlinked text.
- `Made in California.` remains unlinked text.
- Footer visual layout is unchanged except for link behavior.
- No other footer links or copy are changed.
- Login and demo chat are unchanged.

## Validation

Minimum expected checks:

- `git diff --check` in every repo touched
- grep or parser check that in-scope footer brand text is wrapped in a link to `https://wip.computer/`
- grep or parser check that `Learning Dreaming Machines` and `Made in California.` remain plain text
- verify `/login` and `/demo` runtime files were not changed unless the coder can prove the same footer instance is intentionally in scope, which is not expected for this sprint

## Review Notes For Coder

Use fresh worktrees for every repo touched.

Stop at PR. Do not deploy.

Report:

- exact files changed in each repo
- each page whose footer brand link was updated
- confirmation that no footer taxonomy, header, login, demo chat, auth, wallet, live-wall data, or legal body copy changed
