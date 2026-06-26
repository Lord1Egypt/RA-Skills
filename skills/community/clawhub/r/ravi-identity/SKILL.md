---
name: ravi-identity
description: Get your agent identity (email, phone, owner name) and manage identities. Do NOT use for reading messages (use ravi-inbox), sending email (use ravi-email-send), or credentials (use ravi-passwords or ravi-secrets).
---

# Ravi Identity

You have access to Ravi, an identity provider that gives you your own phone number, email address, and secret store.

## Your Identity

```bash
# Check auth status and current identity
ravi auth status

# Get your email address (use this for signups)
ravi get email

# Get your phone number (use this for SMS verification)
ravi get phone

# Get account owner info
ravi get owner

# List all your identities
ravi identity list
```

**Response shape (identity list):**
```json
[{
  "uuid": "...",
  "name": "Sarah Johnson",
  "inbox": "sarah.johnson472@raviapp.com",
  "phone": "+15551234567",
  "created_dt": "2026-02-25T10:30:00Z",
  "updated_dt": "2026-02-25T10:30:00Z"
}]
```

## Creating a New Identity

Only create a new identity when the user explicitly asks for one (e.g., for a separate project that needs its own email/phone). New identities require a paid plan.

```bash
# Auto-generated name and email (recommended — looks like a real person)
ravi identity create
# → name: "Sarah Johnson", inbox: "sarah.johnson472@raviapp.com"
```

When name is omitted, the server generates a realistic human name like "Sarah Johnson". The auto-generated email uses the same name: `sarah.johnson472@raviapp.com`.

## Switching Identities

```bash
# Switch to a different identity
ravi identity use <uuid>
```

## Important Notes

- **Identity name for forms** — use the identity name for signup forms, not the account owner's name.
- **Identities are permanent** — each identity has its own email, phone, and secrets. Don't create new identities unless the user asks.
- **Not authenticated?** — run `ravi auth login` to onboard.

## Full API Reference

For complete endpoint details, request/response schemas, and parameters: [Identities](https://ravi.id/docs/schema/identities.json)

## Related Skills

- **ravi-inbox** — Read SMS and email messages
- **ravi-email-send** — Compose, reply, forward emails
- **ravi-email-writing** — Write professional emails with proper formatting and tone
- **ravi-contacts** — Look up or manage contacts associated with this identity
- **ravi-passwords** — Store and retrieve website credentials
- **ravi-secrets** — Store and retrieve key-value secrets
- **ravi-login** — Device code onboarding, sign up for and log into services, handle 2FA/OTPs
- **ravi-feedback** — Send feedback, report bugs, request features
