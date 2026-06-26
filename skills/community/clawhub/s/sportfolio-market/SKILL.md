---
name: sportfolio
description: Use when working with Sportfolio through its public authenticated MCP endpoint or the repo-local CLI. Covers user API token authentication, MCP connection setup, CLI command usage, shared public tools/prompts/resources, account and portfolio reads, and confirmation-gated staging for trades, LP actions, boosts, scouts, and related gameplay workflows. Do not use for admin or internal-only routes, billing or checkout flows, or any workflow that assumes autonomous execution without explicit user confirmation.
---

# Sportfolio

Use this skill for Sportfolio external access and agent-assisted workflows.

## Choose the interface

- Use MCP when the user has an MCP-aware client and wants protocol-level access.
- Use the CLI when the Sportfolio repo is checked out locally and the user wants direct terminal commands.
- Prefer MCP over inventing CLI install steps. The CLI is repo-local right now and is not a published public package.
- Prefer the web app for rich visual scanning. Use CLI or MCP for fast reads, docs lookup, and staged actions.

## Authenticate correctly

- Use a user API token created from `Profile -> CLI Access`.
- Treat the token as user-scoped. It inherits the same account boundary as the web app.
- Send the token as `Authorization: Bearer <your-token>` for MCP.
- Do not treat the token as admin access or a back door.
- Avoid putting tokens in plain shell history or logs.

## Connect through MCP

- Production endpoint: `https://www.sportfolio.market/mcp`
- Local endpoint: `http://127.0.0.1:5000/mcp`
- Transport: Streamable HTTP
- Normal MCP traffic goes through `POST /mcp`

When configuring an MCP client, provide:

- the MCP URL
- the bearer token header
- no assumptions about admin-only or internal routes

Use the shared public surface exposed by the server:

- tools for account, portfolio, players, pools, boosts, scouts, watchlists, schedules, docs, news, SMS settings, and agent settings
- prompts such as `review_setup`, `review_idle_cash`, `find_boost_candidates`, and `stage_trade`
- resources such as `sportfolio://docs/index`, `sportfolio://capabilities`, and `sportfolio://action-surface`

## Use the repo-local CLI

From the repo root:

```bash
npm run cli -- --help
npm run cli -- auth login --token <your-token> --base-url https://www.sportfolio.market
npm run cli -- auth whoami
```

For local development:

```bash
npm run cli -- auth login --token <your-token> --base-url http://127.0.0.1:5000
```

Direct fallback entrypoint if the npm script is not available:

```bash
node packages/sportfolio-cli/bin/sportfolio.mjs auth login --token <your-token> --base-url https://www.sportfolio.market
```

Use these command families:

- `auth`
- `docs`
- `portfolio`
- `agent`
- `actions`
- `tools`
- `prompts`
- `resources`

Useful examples:

```bash
npm run cli -- docs list
npm run cli -- docs search boosts
npm run cli -- docs open cli/command-reference
npm run cli -- portfolio summary
npm run cli -- tools list
npm run cli -- resources read sportfolio://capabilities
npm run cli -- agent ask "Review my setup."
```

Use `--json` for machine-readable automation:

```bash
npm run cli -- --json auth whoami
npm run cli -- --json tools call get_account_profile
```

## Respect the safety model

Sportfolio does not grant autonomous gameplay execution through MCP or CLI.

- Reads are immediate.
- Many gameplay mutations are staged first and still require explicit confirmation.
- Confirm and cancel operate on pending bundles instead of bypassing server validation.

Treat these as confirmation-gated unless repo truth explicitly changes:

- market buys and sells
- LP add, remove, and related LP actions
- stack shares
- daily boost assignment and removal
- community boost creation
- scout assignment changes
- thread confirm and cancel flows

Treat these as public but non-admin:

- account and portfolio reads
- docs, prompts, and resources
- agent thread reads and asks
- token listing and revocation
- username and profile image updates
- SMS link and settings actions
- agent settings and BYOK actions

Treat these as excluded:

- billing, funding, checkout, and external purchase flows
- admin routes
- internal-only routes

Do not claim full site parity if the public registry or docs do not expose a capability.

## Follow the recommended workflow

1. Confirm whether the user wants MCP setup or a repo-local CLI workflow.
2. Authenticate with a user API token.
3. Start with docs, resources, or read tools before proposing actions.
4. Use prompts or agent asks for broad setup reviews.
5. Stage gameplay changes only when the user clearly requests them.
6. Require an explicit confirm step before execution.
7. Use cancel if the user changes direction before confirmation.

## Start with docs and capability discovery

Use the public docs and capability surface before guessing:

- `docs list`, `docs search`, `docs open` in CLI
- `sportfolio://docs/index` to inspect published docs
- `sportfolio://capabilities` to inspect the included and excluded public surface
- `sportfolio://action-surface` to inspect public tools by domain

If a request sounds broad, use the shared prompt starters first:

- `review_setup`
- `review_idle_cash`
- `find_boost_candidates`
- `stage_trade`

## Handle common requests

For setup and discovery:

- authenticate first
- inspect docs and resources
- verify whether the user needs CLI commands or MCP configuration

For account and portfolio questions:

- prefer read tools, `portfolio summary`, and agent asks
- keep answers grounded in the authenticated user context

For gameplay actions:

- gather the relevant player, sport, and amount inputs
- stage the action
- surface the pending bundle summary
- wait for explicit confirmation

For community boosts:

- prefer full player names instead of short ids

If the server reports the agent is busy, wait a few seconds and retry.
