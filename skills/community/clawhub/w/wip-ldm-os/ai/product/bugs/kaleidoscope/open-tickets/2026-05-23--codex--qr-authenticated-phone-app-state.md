# QR Authenticated Phone App State

**Date:** 2026-05-23
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0 launch login correctness
**Master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)
**Roadmap:** [`../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md`](../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md)
**Related interim ticket:** [`2026-05-21--codex--qr-authenticator-confirmation-screen.md`](2026-05-21--codex--qr-authenticator-confirmation-screen.md)
**Related superseded scanner ticket:** [`../archive/2026-05-21--codex--login-scan-qr-code-authenticator-action.md`](../archive/2026-05-21--codex--login-scan-qr-code-authenticator-action.md)
**Related future ticket:** [`2026-05-21--codex--qr-session-co-presence.md`](2026-05-21--codex--qr-session-co-presence.md)
**Surface:** `src/hosted-mcp/app/kaleidoscope-login.html`, `src/hosted-mcp/demo/login.html`, QR login routes, authenticated phone state, future Kaleidoscope app surface

## Goal

After a phone authenticates a QR login for another device, the phone should become authenticated as a Kaleidoscope device, but it should not automatically enter the chat.

This ticket captures the product state Parker wants preserved:

```text
The phone is logged in to Kaleidoscope as an app surface.
The desktop or requesting device enters chat.
The phone stays at login or account-ready state.
The phone can later expose app actions, device linking, QR tools, and co-presence.
```

This is not Remote Control yet. This is also not a logged-out dead end.

## Current Problem

The QR authenticator work has gone through several temporary states:

1. The phone authenticated the desktop and also opened chat. That created a duplicate local chat, not a true mirrored session.
2. The phone then stopped at a confirmation screen. That prevented duplicate chat, but risked treating the phone like a dead-end browser tab.
3. The unauthenticated `Scan QR Code` login action was removed because it was confusing and made login feel like it had too many roles.

The missing product model is:

```text
Once the phone successfully authenticates, the phone should be in a logged-in Kaleidoscope state.
It should behave like Kaleidoscope is available on the phone.
It should not auto-open the current chat unless the user explicitly starts or joins something from the phone.
```

## Product Rule

QR approval has two device roles:

| Device | Role | Correct result |
|---|---|---|
| Requesting device | Started `Enter Kaleidoscope` and showed the WIP QR | Enters `/demo` automatically after approval. |
| Authenticator phone | Scanned or opened the QR and approved with platform passkey | Becomes authenticated for Kaleidoscope, returns to login/account-ready state, does not auto-enter `/demo`. |

The authenticator phone should not be treated as logged out after approval.

It should also not imply that the phone is controlling the same chat session. True co-presence is a later ticket.

## Target Interim UX

After successful phone-side QR approval:

```text
Your authenticated Kaleidoscope session is available on your other device.

Back to login
```

`Back to login` should take the phone to:

```text
/login?next=/demo
```

But the meaning must be:

```text
You are authenticated here too.
You are back at the Kaleidoscope entry surface.
You can choose what to do from this phone.
```

It must not mean:

```text
You are logged out.
You need to restart identity from scratch.
The phone has no authenticated Kaleidoscope state.
```

## Future Authenticated Phone Surface

Once the phone is authenticated, Kaleidoscope should eventually expose phone-app actions from that state, including:

- enter Kaleidoscope on this phone;
- show this phone's QR code for linking another device;
- scan another device's WIP QR code from inside the authenticated app surface;
- review trusted devices;
- revoke a device;
- approve agent or wallet requests;
- join or mirror the same live session when co-presence exists.

The QR scanner belongs here, after authentication, not as an unauthenticated bottom action on the login page.

## Relationship To Co-Presence

This ticket is the bridge before co-presence.

For now:

- phone is authenticated;
- phone does not auto-enter the chat;
- desktop/requesting device keeps running the chat;
- phone has a correct future place to expose app actions.

Later, the co-presence ticket should add:

```text
Join this session
Use both devices together
End or leave session
```

That later behavior must attach to the same actual session. It must not create a second local chat that only looks mirrored.

## Behavior Requirements

- Desktop or other requesting device starts External QR login.
- Phone authenticates with platform passkey.
- Requesting device enters Kaleidoscope automatically.
- Phone does not enter `/demo` automatically.
- Phone shows the confirmation copy and a `Back to login` action.
- `Back to login` goes to `/login?next=/demo`.
- The phone should retain authenticated account state where the current architecture supports it.
- The phone must not store a desktop handoff token and then silently open that desktop chat as a local phone chat.
- Phone local login still enters `/demo` automatically when the phone itself initiated the login.
- System Camera app QR path and in-browser `/login?s=...` path should follow the same role split.

## Implementation Notes

- Audit what “authenticated” currently means on the phone after QR approval: token storage, localStorage, handoff payloads, account handle, passkey tenant id, and any session cookie or equivalent.
- Preserve requester/authenticator role separation.
- If the existing login page cannot represent “authenticated but not in chat,” file the smallest UI/state primitive needed.
- Do not re-add the unauthenticated `Scan QR Code` login action.
- Do not call the interim phone state Remote Control.
- Do not add true session co-presence in this ticket.
- Do not duplicate chat state to make it look mirrored.

## Non-Goals

- No Remote Control implementation.
- No true co-presence yet.
- No session mirroring.
- No duplicated chat transcript.
- No unauthenticated QR scanner button on login.
- No wallet changes.
- No image generation changes.
- No prompt changes.
- No live-wall changes.
- No legal, footer, homepage, or visualization changes.
- No new passkey ceremony.

## Acceptance Criteria

- After phone-side QR approval, the requesting device enters `/demo`.
- The authenticator phone does not enter `/demo`.
- The authenticator phone shows `Your authenticated Kaleidoscope session is available on your other device.`
- The authenticator phone action is `Back to login`.
- `Back to login` lands on `/login?next=/demo`.
- The phone is not treated as a logged-out dead end after successful authentication.
- The phone does not preserve a desktop chat handoff that can silently open the wrong local chat.
- Same-device phone local login still enters `/demo`.
- External QR requester flow still works.
- Tests or manual verification cover requester device, authenticator phone, and phone local-login roles separately.

## Coder Handoff

Start by mapping the live phone-side state after `/api/qr-login/approve`.

Report:

- what token or account state the phone has after approving a QR login;
- whether `Back to login` preserves or clears that state today;
- whether `/login?next=/demo` can show an account-ready state without auto-entering chat;
- whether any current code stores a desktop handoff token on the authenticator phone;
- exact change needed so the phone is authenticated as Kaleidoscope but not dropped into chat;
- proof that the desktop requester still auto-enters chat;
- proof that phone local login still auto-enters chat.

Do not implement co-presence here. The follow-up co-presence ticket owns shared live session behavior.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
