# Telegram Mini App Security Checklist

Use this reference for manual review after `scripts/audit_tma.py` produces findings.

## Auth

- Client may read `window.Telegram.WebApp.initData`, but the backend must validate it.
- Server validation should parse the query string, build the data-check string without `hash`, derive the secret from the bot token, compare HMAC with constant-time comparison, and enforce auth freshness when possible.
- Dev bypass flags are acceptable only when disabled by default and named as insecure/local-only.

## Secrets

- Never commit real `TELEGRAM_BOT_TOKEN`, bot API URLs containing tokens, API keys, admin keys, ngrok tokens, or private tunnel credentials.
- If a token-like literal appears in a repo, treat it as leaked until proven fake and rotate real credentials.

## Admin Endpoints

- Admin endpoints must require server-side authorization.
- Client-side hidden admin UIs are not access control.
- Header keys are acceptable for MVP only when read from environment variables and never exposed in static assets.

## Network And Embedding

- Avoid wildcard CORS in production.
- Wildcard CORS with credentials is a blocker.
- Do not set `X-Frame-Options: DENY` or restrictive `frame-ancestors` for Telegram Mini Apps because Telegram must embed the app.
- Production Mini Apps need stable HTTPS URLs; tunnel URLs are suitable only for controlled demos.

## PII And Governance

- Minimize stored Telegram user data.
- Avoid collecting emails, phone numbers, handles, personal contacts, payment terms, or secrets unless the product explicitly requires them and has consent, storage, and retention rules.
- If governance requires link-free or contact-free outbound text, enforce it both client-side and server-side.

## Frontend Injection

- Prefer `textContent` and DOM node creation.
- If using `innerHTML`, ensure all user or fetched content is escaped or sanitized before injection.
- Markdown renderers need explicit escaping or a trusted sanitizer.

## Launch Gate

Before BotFather/channel changes:

1. Static audit has no `BLOCK` findings.
2. Browser QA confirms the Mini App loads on mobile-sized viewports.
3. Request submission works with valid Telegram `initData` or is intentionally dev-only.
4. Health endpoint passes.
5. Launch report captures URL, commit/path, env mode, screenshots, and rollback notes.
