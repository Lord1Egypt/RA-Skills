# Optional local env file example

Prefer user environment variables for real secrets.

Use a local env file only if you explicitly want file-based storage, for example in your OpenClaw home directory:

- `~/.openclaw/raindrop.env`

Example variables to create in the Windows user environment:

- `RAINDROP_CLIENT_ID` -> your client id
- `RAINDROP_CLIENT_SECRET` -> your client secret
- `RAINDROP_ACCESS_TOKEN` -> your test or OAuth access token
- `RAINDROP_REFRESH_TOKEN` -> optional refresh token
- `RAINDROP_REDIRECT_URI` -> `http://127.0.0.1:8765/callback`

Notes:
- `RAINDROP_ACCESS_TOKEN` can be a long-lived **test token** for local use.
- `RAINDROP_REFRESH_TOKEN` is optional unless you use full OAuth exchange/refresh.
- The skill supports `auth-start`, `auth-finish`, and `refresh-token` commands for OAuth flows.
- The published skill should not contain real secrets.
- Do not paste actual key or token values into the skill files, screenshots, or published examples.
- Prefer user environment variables over files.
- Override the env path with `RAINDROP_ENV_FILE` only if needed.
