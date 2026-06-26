# Error Handling

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Parse JSON response |
| 400 | Bad request | Check inputs, model name |
| 401 | Invalid API key | Run `auth.mjs trial` or `auth.mjs login` |
| 429 | Rate limited | Wait and retry (check `Retry-After` header) |
| 500 | Server error | Retry after a few seconds |

## Balance Warnings

API responses may include a `_balance_warning` field. Relay this to the user exactly as provided.

Check balance: `auth.mjs status`
Add credits: https://www.skillboss.co

## Retry Strategy

For 429 responses, wait for the `Retry-After` header value (in seconds) before retrying.
For network errors, retry up to 3 times with exponential backoff (1s, 2s, 4s).
Do not retry 400 or 401 errors — fix the request instead.
