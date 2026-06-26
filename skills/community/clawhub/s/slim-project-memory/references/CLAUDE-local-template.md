# Local Environment Reference (NOT in git)

> **⚠️ SECURITY BEST PRACTICE:** This file records *where* each environment lives and *which env var names* it uses — it should NOT contain inline secret values.
>
> **Secrets belong in environment variables** (`.env`, Railway Dashboard, Vercel Environment Variables, etc.), not in project files. Reference the env var name here so the agent knows what to use:
>
> ```bash
> DATABASE_URL="$STAGING_DB_URL"  # ← reference the env var name, not the value
> ```
>
> If you must document a specific credential value for a debugging or setup workflow, set a short-lived, read-only, staging-only token and rotate it after the session. Never embed production admin tokens in any file.

---

## Environment quick-reference — read this BEFORE any DB or hosting operation

| Branch | Env name | URL | Hosting service |
|--------|----------|-----|-----------------|
{{#BRANCHES}}
| {{branch}} | {{env}} | {{url}} | {{service_name}} |
{{/BRANCHES}}

**Hard rules:**
- Default deploy/operation target is **{{DEFAULT_BRANCH}}**. Other environments require explicit user approval *in the current turn*. Approval for one action does not extend to others.
- Production has live customer data. Read-only by default. Any write must be explicitly authorized in the current turn.

---

{{#FOR_EACH_ENVIRONMENT}}

## {{env_name}}

- **URL**: {{url}}
- **Branch**: `{{branch}}`
- **Hosting service**: `{{service_name}}`
- **DB**: `${{ENV_PREFIX}}_DATABASE_URL` <!-- ← set as Railway/Vercel env var, not inline -->
{{#HAS_REDIS}}
- **Redis**: `${{ENV_PREFIX}}_REDIS_URL`
{{/HAS_REDIS}}
{{#HAS_OTHER_SERVICES}}
- **{{service_name}}**: `${{ENV_PREFIX}}_{{SERVICE_KEY}}_URL`
{{/HAS_OTHER_SERVICES}}

{{/FOR_EACH_ENVIRONMENT}}

---

## Local development

| Service | URL | Notes |
|---------|-----|-------|
| App | http://localhost:3000 | <stack> |

`DATABASE_URL` for local dev comes from `.env` or `docker-compose`, not from this file.

---

## Run migrations against a remote env

```bash
# Reference env vars set in Railway/Vercel, not inline values:
DATABASE_URL="$STAGING_DATABASE_URL" npx prisma migrate deploy
```

---

## API keys and external services — env var references only

| Service | Env var | Notes |
|---------|---------|-------|
<!--
  List env var NAMES here (not values), e.g.:
  | Anthropic | ANTHROPIC_API_KEY | Set in Railway dashboard |
  | Stripe | STRIPE_SECRET_KEY | Test mode only |
  Never paste actual key values.
-->

---

## Other infrastructure

| Service | URL | Notes |
|---------|-----|-------|
<!-- Helpdesk, analytics, admin dashboards — public URLs only, no secrets -->

---

## When you change anything in this file

This file is gitignored, so updates leave no trace in `git log`. When you add a new env var reference, update a URL, or rotate a credential (which happens in the hosting dashboard, not here), **mention it in the session recap**. Example: `Updated CLAUDE.local.md: rotated staging DB password via Railway dashboard.`
