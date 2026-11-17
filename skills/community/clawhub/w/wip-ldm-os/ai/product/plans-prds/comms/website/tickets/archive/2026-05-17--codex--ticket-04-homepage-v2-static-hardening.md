# Ticket 04: Homepage V2 static hardening

**Date:** 2026-05-17
**Filed by:** Codex, after Parker V1 launch override
**Status:** archived, verified closed for the active homepage launch path. Live homepage verification on 2026-05-21 found no React, Babel, unpkg, or remote render dependency.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** V1 homepage live, Ticket 02 login/demo launch path working
**Related V1 merge:** `wip-websites-private` PR #48, merge commit `726af6a3afc71e06ef7860d078879d6c43431f5e`
**Related narrow follow-up:** `archive/2026-05-17--codex--ticket-06-homepage-agent-readable-html.md` (completed and archived)

## Summary

Archived 2026-05-21: the active live homepage no longer depends on the V1 prototype runtime. Any future framework migration belongs to the website dev/Next.js roadmap, not this launch hardening ticket.

V1 intentionally ships the frozen homepage proto runtime so the Speedrun page can get live quickly. Parker explicitly accepted React, Babel, unpkg, and Google Fonts for V1 on 2026-05-17.

This ticket is the required V2 cleanup: preserve the exact approved homepage design and behavior, but replace the prototype runtime with the intended production form.

## Scope

Work in `repos/wip-web/wip-websites-private/wip.computer/`.

Use the tracked V3 export as the visual and behavior reference:

- `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/`
- `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/BEHAVIOR.md`
- `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/components.jsx`
- `ai/product/plans-prds/comms/website/proto-files/archive/v03/export/styles.css`

## Required changes

1. Replace React and JSX with static HTML plus vanilla JavaScript progressive enhancement.
2. Remove Babel Standalone and all `type="text/babel"` scripts.
3. Remove all unpkg runtime dependencies.
4. Remove Google Fonts. Self-host Inter Tight under `wip.computer/`, or use the approved system fallback until the font files are present.
5. Put the resolved headline and founder letter text directly in `index.html` so view-source and JavaScript-disabled rendering show real content.
6. Reimplement the interactive pieces from `BEHAVIOR.md` in vanilla JavaScript:
   - typewriter cycle
   - header scroll state and CTA fade
   - Bucky background drift and image cycle
   - architecture reveal and close
   - footer passkey status behavior
7. Preserve the V1 design and copy. No redesign, recopy, or retiming unless explicitly approved.

## Acceptance criteria

- No React, ReactDOM, Babel, JSX, or framework runtime in shipped homepage files.
- No third-party CDN is required to render the homepage.
- `wip.computer/index.html` contains the real headline and founder letter text as static DOM.
- Page remains readable with JavaScript disabled.
- Fonts are served from `wip.computer` or fall back to system fonts without a remote request.
- Desktop and mobile screenshots match the V1 visual reference within faithful-port tolerance.
- Primary CTA remains `https://wip.computer/login?next=/demo`.
- Existing subpages are not deleted or overwritten by the deploy.

## Out of scope

- Login/demo implementation. That is Ticket 02.
- Full app architecture migration into `kaleidoscope-private`.
- Any visual redesign.
- Any production deploy without dev preview approval.

## Notes

The V1 exception is not a defect in the launch plan. It is a deliberate deadline tradeoff. This ticket exists so the exception does not become permanent by accident.

Homepage static hardening substantially shipped through `wip-websites-private` PR #49 and later PRs. Ticket 06's narrower fetch-readability gap is archived after PR #55 made Claude Code Fetch read the live homepage body. This ticket remains open only for the final hardening audit: confirm no framework runtime or third-party render dependency, confirm JavaScript-disabled readability, and decide whether system font fallback is acceptable or whether Inter Tight self-hosting needs its own ticket.
