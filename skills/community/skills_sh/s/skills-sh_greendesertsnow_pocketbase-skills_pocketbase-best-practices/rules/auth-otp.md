---
title: Use authWithOTP for Email One-Time Codes, Rate-Limit requestOTP
impact: HIGH
impactDescription: OTP endpoints are unauthenticated; unthrottled requestOTP enables email bombing and enumeration
tags: auth, otp, one-time-password, rate-limiting, enumeration
---

## Use authWithOTP for Email One-Time Codes, Rate-Limit requestOTP

Auth collections can enable **OTP login** from the admin UI (Collection → Options → "Enable OTP"). The client flow is two steps: `requestOTP(email)` returns an `otpId`, then `authWithOTP(otpId, code)` exchanges the id + code for an auth token. Two things trip people up: (1) the OTP response is **the same whether the email exists or not** - do not break that by leaking a distinct error; (2) `requestOTP` sends an email, so **it must be rate-limited** or an attacker can use it to spam any address.

**Incorrect (leaks existence, custom requestOTP with no rate limit):**

```javascript
// ❌ Client-side existence check - ignore the 404 and expose it to the user
try {
    await pb.collection("users").getFirstListItem(`email="${email}"`);
} catch (e) {
    alert("No account with that email"); // ❌ account enumeration
    return;
}

// ❌ Ad-hoc route with no rate limit - attacker hammers this to spam mailboxes
routerAdd("POST", "/api/myapp/otp", (e) => {
    const body = e.requestInfo().body;
    const user = $app.findAuthRecordByEmail("users", body.email);
    // send custom email...
    return e.json(200, { ok: true });
});
```

**Correct (use the built-in flow, step 1 always returns an otpId):**

```javascript
// Step 1: request the code. Always returns { otpId } - even if the email
// does not exist, PocketBase returns a synthetic id so enumeration is
// impossible. Treat every response as success from the UI perspective.
const { otpId } = await pb.collection("users").requestOTP("user@example.com");

// Step 2: exchange otpId + the 8-digit code the user typed
const authData = await pb.collection("users").authWithOTP(
    otpId,
    "12345678",
);
// pb.authStore is now populated
```

```go
// Go side - rate-limit and log if you wrap your own endpoint
app.OnRecordRequestOTPRequest("users").BindFunc(func(e *core.RecordRequestOTPRequestEvent) error {
    // e.Collection, e.Record (may be nil - synthetic id path),
    // e.Email (always present), e.Password (unused for OTP)
    e.App.Logger().Info("otp requested",
        "email", e.Email,
        "ip",    e.RequestInfo.Headers["x_forwarded_for"])
    return e.Next() // REQUIRED
})
```

**Rules:**
- `requestOTP` **always returns 200 with an otpId**, even for non-existent emails - preserve that by never adding a pre-check or a different error path.
- Enable the built-in rate limiter (see `deploy-rate-limiting.md`) and raise the cost for the `*:requestOTP` label. Without this, an attacker can email-bomb arbitrary users.
- The OTP code is 8 digits by default, with a 3-minute TTL. Do not extend the TTL - short windows are the whole point.
- `authWithOTP` consumes the code; a successful call invalidates the `otpId`. Always show a generic "invalid or expired code" on failure.
- If you want OTP **without a password**, set the collection's `Password` option to off and `OTP` on. If both are enabled, users can use either.
- OTP emails are sent via the configured SMTP server. In dev, point SMTP at Mailpit or a console logger before testing - do **not** ship with the default "no-reply@example.com" sender.

Reference: [Auth with OTP](https://pocketbase.io/docs/authentication/#auth-with-otp) · [JS SDK - authWithOTP](https://github.com/pocketbase/js-sdk#authwithotp)
