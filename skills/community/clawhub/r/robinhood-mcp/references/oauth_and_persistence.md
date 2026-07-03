# OAuth & cross-session persistence

This document explains how `robinhood_mcp.py` authenticates to the Robinhood
Trading MCP server and how it keeps the user logged in across sessions.

## The MCP server

- URL: `https://agent.robinhood.com/mcp/trading` (override with
  `ROBINHOOD_MCP_URL`).
- Transport: **Streamable HTTP** (JSON-RPC over HTTP POST with SSE responses),
  handled by `mcp.client.streamable_http.streamablehttp_client`.
- Auth: **OAuth 2.0**, advertised by the server and driven by the MCP SDK's
  `OAuthClientProvider`. The agent never handles the user's Robinhood
  password; the user approves access in the browser plus a verification step
  in the Robinhood mobile app.

## The OAuth flow (handled by the SDK)

1. The first request returns `401` with a `WWW-Authenticate` header pointing at
   the protected-resource metadata.
2. The SDK discovers the **protected resource metadata** (RFC 9728) and then
   the **authorization server metadata** (RFC 8414).
3. **Dynamic Client Registration** (RFC 7591): the SDK registers a public
   client (`token_endpoint_auth_method = none`) with our redirect URI and
   stores the result in `client.json`.
4. **Authorization Code + PKCE**: the SDK builds an authorization URL. Our
   `redirect_handler` shows/opens it; the user approves; our
   `callback_handler` captures the `code` (via a loopback server, or pasted
   stdin in `--manual` mode).
5. The SDK exchanges the code for an **access token + refresh token**, stored
   in `credentials.json`.

All five steps happen inside the single `login` connection. `tools`, `status`,
and `call` skip straight to using/refreshing the stored tokens.

## Why login needs a human (once)

Step 4 requires interactive consent and a Robinhood mobile-app verification.
There is no way to complete the *initial* authorization unattended — that is
by design on Robinhood's side. Everything after that is silent.

## Cross-session silent refresh

The credentials live in `ROBINHOOD_MCP_HOME` (default
`~/.config/robinhood-mcp`). As long as that directory persists across
sessions, later sessions never prompt:

- `credentials.json` holds `access_token`, `refresh_token`, and an absolute
  `_expires_at` timestamp.
- On load, `FileTokenStorage.get_tokens()` checks `_expires_at`. If the access
  token is within `EXPIRY_SKEW_SECONDS` of expiry, it returns the token with
  the **access token blanked but the refresh token intact**. This is the key
  trick: the MCP SDK loads tokens from storage but does **not** restore the
  expiry clock across processes, so without this it would trust a stale access
  token, hit a `401`, and fall back to a full interactive re-auth. Blanking the
  access token steers the SDK into its silent `refresh_token` grant instead.
- When a refresh response omits a new `refresh_token`, the previous one is
  preserved so the chain doesn't break.

The only time a human is needed again is if the refresh token is revoked or
expires (e.g. the user revokes the agent in Robinhood, or it sits unused past
the server's refresh-token lifetime). Then `status` / `tools` / `call` return
`reauth_required` and the user must run `login` again.

## Making `ROBINHOOD_MCP_HOME` persistent

The skill cannot make storage durable by itself — the host must provide it:

- **Local desktop:** the default `~/.config/robinhood-mcp` already persists.
- **Containerized / remote agents:** point `ROBINHOOD_MCP_HOME` at a mounted
  volume or synced secret directory that outlives the ephemeral container, and
  run `login` once on a machine where a browser is reachable (or via
  `--manual`). Subsequent sessions mounting the same path refresh silently.

## File reference

| File              | Written by            | Sensitivity                          |
| ----------------- | --------------------- | ------------------------------------ |
| `client.json`     | DCR (step 3)          | Low (public client id/metadata).     |
| `credentials.json`| token exchange/refresh| **High** — grants trading access; `0600`. |

## Troubleshooting

| Symptom                                   | Cause / fix                                                        |
| ----------------------------------------- | ------------------------------------------------------------------ |
| `not_authenticated`                       | No `credentials.json`. Run `login`.                                |
| `reauth_required`                         | Refresh token revoked/expired. Run `login` again.                  |
| `connection_error: ... 401/403`           | Server rejected the request; if persistent, re-run `login`. A 403 with no creds usually means the network/IP is blocked from reaching Robinhood. |
| Login hangs in default mode               | Loopback port unreachable (remote host). Use `login --manual`.     |
| Each new session prompts for login        | `ROBINHOOD_MCP_HOME` is not persisted — point it at durable storage. |

## Environment variables

| Variable                     | Default                                      |
| ---------------------------- | -------------------------------------------- |
| `ROBINHOOD_MCP_HOME`         | `$XDG_CONFIG_HOME/robinhood-mcp` or `~/.config/robinhood-mcp` |
| `ROBINHOOD_MCP_URL`          | `https://agent.robinhood.com/mcp/trading`    |
| `ROBINHOOD_MCP_SCOPE`        | unset (server default)                       |
| `ROBINHOOD_MCP_REDIRECT_URI` | `http://localhost:8765/callback`             |
