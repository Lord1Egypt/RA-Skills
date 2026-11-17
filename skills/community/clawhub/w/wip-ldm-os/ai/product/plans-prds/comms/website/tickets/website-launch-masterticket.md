# Ticket 00 (Master): Website launch order of operations

**Date:** 2026-05-17
**Filed by:** cc-mini (reviewer session, with Parker)
**Status:** open, index ticket
**Deadline driver:** a16z Speedrun submission. Parker submits once the homepage is live and the login/demo path works.
**Relates to:**
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--cc-mini--ticket-03-launch-as-is-then-architecture-compliance.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-04-homepage-v2-static-hardening.md`
- `ai/product/plans-prds/comms/website/tickets/2026-05-17--codex--ticket-05-marketing-deploy-topology-cleanup.md`
- `ai/product/plans-prds/comms/website/tickets/2026-05-18--codex--ticket-11-demo-background-and-blue-polish.md`
- `ai/product/plans-prds/comms/website/tickets/2026-05-18--codex--ticket-12-homepage-hero-duplicate-text.md`
- `ai/product/plans-prds/comms/website/tickets/2026-05-18--codex--ticket-16-website-copy-remove-sovereign-language.md`
- `ai/product/plans-prds/comms/website/tickets/2026-05-21--codex--ticket-23-homepage-hero-background-device-presets.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-18--codex--ticket-17-apply-v04-footer-login-legal-export.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-18--codex--ticket-18-product-wide-privacy-terms-review.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-20--codex--ticket-19-v05-header-nav-legal-polish.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-20--codex--ticket-20-footer-brand-home-link.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-21--codex--ticket-21-login-footer-brand-home-link.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-21--codex--ticket-22-footer-visualizations-link.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--cc-mini--ticket-01-replace-homepage-with-export.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--cc-mini--ticket-02-fix-login-demo-entry.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-06-homepage-agent-readable-html.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-07-demo-mobile-chat-footer.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-08-demo-image-api-400.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-09-demo-icon-login-next.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-17--codex--ticket-10-update-agent-txt-for-launch.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-18--codex--ticket-13-homepage-demo-walkthrough-copy.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-18--codex--ticket-14-homepage-extractor-fallback.md`
- `ai/product/plans-prds/comms/website/tickets/archive/2026-05-18--codex--ticket-15-demo-direct-entry-login-gate.md`
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md` (stale in places; see Ticket 03)

## Purpose

One place to see every ticket for the website launch and the exact order they run in. This is the index. Detail lives in the individual tickets.

## Verified ground truth (checked 2026-05-17, do not relitigate)

Established by direct verification this session, not by reading plan docs. Plan docs that disagree are stale.

1. The live marketing site is `repos/wip-web/wip-computer-website/static/wip-websites-private`, plain static HTML in its `wip.computer/` directory, deployed by a manual `bash deploy.sh` rsync to the Linode VPS. The server runs no build and no git.
2. `repos/wip-web/wip-computer-website/dev/` is the planning lane for static-to-app staging. Use it for shared WIP Site Shell prototypes and migration work before promoting to static production or the full Next.js app.
3. `repos/wip-web/wip-computer-website/next-js/wip-web-private/` is the future full Next.js WIP website app. It is not the current production source.
4. The live `wip.computer/login` and `wip.computer/demo` are served byte-for-byte by `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/`. Verified by fetching the live site on 2026-05-17: `/login` returned 34,343 bytes containing `Enter the Kaleidoscope`, `success-view`, `redirectToRemoteControlIfDirectLogin`; `/demo/` returned 41,727 bytes, an exact byte match to `src/hosted-mcp/demo/index.html`. No `__NEXT_DATA__`, no `/_next/`. The Next.js app in `repos/ldm-os/apps/kaleidoscope-private/web` does NOT serve these routes today.
5. `kaleidoscope-private` is the documented future home for Kaleidoscope app UI and app logic, but moving `/login` and `/demo` there is a live-domain nginx cutover, not a fast-track. That is the post-launch pass, not the submission pass.

## Roles (set by Parker, 2026-05-17)

1. cc-mini writes the tickets. (this PR)
2. Codex reviews the tickets.
3. Codex codes the implementation.
4. A separate Claude Code deployer deploys.

A coder hands off to reviewers. Reviewers hand off to the deployer. The deployer is the only one who runs `bash deploy.sh`.

## Worktree Rule

All implementation work for this launch happens in a fresh git worktree on a new branch. No coding in a dirty or shared checkout. Parker, 2026-05-17: "all of this stuff should happen in a worktree, and all this stuff should be stashed so that nothing ever gets deleted."

- Do not clean, reset, or delete existing local changes in the shared checkout. If it is dirty, leave it alone and branch a worktree from the current target branch.
- Capture any local state non-destructively first: `git stash push -u -- <paths>` or a backup branch. Never discard untracked files or deleted-file state. Nothing gets deleted; it gets stashed or branched aside.
- The frozen export and ticket artifacts must be committed, or intentionally copied into the implementation worktree, before coding starts. Do not rely on untracked files in the shared checkout. This is the exact failure to prevent: a seat sees dirty, untracked, or deleted state, "cleans it up," and loses the design export or the copy archive.
- The original checkout is read-only for context unless Parker explicitly says otherwise.

Required pattern:

```bash
git fetch origin
git worktree add .worktrees/<repo>--<agent>--<ticket-slug> origin/main -b <agent>/<ticket-slug>
```

Then all edits, commits, tests, and PR creation happen from the worktree.

## Execution Order

Set by Parker 2026-05-17. These seven steps are the authoritative sequence; the three tickets map onto them.

1. Update the tickets so the source artifacts and scope are correct. The frozen export is tracked at `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/`, and the website text source is tracked at `ai/product/plans-prds/comms/website/website-text/`. Ticket 01 is homepage only. Ticket 02 is login/demo only. Ticket 03 is launch policy plus post-launch architecture compliance.
2. Replace the current `wip.computer` homepage. Work in `repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/`. V1 ships the frozen proto runtime as-is by explicit Parker override on 2026-05-17 so the page can get live quickly. The vanilla static, no-CDN, no-React production form is deferred to Ticket 04. (Ticket 01, then Ticket 04)
3. Verify homepage links. All homepage links resolve. Primary CTA points to `https://wip.computer/login?next=/demo`. Architecture reveal works. Footer links work. (Ticket 01)
4. Deploy homepage V1 directly to production with a homepage-scoped copy. The `dev.wip.computer` preview gate is waived for V1 because no dev vhost is currently serving the marketing site. For V1, render correctness and link correctness are checked on production immediately after the scoped push; JS-disabled readability and no third-party CDN are knowingly deferred to Ticket 04. Homepage V1 deploy is homepage-only: do not run a blind full-site mirror that can overwrite or delete existing subpages. (Ticket 01 produces V1; Ticket 03 Phase A is the launch gate)
5. Fix the login page success flow. Work in `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/login.html`. Plain `/login` sign-in or create-account with no `next` shows a clear primary "Try the Demo" action. `/login?next=/demo` does not stop on the success screen; after a successful login it goes straight to `/demo`. (Ticket 02)
6. Make the demo entry actually work. Add `/demo` as an exact allowed `next` target where required. No wildcard or prefix allowlist. Existing Remote Control `next` paths keep working. Clicking "Try the Demo" from plain login enters `/demo`. (Ticket 02)
7. Fix the inside of `/demo` just enough for Demo 1. Keep it scripted. Fix only the CSS and entry-state bugs needed for the launch path so it reads as one product with the homepage and login. Do not connect a live Lēsa backend. Do not build Demo 2. Do not refactor Remote Control, passkey/WebAuthn, pair/relink, relay, daemon sync, or E2EE. (Ticket 02)

Dependency: steps 5 and 6 (login/demo) gate the truthfulness of the steps 2 to 4 homepage launch, because the primary CTA points at `https://wip.computer/login?next=/demo`. Steps 2 and 5 can be coded in parallel; the launch waits on both being deployed.

## Status

Twenty-three tickets were filed for the launch. As of 2026-05-21, the active website tickets are Ticket 05 (marketing deploy topology cleanup), Ticket 11 (login/demo background and blue polish, pending direct live visual assessment), Ticket 12 (homepage duplicate parsed hero text, still open for the `hero__ghost` reader-inert check), Ticket 16 (active launch-surface copy audit to remove `sovereign` language while leaving historical/Lēsa/archive pages out of scope unless Parker expands it), and Ticket 23 (homepage hero background desktop/mobile first-load presets plus 15-second preset fading). Completed launch tickets are archived under `ai/product/plans-prds/comms/website/tickets/archive/`.

CURRENT OPEN PR 2026-05-21: `wip-ldm-os-private` PR #1041 remains the only immediate open PR relevant to the mobile cache issue. Live hosted HTML responses for `/login`, `/demo/`, and `/legal/privacy/` were checked on 2026-05-21 and did not include explicit no-cache headers. Treat #1041 separately from the completed footer/header/legal launch tickets.

RESOLVED 2026-05-17: the source-artifact blocker is closed. The frozen V3 export is tracked at `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/`, and the website text source is tracked at `ai/product/plans-prds/comms/website/website-text/`. Old duplicate copy lives under `ai/product/plans-prds/comms/website/_trash/`. Ticket 01 can now start from a fresh worktree.

RESOLVED 2026-05-17: Ticket 01 V1 homepage PR #48 merged in `wip-websites-private` at merge commit `726af6a3afc71e06ef7860d078879d6c43431f5e`. That PR intentionally ships the proto runtime with React, Babel, unpkg, and Google Fonts by Parker override for V1. This does not close the production-form debt; Ticket 04 tracks the vanilla static, no-third-party-CDN, JS-disabled-readable hardening pass.

DEPLOY CONSTRAINT 2026-05-17: Parker clarified "don't delete the sub pages, just that home page." V1 homepage deployment must update only the homepage files and required homepage assets. Do not use a full `rsync --delete` mirror of `wip.computer/` unless the deployer has first proven it cannot overwrite or delete live subpage content.

V1 PROD OVERRIDE 2026-05-17: the deployer verified that `dev.wip.computer` is not a working marketing-site preview vhost. Do not block V1 on setting up dev. Push only the nine homepage files from PR #48 to production, no `--delete`, then immediately verify the production homepage and the existing subpages. The broken deploy topology is post-launch cleanup tracked by Ticket 05, not a homepage launch blocker. The local `repos/wip-web/wip-computer-website/dev/` lane is now reserved for staging static-to-app shell work; it is not the same thing as a live `dev.wip.computer` vhost until deployment docs say so.

ARCHIVED 2026-05-18: the original fetch-readability gap was closed for the narrow launch path. Ticket 06 is archived after the homepage static hardening and PR #55 semantic cleanup made the live homepage body readable to Claude Code Fetch. Ticket 04 remains active for the broader production-form hardening audit.

ARCHIVED 2026-05-18: the demo image API blocker was fixed for launch. Ticket 08 is archived after the minimal xAI request fix, production xAI env correction, deploy, and Parker's manual confirmation that image generation works.

ARCHIVED 2026-05-18: the active demo icon now routes through `https://wip.computer/login?next=/demo`. Ticket 09 is archived after the implementation landed and deployed.

ARCHIVED 2026-05-18: `agent.txt` and `llms.txt` are live as agent-native inspection surfaces. Ticket 10 is archived after both files shipped, mirrored byte-for-byte, and fetched cleanly.

LOGIN/DEMO VISUAL POLISH 2026-05-18: Parker asked for the login background and active demo background to be white, and for the demo blue to match the Kaleidoscope bubble blue, without changing shape or redesigning the demo. Ticket 11 tracks this narrow CSS/color cleanup.

HOMEPAGE PARSER POLISH 2026-05-18: a reviewer parse showed the hero duplicated as "Every AI. Every AI. One experience. One experience." The visual site is good enough, but the parser/accessibility artifact should be fixed without changing the homepage design. Ticket 12 tracks this narrow homepage text exposure cleanup.

ARCHIVED 2026-05-18: the concise four-step demo walkthrough is live on the homepage. Ticket 13 is archived after the copy landed and follow-up styling corrected the list presentation.

ARCHIVED 2026-05-18: Ticket 14 closed with the no-design-change semantic cleanup in PR #55. Hidden extractor-only fallback text was removed, the current design was preserved, and Claude Code Fetch now reads the homepage body. Caveat retained: one weaker Anthropic-style extractor may still return metadata-only; any visible-prose redesign requires a separate design-approved ticket.

ARCHIVED 2026-05-18: direct unauthenticated `/demo` entry now routes through `/login?next=/demo`. Ticket 15 is archived after PR #1002 deployed and Parker confirmed the flow works.

STATUS REFRESH 2026-05-18: Claude Code reviewer verified PR #55 and live state read-only. Completed and archived: Ticket 01 (homepage V1), Ticket 02 (login/demo continuation), Ticket 06 (agent-readable HTML narrow gap), Ticket 07 (active demo footer), Ticket 08 (demo image API), Ticket 09 (demo icon login-next), Ticket 10 (`agent.txt` / `llms.txt`), Ticket 13 (homepage walkthrough), Ticket 14 (no-design-change extractor cleanup), and Ticket 15 (direct demo login gate). Ticket 14 closes as: no-design-change semantic cleanup shipped in `wip-websites-private` PR #55, Claude Code Fetch reads the homepage body, one weaker Anthropic-style extractor may still return metadata-only, and any further visible-prose work requires a separate design-approved ticket.

OPEN REVIEW ITEM 2026-05-18: Ticket 12 remains active because PR #55 exposed the hero heading as normal markup while preserving `hero__ghost` width-reservation spans. Verify the ghost spans remain reader-inert and do not reintroduce `Every AI. Every AI. One experience. One experience.` in stricter parsers or screen readers.

COPY REVIEW 2026-05-18: Parker asked to remove `sovereign` / `sovereignty` language from the active launch website and onboarding-facing copy. Ticket 16 tracks this as a narrow copy audit for active launch surfaces only; historical Day 63, Lume, install specs, archived drafts, and Lēsa pages are not automatically in scope.

V04 EXPORT 2026-05-18: Parker updated the V04 export with the grouped product footer, white Kaleidoscope login background, matching login footer, and white privacy/terms pages with the same footer. Ticket 17 applies those export changes to the current site repos. It also records the work order: review copy and footer link targets first, then apply styles/markup; substantive privacy policy and terms-of-service correctness gets a separate follow-up ticket.

LEGAL REVIEW 2026-05-18: Parker identified that the privacy policy and terms still read as narrow `Kaleidoscope Demo` pages. Ticket 18 tracks the product-wide legal copy review so the pages cover WIP Computer, the website, Kaleidoscope, passkeys, wallet/credits, third-party AI APIs, and future product surfaces without overclaiming what is live.

V05 HEADER POLISH 2026-05-20: Parker supplied the V05 header export with the sprite plus `WORK IN PROGRESS` wordmark, 55px fixed bar, homepage CTA crossfade, and matched edge spacing. Ticket 19 tracks applying that header to the homepage, the Kaleidoscope live wall, and the three legal pages: Privacy Policy, Website Terms, and Kaleidoscope Terms. Login and demo chat remain out of scope.

FOOTER BRAND LINK 2026-05-20: Parker asked for the bottom footer brand line to link back to WIP Computer. Ticket 20 tracks the narrow fix: link only `WIP Computer, Inc.` to `https://wip.computer/` everywhere the current footer appears, while leaving `Learning Dreaming Machines`, `Made in California.`, footer taxonomy, login, demo chat, and legal body copy unchanged.

LOGIN FOOTER BRAND LINK 2026-05-21: Ticket 20 intentionally excluded `/login`. Parker then noticed the login footer still had an unlinked `WIP Computer, Inc.` line. Ticket 21 tracks the narrow login-only follow-up: link only `WIP Computer, Inc.` to `https://wip.computer/`, while leaving login/auth behavior, QR, Local passkeys, `next` routing, `Learning Dreaming Machines`, and `Made in California.` unchanged.

FOOTER VISUALIZATIONS LINK 2026-05-21: Parker wants the Kaleidoscope live wall discoverable from the footer without making it a main CTA. Ticket 22 tracks adding a `Visualizations` link under `Tools` everywhere the current grouped footer appears. The link points to `https://wip.computer/visualizations/kaleidoscope/onboarding/live/`, opens in the same tab, and does not change footer taxonomy beyond that one link or any login, demo, Local passkeys, live-wall data, legal body, or auth behavior.

TRACKER CLEANUP 2026-05-21: Tickets 03, 04, 17, 18, 19, 20, 21, and 22 were moved to `archive/` after their launch decisions or implementation PRs landed. Ticket 03 is historical launch policy. Ticket 04 is closed for the live homepage hardening pass after live verification found no React/Babel/unpkg/remote render dependency. Ticket 17 is superseded by V05/header/footer/legal follow-ups. Ticket 18 shipped through legal PRs #1026, #1033, and #1056. Ticket 19 shipped through website #61 and hosted legal #1054. Ticket 20 shipped through website #62 and hosted legal #1055. Ticket 21 shipped through hosted-mcp #1058. Ticket 22 shipped through website #63 and hosted-mcp #1061. Stale live-wall ticket PR #1024 should be closed as superseded by the shipped live wall and the newer Kaleidoscope stats baseline ticket #1062.

HOMEPAGE HERO BACKGROUND PRESETS 2026-05-21: Parker supplied separate desktop and mobile first-load hero background coordinates because the same coordinate set does not frame correctly across form factors. Ticket 23 tracks the narrow homepage change: deterministic first-load Bucky preset per device, separate desktop/mobile preset buckets, existing desktop preset list preserved, a seed mobile bucket, and 15-second fading transitions after load.
