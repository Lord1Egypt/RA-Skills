# Ticket 19: Apply V05 header/nav polish to homepage and legal pages

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** archived, implemented. Website PR #61 and hosted legal PR #1054 applied the V05 header treatment.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Source artifact:** `ai/product/plans-prds/comms/website/proto-files/archive/v05-new-nav/export-header-2026-05-20/`
**Related:** Ticket 17 footer/login/legal export, Ticket 18 legal rewrite, PR #60 footer passkeys mobile default
**Surface:** homepage, Kaleidoscope live wall, Privacy Policy, Website Terms of Use, Kaleidoscope Terms

## Problem

Archived 2026-05-21: V05 header/nav polish landed for homepage, Kaleidoscope live wall, and hosted legal pages. Keep this ticket as the design source and audit record.

The final sprint polish needs the V05 header treatment applied consistently across the public website, the Kaleidoscope live wall, and the three legal pages.

Today the homepage header has moved closer to the intended behavior, but the legal pages still do not feel like the same surface. When scrolling legal pages, the fixed bar behavior is not matching the homepage: the bar can fail to show correctly, and the page does not read as content moving underneath the same header system.

Separately, the homepage header logo and CTA alignment need to match the V05 header export:

- replace the square WIP logo with the Kaleidoscope sprite plus `WORK IN PROGRESS` wordmark
- keep the brand aligned left and stationary
- keep the sprite inset from the left edge by the same margin used by the right CTA
- keep the blue `Demo Kaleidoscope` button right aligned with the same edge spacing
- use the shorter header height from the V05 export
- preserve the homepage scroll-crossfade behavior for the blue CTA

This ticket exists to capture that last public website polish pass without touching login, chat, wallet, auth, or demo runtime behavior.

## Source Of Truth

Use the V05 export bundle:

```text
ai/product/plans-prds/comms/website/proto-files/archive/v05-new-nav/export-header-2026-05-20/
```

Read its `README.md` before coding. It documents:

- 55px header bar height
- sprite plus `WORK IN PROGRESS` wordmark
- sprite sheet asset at `assets/sprites.png`
- 20px desktop edge padding and 16px mobile edge padding
- homepage right CTA crossfade behavior
- transparent top state and scrolled translucent-white state

The source artifact is included in this ticket PR so the coder should not rely on untracked local files in the shared checkout.

## Scope

### `wip-websites-private`

Target current live website source:

```text
repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/
```

Apply the V05 header to the homepage:

- update the homepage header logo from the old WIP square to the sprite plus `WORK IN PROGRESS` wordmark
- keep the sprite and wordmark left aligned
- keep the brand fixed at the left edge spacing, not centered and not drifting on scroll
- set the header bar height to the V05 value, currently 55px
- preserve the homepage hero and body copy
- preserve the homepage CTA destination unless a separate ticket changes it
- preserve the homepage blue CTA scroll-crossfade behavior
- ensure the blue CTA is right aligned using the same edge spacing as the brand's left spacing
- ensure the blue CTA does not appear duplicated, centered, or offset from the right edge

Apply only the left brand/logo treatment to the Kaleidoscope live wall page:

```text
wip.computer/visualizations/kaleidoscope/onboarding/live/index.html
```

Live-wall requirements:

- use the same sprite plus `WORK IN PROGRESS` wordmark
- use the same 55px header bar height
- keep the brand left aligned with the same edge spacing as the homepage
- keep the centered `Kaleidoscope` page title exactly as the live wall has it now
- do not add the blue `Demo Kaleidoscope` CTA to the live wall
- the blue `Demo Kaleidoscope` header CTA belongs only on the homepage index
- keep the live wall's existing page behavior and data feed unchanged
- do not change live-wall image registry, feed URL, stats, public-wall logic, or image archival behavior

### `wip-ldm-os-private`

Target current legal page source:

```text
repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/legal/
```

Apply the matching V05 header treatment to:

```text
src/hosted-mcp/legal/privacy/index.html
src/hosted-mcp/legal/internet-services/terms/site.html
src/hosted-mcp/legal/internet-services/kaleidoscope/index.html
```

Legal-page requirements:

- use the same 55px header bar height as the homepage
- use the same sprite plus `WORK IN PROGRESS` wordmark
- use the same fixed-header scroll animation as the homepage
- do not include the blue `Demo Kaleidoscope` CTA on legal pages
- ensure the bar stays visible and legible when the user scrolls
- ensure legal content scrolls under the fixed header system in the same way the homepage content does
- keep legal body copy unchanged
- keep footer legal links unchanged unless a direct header layout conflict requires a non-copy fix

## Explicitly Out Of Scope

- Do not touch `/login`.
- Do not touch `/demo` chat.
- Do not touch Kaleidoscope onboarding copy.
- Do not touch WebAuthn, passkeys, QR login, local passkey behavior, Remote Control, relay, daemon, E2EE, wallet, image generation, or API keys.
- Do not touch live-wall data, image feed logic, image archival, xAI URLs, public-wall publishing rules, or stats.
- Do not rewrite legal body content.
- Do not redesign footer taxonomy in this ticket.
- Do not mass-apply this to subpages that are not homepage or the three legal pages.
- Do not deploy.

## Implementation Notes

- The homepage source is static website code in `wip-websites-private`.
- The legal pages are hosted-mcp static HTML files in `wip-ldm-os-private`.
- This will likely require two PRs if the coder touches both repos.
- If the coder finds duplicate header implementations, keep the fix narrow for this sprint and report the duplication as a follow-up. Do not start a full shared-header/template refactor inside this ticket.
- The broader shared WIP Site Shell/template work is a separate follow-up. This ticket is the final sprint polish, not the full architecture cleanup.

## Acceptance Criteria

- Homepage header uses the V05 sprite plus uppercase `WORK IN PROGRESS` wordmark.
- Homepage header height is 55px.
- Homepage brand is left aligned with the V05 edge spacing.
- Homepage blue CTA is right aligned with matching edge spacing.
- Homepage scroll-crossfade CTA still works.
- Homepage does not show a centered or duplicated blue CTA in the header.
- Kaleidoscope live wall left logo/brand matches the homepage brand treatment.
- Kaleidoscope live wall keeps the centered `Kaleidoscope` title.
- Kaleidoscope live wall does not show the blue `Demo Kaleidoscope` header CTA.
- Kaleidoscope live wall keeps its existing wall, stats, feed URL, and interactions unchanged.
- Privacy Policy header matches the homepage header treatment, without the blue CTA.
- Website Terms header matches the homepage header treatment, without the blue CTA.
- Kaleidoscope Terms header matches the homepage header treatment, without the blue CTA.
- On all three legal pages, the fixed bar remains visible on scroll.
- On all three legal pages, the page scroll behavior visually matches the homepage fixed-header behavior.
- Legal body copy is unchanged.
- Login and demo chat are unchanged.

## Validation

Minimum expected checks:

- `git diff --check` in every repo touched
- `node --check wip.computer/app.js` if homepage JS changes
- inline script parse for each legal HTML file whose inline JS changes
- grep that the legal pages do not contain the header blue CTA
- grep that `/login` and `/demo` files were not changed
- visual/manual check on desktop and mobile widths:
  - homepage at top
  - homepage mid-scroll when CTA crossfade should be visible
  - Kaleidoscope live wall at top and mid-scroll
  - Privacy Policy at top and mid-scroll
  - Website Terms at top and mid-scroll
  - Kaleidoscope Terms at top and mid-scroll

## Review Notes For Coder

Use fresh worktrees for every repo touched.

Stop at PR. Do not deploy.

Report:

- exact files changed in `wip-websites-private`
- exact files changed in `wip-ldm-os-private`
- whether the V05 sprite asset had to be copied into the live website repo
- whether legal body copy remained unchanged
- screenshots or clear manual observations for homepage, Kaleidoscope live wall, and all three legal pages at desktop and mobile widths
