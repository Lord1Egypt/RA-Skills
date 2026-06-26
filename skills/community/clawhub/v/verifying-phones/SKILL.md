---
name: verifying-phones
description: Verifies phone numbers via SMS OTP using the Sendly Verify API. Sends codes, checks codes, handles expiry, and provides hosted verification sessions. Applies for phone verification, OTP, 2FA, or passwordless login flows.
---

# Phone Verification with Sendly

## Quick start

```typescript
import Sendly from "@sendly/node";

const sendly = new Sendly(process.env.SENDLY_API_KEY!);

const verification = await sendly.verify.send({ to: "+15551234567" });
console.log(verification.id); // ver_abc123

const result = await sendly.verify.check(verification.id, { code: "123456" });
console.log(result.status); // "verified" | "failed" | "expired"
```

## REST API

**Base URL:** `https://sendly.live/api/v1`

### Send OTP

```bash
curl -X POST https://sendly.live/api/v1/verify \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "+15551234567", "app_name": "MyApp", "code_length": 6, "timeout_secs": 300}'
```

**Required:** `to` (E.164 format)

**Optional:** `app_name` (shown in SMS), `code_length` (4–10, default 6), `timeout_secs` (default 300)

**Response:**
```json
{
  "id": "ver_abc123",
  "status": "pending",
  "phone": "+15551234567",
  "expires_at": "2026-04-01T10:05:00Z"
}
```

In sandbox mode (`sk_test_*` keys), the response includes `sandbox_code` with the actual code.

### Check code

```bash
curl -X POST https://sendly.live/api/v1/verify/ver_abc123/check \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'
```

**Statuses:** `verified`, `failed` (wrong code), `expired`, `max_attempts_exceeded` (3 attempts max)

### Resend OTP

```bash
curl -X POST https://sendly.live/api/v1/verify/ver_abc123/resend \
  -H "Authorization: Bearer $SENDLY_API_KEY"
```

### Hosted verification sessions

Zero-code verification UI hosted by Sendly:

```bash
curl -X POST https://sendly.live/api/v1/verify/sessions \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"success_url": "https://yourapp.com/verified?token={TOKEN}", "brand_name": "MyApp"}'
```

Returns a `url` the user visits. After verification, redirects to `success_url` with a token. Validate the token server-side:

```bash
curl -X POST https://sendly.live/api/v1/verify/sessions/validate \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"token": "tok_from_redirect"}'
```

## Node.js SDK

```typescript
import Sendly from "@sendly/node";
const sendly = new Sendly(process.env.SENDLY_API_KEY!);

const v = await sendly.verify.send({ to: "+15551234567", appName: "MyApp" });
const check = await sendly.verify.check(v.id, { code: "123456" });
const resend = await sendly.verify.resend(v.id);
const session = await sendly.verify.sessions.create({ successUrl: "https://app.com/done?token={TOKEN}", brandName: "MyApp" });
const validated = await sendly.verify.sessions.validate({ token: "tok_xxx" });
```

## Error handling

| Error | Meaning | Action |
|---|---|---|
| `invalid_phone_number` | Not E.164 format | Format as +{country}{number} |
| `verification_expired` | Code timed out | Call resend or start new verification |
| `max_attempts_exceeded` | 3 wrong codes | Start new verification |
| `rate_limit_exceeded` | Too many requests | Wait and retry |

## Sandbox testing

With `sk_test_*` keys, the `sandbox_code` field in the send response contains the code. No real SMS is sent. OTP to +15005550000 always works.

## Full reference

- Verify API docs: https://sendly.live/docs/verify
- OTP tutorial: https://sendly.live/docs/tutorials/otp
- Error handling guide: https://sendly.live/docs/how-to/handle-otp-errors
