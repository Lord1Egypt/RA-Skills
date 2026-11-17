# Ticket 03: Launch as-is, then architecture-compliance refactor

**Date:** 2026-05-17
**Filed by:** cc-mini (reviewer session, with Parker)
**Status:** archived, launch policy recorded. V1 homepage exception was recorded; V2 static hardening split to Ticket 04 and later closed after live verification.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 01 (homepage port) and master Step 1 (login/demo fix) deployed.

## Summary

Archived 2026-05-21: this is historical launch policy, not remaining implementation work. The launch exception and follow-up split are preserved here for audit history.

A two-phase policy ticket. Phase A: once the homepage V1 and the login/demo fix are deployed (may be the next day), launch the homepage as-is for the Speedrun submission. Phase B: go back and make everything the page links to compliant with our architecture, with zero change to the approved design.

The design is finished and frozen. This ticket is explicitly not a redesign. It changes what is underneath and what the page points at, not how the page looks or behaves.

## Phase A: launch as-is

"As-is" for V1 means the frozen proto runtime merged in `wip-websites-private` PR #48 at `726af6a3afc71e06ef7860d078879d6c43431f5e`, with the login/demo path (master Step 1) real behind the CTA. Parker explicitly accepted React, Babel, unpkg, and Google Fonts for V1 on 2026-05-17 so the page can get live quickly. The faithful production-static port is deferred to Ticket 04.

- Trigger: Ticket 01 deployed and master Step 1 deployed. Could be the next day.
- The deployer launches the homepage directly to production for V1. The `dev.wip.computer` preview gate is waived because no dev vhost is currently serving the marketing site.
- Deploy scope: homepage V1 only. Parker clarified 2026-05-17: "don't delete the sub pages, just that home page." Do not run a blind full-site mirror that can overwrite or delete existing subpages. Update only the homepage files and required homepage assets unless a scoped deploy plan proves subpages are untouched.
- For this V1 push, use a scoped copy of the nine PR #48 homepage files only: `index.html`, `styles.css`, `components.jsx`, `assets/wip-logo.png`, and `assets/bucky-patent-1.gif` through `assets/bucky-patent-5.gif`. No `--delete`.
- Verify on production immediately after the push. Confirm the new homepage loads, homepage assets return 200, and existing subpages are still present. Do not spend time setting up dev before the Speedrun submission.
- Accept knowingly: the page is design-final but not yet architecture-compliant. Some linked surfaces and the underlying structure are not yet refactored to our system. That is a deliberate, time-boxed tradeoff to make the Speedrun submission. It is not a defect to be fixed before launch.
- Accept knowingly: homepage V1 is not yet sovereignty-compliant. JS-disabled readable DOM, no React/Babel, no unpkg, and no Google Fonts are deferred to Ticket 04.
- Launch gate (truthfulness): the homepage primary CTA points at `https://wip.computer/login?next=/demo`. Phase A does not launch until that path is real (master Step 1 deployed) or the CTA is consciously gated or softened. A live homepage with a dead or dishonest primary CTA does not ship. This is the one hard precondition.

## Phase B: architecture-compliance refactor

After the submission is in, refactor for compliance. Hold the design exactly constant.

- Do not change anything from the design process. The visual design and the interaction behavior are frozen. No pixel, no copy, no animation timing changes. If a compliance change would alter the rendered result, it is out of scope for this ticket and gets escalated, not absorbed.
- What does change: everything the page links to and the architecture underneath it gets brought to our system. In scope:
  - Every external and internal link target reviewed and pointed at the correct, canonical surface (for example, the login/demo path on its final architecture, legal URLs, agent.txt, repo links).
  - Alignment with the documented destination architecture (the eventual `kaleidoscope-private` app lane and the marketing-site conventions), without re-rendering the page differently.
  - Extraction of the now-canonical design language (the IKB token, the neutrals, the type scale, spacing, and the shared components the homepage and the Kaleidoscope chat establish) into a single shared spec so future pages are generated against one system instead of re-guessing it. Same output, codified.
- The test of a correct Phase B change: the page looks and behaves identically before and after, but what it links to and what it is built on are correct.

### Phase B is not one coding unit (from Codex ticket review 2026-05-17)

This ticket stays a policy / epic. Phase B must not be handed to a coder as a single implementation. Before any Phase B coding starts, split it into separate, independently reviewable tickets:

1. Link audit: every external and internal link target inventoried and pointed at its canonical surface.
2. Architecture cutover plan: how the page aligns to the destination architecture (the `kaleidoscope-private` app lane and marketing-site conventions) without re-rendering differently.
3. Shared design spec extraction: the IKB token, neutrals, type scale, spacing, and the shared homepage/chat components codified into one spec.
4. Visual-regression harness: the before/after zero-difference proof mechanism.

Each spawned from this epic, each its own ticket, reviewed and shipped on its own.

## Acceptance criteria

Phase A:
- Live `wip.computer` is the Ticket 01 V1 homepage.
- The primary CTA resolves into a working Demo 1 (master Step 1 live), or is consciously gated. No dishonest CTA on the live page.
- Existing subpages are not deleted or overwritten by the homepage deploy.
- `dev.wip.computer` is not required for V1 because it is not currently wired to the marketing site.
- Parker can submit Speedrun pointing at a working homepage and demo.

Phase B:
- Every linked surface from the homepage points at its canonical target.
- The design language is extracted into one shared spec; the homepage consumes it with no visual or behavioral change.
- A before/after comparison shows zero rendered difference. Any required visual change was escalated, not silently made.

## Out of scope

- Redesigning, recopying, or re-timing anything. The design process output is final.
- The homepage port mechanics themselves (Ticket 01).
- The homepage V2 static/no-CDN/no-React hardening pass (Ticket 04).
- Marketing deploy topology cleanup (Ticket 05).
- The login/demo implementation (master Step 1).

## Process

1. cc-mini wrote this ticket.
2. Codex reviewed it (2026-05-17): accepted as policy/epic, flagged that Phase B is too broad for one coding pass.
3. cc-mini revised per the review (this PR): added the explicit Phase B split into four sub-tickets before any implementation.
4. Parker explicitly accepted the homepage V1 proto-runtime exception on 2026-05-17.
5. Codex recorded that exception here and split the homepage static/no-CDN/no-React hardening into Ticket 04.
6. Phase A is a deploy decision, not code. Phase B sub-tickets are spawned and coded individually when scheduled.
7. A separate Claude Code deployer performs the Phase A launch and any Phase B deploys.

Next step: deploy homepage V1 with the homepage-only deploy constraint, then complete Ticket 02.
