---
name: robinhood-agentic
description: Connect to Robinhood Agentic Trading via MCP — view portfolio, analyze positions, place trades, and execute automated strategies through Robinhood's official MCP server.
metadata:
  author: github.com/LeoSaucedo
  version: "1.0.0"
---

# Robinhood Agentic Trading

Connect to Robinhood Agentic Trading via MCP. This skill lets OpenClaw access your Robinhood Agentic account — view portfolio, analyze positions, place trades, and execute automated strategies.

## Setup

The MCP client (`rh-client.mjs`) handles OAuth 2.1 PKCE authentication to `https://agent.robinhood.com/mcp/trading` and manages token storage/refresh automatically.

### Prerequisites

1. Robinhood Agentic access (still rolling out — you'll get an email)
2. A dedicated Agentic account (created during OAuth flow)
3. Node.js ≥ 18

### Install Dependencies

```
cd robinhood-agentic
pnpm install
```

### First-time Auth

```
node rh-client.mjs auth
```

The script will:
1. Discover Robinhood's OAuth endpoints
2. Generate a PKCE challenge
3. Print an authorization URL → **Open this in a desktop browser** (mobile redirects to the Robinhood app which doesn't support the Agentic flow)
4. Log into Robinhood, authorize the agent
5. You'll be redirected to `http://localhost:1455/callback?code=XXXX...`
6. **Copy the full redirect URL and paste it** back into the terminal
7. Tokens are stored in `.rh-tokens.json` (gitignored, mode 0600)

## Usage

All commands output to stdout. Errors and status messages go to stderr.

### Check auth status
```
node rh-client.mjs status
```
Returns a JSON object with `authenticated`, `expired`, `expiresAt`, `hasRefreshToken`, and `savedAt`.

### List available MCP tools
```
node rh-client.mjs list-tools
```
Returns a JSON array of tool definitions with names, descriptions, and input schemas.

### Call a tool
```
node rh-client.mjs call <tool_name> '<json_args>'

# Or with stdin for complex args:
echo '{"symbol": "AAPL"}' | node rh-client.mjs call get_equity_quotes -
```
Output depends on the MCP tool response — may be plain text or JSON. Error messages go to stderr.

### Refresh token (auto)
Token refresh happens automatically when the access token is within 5 minutes of expiry (only if a refresh token is available). No manual intervention needed unless the refresh token itself expires.

## What OpenClaw Can Do

After auth, OpenClaw can call any tool Robinhood exposes through the MCP server. Based on official docs, the available tools are:

> **Read-only tools** (portfolio, positions, quotes, etc.) work on **all** your Robinhood accounts. **Trading tools** (place/cancel orders) are restricted to the dedicated Agentic account — fund it separately.

### Account & Portfolio

| Tool | Description |
|------|-------------|
| `get_accounts` | View all Robinhood accounts |
| `get_portfolio` | Portfolio snapshot — total value, asset class breakdown, buying power |
| `get_equity_positions` | Open equity positions with quantity and cost basis |

### Market Data

| Tool | Description |
|------|-------------|
| `get_equity_quotes` | Real-time quotes + prior close for up to 20 symbols |
| `search` | Find ticker by company name |
| `get_equity_tradability` | Check if a symbol can be traded (including fractional) |

### Orders

| Tool | Description |
|------|-------------|
| `review_equity_order` | Simulate an order and get pre-trade warnings |
| `place_equity_order` | Place an equity order |
| `cancel_equity_order` | Cancel an open equity order |
| `get_equity_orders` | View equity order history |

Use `list-tools` after auth to discover the exact API surface — Robinhood is actively adding more tools.

For the latest tool list, see [Robinhood's official docs](https://robinhood.com/us/en/support/articles/trading-with-your-agent/).

## Security Notes

- **Separate account**: The Agentic account is separate from your main Robinhood account — fund it with what you're comfortable with the agent managing
- **Tokens stored locally**: OAuth tokens in `.rh-tokens.json` with restrictive 0600 permissions (gitignored, never committed)
- **Orders execute immediately**: `place_equity_order` sends the order directly with no app-side confirmation prompt. The only preview is the `review_equity_order` MCP call — use it before placing.
- **Pre-trade preview only in MCP**: The `review_equity_order` tool is the only pre-trade check (returns quote + alerts); `place_equity_order` skips any app-side prompt entirely.
- **Instant shutdown**: You can revoke agent access anytime from Robinhood account settings.
