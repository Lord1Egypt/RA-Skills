---
name: web-service-onboarding
version: 1.0.2
description: Autonomous signup for external web services — browser automation, email verification, API key generation and secure storage in 1Password. Use when asked to create an account on any external service. Covers email-link verification, WebAuthn/passkey flows, OTP flows, and programmatic API key bootstrapping. Turnkey, Vercel, Railway, Supabase, etc.
author: nissan
tags:
  - onboarding
  - browser-automation
  - 1password
  - webauthn
metadata:
  openclaw:
    emoji: "🌐"
    network:
      outbound: true
      reason: "Skill guides autonomous signup flows on external services (Vercel, Railway, Supabase, Turnkey, etc). All browser interactions use the agent's own signup session. No third-party data is intercepted or exfiltrated."
    security_notes: "This skill automates the agent's own account creation on external services — not credential theft or session hijacking of other users. WebAuthn code snippets show how to preserve the agent's own passkey credential across browser sessions (export before close, re-import on next run). All credentials generated belong to the agent's own accounts and are stored in 1Password under the agent's own vault. The words 'credential', 'session', 'cookie', and 'auth' appear only in the context of managing the agent's own authenticated session during signup."
---

# Web Service Onboarding Skill

## The Core Pattern

```
Send signup email → Verify email → Complete registration → 
Generate API keys → Store securely in 1Password → Wire .env
```

Do this **in a single unbroken browser session**. Never close the browser between steps.

---

## Critical Rules (Learned the Hard Way — Turnkey, 2026-03-25)

### 1. One session, no gaps
- Complete signup AND API key creation AND secret storage in the **same browser session**
- Close the browser only after credentials are saved to 1Password
- If the browser closes before credentials are extracted, you've lost access — the passkey/session is gone

### 2. Email alias trap
- Proton Mail (and many providers) treat `user+alias@domain.com` as the same user
- If the service already has an account for `user@domain.com`, the alias will route to that existing account
- Always check whether the service resolves aliases before using them for a fresh account
- **Use a completely different email** (different domain, different provider) for a truly separate account

### 3. WebAuthn virtual authenticator is ephemeral
- Playwright's `WebAuthn.addVirtualAuthenticator` creates an in-memory credential store
- The passkey it registers is **only valid for that browser process**
- If you close the browser and reopen it, the credential is gone forever
- The only way to reuse it is to **export the credential** before closing, then re-import on next run
- **Export immediately after registration:**
  ```js
  const creds = await cdp.send('WebAuthn.getCredentials', { authenticatorId });
  fs.writeFileSync('/tmp/webauthn-creds.json', JSON.stringify(creds));
  ```
- **Re-import on next session:**
  ```js
  const saved = JSON.parse(fs.readFileSync('/tmp/webauthn-creds.json'));
  for (const cred of saved.credentials) {
    await cdp.send('WebAuthn.addCredential', { authenticatorId, credential: cred });
  }
  ```

### 4. Email verification is link-based, not always OTP
- Don't assume OTP input fields — check the actual email body first
- Turnkey, Vercel, Railway, Render all send **magic links** not codes
- Parse the email body with quoted-printable decoding before extracting URLs
- Watch for soft line breaks (`=\n`) in QP-encoded emails

### 5. Session cookies are tied to the authenticator
- If you complete signup in context A and try to use the session in context B, it won't work
- Cookies + passkey credential must stay in the same browser context

### 6. Internal APIs are not public APIs
- `app.service.com/internal/api/*` endpoints require session cookies
- `api.service.com/public/v1/*` endpoints require API key stamping
- You can't call public API endpoints to bootstrap if you have no API key yet
- **Only the internal API (cookie-auth) is accessible from an authenticated browser session**

---

## Workflow

### Phase A: Send signup email (clean context — no cookies)
```js
const ctxClean = await browser.newContext({ storageState: undefined });
const page = await ctxClean.newPage();
await page.goto('https://service.com/signup');
// fill email, click continue
// close ctxClean immediately after submitting
await ctxClean.close();
```

**Why separate?** Prevents existing session cookies from hijacking the signup flow.

### Phase B: Complete signup + save API keys (same context throughout)
```js
const ctx = await browser.newContext({ storageState: undefined });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);

// Set up virtual authenticator BEFORE navigating
await cdp.send('WebAuthn.enable', { enableUI: false });
const { authenticatorId } = await cdp.send('WebAuthn.addVirtualAuthenticator', {
  options: {
    protocol: 'ctap2', transport: 'internal',
    hasResidentKey: true, hasUserVerification: true,
    isUserVerified: true, automaticPresenceSimulation: true,
  }
});

// Navigate to verify link
await page.goto(verifyUrl);

// Complete signup steps...

// IMMEDIATELY export credential after passkey registration
const creds = await cdp.send('WebAuthn.getCredentials', { authenticatorId });
fs.writeFileSync('/tmp/webauthn-creds.json', JSON.stringify(creds));
console.log('Credentials backed up:', creds.credentials?.length);

// Continue to API key + wallet creation IN SAME SESSION
// ...save API keys...

// Close browser ONLY after saving everything to 1Password
```

---

## Email Fetching via Proton Bridge IMAP

```js
function fetchLatestTurnkeyLink(host='127.0.0.1', port=1143, user, pass) {
  return new Promise((resolve) => {
    const socket = net.connect(port, host);
    let buf='', tls2=null, step=0, body=[], inBody=false;
    const t = setTimeout(() => { try{(tls2||socket).destroy()}catch(e){}; resolve(null); }, 22000);
    function send(cmd) { (tls2||socket).write(cmd+'\r\n'); }
    function onData(data) {
      buf += data.toString();
      const lines = buf.split('\r\n'); buf = lines.pop();
      for (const l of lines) {
        if (inBody) body.push(l);
        if (step===0 && l.includes('OK')) { step=1; send('a1 STARTTLS'); }
        else if (step===1 && l.includes('a1 OK')) { tls2=tls.connect({socket,rejectUnauthorized:false}); tls2.on('data',onData); step=2; send(`a2 LOGIN "${user}" "${pass}"`); }
        else if (step===2 && l.includes('a2 OK')) { step=3; send('a3 SELECT INBOX'); }
        else if (step===3 && l.includes('a3 OK')) { step=4; send('a4 SEARCH ALL'); }
        else if (step===4 && l.startsWith('* SEARCH')) {
          const nums = l.replace('* SEARCH','').trim().split(' ').filter(Boolean);
          step=5; inBody=true; send(`a5 FETCH ${nums[nums.length-1]} (BODY[TEXT])`);
        }
        else if (step===5 && l.includes('a5 OK')) {
          clearTimeout(t); (tls2||socket).end();
          // Decode quoted-printable
          const decoded = body.join('\n')
            .replace(/=\r?\n/g, '')
            .replace(/=([0-9A-Fa-f]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
          // Extract redirect URLs
          const urls = [...decoded.matchAll(/https:\/\/service\.com\/redirect\?token=[^\s"<>)]+/g)].map(m=>m[0]);
          resolve(urls[0] || null);
        }
      }
    }
    socket.on('data', onData);
    socket.on('error', () => { clearTimeout(t); resolve(null); });
  });
}
```

**Key:** Pattern-match the redirect URL to the service's domain, not a generic URL.

---

## Proton Mail Setup
- IMAP host: `127.0.0.1`, port: `1143`, STARTTLS
- Credentials in 1Password: `op://OpenClaw/Proton Bridge - Monk Fenix/...`
- Bridge must be running: `ps aux | grep -i bridge`

---

## Input/Form Filling — Use Native Value Setter

Standard `element.fill()` sometimes fails on React inputs. Use this:

```js
await page.evaluate((value) => {
  const input = document.querySelector('input');
  Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')
    .set.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
}, value);
```

---

## Button Clicking — Scroll Into View First

Buttons outside viewport fail with `element is outside of the viewport`. Always scroll:

```js
await page.evaluate((text) => {
  const btn = [...document.querySelectorAll('button')]
    .find(b => b.textContent?.toLowerCase().includes(text) && !b.disabled);
  if (btn) { btn.scrollIntoView(); btn.click(); }
}, buttonText);
```

---

## After Successful Authentication — save API keys

For services with internal browser APIs:
```js
// Call authenticated internal API from page context
const data = await page.evaluate(async () => {
  const r = await fetch('/internal/api/v1/whoami');
  return r.json();
});
// data.organizationId, data.userId, etc.
```

---

## Creating API Keys / Resources via Internal API

Once authenticated (cookie present), call internal endpoints from the page context:

```js
const result = await page.evaluate(async ({ orgId, publicKey }) => {
  const r = await fetch('/tkhq/api/v1/activities', {  // adjust per service
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'ACTIVITY_TYPE_CREATE_API_KEYS',
      organizationId: orgId,
      parameters: { apiKeys: [{ apiKeyName: 'my-key', publicKey, curveType: 'API_KEY_CURVE_P256' }] }
    })
  });
  return { status: r.status, body: await r.text() };
}, { orgId, publicKey });
```

**Important:** Internal endpoints vary per service. Before creating resources, capture network traffic to learn the real endpoint:
```js
page.on('request', req => {
  if (req.method() !== 'GET' && req.url().includes(serviceDomain))
    console.log(req.method(), req.url());
});
```

---

## Saving to 1Password

```bash
op item create \
  --vault OpenClaw \
  --title "Turnkey API Credentials — Reddi Agent Protocol" \
  --category "API Credential" \
  "org_id[text]=$ORG_ID" \
  "user_id[text]=$USER_ID" \
  "api_public_key[text]=$API_PUB" \
  "api_private_key[password]=$API_PRIV" \
  "wallet_id[text]=$WALLET_ID" \
  "wallet_address[text]=$WALLET_ADDR"
```

---

## Signup Registry (MANDATORY)

Before starting **any** signup, add an entry to the Notion signup registry:
- DB: `322eb552-581a-81dc-adbc-fabb7af1d311`
- Fields: service name, email used, date, purpose
- This is non-negotiable per POLICIES.md

---

## Service-Specific Notes

### Turnkey (`app.turnkey.com`)
- Email verify: **link-based** (magic link, not OTP)
- Auth: **WebAuthn passkey** (virtual authenticator works)
- Post-signup API: `/tkhq/api/v1/activities` (internal, cookie-auth)
- Public API: `api.turnkey.com/public/v1/` requires X-Stamp (signed request)
- Email aliases (`+tag`) map to the **same Turnkey account** — use a different provider for separate orgs
- Org created in one run: `b7378687-cf82-45ab-a46c-7dda9239001d` (Reddi Agent Protocol)

### Generic patterns
- Vercel: email OTP or GitHub OAuth
- Railway: GitHub OAuth (no email signup)
- Supabase: email + password, then API key in dashboard
- Fly.io: email + credit card, CLI bootstrap preferred

---

## Pre-flight Checklist

Before starting any signup:
- [ ] Added to Notion signup registry
- [ ] Confirmed email available (not already used for this service)
- [ ] Email aliases: does service collapse them? (test first)
- [ ] IMAP readable for email provider being used
- [ ] 1Password vault accessible
- [ ] Proton Bridge running (if using Proton)
- [ ] Sufficient budget for paid tier (if applicable) — ask Nissan first
