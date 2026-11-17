# Ticket 16: Website launch copy review to remove sovereign language

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** open
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 10 `agent.txt` / `llms.txt`, Ticket 13 homepage walkthrough, Kaleidoscope guided onboarding ticket
**Surface:** active launch website and onboarding-facing website copy only

## Problem

The current website copy still has launch-facing lines like:

```text
WIP Computer builds sovereign infrastructure for AI agents.
```

Parker wants the active website and onboarding-facing copy to stop using `sovereign` / `sovereignty` language. The word is too abstract and loaded for the current launch surface. The launch should explain what the product does in concrete terms: user control, phone-rooted identity, portable memory, permissions, payments, and guided onboarding.

This is a copy audit ticket, not a product rewrite.

## Scope

Audit and update active launch surfaces in `repos/wip-web/wip-websites-private/wip.computer/`:

- `index.html`
- `agent.txt`
- `llms.txt`
- any active homepage/onboarding CTA copy that references the demo/onboarding path
- any launch-facing machine-readable summary used by agents or reviewers

Also check the current hosted onboarding/demo copy if the website copy points into it:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/login.html`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html`

## Out Of Scope

Do not rewrite historical or archival pages just because they use the word.

Out of scope unless Parker explicitly expands this ticket:

- `day-63/`
- `usr/lesa/`
- `lume/`
- `install/*.txt`
- archived website text drafts
- old `_trash/` or `_sort/` copies
- historical letters, proof pages, daily recaps, or product archaeology

Those pages can keep historical language. This ticket is about what current launch readers and onboarding users see first.

## Required Copy Direction

Replace `sovereign` language with concrete product language.

Preferred terms:

- user-controlled
- phone-rooted
- portable
- private
- human-approved
- permissioned
- inspectable
- local-first, where technically true
- one experience across AIs

Avoid vague replacements like:

- revolutionary
- trustless
- decentralized
- ownership layer, unless the sentence explains what that means

## Known Occurrences To Check

Initial search found likely active launch occurrences in the website repo:

- `wip.computer/agent.txt`: `WIP.computer builds sovereign infrastructure for AI agents.`
- `wip.computer/index.html`: `Identity, memory, sovereignty.`

The search also found many historical occurrences in Day 63, Lume, install specs, archive drafts, and Lēsa pages. Those are not automatically in scope.

## Acceptance Criteria

- Active launch website copy no longer uses `sovereign`, `sovereignty`, or related variants.
- `agent.txt` and `llms.txt` still fetch cleanly and still explain WIP clearly to agents.
- Homepage raw HTML still contains the current launch thesis and onboarding path.
- Any replacement copy says what the product does, not just a softer abstract slogan.
- Historical pages are not mass-rewritten.
- No design/layout change unless required by copy length.
- No hosted-mcp auth, wallet, Remote Control, relay, daemon, E2EE, or server behavior changes.
- If hosted onboarding/demo copy contains `sovereign` language, update only the visible or agent-readable launch/onboarding copy.

## Suggested Replacement Shape

Instead of:

```text
WIP Computer builds sovereign infrastructure for AI agents.
```

Use something closer to:

```text
WIP Computer builds user-controlled infrastructure for AI agents.
```

or:

```text
WIP Computer gives people one phone-rooted identity, memory, permission, and payment layer for the AIs they use.
```

Pick the sentence that fits the surrounding file. Do not force one replacement everywhere.

## Review Notes For Coder

Work from current `origin/main`.

Use a fresh worktree.

Stop at PR. Do not deploy.

Report:

- every active launch file changed
- every `sovereign` occurrence intentionally left alone and why
- whether `agent.txt` and `llms.txt` remain byte-identical after the edit
