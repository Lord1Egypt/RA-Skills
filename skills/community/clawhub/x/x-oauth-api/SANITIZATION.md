# Sanitization Log

Changes made to prepare `x-oauth-api` for public ClawHub release.

## Removed Files

| File | Reason |
|------|--------|
| `clawbot-persona.md` | Account-specific persona (brand voice, handle, content templates) |
| `clawbot-post.sh` | Hardcoded persona content, account-specific URLs and branding |
| `.clawhub/origin.json` | Contains publisher `ownerId` |

## Renamed / Rewritten Files

| Original | New | Changes |
|----------|-----|---------|
| `clawbot-post.sh` | `generic-post.sh` | Removed all persona content; generic template with customizable `get_content()` function; configurable via env vars |
| `heartbeat.sh` | `heartbeat.sh` | Replaced `rate-limits` check (not a valid command) with `me` connectivity check; generic state paths |
| `_meta.json` | `_meta.json` | Removed `ownerId` and `publishedAt` |

## Identifying Information Removed

- **User names**: Neal, ClawBot, OpenClawKit — all removed
- **Twitter handle**: `@OpenClawKit` — removed from all files
- **Hardcoded paths**: `/Users/nealme/clawd`, `$HOME/.openclaw/clawbot/` — replaced with `${OPENCLAW_STATE_DIR:-$HOME/.openclaw/x-poster}`
- **Product URLs**: `https://openclawkit.ai` — removed from tweet templates
- **Publisher ID**: `ownerId` in `_meta.json` — removed
- **Persona content**: Entire ClawBot persona (voice guidelines, signature phrases, content templates) — removed

## Security Audit

- ✅ `bin/x.js` — No hardcoded credentials; reads from env vars only
- ✅ `generic-post.sh` — No hardcoded paths or credentials; uses env vars
- ✅ `heartbeat.sh` — No hardcoded paths or credentials; uses env vars
- ✅ No `.env` files included
- ✅ No secrets in any committed file
- ✅ OAuth flow is generic (works for any X Developer App)

## Files Unchanged

- `bin/x.js` — Already generic (env-based auth, no account-specific logic)
- `package.json` — Already generic
- `package-lock.json` — Dependency lockfile, no sensitive data

## Added Files

- `LICENSE` — MIT license
- `SANITIZATION.md` — This file
