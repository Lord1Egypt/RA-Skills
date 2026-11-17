# Ticket 06: Homepage agent-readable HTML

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Narrow agent-readable homepage goal is met by the static homepage hardening plus `wip-websites-private` PR #55; Claude Code Fetch now reads the live homepage body.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** V3 homepage deployed
**Related:** Ticket 04 homepage V2 static hardening

## Summary

V3 is live and improved unfurls and non-JS fallback behavior, but it did not make the full homepage content available as raw HTML. The live `index.html` still mounts the primary page through React and Babel into an empty `#app` element. A fetcher that does not execute JavaScript sees metadata plus the `noscript` fallback, not the full founder letter or full architecture copy.

That is acceptable for the V1 launch, but it is a real product gap for the public claim that AIs can point at the site and understand what WIP Computer is building.

## Verified current behavior

Live `https://wip.computer/` contains:

- real `<title>`
- real meta description
- Open Graph and Twitter Card metadata
- a `noscript` fallback with short positioning copy
- scripts for React, ReactDOM, Babel, and `components.jsx`
- an empty `<div id="app"></div>` for the full rendered page

Live `https://wip.computer/` does not contain the full founder letter text in the raw HTML response. For example, the raw HTML does not include the letter heading `Transmuting Command C + Command V`. That text still lives in `components.jsx` and appears only after client-side rendering.

## Answer to reviewer or external tester

If someone reports "I only see the meta title and not the body copy," the answer is:

V3 is deployed, but it is not an SSR or static-body conversion. V3 added metadata and a `noscript` fallback so unfurlers and non-JS agents see positioning content. The full homepage body is still client-rendered from `components.jsx`. The full raw-HTML/static DOM conversion is tracked by Ticket 04. This ticket tracks the narrower agent-readable HTML gap and any short-term page we may add before the full static hardening pass.

## Options

Pick one implementation path.

1. Preferred short-term: add a small static page at `/about/`, `/manifesto/`, or `/ai.txt` that contains the founder letter, architecture summary, and canonical links as plain HTML or text. Link it from the homepage and point Speedrun or agent reviewers at it when they need a fetch-readable artifact.
2. Better long-term: complete Ticket 04 and convert the homepage itself to static HTML plus vanilla JavaScript progressive enhancement.
3. Minimum patch: expand the `noscript` block in `index.html` to include the full founder letter and architecture copy. This helps no-JS browsers but may still not satisfy fetchers that ignore or strip `noscript`.

## Recommendation

Do not block the login/demo launch on this ticket.

For Speedrun, use the live homepage for humans and the login/demo flow for the product. If a reviewer, agent, crawler, or fetcher needs a text-readable artifact, point them at a dedicated static URL that we control, or at GitHub, until Ticket 04 is complete.

## Acceptance criteria

- There is at least one WIP-controlled URL that returns meaningful WIP Computer positioning, founder-letter-level context, and architecture copy in raw HTML or plaintext without executing JavaScript.
- The URL is linked from the homepage or otherwise documented in the Speedrun submission notes.
- `curl <url>` shows the relevant body copy directly.
- The implementation does not touch the login/demo lane.
- The implementation does not delete or overwrite existing marketing subpages.
- Ticket 04 remains the full homepage static-hardening ticket.

## Out of scope

- Redesigning the homepage.
- Login/demo fixes.
- Completing the whole Ticket 04 static-hardening pass unless explicitly scheduled.
- Changing the V3 launch decision.
