# Ticket 11: Match login/demo background and blue to Kaleidoscope bubble

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** open. Launch-path login/demo visual polish. Keep open until Codex or Parker verifies the current live login and demo surfaces on mobile and desktop against the acceptance criteria.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 02 login/demo entry, Ticket 07 active demo chat footer removal
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html`, `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html`, and fallback `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/login.html` if still maintained

## Summary

The Kaleidoscope login and active demo should read as one clean product surface. The current demo has visual drift: the login background, active demo background, and blue accents do not fully match the white/blue feel of the Kaleidoscope bubble shown in the scripted chat.

Make the login background white, make the whole active demo background white, and make the demo blue match the Kaleidoscope bubble blue. Keep the same shape, same bubble styling, same layout behavior, and same scripted flow. This is a color and background polish ticket, not a redesign.

Parker's direction:

```text
make the whole demo background white and the blue the same color as the demo kaleidoscope bubble

The same shape, the same colors.

also make the login background white too
```

## Desired behavior

- The Kaleidoscope login surface uses a white background.
- The active `/demo` chat surface uses a white background.
- The visual blue used for primary demo accents matches the blue already used by the Kaleidoscope bubble in the demo.
- The Kaleidoscope bubble shape stays the same.
- Message bubbles keep the same geometry, spacing, and rounded shape.
- The demo still feels like the same product, just cleaner and visually unified.
- Applies on mobile and desktop.

## Scope

This is a narrow visual patch.

Allowed:

- CSS and inline style changes in `src/hosted-mcp/demo/index.html`.
- CSS and inline style changes in `src/hosted-mcp/app/kaleidoscope-login.html`.
- Matching fallback CSS/style changes in `src/hosted-mcp/demo/login.html` only if that fallback file is still maintained for login parity.
- Introducing a local CSS custom property for the Kaleidoscope blue if it reduces drift.
- Reusing the exact existing Kaleidoscope bubble blue for buttons, borders, active accents, or other blue UI elements that should match.
- Making the login page background white.
- Making the active chat/demo page background white.

Not allowed:

- No auth changes.
- No login redirect changes.
- No `next` allowlist changes.
- No wallet changes.
- No image API changes.
- No Remote Control, pair/relink, relay, daemon sync, passkey/WebAuthn, or E2EE changes.
- No homepage changes.
- No broad redesign.
- No layout rewrite.
- No new animation behavior.

## Implementation notes

Find the existing blue used by the Kaleidoscope bubble in `src/hosted-mcp/demo/index.html` and make that the canonical demo blue for this visual pass. Do not invent a new blue by eye.

If there are multiple blues today, consolidate only the ones that are meant to be the same product accent. Leave unrelated status, warning, disabled, or system colors alone unless they are clearly part of the same demo accent drift.

Keep the existing shape. Do not change border radius, bubble sizing, avatar sizing, chat input sizing, login card sizing, chat input sizing, or scripted demo timing unless a current color/background rule directly forces an obvious visual bug.

Keep login behavior unchanged. This ticket is not allowed to change passkey, account creation, `next` handling, success screen copy, sessionStorage, or redirect behavior.

## Acceptance criteria

- On mobile, the Kaleidoscope login background is white.
- On desktop, the Kaleidoscope login background is white.
- On mobile, the active demo chat background is white.
- On desktop, the active demo chat background is white.
- The primary demo blue matches the Kaleidoscope bubble blue.
- The Kaleidoscope bubble shape is unchanged.
- The chat bubbles keep their existing shape.
- The chat input remains visible and usable.
- The scripted demo still runs.
- Login and `/login?next=/demo` behavior are unchanged.
- No homepage, Remote Control, auth, wallet, image API, relay, daemon sync, or E2EE files change.
- If only HTML/CSS/inline JS changes, run inline parse checks for changed HTML files and `git diff --check`.

## Out of scope

- Redesigning the demo.
- Changing the script copy.
- Changing generated image behavior.
- Changing passkey/login behavior.
- Changing the homepage or agent-readable files.
