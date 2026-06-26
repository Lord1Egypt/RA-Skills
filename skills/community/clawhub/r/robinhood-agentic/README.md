# Robinhood Agentic Trading

[![ClawHub](https://img.shields.io/badge/%F0%9F%A6%9E_ClawHub-Published-22c55e?style=flat)](https://clawhub.ai/leosaucedo/robinhood-agentic)

MCP client for [Robinhood Agentic Trading](https://robinhood.com/us/en/support/articles/agentic-trading-overview/) — connect an AI agent to a dedicated Robinhood account for automated investing.

## Install

```bash
cd robinhood-agentic
pnpm install
```

## Authentication

Robinhood Agentic uses OAuth 2.1 with PKCE. Run the auth command and follow the prompts:

```bash
node rh-client.mjs auth
```

This prints an authorization URL. Open it in a **desktop browser** (mobile redirects to the Robinhood app which won't work), log into Robinhood, then paste the redirect URL back. Tokens are stored in `.rh-tokens.json` with 0600 permissions and never committed.

Set `RH_TOKEN_FILE` to override the token storage path. Set `RH_DEBUG=1` for verbose logging.

## Usage

```bash
# Check auth status
node rh-client.mjs status

# Discover available MCP tools
node rh-client.mjs list-tools

# Call a tool
node rh-client.mjs call get_portfolio
node rh-client.mjs call place_equity_order '{"symbol":"AAPL","quantity":1,"side":"buy"}'

# Pipe complex args from stdin
echo '{"symbol":"AAPL"}' | node rh-client.mjs call get_equity_quotes -
```

## How It Works

- Uses `@modelcontextprotocol/sdk` v1.29 Streamable HTTP transport
- Connects to `https://agent.robinhood.com/mcp/trading`
- OAuth 2.1 PKCE with manual paste flow (headless-friendly)
- Automatic token refresh at 5 minutes before expiry
- RFC 8707 resource indicators, RFC 7591 dynamic client registration

## Requirements

- Robinhood Agentic access (rolling out — wait for email)
- A dedicated Agentic account (separate from your main Robinhood) — trading tools are restricted to this account
- Read-only tools (portfolio, positions, quotes) work on **all** your Robinhood accounts
- Node.js ≥ 18

## Security

- Separate Agentic account isolates AI trades from your main portfolio
- OAuth tokens stored with restrictive 0600 permissions, gitignored
- Review before placing via `review_equity_order` MCP tool (no app-side confirmation prompt)
- Spending caps and instant shutdown available in Robinhood settings
