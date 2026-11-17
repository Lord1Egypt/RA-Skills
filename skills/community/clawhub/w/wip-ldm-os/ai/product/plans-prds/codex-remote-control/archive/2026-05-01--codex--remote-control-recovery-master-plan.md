# Codex Remote Control Recovery Master Plan

**Date:** 2026-05-01
**Author:** Cody, with Parker
**Status:** active restart packet
**Scope:** Remote Control private dogfood recovery after the VPS hardening train, #773 deploy, and `/login` route regression.

## Purpose

This file is the restart point for Codex Remote Control work if the active agent context is lost.

The older folder contains good plans, but they are now split across time:

- `2026-04-28--cc-mini--codex-remote-control-master-plan.md` is the original product master plan.
- `2026-04-29--codex--overall-security-gate-matrix.md` is the security gate matrix, but its live status changed after the VPS hardening train.
- `2026-04-30--cc-mini--pair-via-login-qr-flow.md` is the correct pairing product plan, but it is not a full recovery/deploy master.

Use this document first for current work. Use the older documents as referenced background, not as the live state.

## Current State

### VPS auth/perimeter

Private-dogfood auth/perimeter is live-pass, not public-alpha-pass.

Accepted train:

- `#727` fail-closed/Postgres containment deployed.
- `#729` log redaction deployed.
- `#731` WebSocket Origin allowlist deployed.
- `#732` rate limits deployed.
- `#733` ticket/subprotocol, daemon query-token closure, and per-thread isolation deployed and smoked.
- `#734` deploy provenance deployed and verified.
- `#778` merged so source deploy tooling matches the repaired live state.

Accepted #733 post-deploy evidence:

- web subprotocol ticket returns `101`.
- web `?ticket=` back-compat returns `101`.
- web `?token=` rejects with `LDM_HOSTED_MCP_ALLOW_WS_URL_TOKEN` unset.
- daemon `Authorization: Bearer` returns `101`.
- daemon `?token=` rejects.
- bad Origin returns `403` before auth.
- same-agent different-thread isolation passes.
- malformed daemon frames are dropped with redacted warnings.
- active nginx and PM2 logs are clean after test-key rotation/quarantine.

Residual private-dogfood risk:

- `#775` tracks nginx `error_log` request-URI leakage. The known smoke leak was contained: test key rotated, old key returns `401`, active logs clean, historical leak quarantined. Do not use real keys in URL-token smoke tests again.
- `pair-status` currently returns `api_key` for daemon bearer issuance. Smoke tooling must redact it; follow-up should constrain poll access and lifetime.

### Remote Control pairing

`#773` pair-via-login implementation is merged and has been deployed once.

The product shape is still correct:

- `codex-daemon link` should send the user to `https://wip.computer/login?next=/pair/<CODE>`.
- Desktop `/login` shows the existing Kaleidoscope QR login page.
- Phone scans QR, signs in with passkey/Face ID, and lands on `/pair/<CODE>`.
- `/pair/<CODE>` shows an explicit Confirm step before pair-complete.
- Phone is the authority for pairing.
- Desktop QR status must not receive `apiKey` or pair-mode `next`.

The deployment/recovery state is not fully closed:

- `/login` route ownership regressed once because `app/login.html` silently took over from `demo/login.html`.
- `/login` was restored to `demo/login.html` first, with `/login/app` as the explicit app-login route.
- Chrome then failed because the restored demo page calls `/api/qr-login/*`, but nginx did not proxy those API routes to Node.
- A live nginx hotfix added `/api/qr-login` and `/api/qr-login/` proxy routes. Source must include this fix before the next deploy.
- `#781` is the active Remote Control recovery/deploy PR lane. It must include route ownership, deploy inventory, and QR-login API routing before baseline retry.

## Route Ownership

These routes are the current contract. Do not change them implicitly.

| Route | Owner | Expected behavior |
|---|---|---|
| `/login`, `/login/` | hosted MCP / Kaleidoscope auth | Canonical Kaleidoscope QR login. Serves `app/kaleidoscope-login.html` (production-owned). Legacy fallback to `demo/login.html` exists during the transition and will be removed once production-owned is verified live. |
| `/login/app`, `/login/app/` | hosted MCP app-login variant | Preserves the developed app login page explicitly. Serves `app/login.html`. |
| `/api/qr-login` | hosted MCP / Kaleidoscope auth | POST creates QR login session. Must return JSON, not HTML or 405. |
| `/api/qr-login/qr` | hosted MCP / Kaleidoscope auth | GET returns the QR image for a QR login session. |
| `/api/qr-login/status` | hosted MCP / Kaleidoscope auth | GET returns JSON status. Fake/expired sessions should return JSON 404, not homepage HTML. |
| `/api/qr-login/approve` | hosted MCP / Kaleidoscope auth | POST phone-side approval after passkey auth. |
| `/webauthn/*` | hosted MCP / Kaleidoscope auth | Passkey register/auth endpoints. Must return JSON. |
| `/pair`, `/pair/<CODE>` | hosted MCP / CRC pairing | Bare manual fallback and URL-first pair-confirm page. Serves `app/pair.html`. |
| `/api/codex-relay/*` | hosted MCP / CRC relay | Pair-init/status/complete, bootstrap, ws-ticket, daemon/web WS. |
| `/codex-remote-control/*` | Kaleidoscope Next.js app | Phone remote-control surface via port 3001. |
| `/app/*` | hosted MCP / production static | Production-owned static assets served by Node via `serveAppFile`. Includes `app/footer.js`, `app/sprites.png`, and any other production assets. Nginx must proxy `/app/` to Node so requests get correct Content-Type and don't fall through to the static homepage. |
| `/demo/*` | hosted MCP static demo assets | Demo site, served via nginx alias to `/var/www/wip.computer/app/mcp-server/demo/`. **Demo-only.** Production auth must NOT depend on these files; production owns its own login HTML at `app/kaleidoscope-login.html`. The demo site stays available unchanged. |

## Non-Negotiables

- Do not delete developed pages to fix routing.
- Do not make production correctness depend on a file being absent.
- Do not let `app/login.html` silently take over `/login`.
- Do not treat "Kaleidoscope markers" as enough; verify the actual copy and behavior.
- Do not baseline retry while Chrome login shows `Unexpected token '<'` or any API returns HTML where JSON is expected.
- Do not use real `ck-` keys in URL-token rejection smoke tests.
- Do not print `api_key` from `pair-status` in chat, shell logs, screenshots, or PR comments.
- Do not call this public-alpha ready. The current target is Parker/private dogfood only.

## Immediate Recovery Checklist

This is the next active work. `remote-control--cc--coder` owns implementation. `remote-control--kay--partner` reviews the product/security contract. VPS Security should be aware because nginx and hosted MCP are shared infrastructure.

### 1. Source parity for live hotfixes

Ensure source contains every live hotfix:

- `server.mjs`: `/login` and `/login/` serve `app/kaleidoscope-login.html` (with a legacy `demo/login.html` fallback during the transition); `/login/app` and `/login/app/` serve `app/login.html`. Production auth must not depend on demo/.
- `nginx/mcp-oauth.conf`: proxies `/login`, `/login/app`, `/webauthn/*`, `/api/qr-login`, `/api/qr-login/*`, and `/app/*` to Node. The `/app/` proxy is required so production-owned static assets (`/app/footer.js`, `/app/sprites.png`) reach `serveAppFile` with the correct Content-Type rather than falling through to the static homepage.
- `nginx/codex-relay.conf`: proxies `/pair`, `/pair/<CODE>`, and `/api/codex-relay/*`.
- `deploy.sh`: deploys `demo/*` and `app/*`.
- `deploy.sh` or smoke tooling must make route ownership explicit so `app/login.html` cannot silently become canonical `/login` again.

### 2. Live route smoke

Run before any baseline retry:

```text
GET  /health                                      -> 200 JSON, database=postgres
GET  /login                                      -> existing Kaleidoscope QR login page
GET  /login/app                                  -> developed app login page
POST /api/qr-login                               -> 200 JSON with sessionId and qrUrl
GET  /api/qr-login/status?s=bad                  -> JSON 404, not homepage HTML
GET  /api/qr-login/qr?s=<real-session>           -> QR/image response
POST /webauthn/register-options                  -> JSON
POST /webauthn/auth-options                      -> JSON
GET  /pair/<valid-code>                          -> pair page, not homepage
GET  /codex-remote-control/<thread-id>           -> Next.js remote-control surface
GET  /app/footer.js                              -> 200 Content-Type: text/javascript, not HTML
GET  /app/sprites.png                            -> 200 Content-Type: image/png, not HTML
```

Required `/login` markers:

- contains `Enter the Kaleidoscope`
- contains `Already have an account? Sign in.`
- contains the local passkeys footer
- does not contain `drive this session`
- clicking `Enter the Kaleidoscope` in Chrome does not show `Unexpected token '<'`

Required API response rule:

- QR login and WebAuthn endpoints must return JSON for API errors, not static homepage HTML.

QR phone-side smoke variants. The phone-side QR landing no longer changes the primary button based on `m=signin`, so the phone tester taps the right element for the path:

- **Register QR path**: scan QR (mode default or `m=register`) → tap `Enter the Kaleidoscope` → Face ID / passkey → approve.
- **Signin QR path**: scan QR (`m=signin`) → tap `Already have an account? Sign in.` → Face ID / passkey → approve.

Both paths must complete without `NotAllowedError` (Chrome) and without auto-firing WebAuthn. Safari and Chrome must both reach Face ID after the user's tap.

Demo cross-route-state smoke:

- `localStorage["kscope-has-account"] = "true"`, reload `/demo/`. The handle input (`What should Lēsa call you? (optional)`) and the `Already have an account? Sign in.` link must remain visible. The primary `Enter the Kaleidoscope` button must still create an account; production `/login` state must not change `/demo/` rendering.

### 3. Pairing smoke

Only after route smoke passes:

```text
codex-daemon link
```

Expected:

- daemon prints a URL shaped like `https://wip.computer/login?next=/pair/<CODE>`
- desktop `/login` shows QR
- phone scans QR and signs in with passkey/Face ID
- phone lands on `/pair/<CODE>`
- pair page shows explicit Confirm
- Confirm calls `pair-complete`
- daemon polling completes and stores relay key
- daemon status reports paired/running

Transcript hygiene:

- redact `api_key` from any `pair-status` output before it reaches chat
- do not paste full `ck-` values
- active logs must remain clean after the smoke

### 4. Remote-control UI smoke

Only after pairing smoke passes:

- generate the session remote-control URL
- open it on phone
- confirm login/session state
- confirm `/bootstrap` returns `200`
- confirm `/ws-ticket` returns `200`
- confirm browser WS uses subprotocol ticket, not `?token=ck-`
- confirm daemon and phone are connected to the same thread

Do not send a real Codex prompt until the UI shell and attach state are correct.

## Then Dogfood Gates

After the immediate recovery checklist passes, run the live-test runbook gates:

1. Privacy gate: relay/operator logs do not contain prompt text, decrypted Codex output, `ck-` values, tickets, envelopes, or payload bytes.
2. Plaintext rejection gate: plaintext `session.*` is rejected for E2EE-capable daemon pairs.
3. Attach gate: existing thread attach succeeds or fails explicitly; it never silently runs against a different thread.
4. Interrupt gate: Stop aborts a running turn end-to-end.

Only after these pass can the build be treated as private dogfood-ready.

## Current Follow-Ups

- `#775`: nginx `error_log` request-URI leakage. Low-priority hardening for private dogfood, still required before broader exposure.
- `#781`: Remote Control recovery/deploy lane. Must merge the route ownership and deploy inventory fixes before baseline retry.
- `pair-status` bearer issuance: file a follow-up to require a daemon-side poll secret or equivalent, shorten expiry if practical, and redact smoke output.
- ~~cleanup stale naming: `demo/login.html` is currently the canonical live login file by route contract~~ **Resolved 2026-05-01**: production now owns `app/kaleidoscope-login.html`. `demo/login.html` is a legacy fallback only and the demo site remains demo-only.
- remove the `demo/login.html` fallback in `/login` once `app/kaleidoscope-login.html` is verified live with both Safari and Chrome QR scans.

## Historical Docs Map

Read in this order:

1. This file: current restart packet.
2. `2026-04-30--cc-mini--pair-via-login-qr-flow.md`: product contract for URL-first pairing via existing `/login` QR flow.
3. `2026-04-29--codex--overall-security-gate-matrix.md`: gate framing. Must be updated after the current recovery closes.
4. `2026-04-29--codex--relay-auth-security-ticket.md`: relay-auth threat model and hardening rationale.
5. `2026-04-28--cc-mini--codex-remote-control-master-plan.md`: original product plan and four dogfood gates.
6. `2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md`: live dogfood gate procedure, but update commands mentally against the route ownership in this file.
7. `2026-04-28--cc-mini--app-server-pivot-phase-7.md`: future adapter swap. Do not start until private dogfood proves the product.

## Stop Conditions

Stop and report instead of continuing if any of these happen:

- `/login` serves the wrong page again.
- an API endpoint returns homepage HTML where JSON is expected.
- nginx config is broken on disk even if the in-memory config still serves traffic.
- a real `ck-` key, ticket, or `api_key` reaches chat, logs, screenshots, or PR comments.
- a deploy changes both auth/perimeter and product UI without a route smoke plan.
- a fix requires deleting or hiding a developed page.

The recovery principle: preserve every developed flow, but make route ownership explicit so one flow cannot silently replace another.
