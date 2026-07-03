---
name: robinhood-mcp
description: Connect to Robinhood's Agentic Trading MCP server and act on the user's behalf — list account/positions tools, analyze a portfolio, and place trades via the official MCP. Handles OAuth once and persists tokens outside the session so future sessions re-authenticate silently. Use when the user wants their agent to read or trade their Robinhood account.
version: 0.1.0
emoji: 📈
homepage: https://robinhood.com/us/en/support/articles/agentic-trading-overview/
metadata:
  openclaw:
    requires:
      bins: [python3]
    envVars:
      ROBINHOOD_MCP_HOME:
        required: false
        description: >
          Directory where OAuth credentials are persisted. MUST point at storage
          that survives across sessions (a mounted volume / persistent home) so
          future sessions can refresh silently. Defaults to
          $XDG_CONFIG_HOME/robinhood-mcp or ~/.config/robinhood-mcp.
      ROBINHOOD_MCP_URL:
        required: false
        description: >
          Override the MCP server URL. Defaults to
          https://agent.robinhood.com/mcp/trading.
      ROBINHOOD_MCP_SCOPE:
        required: false
        description: Optional OAuth scope string, if Robinhood requires one for your account.
      ROBINHOOD_MCP_REDIRECT_URI:
        required: false
        description: >
          Loopback redirect URI used during interactive login. Defaults to
          http://localhost:8765/callback.
    install:
      uv:
        - mcp>=1.9.0
---

# Robinhood Agentic Trading (MCP)

This skill connects to **Robinhood's official Agentic Trading MCP server**
(`https://agent.robinhood.com/mcp/trading`, a remote Streamable-HTTP MCP
endpoint) and lets the agent use its tools on the user's behalf — reading
positions, analyzing the portfolio, and (when the user explicitly asks)
placing trades.

Authentication is **OAuth 2.0**, handled end-to-end by the MCP SDK
(discovery → dynamic client registration → authorization code + PKCE →
refresh tokens). The user's password is never seen by the agent.

The whole point of this skill: **the user authorizes once**, and the tokens
are written to a persistent directory so **every future session refreshes
silently** without user intervention.

> Robinhood's tools change as the beta evolves. Never assume tool names —
> always discover them with `tools` and read each tool's `inputSchema` before
> calling it.

## Requirements

- A primary Robinhood individual investing account in good standing, with an
  **Agentic account** opened (done once, on a desktop, in the Robinhood app —
  see the homepage link). Approving the agent requires a verification step in
  the Robinhood **mobile app**.
- `ROBINHOOD_MCP_HOME` pointing at **persistent** storage. If this directory
  is wiped between sessions, the user will have to log in again.

## Persistence model (read this)

| File                          | Contents                                              |
| ----------------------------- | ----------------------------------------------------- |
| `$ROBINHOOD_MCP_HOME/client.json`      | The dynamically-registered OAuth client.     |
| `$ROBINHOOD_MCP_HOME/credentials.json` | Access token, refresh token, expiry (0600).  |

On every non-`login` command the skill loads these, and if the access token
is expired it uses the **refresh token** to mint a new one silently. The user
is only re-prompted if the refresh token itself is revoked or expired.

Treat `credentials.json` as a secret — it grants trading access. The scripts
write it `0600` and never echo token values.

## First-time login

Run **once** per user. This is the only step that needs a human.

- **Local / desktop session (a browser is reachable):**

  ```bash
  python3 scripts/robinhood_mcp.py login
  ```

  The skill prints an authorization URL (and tries to open it), runs a local
  loopback server on `localhost:8765`, and captures the redirect automatically.

- **Remote / headless session (no local browser, e.g. cloud agent):**

  ```bash
  python3 scripts/robinhood_mcp.py login --manual
  ```

  The skill prints the authorization URL. Relay it to the user; they open it
  on their own desktop, approve (including the mobile-app verification), then
  copy the resulting `http://localhost:8765/callback?...` URL from their
  browser's address bar (it won't load — that's expected) and you feed it back
  on **stdin**:

  ```bash
  echo 'http://localhost:8765/callback?code=...&state=...' \
    | python3 scripts/robinhood_mcp.py login --manual
  ```

On success it prints `{"status": "authenticated", ...}` and the credentials
path. After this, the other commands work unattended.

## When to use

- "Connect my agent to Robinhood" / "Log my agent into Robinhood"
- "What's in my Robinhood portfolio?" / "Analyze my concentration risk"
- "Buy/sell N shares of TICKER on Robinhood" (after explicit confirmation)

## When NOT to use

- Market data, charting, or research that doesn't need the user's account —
  use a market-data source instead.
- Opening the Agentic account itself — that's a one-time manual step in the
  Robinhood app, not something this skill automates.
- Any broker other than Robinhood.

## Scripts

| Command                                   | Purpose                                            |
| ----------------------------------------- | -------------------------------------------------- |
| `robinhood_mcp.py login [--manual]`       | One-time interactive OAuth; persists tokens.       |
| `robinhood_mcp.py status`                 | Silent check that stored creds still work.         |
| `robinhood_mcp.py logout`                 | Delete stored credentials + client registration.   |
| `robinhood_mcp.py tools`                  | List the server's tools + JSON input schemas.      |
| `robinhood_mcp.py call <tool> [json]`     | Call a tool with JSON arguments.                   |

### Discover tools

```bash
python3 scripts/robinhood_mcp.py tools
```

Returns `{"tools": [{"name", "description", "inputSchema"}, ...]}`. Always read
the `inputSchema` for the tool you intend to call.

### Call a tool

Arguments are a JSON object, passed as the second argument or on stdin:

```bash
python3 scripts/robinhood_mcp.py call get_positions '{}'
# or
echo '{"symbol": "NVDA", "quantity": 1, "side": "buy"}' \
  | python3 scripts/robinhood_mcp.py call place_order
```

Output is the MCP `CallToolResult` as JSON: `content` blocks, optional
`structuredContent`, and `isError`. A tool-level error sets `isError: true`
and exits non-zero — surface the message to the user; do not blindly retry.

### Verify / re-auth

```bash
python3 scripts/robinhood_mcp.py status
```

Exit codes: `0` authenticated; `2` re-auth required (`reauth_required` or
`not_authenticated` → run `login` again); `1` other connection/tool error.
Errors are emitted as `{"error": ..., "message": ...}` JSON.

## Safety

- **Trades move real money.** Before any order-placing tool call, confirm the
  symbol, side, quantity, order type, and an estimated cost with the user, and
  get explicit go-ahead. Never place or modify orders speculatively.
- Prefer read-only tools (positions, balances, analysis) unless the user has
  clearly asked to trade.
- Never print or log `credentials.json` contents or token values.
- If `status` reports `reauth_required`, stop and ask the user to run `login`
  — do not attempt to work around the auth.

## References

See [`references/oauth_and_persistence.md`](references/oauth_and_persistence.md)
for how the OAuth flow and cross-session token persistence work, and how to
troubleshoot auth problems.
