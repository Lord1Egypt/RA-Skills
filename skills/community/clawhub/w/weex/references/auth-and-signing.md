# Auth and Signing (Compact)

REST base URL:
- `https://api-contract.weex.com`

Private headers:
- `ACCESS-KEY`
- `ACCESS-PASSPHRASE`
- `ACCESS-TIMESTAMP` (ms)
- `ACCESS-SIGN`

Signing message:
- no query: `timestamp + METHOD + requestPath + body`
- with query: `timestamp + METHOD + requestPath + "?" + queryString + body`

Signature:
- `Base64(HMAC_SHA256(secret, message))`

Env vars used by script:
- `WEEX_API_KEY`
- `WEEX_API_SECRET`
- `WEEX_API_PASSPHRASE`
- optional: `WEEX_API_BASE`, `WEEX_LOCALE`, `WEEX_API_TIMEOUT`

Credential source policy:
- env vars only
- if missing, fail fast and ask user to set env vars

Main reference:
- https://www.weex.com/api-doc/spot/QuickStart/Signature
