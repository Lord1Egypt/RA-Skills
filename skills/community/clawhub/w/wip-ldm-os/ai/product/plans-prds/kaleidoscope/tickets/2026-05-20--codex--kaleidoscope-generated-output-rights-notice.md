# Kaleidoscope Generated Output Rights Notice

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Related:** [`2026-05-18--codex--guided-onboarding-intent-engine.md`](2026-05-18--codex--guided-onboarding-intent-engine.md), [`2026-05-19--codex--kaleidoscope-live-image-wall.md`](2026-05-19--codex--kaleidoscope-live-image-wall.md), [`../../comms/website/tickets/2026-05-18--codex--ticket-18-product-wide-privacy-terms-review.md`](../../comms/website/tickets/2026-05-18--codex--ticket-18-product-wide-privacy-terms-review.md)
**Surface:** `src/hosted-mcp/demo/index.html`, image-generation steps in Kaleidoscope onboarding, and any future `/onboarding` alias

## Summary

Ticket 18 shipped Kaleidoscope terms that intentionally give WIP Computer broad rights to use generated Kaleidoscope outputs. That legal copy is deployed and should not be reopened for this issue.

The remaining gap is product UI: before a user generates a Kaleidoscope image, the interface should clearly say that generated Kaleidoscope outputs may appear in WIP galleries, live walls, demos, product materials, and marketing.

This is not a legal rewrite. It is an in-flow notice at the moment of generation.

## Problem

Kaleidoscope now has a public live wall direction: official generated Kaleidoscope outputs should be eligible to appear publicly, while uploaded source photos should not be published.

The legal terms cover that broad generated-output license. The product should also make it visible in the flow so the user is not surprised after generation.

This matters more now because the live wall is becoming product proof, not a hidden implementation detail.

## Required UI

Show a concise notice before or directly at the generation action.

Recommended copy:

```text
Generated Kaleidoscopes may appear in WIP galleries, live walls, demos, and product materials. Your uploaded photos stay yours.
```

If space allows, link `Kaleidoscope Terms` to:

```text
https://wip.computer/legal/internet-services/kaleidoscope/
```

Keep the language plain and short. Do not add a modal, checkbox, or legal wall unless a later product decision requires stronger explicit consent.

## Required Behavior

The notice must appear on every official image-generation path:

1. Generic Kaleidoscope generation.
2. Image-based Kaleidoscope generation after photo analysis.
3. Any "No thanks, make one anyway" path that still generates an output.
4. Any future `/onboarding` alias that reuses the same generation flow.

The notice should distinguish:

- Generated Kaleidoscope outputs can be used by WIP.
- Uploaded source photos, selected photos, files, and prompts remain user content.
- Uploaded source photos are not published to the live wall.
- The wall keeps the exact xAI-generated image URL for now. This ticket must not add storage, rehosting, proxying, S3, R2, or CDN ingestion.

## Scope

In scope:

- onboarding chat copy around image generation
- generation choice button area
- concise link to Kaleidoscope Terms
- mobile layout check

Out of scope:

- rewriting legal pages
- changing the generated-output license
- changing xAI image generation
- changing wallet deduction behavior
- changing public-wall server trust rules
- adding image storage or rehosting
- publishing uploaded source photos
- changing arbitrary prompt behavior

## Acceptance Criteria

1. A user sees the generated-output rights notice before an official generated Kaleidoscope output is created.
2. The notice appears for generic and image-based generation paths.
3. Uploaded source photos are still not described as public wall content.
4. The notice links to Kaleidoscope Terms where layout allows.
5. No legal body copy changes are included in this ticket.
6. No API key, wallet, auth, Remote Control, relay, daemon, E2EE, or storage behavior changes are included.

## Validation

Run:

```bash
git diff --check
node --check src/hosted-mcp/server.mjs
```

Also parse any inline scripts in `src/hosted-mcp/demo/index.html`.

Manual check:

- create or sign into a Kaleidoscope account
- reach the image generation step
- verify the rights notice is visible before generation
- complete generic generation
- complete image-based generation if available
- verify uploaded source photos are not shown as public wall items

## Notes

This follow-up came from the final Ticket 18 legal review after PR #1026 was merged and deployed. It belongs in the product UI lane because the legal terms already landed and the remaining issue is user-facing notice at the action moment.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
