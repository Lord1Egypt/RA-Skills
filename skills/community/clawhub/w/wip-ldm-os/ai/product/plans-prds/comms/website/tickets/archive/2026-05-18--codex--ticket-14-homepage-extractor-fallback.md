# Ticket 14: Make the homepage extract cleanly without design changes

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. No-design-change semantic cleanup shipped by `wip-websites-private` PR #55. Claude Code Fetch reads the homepage body; one weaker Anthropic-style extractor may remain metadata-only. Further visible-prose work requires a separate design-approved ticket.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 04 homepage static hardening, Ticket 10 agent.txt and llms.txt launch surfaces
**Surface:** `repos/wip-web/wip-websites-private/wip.computer/index.html`, and only if required `repos/wip-web/wip-websites-private/wip.computer/styles.css`

## Summary

The homepage should be enough. Parker should not have to tell reviewers to point their AI at `agent.txt` or `llms.txt` in the Speedrun submission. Those files are useful convention and fallback surfaces, but the public gambit should still work when someone says:

```text
Point your AI at https://wip.computer and https://github.com/wipcomputer.
```

The homepage is now static HTML and human-readable, but at least one AI reader still extracts only title/metadata from `https://wip.computer/`. PR #54 added hidden semantic fallback text near the top of `<main>`, and it did not work for the target extractor. That is expected behavior for serious extractors: visually hidden text is commonly filtered as SEO/spam content.

Fix the homepage so common extractors can recover the canonical launch story directly from the page that humans already see. Do not rely on hidden text, clipped text, or `noscript` as the primary strategy.

Parker's constraint is strict: do not change the homepage design to satisfy an extractor. No new visible block, no new visible section, no layout shift, no different visual hierarchy. If the coder cannot make the existing design extract cleanly through semantic markup and source-order changes alone, they must stop and report that finding instead of shipping a visual change.

## Desired behavior

- A human visiting the homepage sees the same intended hero and letter.
- The rendered page is visually unchanged or only mechanically equivalent at the pixel/layout level.
- The homepage still has the current design direction, architecture reveal, and CTAs.
- A raw fetch or common AI reader can extract a concise canonical summary from `https://wip.computer/`.
- The extracted text should include the launch hierarchy and demo path without requiring a direct `agent.txt` link.
- `agent.txt` and `llms.txt` remain live as fallback convention surfaces, but the Speedrun submission does not need to expose them.

## Diagnostic result

Current source already contains:

- a CSS-only `<noscript>` block in `<head>`
- a hidden `.extractor-fallback` section near the top of `<main>`
- visible homepage letter copy later in the document

The target extractor still returns only title/meta frontmatter. Therefore:

- Hidden/clipped fallback text is not enough.
- `noscript` is not a reliable primary strategy for this reader.
- The likely failure mode is that the page is classified as a landing/index page rather than an article-like page with substantive prose.

## Canonical source prose

The first significant readable text inside `<main>` should come from the homepage's existing visible launch copy, not from a new visible fallback block. If the current copy is split across decorative fragments, the coder may restructure the markup so extractors see a real paragraph while CSS preserves the current rendered appearance.

Use this as the canonical meaning to preserve, but do not add it as a new visible paragraph unless Parker separately approves the visual result:

```text
WIP Computer builds the user-controlled operating layer for AI. It gives people one coherent place to work with their AIs across memory, identity, tools, payments, and apps. Kaleidoscope is the app. Lēsa is the AI inside it. Learning Dreaming Machines Operating System (LDM OS) is the operating layer underneath. This is serious working alpha: real software, real rough edges, built in public.
```

Keep the demo and repo paths semantically discoverable in the source. Preserve the current visible CTA design:

```text
Try the demo: https://wip.computer/login?next=/demo
Inspect the public repos: https://github.com/wipcomputer
```

## Implementation direction

Do not add another hidden fallback. Make the existing homepage itself structurally extractable.

Preferred shape:

1. Start from the current live/merged homepage design in `wip-websites-private`, not from a stale export.
2. Identify the existing visible hero and supporting copy that should be the first meaningful prose in `<main>`.
3. Adjust markup, source order, ARIA exposure, or wrapper semantics so that existing copy reads as normal extractable text.
4. Use CSS only to preserve the current rendered appearance. The human-facing design should not visibly change.
5. Keep the animated hero title, but ensure the accessible/parser text still exposes `Every AI. One experience.` once.
6. Remove or stop relying on `.extractor-fallback` if it remains hidden and ineffective. Do not leave dead hidden SEO-like text unless there is a separate accessibility reason.
7. If the only way to make the target extractor work is to add a new visible paragraph, new visible block, or layout change, stop and report. Do not ship that change under this ticket.

The goal is not to add a visible debug block. The goal is to make the homepage's actual existing copy article-shaped enough for extractors while preserving the page's current design.

## Constraints

1. No design change.
2. No new visible block or section.
3. No visible copy addition unless Parker separately approves the exact visual result.
4. No CTA changes.
5. No React, Babel, JSX, unpkg, or Google Fonts.
6. No demo/login/hosted-mcp changes.
7. No deploy changes. Stop at PR.
8. Do not point the visible homepage hero or letter at `agent.txt` as the main path.
9. Keep `agent.txt` and `llms.txt` as fallback/convention surfaces, not the Speedrun-facing primary URL.
10. Do not rely on visually hidden or clipped text as the primary extraction fix.
11. Do not create duplicate visible or accessible hero text.

## Acceptance criteria

- `https://wip.computer/` raw HTML contains the canonical launch meaning through existing visible homepage copy, not only hidden fallback text.
- The visible homepage design is unchanged from the current live/merged page.
- No new visible text block, section, or layout element is added.
- The homepage does not visibly duplicate `Every AI. One experience.`
- Accessibility text does not duplicate `Every AI. One experience.`
- The primary CTA remains `https://wip.computer/login?next=/demo`.
- No homepage JavaScript framework or third-party render dependency is introduced.
- If the target extractor still fails after no-design-change semantic cleanup, the PR documents that result and does not make a visual workaround.
- Run `git diff --check`.
- Run `node --check wip.computer/app.js` if `app.js` changes.

## Out of scope

- Changing the Speedrun submission.
- Changing `agent.txt` or `llms.txt`.
- Changing GitHub org README copy.
- Changing the demo.
- Redesigning the homepage.
