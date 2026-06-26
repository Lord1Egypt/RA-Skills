---
name: ravi-login
description: Sign up for and log into services using your Ravi identity — handles onboarding, forms, 2FA, OTPs, and credential storage. Do NOT use for standalone inbox reading (use ravi-inbox) or email sending (use ravi-email-send).
---

# Ravi Login

End-to-end workflows for onboarding to Ravi, signing up for services, logging in, and completing verification using your Ravi identity.

## Step 0: Check Auth Status

Before doing anything, check whether you're already authenticated:

```bash
ravi auth status
```

If authenticated, skip to [Sign up for a service](#sign-up-for-a-service).

---

## Step 1: Onboard to Ravi

If you're not authenticated, run the login flow. This is a one-time setup — the CLI handles the device code flow, polls for authorization, and stores keys automatically.

```bash
ravi auth login
```

The CLI will:
1. Initiate a device code flow
2. Display a URL and code for the human to visit
3. Poll until the human approves
4. Store all keys in `~/.ravi/config.json`

Present the URL and code clearly to the human:

```
Please visit https://ravi.id/device and enter the code: ABCD-1234
```

The human visits the URL, signs in with Google, and approves the request.

---

## Step 2: Select Identity (Returning Users)

If you have multiple identities, list and switch between them:

```bash
# List all identities
ravi identity list

# Switch to a specific identity
ravi identity use <uuid>
```

---

## Step 3: Create an Identity (if needed)

If you have no identities, create one:

```bash
ravi identity create
```

The server auto-generates a realistic human name (e.g. "Sarah Johnson") and matching email.

---

## Sign up for a service

```bash
# 1. Get your identity details
EMAIL=$(ravi get email)
PHONE=$(ravi get phone)
NAME=$(ravi auth status | jq -r '.name')
FIRST_NAME=$(echo "$NAME" | awk '{print $1}')
LAST_NAME=$(echo "$NAME" | awk '{print $2}')

# 2. Fill the signup form with $EMAIL, $PHONE, $FIRST_NAME, $LAST_NAME

# 3. Generate and store a password during signup
CREDS=$(ravi passwords create example.com --username "$EMAIL")
PASSWORD=$(echo "$CREDS" | jq -r '.password')
# Use $PASSWORD in the signup form

# 4. Wait for verification
sleep 5
ravi inbox sms    # Check for SMS OTP
ravi inbox email  # Check for email verification
```

## Your Name

When a form asks for your name, use your **identity name** — not the account owner's name. Identity names look like real human names (e.g. "Sarah Johnson").

```bash
ravi auth status
# → Returns identity name, email, phone
```

> **Note:** The first/last split works for auto-generated names (e.g. "Sarah Johnson"). For custom names (e.g. "Shopping Agent"), use the full name as-is or adapt the split to the form's requirements.

**Never** use the account owner's name for form fields. The identity name is *your* name.

## Log into a service

```bash
# Find stored credentials by domain
CREDS=$(ravi passwords list | jq -r '.[] | select(.domain == "example.com")')
UUID=$(echo "$CREDS" | jq -r '.uuid')

# Get full credentials including password
CREDS=$(ravi passwords get "$UUID")
USERNAME=$(echo "$CREDS" | jq -r '.username')
PASSWORD=$(echo "$CREDS" | jq -r '.password')
# Use $USERNAME and $PASSWORD to log in
```

## Complete 2FA / OTP

```bash
# After triggering 2FA on a website:
sleep 5
CODE=$(ravi inbox sms | jq -r '.[].preview' | grep -oE '[0-9]{4,8}' | head -1)
# Use $CODE to complete the login
```

## Extract a verification link from email

```bash
THREAD_ID=$(ravi inbox email | jq -r '.[0].thread_id')

ravi inbox email "$THREAD_ID" | jq -r '.messages[].text_content' | grep -oE 'https?://[^ ]+'
```

## Tips

- **Poll, don't rush** — SMS/email delivery takes 2-10 seconds. Use `sleep 5` before checking.
- **Store credentials immediately** — create a passwords entry during signup so you don't lose the password.
- **Identity name for forms** — always use the identity name, not the owner name.
- **Rate limits apply to sending** — 60 emails/hour, 500/day. See `ravi-email-send` skill for details.
- **Email quality matters** — if you need to send an email during a workflow, see **ravi-email-writing** for formatting and anti-spam tips.

## Full API Reference

For complete endpoint details, request/response schemas, and parameters: [Device Auth](https://ravi.id/docs/schema/device-auth.json) | [Auth & Keys](https://ravi.id/docs/schema/auth.json)

## Related Skills

- **ravi-identity** — Get your email, phone, and identity name for form fields
- **ravi-inbox** — Read OTPs, verification codes, and confirmation emails
- **ravi-email-send** — Send emails during workflows (support requests, confirmations)
- **ravi-email-writing** — Write professional emails that avoid spam filters
- **ravi-passwords** — Store and retrieve website credentials after signup
- **ravi-secrets** — Store API keys obtained during service registration
- **ravi-sso** — Prove your Ravi identity to third-party services via short-lived tokens
- **ravi-feedback** — Report login flow issues or suggest workflow improvements
