# Ticket 17: Apply V04 footer, login, and legal-page export to current site

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** archived, superseded by V05/header/footer/legal follow-up tickets and implementation PRs.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Source artifact:** `ai/product/plans-prds/comms/website/proto-files/archive/v04/export-2026-05-18/`
**Related:** Ticket 11 demo/login visual polish, Ticket 16 website copy audit, future legal-copy review ticket
**Surface:** active homepage, hosted Kaleidoscope login, privacy policy, terms of use

## Problem

Archived 2026-05-21: V04 was the intermediate export. The active site moved through V05 header polish, footer brand links, login footer link, legal footer work, and the Visualizations footer link. Keep this ticket as source-history only.

Parker updated the V04 export with the next website polish pass:

- homepage footer uses the new grouped product/system map
- Kaleidoscope login uses the same footer and a white background
- privacy policy and terms pages use the same footer and white background
- passkeys info popover behavior is improved

Those changes are currently in the V04 export artifact, not yet applied to the current live site repos.

This ticket exists so the coder can apply the V04 export to the actual current codebase without drifting into unrelated copy rewrites or deploy work.

## Source Of Truth

Use this export as the design reference:

```text
ai/product/plans-prds/comms/website/proto-files/archive/v04/export-2026-05-18/
```

The export includes:

```text
CHANGELOG.md
wip.computer/index.html
wip.computer/styles.css
wip.computer/app.js
```

The `CHANGELOG.md` in that export is part of the implementation brief. Read it before editing.

## Scope

Apply the V04 export changes to the current website and hosted-mcp surfaces.

### `wip-websites-private`

Target current files under:

```text
repos/wip-web/wip-websites-private/wip.computer/
```

Apply the V04 homepage changes:

- update the homepage footer to the grouped footer structure
- preserve the footer taxonomy from the V04 export:
  - `AI Infrastructure`
  - `AI Skills`
  - `Applications`
  - `Tools`
  - `Connect`
- keep the current homepage content and behavior unless the export explicitly changes footer or passkeys behavior
- apply the footer CSS, responsive behavior, and overflow fixes from the export
- apply the passkeys info popover behavior from the export

### `wip-ldm-os-private`

Target current files under:

```text
repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/
```

Apply the V04 hosted-mcp changes:

- `app/kaleidoscope-login.html`
  - change login background to white
  - remove desktop overflow clipping if needed so the footer can flow naturally
  - replace the old Kaleidoscope footer with the V04 homepage footer
  - preserve existing login, WebAuthn, passkey, next-routing, Remote Control, pair/relink, and token behavior
- `legal/privacy/en-ww/index.html`
  - change background and header background to white
  - replace the old footer with the V04 homepage footer
  - fix legal-page footer CSS that forces centered inline blocks
  - do not rewrite the policy content in this ticket
- `legal/internet-services/terms/site.html`
  - change background and header background to white
  - replace the old footer with the V04 homepage footer
  - fix legal-page footer CSS that forces centered inline blocks
  - do not rewrite the terms content in this ticket

## Copy Pass Order

Do the visible copy review first, before the CSS/apply pass, so the footer labels and links are not blindly copied if the current product naming has shifted.

Required checks:

- `DevOps Toolkit` is the preferred name unless the current repo/source of truth says otherwise.
- Keep footer labels as product names, not type names. Example: `1Password`, not `1Password Skill`.
- `Universal Installer` belongs under `AI Skills` in the footer for user discovery, even if it now lives structurally under LDM OS.
- Ensure this ticket does not reintroduce `sovereign` / `sovereignty` language into active launch copy. Coordinate with Ticket 16 if there is overlap.
- Verify every footer link target before PR handoff. If a repo URL is uncertain, do not invent one. Report it.

## Legal Copy Is A Separate Follow-Up

Parker wants to review the privacy policy and terms of service because the current text may not be correct.

That is not this ticket.

This ticket applies the V04 footer and white-background presentation to the legal pages, while preserving the legal body copy. File or update a separate legal-review ticket after this one if legal terms or privacy language need substantive changes.

## Out Of Scope

- Do not redesign the homepage outside the V04 footer changes.
- Do not change homepage hero, letter, architecture reveal, typewriter, or Bucky behavior except where the V04 `app.js` footer popover change requires careful integration.
- Do not change hosted-mcp server behavior.
- Do not change login auth, WebAuthn, passkey creation, passkey sign-in, `next` allowlist, Remote Control, pair/relink, wallet, image API, relay, daemon, E2EE, or API keys.
- Do not deploy.
- Do not update legal-policy substance in this ticket.
- Do not mass-rewrite historical pages.

## Acceptance Criteria

- Homepage footer matches the V04 grouped footer design and remains responsive.
- Kaleidoscope login page uses white background and the same grouped footer.
- Privacy page uses white background and the same grouped footer.
- Terms page uses white background and the same grouped footer.
- Footer passkeys state toggle still works where present.
- Passkeys info popover stays inside the viewport and closes on outside click, Escape, scroll, and resize as described by the V04 changelog.
- Existing login/demo behavior still works.
- Existing homepage CTA remains pointed at the current launch path unless a separate ticket changes `/demo` to `/onboarding`.
- Legal content is preserved except for footer/header/background presentation changes.
- Footer links are verified and reported in the PR.
- No `sovereign` / `sovereignty` language is newly added to active launch copy.
- No hidden extractor-only content is added.

## Validation

Run the relevant checks for each repo touched.

Minimum expected checks:

- `git diff --check`
- homepage raw HTML still includes current launch copy and CTA
- homepage has no React, Babel, JSX, unpkg, or Google Fonts reintroduced
- `node --check wip.computer/app.js` if `app.js` changes
- inline script parse check for `app/kaleidoscope-login.html` if its inline JS changes
- static grep that old footer script references are not left behind on pages converted to the new inline footer
- verify only intended files changed in each repo

## Review Notes For Coder

Use fresh worktrees for every repo touched.

Stop at PR. Do not deploy.

Report:

- exact files changed in `wip-websites-private`
- exact files changed in `wip-ldm-os-private`
- footer links and their final targets
- whether `DevOps Toolkit` / `DevOps Toolbox` required a naming decision
- whether legal body copy was preserved byte-for-byte apart from presentation/footer integration
- any uncertainty that should become a follow-up ticket
