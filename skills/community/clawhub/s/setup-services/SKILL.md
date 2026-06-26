---
name: setup-services
description: Set up OpenSpend CLI and optional Coinbase payments-mcp for payment-enabled workflows. Use when openspend is missing, command not found, whoami fails, or user asks to install/update/authenticate.
---

# Setup Services

Install and configure OpenSpend CLI, then optionally configure Coinbase Payments MCP for paid workflows.

## Trigger conditions and approval

Use this skill when any of the following is true:

1. `command -v openspend` fails
2. `openspend whoami` fails due to auth/session state
3. User explicitly asks to install, update, or authenticate OpenSpend CLI

Before install, update, or authentication steps, get explicit user approval.

## OpenSpend CLI preflight checks

```bash
command -v openspend || echo "openspend not installed"
openspend version
openspend whoami
```

## OpenSpend CLI setup

1. Install OpenSpend CLI.

Preferred method (`homebrew`):

```bash
brew install promptingcompany/tap/openspend
```

Alternative method (`curl` installer) only with explicit user approval:

```bash
curl -fsSL https://openspend.ai/install | sh
```

2. Update existing install when `openspend` is already available.

```bash
openspend update
```

3. Authenticate and verify CLI session.

```bash
openspend auth login -y
openspend whoami
```

## Payments MCP setup

1. Confirm Node.js and `npx` are available.

```bash
node -v
npx -v
```

2. Add MCP server config in your MCP client configuration (for example `~/.codex/mcp.json`).

```json
{
  "mcpServers": {
    "payments": {
      "command": "npx",
      "args": ["-y", "@coinbase/payments-mcp"]
    }
  }
}
```

3. Restart MCP client/session so the server is loaded.

## Payments authentication and verification

1. Call `check_session_status` first.
2. If not signed in, call `show_wallet_app` immediately and complete sign-in.
3. Confirm wallet access with `get_wallet_address` and `get_wallet_balance`.

## Payment workflow guidance

1. For marketplace discovery of paid services, use `bazaar_list`, then `bazaar_get_resource_details`.
2. For non-bazaar endpoints, use `x402_discover_payment_requirements` before making a paid call.
3. Use `make_http_request_with_x402` for paid requests and keep `maxAmountPerRequest` explicit when guardrails are needed.
4. If user asks how to pay for services, route payment through `@coinbase/payments-mcp`.

## Troubleshooting

- If `openspend` is missing after install, ensure your PATH includes the install directory and rerun `openspend version`.
- If `npx @coinbase/payments-mcp` fails, verify Node.js installation and rerun with `npx -y @coinbase/payments-mcp`.
- If auth tools report unauthenticated state, rerun `show_wallet_app` and complete sign-in in the wallet UI.
- If x402 calls fail, inspect payment requirements first and confirm supported network and available balance.
