---
title: "Pair-mode login must clearly separate existing keys from new keys"
date: 2026-05-03
author: Codex
status: ticketed
severity: P1
component: codex-remote-control
---

# Pair-Mode Login Choice Clarity

## Summary

The Codex Remote Control pair mechanism now works end-to-end, but the pair-mode login UX is confusing. When a user opens `/login?next=/pair/<CODE>`, the phone/desktop flow reuses the normal Kaleidoscope account-entry UI. The giant `Enter the Kaleidoscope` button makes it unclear whether the user is using existing keys, making new keys, or approving a device pair.

This is acceptable for the current build smoke, but it is not product-ready. Before broader dogfood or public exposure, pair mode needs an intent-specific first step.

## Current Behavior

Observed after successful pair smoke:

- `codex-daemon link` prints `https://wip.computer/login?next=/pair/<CODE>`.
- Mac Chrome opens the URL.
- User clicks `Enter the Kaleidoscope`.
- QR appears.
- iPhone scans QR.
- Phone authenticates and redirects to `/pair/<CODE>`.
- User confirms.
- Daemon pairs successfully.

The backend and pair contract work. The confusion is in the first login choice:

- The user sees the normal account creation/sign-in UI.
- The handle prompt (`What should Lēsa call you?`) appears too early for pair mode.
- It is not obvious that this is about pairing a computer with Codex Remote Control.
- It is not obvious which path means "use existing keys" versus "make new keys."

## Expected Behavior

When `next=/pair/<CODE>` is present, `/login` should enter a pair-specific login-choice mode.

The first screen should make the intent explicit:

- Pair this computer with Codex Remote Control.
- Use existing keys.
- Make new keys.

Behavior:

- `Use existing keys` starts the sign-in/passkey path.
- `Make new keys` reveals the handle prompt and starts the create-passkey path.
- The handle prompt should not be visible before the user chooses `Make new keys`.
- The copy should make clear the phone is approving a pairing, not just entering the general Kaleidoscope demo.
- Phone remains the authority.
- Desktop still receives no `apiKey` in pair-mode status responses.
- Desktop still does not navigate to `/pair/<CODE>`.
- `/pair/<CODE>` still has explicit Confirm.

## Non-Goals

- Do not redesign normal `/login`.
- Do not redesign `/demo/`.
- Do not change pair-code generation.
- Do not change the server-side `apiKey` strip for pair-mode desktop status.
- Do not remove the explicit `/pair/<CODE>` Confirm step.
- Do not release daemon alpha.7 as part of this ticket.
- Do not reopen the hosted-auth/token hardening gate.

## Impact

Severity: P1.

The core mechanism works, but the current UI will confuse real users:

- Users may think they are creating a normal account when they are pairing a device.
- Users with existing passkeys may not understand they should sign in instead of making new keys.
- The handle prompt appears before the user has chosen to make new keys.
- The pair flow feels like "login twice" instead of "approve this device."

This should be solved after the current build/pair smoke is complete, before this becomes a broader dogfood or public-alpha experience.

## Evidence

Successful pair smoke on 2026-05-03:

```text
codex-daemon: pairing against https://wip.computer
code: FSN2ZR
open: https://wip.computer/login?next=%2Fpair%2FFSN2ZR
...
codex-daemon: paired as parker-smoke-test
codex-daemon: relay key saved to /Users/lesa/.codex-daemon/relay-key
```

User feedback immediately after the pass:

> The UI is not clear enough about when I open the URL. It shouldn't be that the login for the pairing mode is the same. It should be very clear: "Login with existing keys" or "Make new keys." I shouldn't have any of this other Lēsa call you stuff unless it says "Login with existing keys," and then the flows change. If it's "Make new keys," then it goes into what Lēsa calls you.

## Root Cause

`/login?next=/pair/<CODE>` currently uses the same visual state as normal `/login`. The pair intent is carried in `next`, but the first screen does not translate that intent into a distinct user choice.

The route/security contract is correct; the UI state machine is not pair-aware enough.

## Proposed Fix

Add a pair-mode branch to the `/login` UI when `readPairNextFromQuery()` returns a valid `/pair/<CODE>`.

Pair-mode first screen:

1. Show pair intent:
   - `Pair this computer with Codex Remote Control`
   - short supporting copy, if needed
2. Show two explicit actions:
   - `Use existing keys`
   - `Make new keys`
3. Hide the handle prompt by default.

Action behavior:

- `Use existing keys` calls the existing sign-in path.
- `Make new keys` reveals the existing handle prompt and create-account action.
- In QR continuation mode on the phone, preserve the known-good auto-start and strict-browser fallback behavior.

Implementation constraints:

- Reuse existing auth/pair handlers.
- Do not create new server endpoints unless absolutely required.
- Do not change pair-mode response shapes.
- Keep pair-mode desktop status stripped.
- Keep `/pair/<CODE>` Confirm explicit.

## Acceptance Criteria

- Opening `/login?next=/pair/<CODE>` shows pair-specific intent before account actions.
- Initial pair-mode screen has two clear choices:
  - use existing keys
  - make new keys
- The handle prompt is hidden until `Make new keys` is selected.
- Existing-key path signs in with passkey and continues the pair flow.
- New-key path creates passkey and continues the pair flow.
- Phone redirects to `/pair/<CODE>` after approval.
- User taps Confirm on `/pair/<CODE>`.
- Daemon pairs.
- Desktop shows approved-on-phone status and never receives `apiKey`, `next`, or `credentialLabel`.
- Normal `/login` behavior outside pair mode is unchanged.

## Test Plan

Manual:

1. Run `codex-daemon link`.
2. Open the printed `/login?next=/pair/<CODE>` URL on Mac Chrome.
3. Verify pair-specific choice screen appears.
4. Test `Use existing keys`.
5. Test `Make new keys`.
6. Verify both paths reach phone `/pair/<CODE>` and pair after Confirm.
7. Verify desktop status response remains stripped.

Automated follow-up:

- Add Playwright coverage in the Remote Control smoke automation plan:
  - `/login?next=/pair/<CODE>` renders pair-mode choice screen.
  - handle prompt absent initially.
  - choosing `Make new keys` reveals handle prompt.
  - choosing `Use existing keys` calls sign-in flow.

## Release Path

This is a follow-up product/UI PR after the current build is stabilized:

1. Plan or implementation PR in `wip-ldm-os-private`.
2. Review with Remote Control partner.
3. Deploy with `src/hosted-mcp/deploy.sh`.
4. Run route/browser/CRC pair smokes.

## Rollback

Revert the pair-mode UI PR. The existing backend pair flow should remain intact because the fix must reuse current auth/pair endpoints.

## Review Questions

- Exact copy for the pair-mode first screen.
- Whether the two actions should say `Use existing keys` / `Make new keys`, or `Sign in with existing passkey` / `Create new passkey`.
- Whether this should be implemented directly in `app/kaleidoscope-login.html` first or extracted into shared login-state code after smoke automation lands.
