# Local Passkey Same-Account Guard Rejects QR-Accepted Account

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** closed, fixed live
**Priority:** P0
**Product surface:** Kaleidoscope onboarding authorization
**Related system owner:** Sapien ID
**Related product area:** Agent Pay authorization demo
**Primary route:** `/demo`
**Bug master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)

## Resolution

Fixed by PR `#1047`, deployed live on 2026-05-20.

Verified by Parker:

- local passkey approval no longer blocks the active same account;
- External QR approval still works;
- the flow continues past authorization for the same account.

Implementation summary:

- QR login preserves `tenantId` through approval and `/demo` handoff;
- the demo same-account guard compares canonical account ids first;
- `acct:<id>` and `<id>` compare as the same account;
- API key comparison remains fallback only when tenant ids are unavailable.

## Problem

The local passkey authorization path and QR authorization path do not agree about the current account.

Observed live behavior:

- The onboarding session is logged in as `parker-smoke-test`.
- Authorizing with a local passkey shows:

```text
That passkey belongs to a different account. This onboarding session is using parker-smoke-test. Restart if you want to switch accounts.
```

- Authorizing through the QR flow with the same `parker-smoke-test` account succeeds and continues:

```text
Thanks for authorizing. Let me show you what I can do.
I'd like to turn your photo into a kaleidoscope. Want to take one?
```

That means the same-account guard is using different identity material, normalization, or display labels across local and QR approval paths.

## Expected Behavior

Local passkey approval and QR approval must use the same canonical account comparison.

- If the local passkey belongs to the same account as the onboarding session, authorization succeeds.
- If the QR approval belongs to the same account as the onboarding session, authorization succeeds.
- If either path belongs to a different account, authorization is blocked with the existing mismatch message.
- The two paths must not disagree for the same real account.

## Why This Matters

This is a Sapien ID correctness bug visible inside Kaleidoscope.

The product promise is that a user can authorize an action with their device. If one passkey path says the account is wrong while another path accepts the same account, users cannot trust the account boundary or the spend authorization boundary.

This also affects the Agent Pay demo because the approval action is presented as permission to spend money.

## Scope

This ticket belongs in Kaleidoscope bugs because the visible failure happens during Kaleidoscope onboarding and authorization.

It is related to Sapien ID because the deeper issue is canonical account identity across local passkeys, QR approvals, tenant ids, account labels, and any `acct:` normalization.

It is related to Agent Pay because this same-account guard protects spend authorization.

## Acceptance

- Reproduce the current live mismatch before patching.
- Identify which values are compared in the local passkey authorization path.
- Identify which values are compared in the QR authorization path.
- Normalize both paths to the same canonical account identity before comparison.
- Do not use display labels as the primary guard if canonical tenant or account ids are available.
- `acct:<id>` and `<id>` forms are handled consistently if either appears in the path.
- Local passkey approval succeeds for the same account currently accepted through QR.
- Local passkey approval still rejects a genuinely different account.
- QR approval behavior remains unchanged for valid and invalid accounts.
- Add a focused regression test or fixture that covers local and QR same-account comparison parity.

## Non-Goals

- Do not redesign Sapien ID.
- Do not change passkey creation.
- Do not change Local on or Local off mode selection.
- Do not change the QR login UI.
- Do not change demo copy.
- Do not change wallet balance logic.
- Do not change image generation.
- Do not change live wall behavior.
- Do not change legal pages or footer.
- Do not touch nginx.
- Do not touch Remote Control, relay, daemon, E2EE, or API keys.

## Implementation Notes

Resolved by PR `#1047`.

This should be an account identity normalization and same-account guard fix, not a UI rewrite.

The invariant is:

```text
Local passkey approval and QR approval compare the same canonical account identity.
```

## Related

- [`2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md`](2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md)
- [`../../../plans-prds/kaleidoscope/tickets/2026-05-19--codex--kaleidoscope-onboarding-chat-copy-and-account-guard.md`](../../../plans-prds/kaleidoscope/tickets/2026-05-19--codex--kaleidoscope-onboarding-chat-copy-and-account-guard.md)

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
