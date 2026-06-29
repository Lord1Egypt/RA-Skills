---
name: via-commerce
description: Agentic commerce over the VIA network. Discover products and sellers, submit a buyer brief and get genuine matches, find live buyer demand, and register your own store, all settled in USDC on Base. Use this whenever the user wants to buy something from an agent seller, source a product or supplier, sell to agent buyers, or stand up a store.
metadata: {"openclaw": {"category": "business", "requires": {"binaries": []}}}
---

# VIA agentic commerce

VIA is an agentic-commerce network. Every seller exposes a Sales Agent over MCP; every buyer can run a Buying Agent that finds, negotiates, and pays. Payments settle in USDC on Base. This skill lets you act on the VIA network on the user's behalf.

## Setup (one time, operator)

The VIA network MCP must be connected as an MCP server. Add it to `openclaw.json` once:

```
openclaw config set mcp.servers.via '{"url":"https://app.getvia.xyz/mcp","transport":"streamable-http"}'
```

Then restart the gateway. After that the VIA tools below appear alongside built-in tools. No API key is needed for discovery: the network MCP is public.

## When to use this skill

Trigger on intents like: "buy X", "find a supplier / seller for X", "source X", "what's available on VIA", "I sell X, who wants it", or "register / list my store".

## Tools and how to use them

All tools live on the VIA network MCP (`https://app.getvia.xyz/mcp`).

- **`get_via_overview`** — orientation. Call once if you are unsure what VIA offers or need the buyer/seller onboarding URLs.

- **`find_seller`** — product and seller search across the whole network. Pass the user's request as `query` (e.g. `"raw selvedge denim"`, an author, a title, a category). On a defined query it returns `results`, one relevance-ranked list; each result has a working `page_url` (the direct product page you give the user), `seller`, `price_usdc`, `image_url` (or null), and `mcp_ref` to transact. If more than one matches, present them side by side with prices and the key differences; do not silently pick one. If the response is `status: "need_more_info"`, do not say "nothing is available". Ask one clarifying question (budget, brand, category, use) or retry with a broader term, a synonym, or the brand/author name.

- **`submit_intent`** — use this when buying on behalf of someone and you want defined matches rather than a raw search. Pass the brief in plain words, including hard requirements (`"made in japan raw selvedge denim around 32 waist"`). Hard requirements are enforced; broad briefs return on-category options. Returns matches with `seller`, price, a direct `page_url`, and the `mcp_url` to transact.

- **`get_seller_products`** — drill into ONE seller's catalogue to answer "is X available at seller Y". Pass the `seller_mcp_url` from a `find_seller` / `list_sellers` result, plus an optional `query`.

- **`list_sellers`** — enumerate active sellers across the network, each with its per-seller MCP URL. Use for browsing, not for a specific product search (use `find_seller` for that).

- **`seller_mcp_url`** — resolve a known seller slug to its verified per-seller MCP URL.

- **`find_buyers`** — the demand mirror. When the user SELLS something, pass what they have as `query` to find buyers whose open briefs match. Each buyer comes back with structured intent (category, hard requirements, budget, never raw wording) and a buyer `mcp_url`. To act, connect to that `mcp_url` and call `pitch_against_brief` or `negotiate`.

- **`register_store`** — self-register the user's own store. You need only ONE wallet: their `payout_wallet` (a USDC EOA on Base; sale proceeds land there). The platform creates and operates the store's ERC-8004 identity wallet. Required: `store_name`, `kind` (`product` | `service` | `mixed`), `payout_wallet`, a contact `email`, and a `password` for the dashboard. The store is created PENDING and stays invisible until a human reviews it for quality (within 24 hours).

- **`get_store_status`** — poll a registered store's slug for `pending` / `approved` / `rejected`. On approval it returns the ERC-8004 agent id and the per-seller MCP URL.

## Buying and paying

The network MCP is for discovery and matching. To actually purchase, connect to a result's `mcp_ref.seller_mcp_url` (or `mcp_url`) and call that seller's `get_product` then `buy_product` (or `get_offering_schema` + `request_quote` when pricing is configurable). Settlement is USDC on Base via x402. Always confirm the price with the user before paying, and never exceed a delegation cap the user has set.

## Economics

VIA keeps a flat 2.5% network fee per sale; the seller keeps 97.5% to their payout wallet.

## Rules

- Do not tell a user an item is unavailable on a single zero-result query. Broaden or clarify first; frame any genuine miss as "not found yet", not "does not exist".
- When several products match, show the options with prices and differences. Do not pick one silently.
- Confirm price and get explicit user approval before any payment moves funds.
