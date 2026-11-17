# QR Session Co-Presence

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P1 session continuity, after the confirmation-screen fix
**Master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)
**Roadmap:** [`../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md`](../../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md)
**Related interim ticket:** [`2026-05-21--codex--qr-authenticator-confirmation-screen.md`](2026-05-21--codex--qr-authenticator-confirmation-screen.md)
**Related product model:** Codex Remote Control co-presence, WIP Remote Control platform vision

## Goal

Add a proper co-presence path after QR authentication so an authenticator device can join the same actual Kaleidoscope session when the user explicitly asks for it.

This should follow the Remote Control model: one real session, multiple attached surfaces, live updates. It is not a duplicated chat and not a screen mirror.

## Product Decision

Remote Control is a live update/co-presence model. The local session remains the actual session. Other devices attach to it as live clients.

Kaleidoscope should eventually use the same product concept for QR login continuation:

```text
one actual Kaleidoscope session
multiple authenticated surfaces
live session updates when joined
no duplicated chat state
no custom Kaleidoscope-only session engine
```

## Target UX

After the interim confirmation screen exists, extend it with:

```text
Kaleidoscope

You authenticated Kaleidoscope on another device.

Kaleidoscope is ready there.

Continue Session on this device
Open Kaleidoscope here.

Mirror Session
Use this device and the other device in the same session.

Cancel
Keep using Kaleidoscope on the other device.
```

Names can change in final copy, but the behavior must stay clear:

- `Continue Session on this device` opens Kaleidoscope here as a normal authenticated surface.
- `Mirror Session` attaches this device to the same actual session as the other device, with live updates.
- `Cancel` does not open chat on this device.

## Architecture Rule

Do not reinvent Kaleidoscope session state.

Before coding, inspect:

- current Kaleidoscope QR login flow;
- current hosted-mcp session/token flow;
- Codex Remote Control co-presence model;
- any existing live-session or attachment primitives in Kaleidoscope and hosted-mcp.

If the existing system lacks a small primitive needed for co-presence, file or report that primitive. Do not build a parallel session ownership store inside the demo page.

## Behavior Requirements

- Requesting device enters chat automatically after authentication.
- Authenticator device never auto-enters chat merely because it approved another device.
- `Mirror Session` joins the same actual session, not a new chat.
- Both devices should receive live updates for the same session after mirroring.
- If the mirrored device closes, the other device should continue.
- If the user chooses normal single-device continuation instead of mirroring, stale action buttons must not survive after the active device exits.
- Session-close behavior must be explicit and tested. Do not leave a passive device with old buttons that imply a dead session can still be joined.

## Non-Goals

- No custom Remote Control fork inside Kaleidoscope.
- No screen sharing.
- No duplicated chat transcript.
- No wallet changes.
- No image generation changes.
- No prompt changes.
- No live-wall changes.
- No legal/footer/homepage changes.
- No API key exposure.

## Acceptance Criteria

- The implementation reuses or cleanly extends existing live-session primitives.
- QR-authenticated phone can choose not to join chat.
- QR-authenticated phone can explicitly join the same live session.
- When joined, both devices show the same session state.
- Closing one mirrored surface does not break the other.
- Non-mirrored close behavior does not leave stale continuation controls.
- Tests cover requester versus authenticator roles and co-presence attachment.

## Coder Handoff

Start with investigation. Do not code until the existing session model is mapped.

Report:

- whether Kaleidoscope already has a reusable session id or live-update channel;
- whether hosted-mcp can distinguish requester, authenticator, and joined surface;
- which Remote Control primitive is being reused or mirrored conceptually;
- smallest missing primitive if reuse is not yet possible;
- why the implementation is not creating a second Kaleidoscope session engine.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
