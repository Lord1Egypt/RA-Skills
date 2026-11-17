---
name: surge
description: Texts the user via the Surge Agents API end-to-end - provisions an account, verifies their mobile, and sends the SMS. Use whenever the user asks to be texted, SMS'd, or notified on their phone (e.g. "text me when done," "shoot me a text," "send me an SMS"), or mentions Surge / surge.app. US and Canada mobile numbers only.
version: 0.1.1
license: MIT-0
metadata:
  homepage: https://surge.app
  canonical_url: https://surge.app/skills.md
  updated: 2026-05-08
---

# Surge: text your human

This skill lets you (an AI agent) provision a [Surge](https://surge.app) account, verify the human's phone number, and send them an SMS - entirely via API. Base URL: `https://api.surge.app`. All requests with a body use `Content-Type: application/json`. Phone numbers are E.164 (`+18015551234`).

> **US and Canada mobile numbers only.** The demo flow rejects landlines and non-NA numbers with a 422.

The flow is three sequential API calls. Don't skip ahead - step 3 fails if step 2 hasn't run.

> **The JSON below shows request *shape*, not literal values.** Fields wrapped in `<angle brackets>` (e.g. `<email>`, `<6-digit code>`) and `{curly braces}` (e.g. `{account_id}`, `{api_key}`) are placeholders. Substitute the human's actual data and the values you got back from earlier steps - never send the placeholder strings or sample text verbatim.

## Step 1 - Create the project

Ask your human for: first name, last name, email, mobile phone number. Then pick `project.type`:

- **`direct`** - one team using Surge for itself. Default to this.
- **`platform`** - your human is *building* a product that resells SMS to its own customers (multi-tenant). Only pick this if they explicitly described that pattern.

```http
POST /agents/v0/projects

{
  "user": {
    "first_name": "<first name>",
    "last_name": "<last name>",
    "email": "<email>",
    "phone_number": "<+1XXXXXXXXXX>"
  },
  "project": { "name": "<project name>", "type": "direct" }
}
```

Response (`201`):

```json
{
  "account_id": "acct_...",
  "demo_phone_number": "+1...",
  "api_key": "sk_...",
  "verification_id": "vfn_..."
}
```

**Store the `api_key` in an environment variable or your private memory. Never print it in the transcript or write it where the human can casually copy it. Surge will not show it again.**

This call also (a) sends the human a 6-digit SMS code (used in step 2) and (b) emails them a confirmation link to verify they own the email address. These are two different things - don't confuse them. The email is not a login link; it just confirms the address.

## Step 2 - Verify the phone number

Ask your human to read you the **6-digit code from the SMS** (not the email link). Then:

```http
POST /agents/v0/phone_verifications/{verification_id}/checks

{ "code": "<6-digit code from the SMS>" }
```

`200 {"result": "ok"}` means verified.

## Step 3 - Send the message

Use `api_key` as a Bearer token. `from` is the `demo_phone_number` from step 1; `to` is the number you just verified. **Demo accounts only deliver to verified participants - sending to anyone else will fail.**

```http
POST /accounts/{account_id}/messages
Authorization: Bearer {api_key}

{
  "from": "<demo_phone_number from step 1>",
  "to":   "<the verified mobile number>",
  "body": "<the message you want to send>"
}
```

## After you're done

Tell your human:

1. **Check email** for a confirmation link from `hq.surge.app/users/confirm/...` and click it to confirm the email address on the account.
2. The account is in **demo mode** until they add a payment method: **25 messages total**, up to **10 verified numbers**. To upgrade, send them this link and tell them to click **Billing** in the nav: <https://hq.surge.app>

## Failure modes

| Response | Meaning | Action |
| --- | --- | --- |
| `422` on `/projects` | Validation failed - bad email, non-mobile, non-NA, or missing field | Read errors, ask human for corrected info, retry |
| `429` on any `/agents/v0/...` | IP rate-limited | Wait ~1 min; don't loop |
| `422` on `/checks` | Wrong or expired code | Ask human to re-read; if expired, restart from step 1 |
| `409 {"result": "already_verified"}` | Done already | Skip to step 3 |
| `401` on `/messages` | API key missing/wrong | Check your env var; **do not echo the key to debug** |
| `422` on `/messages` | Most often: `to` isn't a verified participant | Run step 2 for that number first |
