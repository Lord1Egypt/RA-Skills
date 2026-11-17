---
name: saferoute-base-swap
description: Inspect supported Base USDC/WETH swap eligibility or request a SafeRoute quote via x402. Payment needs the operator's approved client and budget.
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---

# SafeRoute Base swap check

Start with a wallet-free eligibility check for an approved-token pair. The safety check costs **0.001 USDC**; an optional wallet-bound quote costs **0.01 USDC**, with additional disclosed swap fees if executed. A safety result is indicative evidence, not a guarantee against losses, arbitrary scam-token detection or proof of execution.

## Inspect without paying

Run the bundled Node.js 22+ demo:

```sh
node "{baseDir}/scripts/inspect.mjs"
```

Resolve `{baseDir}` to this skill directory. It makes one unpaid POST with USDC/WETH and amount 1, verifies the expected 402 challenge, Base network, canonical USDC, merchant and exact 0.001 price, then stops. No wallet or dependencies are needed for inspection. The command-line demo has no paid mode. Read the script before use.

## Evaluate with the operator’s existing payment client

Use `POST https://api.usesaferoute.com/v1/swap-safety-check` with:

```json
{ "from": "USDC", "to": "WETH", "amount": "1" }
```

Use the live [OpenAPI](https://api.usesaferoute.com/openapi.json) for supported assets and current schemas. Inspect the challenge first. Before a paid call, verify scheme exact, Base `eip155:8453`, canonical USDC `0x833589fCD6eDb6E08f4C7C32D4f71b54bdA02913`, the intended merchant and an application-controlled spend ceiling. Keep wallet credentials in the caller’s existing local payment client; never send them to SafeRoute or ask for seed phrases.

The bundled helper exports `runFirstCall({fetchImpl, paidFetch, source, applicationId})` for an existing caller-controlled x402 fetch. Passing paidFetch permits one paid service request after the unpaid inspection; callers must apply the above payment policy. Do not add automatic retries after uncertain settlement. A successful payment response plus a received service result establishes that call only.

For an optional quote use `POST /v1/quote`, or MCP tool `get_safe_swap_quote` at `https://api.usesaferoute.com/mcp`, after validating the live schema and obtaining the separate 0.01 USDC allowance. MCP safety tool: `check_base_swap`. Do not escalate to signing, broadcasting or a funded trade from a request to evaluate an API.

## Learn what worked

Optional `discoverySource` and `sourceAgentId` body fields, or `X-SafeRoute-Source` / `X-SafeRoute-Application` headers, carry caller-reported non-personal labels. Use the actual discovery source; omit unknown values. Opening this skill is not proof the operator found it in a particular directory. Keep the response request ID. Display `operatorFeedback.url` to a willing operator; never invent feedback or submit automatically. Contact details and permission are voluntary.

[Developer guide](https://usesaferoute.com/developers) · [First-call guide](https://usesaferoute.com/start)
