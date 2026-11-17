# Ticket 01: Replace the wip.computer homepage with the frozen export

**Date:** 2026-05-17
**Filed by:** cc-mini (reviewer session, with Parker)
**Status:** archived 2026-05-18. V1 merged by PR #48 in `wip-websites-private` at `726af6a3afc71e06ef7860d078879d6c43431f5e`; production-form hardening deferred to Ticket 04.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Source artifact:** `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/`
**Locked copy source:** the export's `proto-files/archive/v03/export/components.jsx` (the frozen reference; the rendered copy is verbatim there) plus `proto-files/archive/v03/export/DEPLOY.md`. Do NOT use `website-text/claude-opus4-7-wip-website-copy-v09.md`: verified 2026-05-17 it is stale (old CTA text, no serious-alpha close, a literal `{ignore}` junk block at line 80).

## Summary

Replace the live `wip.computer` homepage (formerly the LUME dark-theme `wip.computer/index.html` in `repos/wip-web/wip-websites-private`) with the frozen design export. The design and behavior are final and frozen. V1 shipped the proto runtime to get the page live quickly; the faithful production-static form is now tracked as Ticket 04.

## V1 launch exception

Parker explicitly overrode the production-form constraints for V1 on 2026-05-17 so the homepage could get live before the Speedrun submission. PR #48 in `wip-websites-private` merged at `726af6a3afc71e06ef7860d078879d6c43431f5e` and intentionally shipped the frozen proto runtime as-is, including React, Babel, unpkg, and Google Fonts.

That decision was a V1 launch exception, not approval of the final production architecture. The constraints below still describe the required V2 hardening pass, now tracked in `2026-05-17--codex--ticket-04-homepage-v2-static-hardening.md`.

## Source: what the export is

`proto-files/archive/v03/export/` is the faithful frozen reference, not the production artifact:

- `Homepage.html` ... entry point. Loads React 18, ReactDOM, and Babel Standalone from the unpkg CDN, transpiles `components.jsx` in the browser, mounts `<App/>`.
- `components.jsx` ... all UI (Header, Hero, HeroTitle typewriter, Letter, Products/Architecture reveal, Footer; `BUCKY_PRESETS`; `SOCIAL_ICONS`).
- `styles.css` ... vanilla CSS, token block at top.
- `BEHAVIOR.md` ... the authoritative reimplementation spec. Exact timings, easings, caret states, typewriter cycle, bucky background behavior. The port matches this, not a re-derivation.
- `FILE_MAP.md`, `DEPLOY.md` ... structure and deploy notes.
- `assets/` ... `wip-logo.png` and `bucky-patent-1.gif` through `bucky-patent-5.gif`. All five present, verified 2026-05-17 (the earlier missing `bucky-patent-2.gif` was restored).
- `screenshots/` ... 5 reference renders (desktop hero, letter, architecture-open, footer, mobile hero).

`FILE_MAP.md` states plainly that the React + in-browser-Babel form was for design iteration speed and production wants vanilla, no framework runtime, with fonts embedded locally. The port boundary is clean: every component is self-contained.

## Known gaps

1. Copy source. `website-text/claude-opus4-7-wip-website-copy-v09.md` is stale (old CTA text, no serious-alpha close, a literal `{ignore}` junk block at line 80). The authoritative copy is the export's `components.jsx` (the frozen rendered copy, including the current alpha letter at `components.jsx:618-634`) plus `DEPLOY.md`. Port copy from there. If a standalone markdown copy doc is wanted, a `v10` must be generated from the export first; do not port from v09.
2. Missing asset (RESOLVED 2026-05-17). `bucky-patent-2.gif` was absent when this ticket was first filed; it has since been restored. All five `bucky-patent-{1..5}.gif` are present and match the `components.jsx:92` `BUCKY_IMAGES` references. No coder action needed; kept here for review history.

## Target

- Repo: `repos/wip-web/wip-websites-private`.
- File: replace `wip.computer/index.html` (currently LUME dark theme).
- Assets: `wip.computer/assets/` (or the page folder), self-hosted.
- The server runs no build and no git. It serves static files as-is.

## V2 constraints (decided, do not relitigate)

1. Vanilla static HTML, CSS, and JS. No React, no JSX, no build step, no framework runtime in the shipped page.
2. The shipped page renders with no third-party CDN at all. No unpkg React/Babel. No Google Fonts CDN; self-host Inter Tight. Use Georgia or a system serif as the fallback, do not bundle Georgia (it is a system font). This is the sovereignty constraint: the homepage cannot depend on a third party to render the argument it is making.
3. Real page text in the DOM. The page is fully readable with JavaScript disabled. The hero ships the resolved headline ("Every AI. One experience.") as static DOM; the typewriter is progressive enhancement on top, per BEHAVIOR.md.
4. Design and behavior are frozen. `BEHAVIOR.md` is authoritative. Match its timings and states. Do not "improve" anything during the port. Behavior gaps it documents (for example, the bucky background not currently honoring `prefers-reduced-motion`) are decided at this port, on purpose, documented in the PR, not silently changed.
5. Copy is verbatim. The founder letter, the 8 architecture entries (no reordering), the 4 typewriter groups (no edits to individual payoffs), and the title come from the export's `components.jsx` (the frozen rendered copy) and `DEPLOY.md`. Copy v09 is stale and must NOT be used as the source. No paraphrasing.
6. International Klein Blue is the only accent and only on the primary action (the "Demo Kaleidoscope" pill). Nothing else is colored. White background, OpenAI-level restraint.
7. Accessibility: `prefers-reduced-motion` honored for the port's animation decisions, real text in DOM, animation degrades to the resolved static state.

## External links that must stay live (from DEPLOY.md)

- `https://wip.computer/login?next=/demo` ... the three Demo Kaleidoscope CTAs. This is the dependency on the login/demo fix (master Step 1). If that path is not real at launch, the CTA is not truthful; see Ticket 03 for the launch gate.
- `https://github.com/wipcomputer`, `https://x.com/wipcomputer`, `https://wip.computer/agent.txt`, the two legal URLs in `DEPLOY.md`.

## Scope boundary

Marketing repo only (`wip-websites-private`). This ticket does not touch the login/demo app lane (`wip-ldm-os-private/src/hosted-mcp/`) or the Next.js app (`kaleidoscope-private`). It only depends on the CTA target existing.

## V1 acceptance criteria

- `wip-websites-private` PR #48 is merged.
- Homepage V1 renders in the browser from `wip.computer/index.html`.
- Homepage assets needed by V1 are present.
- The primary CTA remains `https://wip.computer/login?next=/demo`.
- No deploy is performed from a dirty shared checkout.
- Production deploy is homepage-only and does not delete or overwrite existing subpages.
- `dev.wip.computer` is not required for V1 because it is not currently wired to the marketing site.

## V2 acceptance criteria

- Live `wip.computer` serves the new homepage; the old LUME dark page is gone.
- View-source shows the real headline and letter text with JavaScript disabled.
- No network request to any third-party CDN is required to render (verify with devtools offline-after-first-paint or request log).
- Fonts are served from `wip.computer`, not Google.
- Visual and interaction parity with `screenshots/` and `BEHAVIOR.md` within faithful-port tolerance.
- All external links above resolve.
- Previewed through a verified marketing-site preview path before any V2 production deploy, after Ticket 05 or equivalent cleanup restores that path.

## Out of scope

- Any design change, copy rewrite, or behavior "fix" not explicitly documented as a port decision.
- The login/demo fix (master Step 1, separate ticket).
- The architecture-compliance refactor (Ticket 03).
- Migration to the Next.js `kaleidoscope-private` app (post-launch).

## Process

1. cc-mini wrote this ticket.
2. Codex reviewed it (2026-05-17): flagged stale copy source (v09), the then-missing bucky asset, and font wording.
3. cc-mini revised per the review (this PR): copy source corrected to the export's `components.jsx` plus `DEPLOY.md`, bucky asset confirmed restored, font wording fixed.
4. Codex coded V1 in `wip-websites-private` PR #48.
5. Codex and cc-mini reviewers blocked the PR against the V2 constraints, then Parker explicitly accepted the V1 proto-runtime exception for speed.
6. PR #48 merged. Deployment is delegated separately and must be homepage-only.
7. Ticket 04 tracks the V2 production-static hardening.

Next step: deploy homepage V1, then complete Ticket 02 login/demo.
