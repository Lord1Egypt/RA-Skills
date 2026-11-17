---
title: "Pair via the existing /login QR flow (do not invent a new pairing UI)"
date: 2026-04-30
status: ready-for-final-review (Cody, 2026-04-30 round 5)
owner: Codex Remote Control pair (Claude Code implements; Cody reviews)
reviewer: Cody / Codex
related:
  - 2026-04-28--cc-mini--codex-remote-control-master-plan.md
  - 2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md
  - 2026-04-29--cc-mini--narrow-pre-hardening-baseline.md
---

# Pair via the existing /login QR flow

## Why this exists

The 2026-04-30 baseline retry got past install and `codex-daemon link`, then died at phone pairing:

- `codex-daemon link` printed `https://wip.computer/pair`.
- `https://wip.computer/pair` returned the wip.computer homepage (10801-byte fallback) instead of a pair page.
- nginx had no `location /pair` block, so the request fell through to the static webroot.
- Even with routing, the published spec told users to manually type a 6-char code into a separate page ... not the URL-first flow Parker actually wants.

Cody's directive: do **not** build a new pairing UI. The Kaleidoscope login flow at `https://wip.computer/login` already implements desktop QR + phone-passkey + browser-continues. Codex Remote Control pairing should plug into that exact flow.

## Product shape

`codex-daemon link` prints **one URL** that the user pastes on a laptop:

```
https://wip.computer/login?next=/pair/<CODE>
```

End-to-end:

1. Laptop browser hits `/login?next=/pair/<CODE>`.
2. Existing Kaleidoscope login page renders. User clicks "Enter the Kaleidoscope" or "Already have an account? Sign in."
3. Page switches to QR view (existing behavior). QR encodes a phone-side login URL with the qr-login `sessionId` (existing behavior).
4. Phone scans the QR. Phone opens the login URL on phone. Phone signs in / signs up with passkey/Face ID (existing behavior). Phone POSTs `/api/qr-login/approve` with `{sessionId, agentId, apiKey}` (existing behavior).
5. **New**: **Phone is the authority** (api_key is created on phone via passkey). After `POST /api/qr-login/approve` succeeds, the phone receives `next` in the response and `location.replace(next)`. Phone has `wip_api_key` + `wip_handle` already in its sessionStorage from the passkey auth step.
6. **New**: **Desktop does not redirect.** The desktop poller, on `status === "approved"`, swaps the QR view for a "Approved on your phone ... continue pairing on your phone" state. The desktop never tries to call `/pair/<CODE>` on its own (it has no api_key).
7. **New**: `/pair/<CODE>` on the phone reads the code from `location.pathname`, normalizes it, and shows an **explicit confirm step**: "Pair this laptop with Codex Remote Control?" with a Confirm button. On Confirm, POSTs `/api/codex-relay/pair-complete` with `{code}` and `Authorization: Bearer ${wip_api_key}`. Success view shows. (Auto-submit considered and rejected: explicit confirm is the right UX even for alpha.)
8. Daemon polls `/api/codex-relay/pair-status/<id>` and writes the `ck-` key to `~/.codex-daemon/relay-key`.

Manual code entry remains as a fallback at the bare `/pair` URL. Phone-direct path: a user who opens `/login?next=/pair/<CODE>` directly on phone runs the existing phone-side passkey path, then phone-side `/login` (which has no QR per existing media query) redirects to `/pair/<CODE>` on phone (api_key already in phone's sessionStorage from passkey sign-in).

## Why this is the right shape

- **Reuses the existing live UX.** No new copy, no new visual design, no new auth ceremony.
- **Keeps the codex-relay backend.** `/api/codex-relay/pair-complete` already binds the daemon's E2EE pubkey to the user's `ck-` key. Untouched.
- **Single URL for the user.** They copy one thing and paste once. The QR + passkey + redirect cascade is invisible.
- **Phone-direct path is automatic.** Open the URL directly on phone: phone-side `/login` already hides the QR (existing media query) and goes straight to passkey + pair-complete.

## Constraints (Cody review, 2026-04-30)

These are non-negotiable; they shape every change in this PR.

### C1. `next` is whitelisted to `/pair/<CODE>` only, using the real daemon alphabet.

`next` is **not** a general redirect primitive. For this feature accept only:

```
^/pair/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$
```

This matches the daemon's actual code generator (`CODEX_PAIR_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"`, length 6). Do **not** loosen to `[A-Z0-9]{6,12}` or any other broader pattern; use this exact regex everywhere `next` and the pair code are validated.

Reject anything else: empty string, `null`, `//`, `\\`, `http:`, `https:`, `data:`, `javascript:`, double-encoded payloads (decode once and re-validate), `/foo/bar`, `/codex-remote-control/...`, `/demo`, codes containing `0`/`O`/`1`/`I`, codes shorter or longer than 6 chars, etc. Validation runs server-side at `POST /api/qr-login`; client-side mirroring is defense-in-depth, not the gate.

### C2. `/login` does not become a general open redirect.

The sanitized `next` is **stored on the qr-login session record server-side**. For pair-mode sessions, `next` is returned **only** by `POST /api/qr-login/approve`, the phone-only endpoint, after passkey approval succeeds. The desktop's `GET /api/qr-login/status` poll does **not** return `next` (see **C6**). Unauthenticated `next` echoes are not allowed at any time. The query-string `next` on `/login?next=...` is read by the page only to pass it into `POST /api/qr-login`; it never appears in a redirect Location header.

### C3. Pair code normalization, against the real daemon alphabet.

Before `POST /api/codex-relay/pair-complete`, the page:
- Reads code from `location.pathname` (or the manual input).
- `trim()` and uppercase.
- Validates against the daemon's alphabet exactly: `[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}` (`CODEX_PAIR_ALPHABET` in `server.mjs`, length 6). The visually-ambiguous chars excluded by the daemon are `I`, `O`, `0`, `1`. **`L` is included** (don't reject it).
- Rejects mismatches with an inline error and does not POST.

Server-side mirroring: `handleCodexPairComplete` already redeems against `codexPairingByCode`, but should also defensively reject codes that don't match the alphabet/length up front rather than only on map miss, so a probing client gets a single uniform reject path.

### C4. Route ownership stays clean.

| Route | Owner |
|---|---|
| `/login`, `/login/` | MCP / Kaleidoscope auth (existing) |
| `/pair`, `/pair/<CODE>` | MCP / Kaleidoscope auth (new in this PR) |
| `/codex-remote-control/*` | Kaleidoscope Next.js app on :3001 (unchanged) |
| `/api/codex-relay/*` | Codex relay API on MCP (unchanged) |
| `/api/qr-login*`, `/webauthn/*`, `/api/pair/*` | MCP / Kaleidoscope auth (unchanged) |

This PR does not move existing routes between owners.

### C5. Do not swap the live `/login` UI.

`server.mjs` currently prefers `app/login.html` and falls back to `demo/login.html`. The live `/login` is `demo/login.html` because `app/` was never deployed.

This PR ships **only** the `demo/login.html` modifications. **Do not deploy `app/login.html`.** That swap is a separate decision: either prove visual + behavioral parity against `demo/login.html` first, or leave the file undeployed. The pairing fix must not change the login page Parker likes.

To make this safe operationally during this PR's deploy: do not create or sync the `/var/www/wip.computer/app/mcp-server/app/login.html` path. Only `app/pair.html` lands there.

### C6. Phone is the authority. Desktop is a QR-display surface. apiKey never crosses to desktop.

The api_key for the user is created on the **phone** during the passkey ceremony. The desktop never sees the api_key in this flow ... and crucially, the server **does not return it** in the desktop's poll response.

- Only the **phone** redirects to `/pair/<CODE>` after `qr-login/approve` succeeds. Phone has the api_key in its own sessionStorage and uses it on the pair page.
- The **desktop** never redirects to `/pair/<CODE>`. The desktop, on `status === "approved"`, swaps the QR view for a "Approved on your phone ... continue pairing on your phone" status panel.
- **Server enforcement.** For pair-mode QR sessions (`purpose: "pair"`), `GET /api/qr-login/status` MUST NOT return `apiKey` or `next` to the desktop. It returns only `{status: "approved" | "pending"}` and possibly a display-only field like `agentId` for the "Approved as @<handle>" label. The desktop cannot get the api_key out of this endpoint at all, even by ignoring fields client-side.
- **Phone-side** receives `next` from `POST /api/qr-login/approve` (the phone-only endpoint). That is the single channel through which `next` reaches a client.
- The pair-complete call always originates from the phone in this flow.

Why the server-side strip matters: "desktop ignores it" is not a security property; it's a hope. Removing the field from the response makes the property structural. A compromised desktop page, a debug log, a network trace, a service worker, or a misbehaving extension cannot exfiltrate what the server didn't send.

### C7. Explicit confirm on `/pair/<CODE>`.

Do not silently auto-pair the moment the phone lands on `/pair/<CODE>`. Render a confirm step (heading + code/device label + Confirm/Cancel) and gate the `POST /api/codex-relay/pair-complete` on the user tapping Confirm. The phone user just did Face ID on the previous page; a deliberate "yes, pair this laptop" tap is the right ceremony.

### C8. Default authority is phone-held passkey. Local desktop passkeys are testing-only.

Pairing ceremony, in order:

1. **Laptop**: displays QR and waits.
2. **Phone**: scans QR, signs in with passkey / Face ID, confirms pairing.
3. **Laptop**: shows approved/paired status.
4. **Daemon**: receives pair completion through polling.

The laptop browser **may** display QR codes, status, and setup instructions, but it does not become the approval authority during pairing just because it opened `/login`. Pairing is completed on the phone after passkey approval.

The "Local passkeys on/off" toggle visible at the bottom of `/login` is a **developer / test affordance**. It exists low on the page so we can test browser-local WebAuthn behavior and fallback paths. The normal product flow keeps the phone as the authority. Do not build Codex Remote Control pairing around the local-desktop-passkey path. Do not special-case desktop sign-in to complete `pair-complete` from the laptop. Do not promote local desktop passkeys in any Codex Remote Control copy.

This fits the broader security model: WIP is not trying to become a hardware wallet company; it defers private-key security and recovery UX to Apple's phone stack by default.

If local desktop passkeys ever become a real user feature (separate plan, separate UX), it must be opt-in and labeled clearly:

> Advanced: use this computer's passkey instead of your phone.

Not the default. Not for this PR.

**Implementation implication.** This PR only wires `next` through the QR / phone-passkey path. We do not add `next` redirect handling to a desktop-local-passkey success path. If a developer in test mode signs in on the desktop with local passkeys via the toggle, they land on the existing `/login` welcome view (no redirect). The CRC pair flow assumes the QR / phone path.

## Files that change

### `src/hosted-mcp/demo/login.html` (the live page that serves wip.computer/login)

The file currently named `demo/login.html` IS the production Kaleidoscope login. Filename is an artifact; product is the live flow.

- Read `?next=` from URL query string.
- Pass `next` through to the `POST /api/qr-login` request body.
- **Phone-side after `qr-login/approve` returns success** (phone has just stored its `wip_api_key` + `wip_handle` from the passkey auth step): if `next` is present in the response, `location.replace(next)`. **Phone is the actor that completes the pair.**
- **Desktop-side after polling returns `status === "approved"`** (pair-mode response: only `{status, agentId}`, no `apiKey`, no `next`): swap the QR view for a "Approved on your phone ... continue pairing on your phone" status. The agentId may be displayed as "Approved as @<handle>". **Do not redirect.** Do not attempt to read or store any apiKey ... the server does not return it for pair-mode sessions (per **C6**).
- Client-side mirror of the `/pair/<CODE>` whitelist regex (`^/pair/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$`) before passing `next` server-ward (defense-in-depth; server validates authoritatively).
- Phone-direct path (user opened `/login?next=/pair/<CODE>` on phone): runs the existing local-passkey sign-in path on the phone (no QR view on mobile per existing media query), stores `wip_api_key`+`wip_handle` in phone sessionStorage on auth-verify success, then redirects to `next` if present.

### `src/hosted-mcp/server.mjs`

- `handleQrLoginStart`: accept `next` from body. Validate strictly per **C1** (single regex against `^/pair/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$`, single-decode, no scheme, no `//`, no `\\`). On invalid `next`: ignore (treat as absent), do not 400 the request. Store sanitized `next` in `qrLoginSessions[sessionId].next`. **Set a `purpose` flag**: if `next` is a valid pair URL, set `qrLoginSessions[sessionId].purpose = "pair"`. Otherwise leave undefined (legacy login behavior unchanged).
- `handleQrLoginStatus`: response shape depends on `purpose`.
  - **Pair-mode (`purpose === "pair"`)**: when status is `approved`, return only `{status: "approved", agentId: <agentId>}` for a display-only label. **Never** include `apiKey`, **never** include `next`. When status is `pending`, return `{status: "pending"}`.
  - **Legacy login mode (`purpose` unset)**: existing behavior unchanged. Returns `{status, agentId, apiKey}` on approved.
- `handleQrLoginApprove`: when the session has `purpose === "pair"`, include `next` in the response so the **phone** can `location.replace(next)`. Legacy login sessions return `{ok: true}` as before.
- `handleCodexPairComplete` (existing): defensively reject codes that don't match `^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$` before the map lookup. Single uniform reject path for invalid input vs. unknown code.
- New route: `GET /pair/<CODE>` ... match `/^\/pair\/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/` (case-sensitive; the daemon's alphabet is uppercase + digits 2–9 only) and serve `app/pair.html`. The page reads the code from `location.pathname`, so the server doesn't need to inject it.
- `handleCodexPairInit`: change `web_url` from `ISSUER_URL + "/pair"` to `${ISSUER_URL}/login?next=${encodeURIComponent("/pair/" + code)}`.

### `src/hosted-mcp/app/pair.html`

This file currently exists in the repo but is **not deployed on the VPS**. This PR deploys it for the first time.

- Read code from `location.pathname` (`/pair/TME8JU` → `TME8JU`).
- Normalize per **C3** (trim, uppercase, validate alphabet + length).
- **If not signed in**: redirect to `/login?next=` + `encodeURIComponent(location.pathname)` (preserves the URL-with-code so the QR phones home to the right route).
- **If signed in AND code is valid in URL**: render an **explicit confirm step**. Heading: "Pair this laptop with Codex Remote Control?" Body: shows the normalized code (and a device label if available from the daemon's pair-init payload). Primary button: "Confirm". Secondary: "Cancel".
- On Confirm: POST `/api/codex-relay/pair-complete` with `{code}` and `Authorization: Bearer ${wip_api_key}`. On success, show "Paired. Your laptop will pick this up in a few seconds."
- On error from pair-complete: show inline error (expired code, wrong code, etc.) and a "Run codex-daemon link again on your laptop to get a fresh code" hint.
- Manual entry stays as a fallback for the bare `/pair` URL (no code in path). Same explicit-confirm UX after the user types the code.

**Auto-submit considered and rejected.** Cody's directive: explicit confirm is the right UX even for alpha. The phone user just did Face ID on the previous page; one more deliberate tap to bind a specific laptop is a reasonable, expected step.

### `src/hosted-mcp/nginx/codex-relay.conf`

Add two location blocks proxying to `127.0.0.1:18800`:

```
# /pair (no code)              ... fallback: manual code entry page
location = /pair {
    proxy_pass http://127.0.0.1:18800;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# /pair/<CODE>                  ... URL-first pair flow
# Real daemon alphabet (CODEX_PAIR_ALPHABET): A-Z minus I and O, digits 2-9.
# Length 6. L IS included.
location ~ ^/pair/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$ {
    proxy_pass http://127.0.0.1:18800;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Without these, `/pair*` falls through to `location /` `try_files` and returns the static homepage. That is the bug the 2026-04-30 baseline retry hit.

### Daemon `src/relay-cli.ts` (separate alpha release after server is verified live)

Update print copy. Currently prints "Sign in on wip.computer with your passkey, then enter the code above." That instruction is now wrong; the page reads the code from the URL. Replace with:

```
codex-daemon: pairing against <base>

  Open this URL on your laptop:
  <web_url>

  Then scan the QR with your phone and approve with Face ID.

  Backup code: <code>
  Expires:     <expires_at>

Waiting...
```

This requires a daemon alpha release (alpha.7), shipped **after** the server side is verified live (per Cody: two separate deliverables).

## Files that do NOT change

- **`/api/codex-relay/pair-complete`** server logic. The page calls it the same way; only how the page learns the code changes.
- **`/api/codex-relay/pair-init`** logic except for the `web_url` field.
- **`src/hosted-mcp/app/login.html`**. Per **C5**, do not deploy this; do not modify; leave undeployed.
- **kaleidoscope-private**. The Next.js `pair/page.tsx` is a separate (kaleidoscope) pair flow with its own backend (`/api/pair/approve`). Not the codex-daemon flow.
- **`/api/qr-login/qr`** endpoint. The QR's encoded URL still goes to phone-side `/login?s=...` exactly as today.

## Deploy

1. `scp` updated `demo/login.html` to `/var/www/wip.computer/app/mcp-server/demo/`.
2. Create `/var/www/wip.computer/app/mcp-server/app/` (currently does not exist) and `scp app/pair.html` only. **Do not place `app/login.html` there.** (Per C5.)
3. `scp` updated `server.mjs` to `/var/www/wip.computer/app/mcp-server/`.
4. `sudo cp` updated `codex-relay.conf` to `/etc/nginx/snippets/`.
5. `sudo nginx -t && sudo nginx -s reload`.
6. `pm2 restart mcp-server`.

## Smoke tests

Run after deploy, before re-running the baseline.

### Routing

```bash
# A1. /login?next=<route> still renders the existing Kaleidoscope login UI.
curl -sI "https://wip.computer/login?next=/pair/TME8JU" | head -3
# expect: 200 OK, Content-Type: text/html (from MCP, not nginx fallback).
curl -s "https://wip.computer/login?next=/pair/TME8JU" | grep -c "Enter the Kaleidoscope"
# expect: 1

# A2. /pair/<code> reaches MCP, not the homepage.
curl -sI https://wip.computer/pair/TME8JU | head -3
# expect: 200 OK from MCP.
curl -s https://wip.computer/pair/TME8JU | wc -c
# expect: small (a few KB), NOT 10801 (homepage fallback).
```

### Redirect safety

```bash
# B1. Absolute URL is rejected (next ignored, login session created without it).
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"https://evil.example.com"}' | jq '.'
# expect: 200 with sessionId, no next field on subsequent /api/qr-login/status.

# B2. Protocol-relative URL is rejected.
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"//evil.example.com"}' | jq '.'
# expect: same as B1, no next.

# B3. Backslash injection is rejected.
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/\\\\evil.example.com"}' | jq '.'
# expect: same as B1, no next.

# B4. Out-of-whitelist relative path is rejected.
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/codex-remote-control/foo"}' | jq '.'
# expect: same as B1, no next (only /pair/<CODE> is whitelisted).

# B4a. Pair path with off-alphabet character is rejected.
# Excluded chars: I, O, 0, 1. (L IS included, so do not test L as off-alphabet.)
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/pair/ABCDE0"}' | jq '.'
# expect: same as B1, no next.

# B4a-bis. Sanity: a code containing L is accepted (regex includes L).
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/pair/LMNPQR"}' | jq '.'
# expect: accepted; subsequent /api/qr-login/approve returns next=/pair/LMNPQR.

# B4b. Pair path with wrong length is rejected.
curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/pair/ABCDEFG"}' | jq '.'
# expect: same as B1, no next.

# B5. Whitelisted path is preserved end-to-end (phone-side only).
SESSION=$(curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/pair/ABC234"}' | jq -r .sessionId)
curl -s "https://wip.computer/api/qr-login/status?s=$SESSION" | jq '.'
# expect (desktop poll): {"status":"pending"}. After phone approve, this becomes
# {"status":"approved","agentId":"<handle>"}. NO apiKey field. NO next field.
```

### Pair-mode strip (C6 enforcement on the server)

```bash
# C6a. Pair-mode status response NEVER includes apiKey, even after phone approve.
SESSION=$(curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest","next":"/pair/ABC234"}' | jq -r .sessionId)
# (simulate phone-side approve out of band, or run the full manual flow)
RESPONSE=$(curl -s "https://wip.computer/api/qr-login/status?s=$SESSION")
echo "$RESPONSE" | jq 'has("apiKey")'   # expect: false
echo "$RESPONSE" | jq 'has("next")'     # expect: false (next goes to phone, not desktop)

# C6b. Legacy (non-pair) status still returns apiKey.
SESSION=$(curl -sX POST https://wip.computer/api/qr-login \
  -H 'Content-Type: application/json' \
  -d '{"handle":"smoketest"}' | jq -r .sessionId)
# (simulate approve)
RESPONSE=$(curl -s "https://wip.computer/api/qr-login/status?s=$SESSION")
echo "$RESPONSE" | jq 'has("apiKey")'   # expect: true (legacy login flow unchanged)
```

### Pair-complete normalization

Manual: enter code in lowercase + leading whitespace into the bare `/pair` page. Verify the page normalizes to the daemon's alphabet before POST and rejects out-of-alphabet characters with an inline error.

### End-to-end manual

```
codex-daemon link
# -> prints https://wip.computer/login?next=/pair/<CODE>
#
# Laptop:
# -> open URL on laptop browser
# -> click "Enter the Kaleidoscope" / "Sign in"
# -> QR appears
# -> (status panel will switch to "Approved on your phone" once phone approves)
#
# Phone:
# -> scan QR
# -> phone signs in with passkey (Face ID)
# -> phone redirects to /pair/<CODE>
# -> phone shows "Pair this laptop with Codex Remote Control? [Confirm]"
# -> tap Confirm
# -> phone POSTs /api/codex-relay/pair-complete
# -> phone shows "Paired."
#
# Daemon:
# -> polls /api/codex-relay/pair-status, gets ck-key
# -> prints "paired as @<handle>"
```

Confirm: laptop browser does **not** redirect to `/pair/<CODE>` at any point. Laptop only ever shows `/login` (QR + waiting) → status panel ("Approved on your phone").

## Acceptance gate (do not retry baseline before all green)

- [ ] A1 + A2 routing tests pass.
- [ ] B1, B2, B3, B4, B4a, B4b reject; B5 preserves.
- [ ] **C6a passes**: laptop's network response from `GET /api/qr-login/status` for a pair-mode session contains **no `apiKey` field** and **no `next` field** at any time (pending or approved).
- [ ] **C6b passes**: legacy login-mode QR sessions still return `apiKey` (no regression for the non-pair login flow).
- [ ] Pair-complete normalization rejects invalid chars/length client-side and server-side, both code-input and `next`-input paths, against the real daemon alphabet `[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}`.
- [ ] One full manual run end-to-end (URL paste → QR scan → passkey on phone → phone redirects to `/pair/<CODE>` → tap Confirm → daemon paired). Test code is the actual code generated by `codex-daemon link`, not a placeholder.
- [ ] Per **C6**: laptop browser never navigates away from `/login` during the run; laptop console shows no fetch to `/pair/*` or `/api/codex-relay/pair-complete`; laptop network trace contains no `apiKey` value anywhere in the qr-login response stream.
- [ ] Per **C7**: phone shows an explicit confirm screen on `/pair/<CODE>` and does not POST `pair-complete` until the user taps Confirm.
- [ ] Per **C8**: with the "Local passkeys" toggle in its default position (off, where applicable), the CRC pair flow goes through QR + phone passkey end-to-end. No code path treats desktop-local-passkey sign-in as the CRC pair authority.
- [ ] Live `/login` page is unchanged visually and behaviorally for the user (per C5). Local-passkeys toggle stays in the same low-on-page position; copy unchanged.

Daemon copy update + alpha.7 ship in a follow-up after this is verified live.

## Non-goals for this PR

- Designing a new pair page from scratch.
- Harmonizing `/api/pair/approve` and `/api/codex-relay/pair-complete`.
- Multi-device pairing UX (phase 5).
- Rewriting the daemon's pair flow logic. Only the print copy changes (separate alpha).
- Deploying `app/login.html` (per C5).
- Generalizing `next` into a reusable redirect primitive (per C1).

## Cody review log

- **2026-04-30 round 1**: plan blessed with refinements. Absorbed as **C1–C5** + redirect-safety smoke tests + daemon-copy-as-separate-deliverable.
- **2026-04-30 round 2**: two corrections.
  - **Phone is the authority, not the desktop.** Phone redirects to `/pair/<CODE>` after approving the QR session; desktop just shows "Approved on your phone" status and never navigates. The api_key is created on phone via passkey; desktop never sees it. Captured as **C6**.
  - **Explicit confirm on `/pair/<CODE>`.** No silent auto-pair. The phone shows "Pair this laptop with Codex Remote Control? [Confirm]" and gates `POST /api/codex-relay/pair-complete` on the user tap. Captured as **C7**.
- **2026-04-30 round 3**: product principle added.
  - **Default authority is phone-held passkey; local desktop passkeys are testing-only.** WIP is not a hardware-wallet company; private-key security and recovery defer to Apple's phone stack by default. The "Local passkeys" toggle on `/login` is a developer affordance for testing browser-local WebAuthn, deliberately placed low on the page. CRC pairing must not be built around the desktop-local-passkey path. Captured as **C8**.
- **2026-04-30 round 4**: two final blockers patched.
  - **apiKey leak to desktop**: prior draft said "desktop ignores it" ... not a security property. Tightened **C6** so the server **does not return** `apiKey` (or `next`) in `/api/qr-login/status` for pair-mode sessions (`purpose === "pair"`). Server-side strip, not client-side hope. Server.mjs section now adds a `purpose` flag and scoped response shape. New smoke tests **C6a** (pair-mode response contains no apiKey/next) and **C6b** (legacy login mode unchanged). Acceptance gate adds an explicit network-response-no-apiKey check.
  - **Code regex too broad**: prior draft used `[A-Z0-9]{6,12}` and example codes like `ABC123` / `TESTCODE`, which include letters/digits the daemon's alphabet excludes. Tightened to the real alphabet everywhere: **C1**, **C3**, server.mjs route, nginx snippet regex, client validation, and all smoke examples now use `^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$` and example codes `TME8JU` / `ABC234`. Added redirect-safety smoke tests **B4a** (off-alphabet char) and **B4b** (wrong length).
- **2026-04-30 round 5**: alphabet-text vs regex contradiction fixed.
  - Cody caught: the regex `[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]` includes `L`, but **C3** prose said "no `I`, `L`, `O`, `0`, `1`," and the **B4a** comment listed `L` among off-alphabet chars. If implementation followed the prose instead of the regex, real daemon codes containing `L` would fail pairing. Removed every "L is excluded" claim. **Excluded chars are `I`, `O`, `0`, `1` only.** Added a positive sanity test **B4a-bis** that explicitly accepts a code containing `L` (`/pair/LMNPQR`).
  - Cody also flagged: **C2** wording made it sound like pair-mode `qr-login/status` returns `next`. Rewritten so C2 explicitly states pair-mode `next` flows only via `qr-login/approve` (phone-only), and `qr-login/status` for pair-mode does not return `next`. Aligns with **C6** server-side strip.

Plan is ready for final review. Implementation begins after Cody's bless.
