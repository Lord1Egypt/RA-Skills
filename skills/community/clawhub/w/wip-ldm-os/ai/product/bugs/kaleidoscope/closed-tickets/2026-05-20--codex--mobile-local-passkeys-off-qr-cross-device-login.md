# Mobile Local Passkeys Off Must Show QR Cross-Device Login

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** closed, fixed by PR #1045 and PR #1047
**Priority:** P0
**Product surface:** Kaleidoscope login and onboarding
**Related system owner:** Sapien ID
**Primary route:** `/login?next=/demo`
**Bug master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)

## Problem

Resolution 2026-05-21: mobile defaults Local on, desktop defaults Local off, and Local off uses WIP QR cross-device login. The remaining same-account guard issue was fixed live by PR #1047.

The Local passkeys toggle does not mean the same thing on every device.

Current observed behavior:

- Desktop with Local passkeys off shows the QR or cross-device login path.
- iOS Safari with Local passkeys off does not reliably switch to the QR path.
- iOS Chrome behaves the same as iOS Safari.
- On mobile, the toggle can look like it does nothing.

That breaks the product model. A user should always be able to log into one device from another trusted device.

## Product Model

Kaleidoscope has two login modes.

### Local Mode

Local mode is controlled by the browser and operating system ecosystem.

Examples:

- Apple platform passkeys;
- iCloud Keychain;
- Safari WebAuthn UX;
- Chrome passkey UX;
- Android platform authenticators;
- password managers that expose passkeys.

WIP asks for WebAuthn, but Apple, Google, Chrome, Safari, Android, or the passkey provider owns the local ceremony and user experience.

### External Mode

External mode is controlled by WIP.

External mode means:

```text
Authenticate this device from another trusted device.
```

The UI should show WIP's QR or cross-device login path. WIP owns this experience and should make it consistent across browsers and devices.

## Expected Behavior

- Mobile browsers default Local passkeys on.
- Desktop browsers default Local passkeys off.
- Local passkeys on means use this device's platform passkey ceremony.
- Local passkeys off means show WIP's QR cross-device login path.
- The QR path is available on every device, including iOS Safari and iOS Chrome.
- Turning the toggle changes the active login path visibly and reliably.

## Why This Matters

This is not only a UI bug. It is the first visible Sapien ID boundary:

```text
Local uses this device's passkey ecosystem.
External uses WIP's cross-device identity path.
```

If the toggle behaves differently per platform, users cannot learn the model and agents cannot explain it.

The product should not need separate rules for Safari, Chrome, iOS, Android, or desktop. It needs one rule.

## Scope

This ticket belongs in Kaleidoscope bugs because the visible failure is in the Kaleidoscope login/onboarding surface.

It is related to Sapien ID because the deeper product concept is passkey identity and cross-device authority.

Do not move this ticket to Sapien ID until the Kaleidoscope login bug is fixed and verified.

## Acceptance

- On iOS Safari, `/login?next=/demo` defaults to Local passkeys on.
- On iOS Safari, turning Local passkeys off shows the QR cross-device login UI.
- On iOS Chrome, turning Local passkeys off shows the QR cross-device login UI.
- On desktop Safari and Chrome, `/login?next=/demo` defaults to Local passkeys off and shows the QR cross-device login UI.
- On desktop Safari and Chrome, turning Local passkeys on uses the local passkey flow.
- The toggle visibly changes the active login path on every tested device.
- Existing WebAuthn challenge and verify semantics remain intact.
- Existing QR login flow remains intact.
- Add a focused test or fixture for mobile versus desktop default mode selection if the codebase has a practical test surface.

## Non-Goals

- Do not redesign Sapien ID.
- Do not change wallet accounting.
- Do not change image generation.
- Do not change live wall behavior.
- Do not change demo chat copy.
- Do not change legal pages or footer.
- Do not change Remote Control behavior.
- Do not touch relay, daemon, E2EE, or API keys.
- Do not rename the UI labels in this ticket unless required to make the existing toggle truthful.

## Implementation Notes

Create a follow-up PR from current `origin/main`.

This should be a login UI state and routing fix, not an auth architecture rewrite.

The key invariant is:

```text
Local off always means External QR login.
```

## Related

- [`../../../plans-prds/kaleidoscope/tickets/2026-04-07--cc-mini--chrome-qr-login-plan.md`](../../../plans-prds/kaleidoscope/tickets/2026-04-07--cc-mini--chrome-qr-login-plan.md)
- [`../../../plans-prds/kaleidoscope/tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md`](../../../plans-prds/kaleidoscope/tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md)
- [`../../hosted-mcp/2026-05-01--codex--demo-local-passkey-qr-parity.md`](../../hosted-mcp/2026-05-01--codex--demo-local-passkey-qr-parity.md)
- [`../../codex-remote-control/2026-05-03--codex--pair-mode-login-choice-clarity.md`](../../codex-remote-control/2026-05-03--codex--pair-mode-login-choice-clarity.md)

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
