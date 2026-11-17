# Login Scan QR Code Authenticator Action

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** archived, superseded
**Priority:** P0 launch login correctness
**Master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)
**Roadmap:** [`../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md`](../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md)
**Surface:** `src/hosted-mcp/app/kaleidoscope-login.html`, `src/hosted-mcp/demo/login.html`, QR login routes, mobile camera/QR scanner flow, tests
**Superseded by:** [`../open-tickets/2026-05-23--codex--qr-authenticated-phone-app-state.md`](../open-tickets/2026-05-23--codex--qr-authenticated-phone-app-state.md)

## Archive Note

This ticket is archived because the unauthenticated `Scan QR Code` login action was removed. Parker decided that QR tools belong after the phone is authenticated as a Kaleidoscope app surface, not as another unauthenticated login action.

Keep this ticket as context for why the unauthenticated scanner was rejected. Do not implement this ticket as written.

## Goal

Add an explicit `Scan QR Code` action to Kaleidoscope login so a phone can intentionally act as the authenticator for another device.

This is not Remote Control. This is not session mirroring. This is the phone approving a login request that was started somewhere else.

## Current Problem

Kaleidoscope currently has two visible login concepts:

1. use this device's local passkey;
2. show a WIP QR code so another trusted device can authenticate this session.

There is also a third real role, but it is not visible in the login UI:

3. use this device's camera to scan a QR code shown on another device and authenticate that other device.

Without an explicit scanner action, the phone-side authenticator flow is confusing. If the phone shows a button like `Open session here`, users can reasonably think Kaleidoscope is transferring or mirroring the same chat session. It is not. Opening `/demo` on the phone creates another local browser chat using the same authenticated identity, not the same live session.

## Product Rule

Kaleidoscope login needs three distinct actions:

| Action | Meaning | Correct result |
|---|---|---|
| Local passkeys | Use this device's platform passkey | This device enters Kaleidoscope. |
| External QR login | Show a WIP QR for another trusted device to scan | This device waits, then enters Kaleidoscope after approval. |
| Scan QR Code | Use this device's camera to authenticate another device | The other device enters Kaleidoscope. This device does not enter chat. |

The scanner action makes the phone's authenticator role intentional instead of accidental.

## UX

Add a bottom login action:

```text
[camera icon] Scan QR Code
```

Placement:

- bottom of the Kaleidoscope login screen;
- separate from the primary local/external passkey actions;
- mobile-first;
- do not replace Local passkeys or External QR login.

When tapped, it should open a camera or QR scanner flow for scanning a WIP Kaleidoscope QR code from another device.

After successful approval:

```text
Your authenticated Kaleidoscope session is available on your other device.

Back to login
```

`Back to login` returns the phone to the login screen, with Kaleidoscope as the intended next destination if the user starts a fresh login from that phone:

```text
https://wip.computer/login?next=/demo
```

It must not open `/demo` on the phone from the authenticator completion screen.

Before returning to login, clear any phone-side QR authenticator continuation state so the phone does not silently carry the approved desktop handoff into a local `/demo` chat. The phone should land on login as an available device, not as the same chat.

## Behavior Requirements

- Desktop or other requesting device starts External QR login.
- Phone taps `Scan QR Code`.
- Phone scans the requesting device's WIP QR code.
- Phone authenticates with its platform passkey.
- Requesting device enters Kaleidoscope automatically.
- Phone does not enter `/demo`.
- Phone lands on a completed state that says `Your authenticated Kaleidoscope session is available on your other device.`
- Phone shows `Back to login`, not `Open session here` and not `Close`.
- `Back to login` clears phone-side QR authenticator continuation state and sends the phone to `/login?next=/demo`.
- `Back to login` must not store `lesa-token` or otherwise open `/demo` from the authenticator completion screen.
- Phone Local passkey login still enters `/demo` automatically when the phone itself initiated the login.
- External QR login still works when this device is the requester.
- QR same-account guard still blocks genuinely different accounts.

## Implementation Notes

- Reuse the existing WIP QR approval mechanics where possible.
- Add scanner UI as a login affordance, not as a Remote Control feature.
- Prefer native browser scanner/camera APIs when possible.
- If adding a third-party scanner dependency is unavoidable, run the security review before adding it.
- Preserve the requester/authenticator split from the QR authenticator confirmation work.
- Do not add live session co-presence in this ticket.
- Do not label this Remote Control.

## Non-Goals

- No Remote Control implementation.
- No session mirroring.
- No session transfer.
- No second phone-side chat after authenticating another device.
- No wallet changes.
- No image generation changes.
- No prompt changes.
- No live-wall changes.
- No legal, footer, or homepage changes.
- No new passkey ceremony beyond the scanner entry point.

## Acceptance Criteria

- `Scan QR Code` appears at the bottom of Kaleidoscope login on mobile.
- The action uses a camera icon and clear label.
- The action scans a WIP QR code from another device.
- The scanned QR approval uses the existing passkey authentication path.
- The requesting device enters Kaleidoscope after approval.
- The authenticator phone does not enter `/demo`.
- The authenticator phone shows `Your authenticated Kaleidoscope session is available on your other device.`
- The authenticator phone shows `Back to login`, not `Open session here` and not `Close`.
- `Back to login` clears phone-side QR authenticator continuation state and sends the phone to `/login?next=/demo`.
- `Back to login` must not store `lesa-token` or otherwise open `/demo` from the authenticator completion screen.
- Local passkey login on the phone still enters `/demo`.
- External QR requester flow still works.
- Tests cover the scanner role as distinct from requester and local-login roles.

## Coder Handoff

Start by mapping the existing QR login roles:

- requester device polling `/api/qr-login/status`;
- authenticator device completing `/api/qr-login/approve`;
- same-device local login going straight to `/demo`.

Then add the `Scan QR Code` login action without changing those role contracts.

Report:

- how the scanner receives or parses the QR login session id;
- how the code distinguishes scanner/authenticator from requester;
- proof that the requester enters chat;
- proof that the authenticator phone does not enter chat;
- proof that local phone login still enters chat;
- proof that no Remote Control or co-presence behavior was added.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
