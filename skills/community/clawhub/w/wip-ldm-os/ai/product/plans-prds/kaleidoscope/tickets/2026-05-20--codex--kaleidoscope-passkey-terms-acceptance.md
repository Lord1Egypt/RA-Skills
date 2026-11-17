# Kaleidoscope Passkey Terms Acceptance

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Related:** [`2026-05-18--codex--guided-onboarding-intent-engine.md`](2026-05-18--codex--guided-onboarding-intent-engine.md), [`../../comms/website/tickets/2026-05-18--codex--ticket-18-product-wide-privacy-terms-review.md`](../../comms/website/tickets/2026-05-18--codex--ticket-18-product-wide-privacy-terms-review.md)
**Surface:** `src/hosted-mcp/app/kaleidoscope-login.html`, `/login`, `/signup` if still served, and any passkey creation entry point

## Summary

Ticket 18 shipped the product-wide privacy policy, website terms, and Kaleidoscope terms. That legal work is deployed and should not be reopened for this issue.

The remaining gap is product UI: when a user creates a Kaleidoscope passkey, the interface should visibly tell them that creating the passkey means agreeing to the Kaleidoscope Terms and Privacy Policy.

This is not a legal copy rewrite. It is an acceptance moment in the passkey creation UI.

## Problem

The legal pages now say the terms govern use of WIP Computer services and Kaleidoscope. The live login and signup surfaces still need a clear acceptance moment at the point where a user creates a passkey.

If the only notice lives in the footer or on the legal page itself, the acceptance path is weaker than it needs to be. Passkey creation is the product moment where the account is created, the identity begins, and the terms should be visible.

## Required UI

Add a concise visible notice near the primary passkey creation action.

Recommended copy:

```text
By creating a passkey, you agree to the Kaleidoscope Terms and Privacy Policy.
```

Links:

- `Kaleidoscope Terms` -> `https://wip.computer/legal/internet-services/kaleidoscope/`
- `Privacy Policy` -> `https://wip.computer/legal/privacy/`

Keep the notice short. Do not turn it into a legal wall. Do not add a checkbox unless a separate product decision asks for one.

## Scope

In scope:

- passkey creation view
- first-run account creation copy
- links to the current deployed legal pages
- responsive styling so the notice fits on mobile

Out of scope:

- rewriting legal pages
- changing WebAuthn behavior
- changing `next` routing
- changing wallet balances
- changing image generation
- changing Remote Control, relay, daemon, E2EE, or API keys
- changing active onboarding chat script beyond the terms notice needed for account creation

## Acceptance Criteria

1. A first-time user sees the terms notice before or directly adjacent to the passkey creation action.
2. The notice links to the Kaleidoscope Terms and Privacy Policy.
3. Existing sign-in for returning passkeys still works.
4. Existing `/login?next=/demo` and future `/login?next=/onboarding` continuation behavior is unchanged.
5. The page still works on mobile.
6. No legal body copy is changed in this ticket.

## Validation

Run:

```bash
git diff --check
node --check src/hosted-mcp/app/footer.js
node --check src/hosted-mcp/demo/footer.js
```

Also parse any inline scripts in `src/hosted-mcp/app/kaleidoscope-login.html`.

Manual check:

- open `/login`
- start the create-passkey path
- verify the notice is visible before account creation
- verify both legal links resolve
- verify a returning sign-in still works

## Notes

This follow-up came from the final Ticket 18 legal review after PR #1026 was merged and deployed. It is a product UI follow-up, not a blocker on the legal rewrite.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
