---
title: "Automate Remote Control smoke tests after the pairing flow stabilizes"
date: 2026-05-01
author: Codex
status: future-work
surface: codex-remote-control
---

# Remote Control Smoke Automation

## Summary

The Remote Control login/pairing recovery exposed a growing manual QA burden: each deploy now wants route checks, `/demo/` checks, `/login` checks, Chrome and Safari QR variants, pair-mode security checks, and end-to-end daemon pairing.

That is correct while the flow is still moving, but it is not sustainable for Parker to manually retest 10 to 15 browser paths on every deploy. Once the current pairing flow is stable, we should turn the discovered contract into automated release-pipeline gates.

Keep this ticket in the Remote Control plan lane for now so it stays attached to the pairing recovery work. It likely graduates into release-pipeline tooling after the contract is stable.

## Goal

Shrink manual QA to the irreducible real-device checks:

1. Scan one QR with Chrome phone.
2. Scan one QR with Safari phone.
3. Confirm one end-to-end daemon pair.

Everything else should be route/API/browser automation.

## Non-Goals

- Do not block the current pairing recovery deploy.
- Do not invent new login UI.
- Do not replace the need for one real-device Face ID/passkey smoke.
- Do not widen to public alpha gates.

## Pipeline Gates To Add

### 1. Route/API Smoke

Run against live deploys and, where possible, staging/local:

- `GET /health` returns 200 and `database=postgres`.
- `GET /login` contains Kaleidoscope markers:
  - `Enter the Kaleidoscope`
  - `Already have an account? Sign in.`
  - `Local passkeys`
  - does not contain `drive this session`
- `GET /demo/` contains:
  - `What should Lēsa call you? (optional)`
  - `Already have an account? Sign in.`
- `GET /app/footer.js` returns JavaScript, not HTML.
- `GET /app/sprites.png` returns `image/png`, not HTML.
- `GET /api/qr-login/status?s=bad` returns JSON 404, not homepage HTML.
- `GET /pair/<valid-code>` reaches the pair page, not the homepage.

### 2. Browser Automation

Use Playwright for browser-visible contracts that do not require real Face ID:

- Chrome desktop `/login` with local passkeys off starts QR.
- QR image appears after the existing login action.
- `/demo/` still shows the handle prompt and sign-in link with `localStorage["kscope-has-account"] = "true"`.
- `/login/app` still reaches the explicit app-login page.
- Pair-mode desktop status view never receives or renders `apiKey`.
- Pair-mode desktop does not navigate to `/pair/<CODE>`.

### 3. Mobile-Shape Browser Automation

Use Playwright device emulation for phone landing behavior:

- QR session URL lands on the expected state.
- Register QR path exposes the expected existing action.
- Sign-in QR path exposes the expected existing sign-in action.
- No duplicate or wrong page state appears.
- WebAuthn is attempted only after the expected user action, not before.

### 4. WebAuthn Mocking

Add controlled browser-test mocks for `navigator.credentials.create` and `navigator.credentials.get`:

- Register path calls `create`.
- Sign-in path calls `get`.
- Phone QR approval calls `/api/qr-login/approve`.
- Pair-mode phone redirects to `/pair/<CODE>`.
- Desktop pair-mode status response does not contain `apiKey` or `next`.

### 5. Pair Flow Harness

Add a narrow daemon/browser harness after the manual pair flow is stable:

- Start or simulate daemon `pair-init`.
- Produce `/login?next=/pair/<CODE>`.
- Drive desktop QR start.
- Drive phone-side QR approval with WebAuthn mocked.
- Confirm `/pair/<CODE>` submits explicit confirm.
- Assert daemon receives completed pairing.
- Assert desktop never receives `apiKey`.

## Manual Smokes That Remain

These are the checks that automation should not pretend to fully replace:

- Real Chrome phone QR scan starts Face ID/passkey correctly.
- Real Safari phone QR scan starts Face ID/passkey correctly.
- One real daemon pair from the installer/product path.

## Acceptance Criteria

- A developer can run one command before deploy and get route/API/browser smoke results.
- `deploy.sh` or a companion smoke command can run the live route checks after deploy.
- Manual deploy checklist is reduced to the real-device checks only.
- Failing smokes stop the deploy or dogfood progression.
- The smoke list stays aligned with the recovery master plan.

## Open Questions

- Should this live under `src/hosted-mcp` as a Playwright suite, or under release-pipeline tooling as a deploy gate?
- Should we add a staging host before running browser smokes against production?
- How much of the daemon pair flow should be real daemon versus protocol simulation?
- Should the smoke runner redact all tokens by construction and refuse to print `apiKey`, `ck-`, or ticket values?

## Next Step

After the current Remote Control pairing flow passes Parker-only dogfood, open an implementation plan for the first slice:

1. Route/API smoke command.
2. Playwright `/login` and `/demo/` smoke.
3. WebAuthn mock for phone QR approve.
