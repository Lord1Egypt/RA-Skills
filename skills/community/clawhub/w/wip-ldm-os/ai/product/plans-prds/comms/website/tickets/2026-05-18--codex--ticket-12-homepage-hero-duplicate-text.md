# Ticket 12: Remove duplicate parsed hero text from homepage

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** open. Homepage accessibility and agent-reader polish. PR #50 fixed the original duplicate parsed hero issue and shipped live. PR #55 later made the hero heading more extractable for Ticket 14, so this ticket remains open only for the post-#55 ghost-span verification below.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 04 homepage static hardening
**Surface:** `repos/wip-web/wip-websites-private/wip.computer/index.html`, and only if required `repos/wip-web/wip-websites-private/wip.computer/app.js` or `repos/wip-web/wip-websites-private/wip.computer/styles.css`

## Summary

The homepage is good enough for the launch and supports the thesis. The remaining glaring text issue is that some parsed views can read the hero as duplicated:

```text
Every AI. Every AI. One experience. One experience.
```

This is likely caused by the animated/typewriter text and the static/accessibility text both being visible to some extraction or accessibility layer.

Fix the homepage so the visible page, raw HTML, accessible text, and common parser output expose the hero once:

```text
Every AI. One experience.
```

## Post-PR-55 Follow-Up

Claude Code reviewer found one real regression risk after `wip-websites-private` PR #55:

- PR #55 removed `aria-label="Every AI. One experience."` from `<h1 class="hero__title">`.
- PR #55 removed line-level `aria-hidden="true"` from the two visible hero line wrappers.
- The hero still contains `hero__ghost` width-reservation spans with `data-hero-top-ghost` and `data-hero-bottom-ghost` values matching the visible headline text.

The change made the homepage more extractable, which was the Ticket 14 goal. The risk is that a stricter parser or screen reader could now read the ghost spans plus the visible spans and expose the headline twice.

Verify the ghost spans are reader-inert after PR #55. If they are not, fix the ghost spans directly without undoing Ticket 14's no-design-change cleanup.

## Desired behavior

- The visual hero still reads correctly.
- The raw HTML remains readable.
- A text parser should not duplicate the hero phrase.
- Screen-reader/accessibility text should not announce duplicate hero content.
- The typewriter/animated behavior should remain intact unless removing duplication requires a minimal accessibility attribute change.

## Scope

Allowed:

- Add or adjust `aria-hidden`, visually hidden text, or semantic heading structure.
- Adjust duplicated fallback/typewriter markup so only one version is exposed to readers and parsers.
- Add `aria-hidden` or another reader-inert treatment directly to `hero__ghost` spans if needed.
- Minimal `app.js` changes if the typewriter injects duplicate text.
- Minimal CSS changes if a visually hidden or parser-safe text pattern is needed.

Not allowed:

- No copy rewrite.
- No homepage redesign.
- No CTA changes.
- No architecture section changes.
- No demo/login/hosted-mcp changes.
- No deploy changes.

## Acceptance criteria

- The homepage still visually shows `Every AI. One experience.`
- Raw HTML still contains the launch copy.
- Parser/accessibility text should not expose `Every AI. Every AI. One experience. One experience.`
- Post-PR-55 `hero__ghost` spans are proven reader-inert or are patched to be reader-inert.
- The Ticket 14 extractability gain is preserved.
- No React, Babel, JSX, unpkg, or Google Fonts are reintroduced.
- Primary CTA remains `https://wip.computer/login?next=/demo`.
- Run `node --check wip.computer/app.js` if `app.js` changes.
- Run `git diff --check`.

## Out of scope

- Any other homepage polish.
- Agent.txt or llms.txt changes.
- Demo visual polish. That is Ticket 11.
