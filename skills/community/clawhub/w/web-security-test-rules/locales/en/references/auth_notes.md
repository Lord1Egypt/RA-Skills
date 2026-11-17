# Authentication & Login Flow Notes (General)

> Companion to `SKILL.md` rules 2, 3, 10, 16.
> This file **contains no hardcoded credentials**. All tokens / accounts / API keys are provided by the authorizer and injected at runtime via env vars or local config.

---

## 1. Credential Management (rules 3, 10)

- **Source**: provided by the authorizer; forbidden to obtain from unauthorized channels such as public repos, logs, or frontend code.
- **Storage**: write to local env vars or config files (e.g. `.env`), **never into skill files, never commit to VCS**.
- **Verify before use**: before use, verify the key / token is still valid; if not, replace or prompt the authorizer (rule 10).
- **Nature check**: confirm whether the token is long-lived or short-lived / refresh-style, to avoid mid-test expiration being misjudged as a vulnerability.

### Recommended env var names (examples, adjust as needed)

```bash
export TARGET_BASE_URL="https://api.example.com"   # authorized target domain
export TEST_AUTH_TOKEN="<provided by authorizer>"   # Bearer Token
export TEST_USER_ID="<test account id designated by authorizer>"  # test account
```

### Typical request headers (placeholders, replace with real values)

```http
Authorization: Bearer ${TEST_AUTH_TOKEN}
x-user-id: ${TEST_USER_ID}
```

> Note: auth header field names differ across targets (some use `Authorization`, some custom headers, some put the user id outside the token). Capture traffic before testing to confirm the real fields.

---

## 2. Login / Captcha Flow Mapping (general method)

Before testing, **map the target's login chain first**, recording key endpoints and parameter-name differences. Common chain:

1. **Get captcha / challenge**: `GET /api/auth/captcha` → returns challenge token and required params.
2. **Verify challenge**: `POST /api/auth/captcha/verify` → params include challenge token, position / trajectory, etc.
   - ⚠️ Parameter names may differ from elsewhere (e.g. here it's `token`, at login it's `captcha_token`), **check endpoint by endpoint**.
3. **Login**: `POST /api/auth/login` → params include account, password, the prior verification credential, etc.
4. **Password-reset chain** (if applicable): send code → get new challenge → submit reset (incl. email / new password / code / challenge credential).

> Recording points: each endpoint's **real path, HTTP method, parameter names, return structure, whether a valid session is required first**. This is the basis for rules 15, 16 (frontend asset tracking, auth regression detection).

---

## 3. Rate Limiting & Lockout (rule 12)

- Most targets rate-limit per **IP + account**, **not globally**.
- A test IP being limited does not mean the target has a vulnerability, nor that the authorized account is invalid.
- **Stop after 1 login failure** (supplementary rule): first confirm whether credentials changed, don't brute-force continuously.
- Control request rate to avoid triggering alerts / limits / anomaly notifications (rule 12).

---

## 4. Auth Regression Detection (rule 16)

Each test re-verifies the auth state of known endpoints:

- Use an **unauthenticated bare request** to access an endpoint that "should require auth".
- If it originally required auth → now returns 200 / data, an **auth regression** occurred and must be reported as a vulnerability.
- Compare against the state recorded in the last report to confirm any change.

---

## 5. Test Account Constraints (rule 2)

- Only use the test accounts designated by the authorizer; record their identifiers (e.g. user id).
- Do not impersonate others' accounts, do not use real user data for destructive testing.
- IDOR tests follow the supplementary "test non-existent ID first → then others' ID → prefer GET/HEAD 403 confirmation" safety flow.
