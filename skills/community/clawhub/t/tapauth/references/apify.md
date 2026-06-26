# Apify via TapAuth

## Available Scopes

| Scope | Access |
|-------|--------|
| `full_api_access` | Full access to the Apify API (actors, runs, datasets, key-value stores, schedules) |

## Example: Run an Apify Actor

```bash
# 1. Get a token with full_api_access scope
scripts/tapauth.sh apify full_api_access

# 2. Run a web scraper actor
curl -X POST \
  -H "Authorization: Bearer $(scripts/tapauth.sh --token apify full_api_access)" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": [{"url": "https://example.com"}]}' \
  "https://api.apify.com/v2/acts/apify~web-scraper/runs?waitForFinish=60"
```

## Example: Get User Info

```bash
curl -H "Authorization: Bearer $(scripts/tapauth.sh --token apify full_api_access)" \
  "https://api.apify.com/v2/users/me"
```

## Gotchas

- **Dynamic Client Registration (DCR):** Apify uses OAuth 2.0 Dynamic Client Registration. TapAuth handles this automatically — no manual app setup needed.
- **PKCE required:** Apify enforces Proof Key for Code Exchange (PKCE) on all OAuth flows. TapAuth handles this automatically.
- **Token expiry:** Apify access tokens expire. TapAuth auto-refreshes using the refresh token when possible. If refresh fails, delete `.tapauth/` and re-run.
- **Rate limits:** Apify API rate limits vary by plan. Check `X-RateLimit-Remaining` headers. Free tier has lower limits.
- **Single scope:** Currently only `full_api_access` is available — there are no granular scopes.
- **API base URL:** All Apify API calls go to `https://api.apify.com/v2`.

## Recommended Minimum Scopes

| Use Case | Scopes |
|----------|--------|
| Run actors | `full_api_access` |
| Read datasets | `full_api_access` |
| Manage schedules | `full_api_access` |
| Get user info | `full_api_access` |
