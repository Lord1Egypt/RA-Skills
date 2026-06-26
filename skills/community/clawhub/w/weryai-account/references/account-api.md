# WeryAI Account API

Use this file when you need the exact public contract for the official WeryAI account endpoint.

## Balance Query

- Endpoint: `GET /v1/generation/balance`
- Auth: `Authorization: Bearer <WERYAI_API_KEY>`
- Purpose: get the current credits balance for the API account

## Success Shape

```json
{
  "status": 0,
  "desc": "success",
  "message": "success",
  "data": 1000
}
```

Notes:

- `data` is the credits balance
- business success can appear as `status: 0` or `status: 200`
- this endpoint is read-only and does not create a task
- if the balance is `0`, the caller may guide the user to recharge at `https://www.weryai.com/api/pricing`

## Failure Shape

Typical auth failure:

```json
{
  "status": 1002,
  "desc": "Authentication failed",
  "message": "Invalid API Key"
}
```

## Guidance Rules

- Treat `WERYAI_API_KEY` as the only runtime secret.
- Keep the key in the runtime environment, never in repository files.
- Use this skill for account balance and credits questions, not for image, video, music, or effect generation.
