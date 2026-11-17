# iPhone Safari Private Browsing rejects QR auto-start with NotAllowedError

**Date:** 2026-05-02
**Owner:** remote-control--cc--coder
**Reviewer:** remote-control--kay--partner
**Severity:** ~~compatibility follow-up~~ **Fixed in this same PR** (Parker escalated; auto-start rejection now shows a QR-specific instructional message and leaves existing controls enabled, replacing the misleading "Cancelled" copy)
**Related:**
- `2026-04-30--cc-mini--pair-via-login-qr-flow.md`
- `2026-05-01--codex--remote-control-recovery-master-plan.md`
- `2026-05-01--codex--demo-local-passkey-qr-parity.md`
- PR #784, PR #793, PR #799 (auto-start restore)

## Symptom

iPhone Safari opened via QR scan from a Mac Chrome desktop QR session.

| Browser mode | Result |
|---|---|
| Safari (normal browsing) | Auto-start fires within ~300ms, Face ID prompt appears, register/sign-in completes, `/api/qr-login/approve` fires, pair-mode redirects phone to `/pair/<CODE>` ... **passes**. |
| Safari (Private Browsing) | Auto-start fires, immediately rejected. Status shows "Cancelled. Try again when ready." Face ID never appears via auto-start. |

## Cause (working hypothesis)

Safari Private Browsing applies stricter rules around WebAuthn user activation and / or passkey state isolation:
- The `setTimeout` callback at 300ms is treated as not-from-a-user-gesture, so `navigator.credentials.create / get` rejects with `NotAllowedError`.
- Possibly also: cross-mode passkey availability differs in Private Browsing.

The desktop QR producer is fine; the relay backend is fine; the bug is purely client-side, on the Private Browsing tab.

## Existing fallback

When the auto-start is rejected, the existing `catch (err)` block in `doCreateAccount` / `doSignIn` does this:

```js
catch (err) {
  if (err.name === 'NotAllowedError') {
    setStatus('Cancelled. Try again when ready.', 'error');
    setTimeout(function() { clearStatus(); }, 3000);
  } else {
    setStatus('Error: ' + err.message, 'error');
  }
  btn.disabled = false;
}
```

That re-enables the primary button (`Enter the Kaleidoscope` for register mode, or restores `Already have an account? Sign in.` interaction for sign-in mode). A user **tap** of that button is a real user gesture and should let Safari Private Browsing complete WebAuthn.

The fallback path (auto-start rejected → user taps button → Face ID) needs an in-Private-mode confirmation. This bug doc tracks that test.

## Acceptance for closing this follow-up

After auto-start rejection in Private mode:

- [ ] Tap **Enter the Kaleidoscope** (register) → Face ID prompt → success → `/api/qr-login/approve` fires.
- [ ] Tap **Already have an account? Sign in.** (signin) → Face ID prompt → success → approve fires.
- [ ] Pair-mode `next` returned by approve still redirects phone to `/pair/<CODE>`.
- [ ] Desktop never receives `apiKey` in pair mode (plan C6 unchanged).

If those tap-fallbacks pass, Private Browsing is "no auto-start, but works on tap." Acceptable as documented behavior; not a launch blocker.

If those tap-fallbacks **also** fail, this becomes a real Private-mode incompatibility. Possible mitigations:
- Detect Private Browsing client-side, suppress the "Cancelled" message, surface a private-mode-specific hint copy. **UI invention; do not ship without explicit approval.**
- Document in install spec / onboarding that Private mode is unsupported for QR pairing.

## Out of scope for this doc

- No code change in this branch.
- No UI invention.
- No daemon alpha.7 release.
- No baseline retry.

## Logging note

When testing in Private mode, do NOT post real `ck-` keys, real `apiKey` values, or real `agentId` to chat / logs / screenshots. Per the recovery master plan stop conditions.

## Status

**Fixed in this PR.** Implementation lands in the same branch (`cc-mini/bug-safari-private-qr`):

- New `qrAutoStarting` flag set true around the setTimeout-driven `doCreateAccount` / `doSignIn` invocation. Reset to false in a `finally` block so user-initiated taps clear the auto-start context.
- Both `NotAllowedError` catches in `demo/login.html` and `app/kaleidoscope-login.html` now check `qrSessionMode && qrAutoStarting`. If true, they show a **QR-specific instructional message** in the existing status area instead of the generic "Cancelled" copy:
  - Register path: `"This browser blocked automatic Face ID. Tap Enter the Kaleidoscope to continue."`
  - Sign-in path: `"This browser blocked automatic Face ID. Tap Already have an account? Sign in. to continue."`
- The neutral "This browser blocked..." phrasing is used because we cannot reliably detect Private Browsing client-side, and the same constraint can apply in other strict modes.
- Buttons are re-enabled exactly as before, so the user's eventual tap on the existing primary button or sign-in link completes the flow with a real user gesture, reusing the same `qrSessionId`.
- No new screen, no redesign, no new visual element ... only the existing status div gets the new copy. The user's tap into `doCreateAccount` / `doSignIn` overwrites the status with the existing "Loading..." / "Waiting for biometric..." flow.

Acceptance:

- Normal Safari: scan QR → Face ID pops within ~300ms; no message shown.
- Private Safari: scan QR → message appears in the status area; existing buttons remain enabled; tap → Face ID prompt → approve → `qr-login/approve` fires.
- Register and sign-in modes both show the right instructional text.
- A real user cancellation after a real user tap still shows `"Cancelled. Try again when ready."` (the user-initiated path has `qrAutoStarting === false`).
- Pair-mode still redirects phone to `/pair/<CODE>`.
- Desktop never receives `apiKey` (plan C6 unchanged).
