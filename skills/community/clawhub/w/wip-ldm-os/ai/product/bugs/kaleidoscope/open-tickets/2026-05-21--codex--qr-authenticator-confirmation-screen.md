# QR Authenticator Confirmation Screen

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0 launch login correctness
**Master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)
**Roadmap:** [`../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md`](../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md)
**Surface:** `src/hosted-mcp/app/kaleidoscope-login.html`, `src/hosted-mcp/demo/login.html`, `src/hosted-mcp/server.mjs`, QR login routes, tests

## Goal

Fix the QR login completion flow so the device that requested Kaleidoscope opens chat automatically, but the device that only authenticated the request does not also auto-enter chat.

This is the interim ticket. It should correct the confusing live behavior without building the full co-presence model yet.

## Current Problem

When a desktop starts External login and a phone scans the WIP QR code, the desktop correctly enters Kaleidoscope. The phone also gets routed into Kaleidoscope chat because it is loaded into the same login/token continuation path.

That is wrong for the authenticator device.

The phone is approving another device. It should behave more like the Apple Camera QR path: after approval, the phone should finish the authentication task and stop, not automatically become another chat surface.

## Product Rule

The requesting device and authenticator device are different roles.

| Role | Example | Correct behavior |
|---|---|---|
| Requesting device | Desktop user clicks Enter Kaleidoscope and shows QR | After approval, automatically enters chat. |
| Authenticator device | Phone scans QR and approves with passkey | After approval, shows a Kaleidoscope confirmation screen and does not enter chat unless the user explicitly chooses to. |
| Same device local login | Phone user taps Enter Kaleidoscope with Local passkeys on | Phone is the requester, so it enters chat automatically. |

## Interim UX

After successful QR approval on the authenticator device, replace the QR/login continuation page with a Kaleidoscope-branded confirmation screen:

```text
Kaleidoscope

You authenticated Kaleidoscope on another device.

Kaleidoscope is ready there.

Continue Session on this device
Open Kaleidoscope here too.

Cancel
Keep using Kaleidoscope on the other device.
```

For this interim ticket, `Continue Session on this device` can simply open the authenticated Kaleidoscope chat on this device using the existing session/token path.

`Cancel` must not open chat. It should finish the authenticator flow. If the browser allows `window.close()`, closing the QR approval tab is acceptable. If not, show a quiet completed state:

```text
You can close this page.
```

Do not refresh back into chat after Cancel.

## Implementation Notes

- The requesting device must still auto-enter chat after QR approval.
- The authenticator device must not auto-enter chat after QR approval.
- Preserve the existing QR login approval mechanics.
- Preserve existing Local passkey login behavior.
- Preserve External QR login behavior on desktop and mobile.
- Add enough state to distinguish the QR requester from the QR authenticator.
- Do not add Remote Control branding or terminology.
- Do not build co-presence or live mirroring in this ticket.

## Non-Goals

- No Remote Control implementation.
- No live session co-presence.
- No session transfer model.
- No wallet changes.
- No image generation changes.
- No prompt changes.
- No live-wall changes.
- No footer, legal, or homepage changes.
- No new passkey ceremony.

## Acceptance Criteria

- Desktop starts External QR login.
- Phone scans and authenticates.
- Desktop enters Kaleidoscope chat automatically.
- Phone lands on the confirmation screen, not chat.
- Phone `Cancel` does not enter chat and does not bounce back into the QR screen.
- Phone `Continue Session on this device` enters Kaleidoscope chat using the authenticated state.
- Phone Local login still enters chat automatically when the phone itself initiated Enter Kaleidoscope.
- Existing QR same-account guard remains intact.

## Coder Handoff

Do not treat this as a session engine rewrite. Inspect the current QR login routes first and fix the continuation target for the authenticator device.

Report:

- exact state or route field used to tell requester and authenticator apart;
- exact behavior for Cancel on iOS Safari, iOS Chrome, and desktop Chrome;
- proof that requester still auto-enters chat;
- proof that authenticator does not auto-enter chat;
- proof that same-device Local login still works.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
