---
title: "/demo/ local-passkey toggle must match /login QR behavior"
date: 2026-05-01
author: Codex
status: ticketed
severity: P2
component: hosted-mcp
---

# /demo/ Local-Passkey QR Parity

## Summary

`/demo/` shows the same footer-level "Local passkeys off" affordance as `/login`, but it does not honor the same behavior. On `/login`, local passkeys off means Chrome desktop uses the QR desktop-to-phone flow. On `/demo/`, clicking `Enter the Kaleidoscope` still calls WebAuthn directly and can open the local passkey dialog.

This is misleading. The demo should work exactly like login for the account/auth entry flow.

## Observed

- `https://wip.computer/demo/` shows the `What should Lēsa call you? (optional)` prompt again after the route recovery deploy.
- With local passkeys off, clicking `Enter the Kaleidoscope` on `/demo/` still starts direct WebAuthn instead of the QR flow.
- Source confirms `/demo/` calls `navigator.credentials.create({ publicKey: options })` directly in `demo/index.html`.
- `/login` and `app/kaleidoscope-login.html` have the QR fallback logic:
  - desktop Chrome
  - local passkeys off
  - `startQrLogin(...)`
  - phone scans QR and completes passkey/Face ID

## Expected

`/demo/` account creation and sign-in should match `/login`:

- Local passkeys off on desktop Chrome should use the QR desktop-to-phone flow.
- Local passkeys on should use local/native WebAuthn.
- Mobile should use platform passkey directly.
- Register and sign-in variants should both work:
  - register: click `Enter the Kaleidoscope`
  - sign-in: click `Already have an account? Sign in.`
- The demo should keep showing:
  - `Enter the Kaleidoscope`
  - `What should Lēsa call you? (optional)`
  - `Already have an account? Sign in.`

## Impact

The demo and the production login present the same account/auth concept but do different things. This causes false failures during manual testing and makes the local-passkey toggle untrustworthy on `/demo/`.

It should not block the Remote Control pairing smoke if the pairing test uses `/login`, but it should be fixed before relying on `/demo/` as the canonical account demo.

## Evidence

Live behavior observed on 2026-05-01:

- Chrome showed the handle prompt.
- Safari had previously hidden it because of stale live code, but that was resolved by deploying the #793 fix.
- After the deploy, local passkeys off still caused `/demo/` to look for local passkeys.

Source evidence:

- `src/hosted-mcp/demo/index.html` directly calls `navigator.credentials.create({ publicKey: options })`.
- `src/hosted-mcp/demo/login.html` and `src/hosted-mcp/app/kaleidoscope-login.html` contain the QR fallback helpers (`needsCustomQR`, `startQrLogin`, local passkey toggle handling).

## Root Cause

`/demo/` is still on the older direct-WebAuthn implementation while `/login` has the newer QR/local-passkey decision logic. The footer/local-passkey UI is shared enough to look like one behavior, but the page code is not shared.

## Fix Plan

1. Reuse the `/login` QR/local-passkey decision logic for `/demo/` register and sign-in.
2. Preserve the visible `/demo/` UI. Do not invent new copy or redesign the page.
3. Make desktop Chrome with local passkeys off call `startQrLogin(...)` instead of direct WebAuthn.
4. Keep mobile behavior as direct platform passkey.
5. Keep local passkeys on behavior as local/native WebAuthn.
6. Keep `/demo/` independent of production `/login` localStorage state except for the intentional shared local-passkey toggle.

## Test Plan

- `/demo/`, Chrome desktop, local passkeys off:
  - click `Enter the Kaleidoscope`
  - QR appears
  - phone scan can complete register path
- `/demo/`, Chrome desktop, local passkeys off:
  - click `Already have an account? Sign in.`
  - QR appears
  - phone scan can complete sign-in path
- `/demo/`, Chrome desktop, local passkeys on:
  - clicking account actions uses native/local WebAuthn
- `/demo/`, mobile:
  - account actions use platform passkey directly
- `/login` still works exactly as before the change.
- `/demo/` still shows the handle input and sign-in link even when `localStorage["kscope-has-account"] = "true"`.

## Smoke Test

1. Set local passkeys off.
2. Open `https://wip.computer/demo/` on Chrome desktop.
3. Click `Enter the Kaleidoscope`.
4. Confirm QR appears instead of the local passkey dialog.
5. Scan with phone.
6. Confirm Face ID/passkey starts after phone tap and completes.

## Release Path

Small hosted-MCP web fix:

1. PR against `wip-ldm-os-private`.
2. Merge after review.
3. Deploy with `src/hosted-mcp/deploy.sh`.
4. Run `/demo/` and `/login` browser smokes.

## Rollback

Revert the PR or restore the prior `src/hosted-mcp/demo/index.html` from the previous deploy manifest.

## Review Questions

- Should `/demo/` share the exact login helper code with `/login`, or should the shared behavior be extracted into a production-owned script first?
- Should the local-passkey toggle remain in the shared footer if a page does not implement the toggle behavior?
- Is `/demo/` allowed to use `/api/qr-login`, or should a demo-specific QR session endpoint be added later?
