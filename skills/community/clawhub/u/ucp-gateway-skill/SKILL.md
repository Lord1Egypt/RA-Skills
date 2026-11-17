---
name: ucp-gateway-skill
version: 0.2.4
description: "MCP Tools skill for AI agent commerce. Use when a user wants agentic Shopping to search/compare products, prepare a buyer-confirmed cart, and create a merchant-hosted checkout handoff link, or when an agent needs to register/reuse a hosted UCP identity (agent_id). Provider-neutral UCP Shopping MCP tools; no scraping and no payment handling."
tags: [ecommerce, shopping-agent, mcp, ucp, universal-commerce-protocol, shopping, agentic-commerce, checkout-handoff]
metadata: {"openclaw":{"emoji":"🛒","category":"mcp-tools","homepage":"https://ucpg.ai/","source":"https://github.com/theagenttimes/ucp-gateway-skill","paths":["./.ucpgateway/"]}}
---

# UCP Gateway runtime

## Endpoint & local state

- MCP endpoint: `https://ucpg.ai/mcp`; registry: `https://ucpg.ai/registry`.
- Legacy endpoint `https://ucpgateway.theagenttimes.com/mcp` still works for saved configs; use `https://ucpg.ai/mcp` for new configs.
- Local state convention: `./.ucpgateway/private_key.jwk` stays local-only, `public_key.jwk` is safe to send as `public_key_jwk`, `agent.json` stores registration results.
- If native MCP access is unavailable, use bundled Python helpers with Python 3.8+: `uv run python scripts/init_ucpgateway.py`, `uv run python scripts/register_profile.py`, `uv run python scripts/call_mcp.py --tools`. `uv run python scripts/call_mcp.py --tool <tool_name>` filters the live descriptor/schema for one MCP tool.
- Prefer `tools/list` schemas over remembered arguments. After every call, read `result.structuredContent.next_step` and warnings.
- JSON-RPC 2.0 over HTTP `POST` to `/mcp`; GET returns a markdown guide/SSE bootstrap; POST fallbacks may exist at `/messages` and `/mcp/messages`.

## Parameters this skill consumes

- `shopping_goal`; `agent_id` if already registered; `buyer_context` such as country/region/currency/intent.
- `merchant_domain`; selected provider variant item IDs and quantity; buyer-provided checkout contact/shipping data.
- `confirmation_state`: no confirmation, cart mutation confirmed, or final checkout confirmation received.

## Branch by task state

- No `agent_id`? Register identity once: call `register_ucp_profile` with `agent_name` + `public_key_jwk`; the backend builds the canonical profile and capabilities. Read `ucp://gateway/profile-registration` only on first registration or `INVALID_UCP_PROFILE` / `INVALID_PUBLIC_KEY`. Save `agent_id`, `namespace`, `profile_url`, `registry_url`, `profile_json`, `created`, `existing_profile`, `message`, and local `saved_at` to `./.ucpgateway/agent.json`.
- Have `agent_id` + shopping intent? Fetch the current schema for the tool you are about to call, then use `shopping_product_search`; optionally use `shopping_product_get` for selected product/variant detail. Present only provider-returned options, prices, availability, URLs, merchant domains, variant IDs/options, messages, and warnings.
- Cart/checkout? After explicit cart confirmation, call `shopping_cart_create` or `shopping_cart_update`; use `shopping_cart_get` to review, `shopping_cart_cancel` only when requested. After final confirmation, call `shopping_checkout_create`; use `shopping_checkout_get`, `shopping_checkout_update`, or `shopping_checkout_cancel` only with buyer/operator intent. Hand off `continue_url`.

## Core tools

`register_ucp_profile`, `get_ucp_profile`, `shopping_product_search`, `shopping_product_get`, `shopping_cart_create`, `shopping_cart_get`, `shopping_cart_update`, `shopping_cart_cancel`, `shopping_checkout_create`, `shopping_checkout_get`, `shopping_checkout_update`, `shopping_checkout_cancel`.

## Safety / confirmation barriers

- Product search/detail is read-only.
- Ask explicit buyer/operator confirmation before any cart create/update/cancel.
- Show cart totals, line items, messages, and warnings; ask final confirmation before checkout.
- Set `operator_confirmed: true` only after final confirmation. It is not payment authorization.
- Never collect payment credentials; never invent buyer PII; never claim an order is paid, placed, complete, or guaranteed.
- Payment happens only on the merchant-hosted `continue_url`.

## Progressive disclosure, not startup

- Gateway resources/prompts are fallbacks for first registration, schema ambiguity, error recovery, or operator handoff — do not load all of them at startup.
- Read when needed: `ucp://gateway/skill-runtime-guide`, `ucp://gateway/profile-registration`, `ucp://gateway/shopping-flow`, `ucp://gateway/safety-and-operator-handoff`.
- Prompts when needed: `ucp-skill-runtime-guide`, `ucp-shopping-flow`, `ucp-operator-handoff`.

## Minimal recovery rules

- `AGENT_ID_REQUIRED` / `AGENT_NOT_REGISTERED`: register or load an active `agent_id`; `get_ucp_profile` can verify a saved identity.
- `INVALID_UCP_PROFILE`: use default `public_key_jwk` registration when possible; advanced `profile_json` must use exact keys only: `dev.ucp.shopping.catalog.search`, `dev.ucp.shopping.catalog.lookup`, `dev.ucp.shopping.catalog`, `dev.ucp.shopping.cart`, `dev.ucp.shopping.checkout`.
- `INVALID_PUBLIC_KEY`: send only an EC P-256 public JWK; keep private fields local.
- `INVALID_TOOL_ARGUMENTS`: compare against `tools/list` or `ucp://gateway/tools/{tool_name}`.
- `RATE_LIMITED`: wait for `retry_after_seconds`; retry the same confirmed mutation only with the same idempotency/client action ID.
- `BUYER_INFO_REQUIRED`: ask for buyer-provided checkout fields; never invent PII.
- `OPERATOR_CONFIRMATION_REQUIRED`: show the cart summary and ask before retrying with `operator_confirmed: true`.
- Payment-data rejection: remove card/CVV/bank/wallet/token/password/payment-method fields; buyer enters payment on the merchant site.
