---
name: ravi-sso
description: Get short-lived identity verification tokens to prove your Ravi identity to third-party services. Do NOT use for agent authentication (use ravi-login) or credential storage (use ravi-secrets).
---

# Ravi SSO

Get a short-lived token to prove your Ravi identity to a third-party service that supports "Login with Ravi".

## Get an SSO Token

```bash
ravi sso token
```

**Response shape:**
```json
{
  "token": "rvt_eyJhbGciOiJIUzI1NiJ9...",
  "expires_at": "2026-04-07T10:35:00Z"
}
```

Pass the token to the third-party service however it requires (request body, header, query param — it varies per service).

## How Third Parties Verify It

The third-party backend calls `POST https://ravi.id/api/sso/verify/` with `{ "token": "rvt_..." }` and receives:
```json
{
  "identity_uuid": "...",
  "identity_name": "Sarah Johnson",
  "identity_email": "sarah.johnson472@raviapp.com",
  "identity_phone": "+15551234567",
  "created_at": "2026-02-25T10:30:00Z",
  "owner": { "name": "...", "email": "..." }
}
```

**This endpoint is for third-party backends — not for you.** You just obtain and pass the token.

## Important Notes

- **5-minute TTL** — get a fresh token immediately before passing it; don't cache.
- **Requires active subscription** — returns 402 if on the free plan.
- **`/api/sso/verify/` is not for you** — that endpoint is for third-party backends. Calling it yourself serves no purpose.

## Full API Reference

For complete endpoint details: [SSO Token](https://ravi.id/docs/schema/sso.json)

## Related Skills

- **ravi-identity** — Get your email, phone, and identity name
- **ravi-login** — Authenticate yourself to Ravi
- **ravi-feedback** — Report SSO issues or suggest improvements
