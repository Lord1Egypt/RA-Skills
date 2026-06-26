# Gotchas: TheHive + Cortex Deployment

## Cortex CSRF Protection (Biggest Automation Blocker)

Cortex uses Elastic4Play's custom CSRF filter. ALL POST/PUT/PATCH/DELETE requests with session cookies require a CSRF token.

**The mechanism:**
- Cookie name: `CORTEX-XSRF-TOKEN`
- Header name: `X-CORTEX-XSRF-TOKEN`

**How to get it:**
1. Login, get `CORTEX_SESSION` cookie
2. Make any GET request with session cookie
3. Response includes `Set-Cookie: CORTEX-XSRF-TOKEN=<token>`
4. Send token as BOTH cookie AND `X-CORTEX-XSRF-TOKEN` header

**Bypass:** After generating an API key, use `Authorization: Bearer <key>` which skips CSRF entirely.

**What does NOT work:**
- `Csrf-Token: nocheck`
- `X-CSRF-TOKEN` (standard Play header)
- Any other standard CSRF bypass header

## TheHive Password Change

- `PATCH /api/v1/user/<login>` returns 204 but **silently ignores** the password field
- **Correct endpoint:** `POST /api/v1/user/<login>/password/change`
- **Required body:** `{"currentPassword":"old","password":"new"}`

## Bash Exclamation Marks

- Passwords with `!` break curl JSON due to bash history expansion
- `-d '{"password":"Foo!"}'` causes parse errors
- **Fix:** Always use `printf '...' | curl -d @-`

## Cortex First-User Endpoint

- `POST /api/user` without authentication only works when zero users exist
- After the first user, all user creation requires auth + CSRF
- One-shot only. If it fails, the Cortex DB needs to be wiped

## TheHive Startup Delay

- TheHive waits 30s for Cassandra on startup
- Total boot time: 15-30s after `docker compose up`
- Poll `GET /api/status` instead of fixed sleeps

## TheHive Secret Length

- Play Framework JWT secret needs 32+ characters
- Shorter secrets cause silent config errors
- Generate with: `openssl rand -base64 32`

## Integration Key

- Use the Cortex **org admin** API key for TheHive-Cortex integration
- NOT the superadmin key (principle of least privilege)
