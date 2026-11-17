# Welcome label does not match the saved passkey label

**Date:** 2026-05-02
**Owner:** remote-control--cc--coder
**Reviewer:** remote-control--kay--partner
**Severity:** polish/consistency, but visible to every user (passkey label is in iOS Passwords / 1Password)
**Related:** none ... independent of the recovery PRs

## Symptom

After registering or signing in via WebAuthn, the welcome view says e.g.:

```
Welcome, passkey-j0AndtfaErkl.
```

But iOS Passwords (and 1Password) display the saved credential as:

```
user-j0Andtfa
```

Two different strings for the same account, both visible to the user.

## Cause

Three places in `src/hosted-mcp/server.mjs` produce the labels:

1. `handleRegisterOptions`: `userName = username || ("user-" + userIdB64.slice(0, 8))`. This is what gets passed to `generateRegistrationOptions` and saved by the platform passkey provider.
2. `handleRegisterVerify`: `agentId = stored.username || ("passkey-" + stored.userId.slice(0, 12))`. This is returned to the client and used internally as the user's identity.
3. Client `welcome-name`: assigned from `result.agentId`.

When the user registers without providing a handle, `userName` and `agentId` use different prefixes (`user-`/`passkey-`) and different slice lengths (8 chars vs 12 chars). The label saved on the phone (`userName`) is not the label shown on the welcome view (`agentId`).

## Fix

Server returns a new `credentialLabel` field from both `register-verify` and `auth-verify`, computed by the same formula as `userName`:

- If a username was provided at registration: `credentialLabel === username === userName === agentId` (no behavior change).
- If username was empty: `credentialLabel = "user-" + userId.slice(0, 8)` (matches the saved label).

For sign-in (`auth-verify`), the saved entry has `userId` and `agentId`. If `agentId.startsWith("passkey-")`, recompute `"user-" + entry.userId.slice(0, 8)`. Otherwise `credentialLabel = entry.agentId`.

QR-login flow propagates the label end-to-end:

- Phone reads `result.credentialLabel` from `register-verify` / `auth-verify`.
- Phone passes `credentialLabel` in `POST /api/qr-login/approve`.
- Server stores it on the QR session.
- `GET /api/qr-login/status` (legacy login mode only) returns it on `approved`.
- Pair-mode response is unchanged (no credentialLabel; pair-mode desktop doesn't use a welcome view).

Client uses `result.credentialLabel || username || result.agentId || 'you'` (or `data.credentialLabel || data.agentId || 'you'` on the desktop poll).

## Auth semantics: unchanged

- `agentId` continues to be the user's identity for API key issuance, passkey storage, and all internal lookups.
- Existing passkeys are back-compat: their saved entries still carry `userId`, so the label can be recomputed at sign-in time.
- No database migration required.

## Acceptance

- [ ] Register on iPhone with no handle → welcome shows `user-XXXXXXXX` matching iOS Passwords.
- [ ] Register on iPhone with a handle (e.g. `parker`) → welcome shows `parker` matching iOS Passwords.
- [ ] Sign in with an existing `passkey-*` account → welcome shows `user-<8 chars>` matching iOS Passwords (no need to re-register).
- [ ] Mac Chrome desktop QR session, after phone approves, shows the same `credentialLabel` in the desktop welcome view.
- [ ] Pair-mode unchanged (desktop shows "Approved on your phone", no apiKey, no welcome name).
- [ ] No change to `agentId` values stored anywhere.

## Status

**Fixed in this PR.** Lands in branch `cc-mini/credential-label-welcome`.
