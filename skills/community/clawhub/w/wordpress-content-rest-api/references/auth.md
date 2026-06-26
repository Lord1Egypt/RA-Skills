# Auth Setup

Use HTTPS only.

## 1) Application Password (Preferred for service-to-service)

Use WordPress username + application password via Basic auth.

Example:
```bash
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_SITE/wp-json/wp/v2/posts?per_page=5"
```

Rules:
- Use an account with minimum required capabilities.
- Rotate/revoke app passwords after incidents or role changes.
- Never log raw credentials.

## 2) Bearer Token (Site/plugin specific)

Use only when the site explicitly supports bearer auth (JWT/OAuth/custom gateway).

Example:
```bash
curl -sS -H "Authorization: Bearer $WP_BEARER_TOKEN" \
  "$WP_SITE/wp-json/wp/v2/pages?per_page=5"
```

Rules:
- Validate token issuer and expiry.
- Keep scopes narrow.
- Prefer short-lived tokens.

## Auth Selection

- Use Application Password by default.
- Use Bearer only when required by site policy or existing integration architecture.

## Preflight Check

Before writes:
1. Call a read endpoint (`/posts` or `/pages`).
2. Confirm auth works and returns expected visibility.
3. Confirm you are on the intended site URL.
