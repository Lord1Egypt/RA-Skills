---
name: discover-mpprouter
description: Discover paid API services available via MPP Router (apiserver.mpprouter.dev) that accept Stellar USDC payments. Triggers on prompts like "summarize X using parallel.ai via MPPRouter", "search with exa via mpp", "find a service for <task>", "list mpp services", "what APIs can I pay for with stellar". Fetches the live service catalog, picks a matching service, and hands off to the pay-per-call sub-skill to actually invoke it.
---

# discover-mpprouter

High-level discovery for the MPP Router service catalog. Lets agents find and call paid APIs on Stellar mainnet without hardcoding URLs.

## What is MPP Router?

[MPP Router](https://www.mpprouter.dev) is a Stellar-native 402 proxy. It takes USDC payments on `stellar:pubnet` and forwards your request to upstream merchant APIs — Parallel.ai, Exa, Firecrawl, OpenRouter, and more. You pay once in Stellar USDC and get back whatever the upstream merchant returns. No need to hold USDC on Base/Tempo.

**Mainnet only.** The router does not run on testnet.

## When to trigger

- "Summarize https://stripe.com/docs using parallel.ai search via MPPRouter"
- "Search for X via exa through mpp"
- "Scrape this page with firecrawl — use stellar to pay"
- "List available MPP services"
- "What paid APIs can I call with stellar USDC?"
- User mentions `mpprouter` or `mpp router` by name

## Flow

1. **Discover** — `GET https://apiserver.mpprouter.dev/v1/services/catalog` returns the live service list.
2. **Match** — pick the service whose `id` or `category` best fits the user's intent. Ask the user if ambiguous.
3. **Read docs** — check the matched service's `docs` field:
   - If `docs.llms_txt` exists → fetch it and read the API schema to build the correct request body. **The router forwards bodies as-is — it does not transform or validate them.**
   - If only `docs.api_reference` → read that instead.
   - If only `docs.homepage` → browse it for the API format.
   - If no docs at all → ask the user for the request body format, or try a minimal probe.
4. **Invoke** — `{method} {base_url}{public_path}` with the correct request body. Use the `method` field from the catalog entry — most services are POST, but a few are GET; do not assume. Expect `402 Payment Required` with a Stellar challenge in `WWW-Authenticate: Payment request=...`.
5. **Pay** — hand off to `pay-per-call` with the 402 challenge; it produces a signed credential.
6. **Retry** — re-POST the same body with `Authorization: Payment <credential>`. Receive the upstream response + `Payment-Receipt` header.

## Service catalog

The catalog is live and large (~500 services). Always call
`/v1/services/catalog` fresh — never hardcode a list, never cache for
more than a minute.

### Payment-mode labels (IMPORTANT for the LLM)

The catalog exposes a `verified_mode` field per service. The discover
skill reads it and tags each record with a `payment_mode` string:

- **`charge`** (`✓ verified charge`) — end-to-end verified to work with
  this skill's Stellar charge flow. Safe to call. Currently known-good:
  `exa_search`, `firecrawl_scrape`, `parallel_search`, `alchemy_rpc`,
  `storage_upload`.
- **`session`** (`⚠ session-only`) — upstream merchant is session-mode
  only. The router now correctly advertises `stellar.intents: ["channel"]`
  (no `charge`) for these services. To use them, the agent must have a
  registered Stellar channel contract — see the `stellar-agent-wallet`
  root SKILL.md "Out of scope" section. Affected:
  `gemini_generate`, `openai_chat`, `openrouter_chat`, `tempo_rpc`.
  Charge-mode clients cannot call these services.
- **`unverified`** (`· unverified`) — the router hasn't labeled
  `verified_mode` (or labeled it as the literal string `"false"`, which
  is a router-side catalog-generator bug). ~97% of the catalog is in
  this bucket. Most of these work but we can't prove it without a paid
  probe. Treat as cautiously optimistic: acceptable to call on user
  request, but warn the user that it's not formally verified.

### Decision rule for the LLM

When the user asks to call a paid API via MPP Router:

1. Fetch the catalog fresh.
2. Find the best service match.
3. Check its `payment_mode`:
   - `charge` → proceed silently.
   - `session` → **refuse to call it.** Tell the user: "This service is
     currently in session-only mode on MPP Router. Paying via Stellar
     charge mode would succeed but the upstream would reject the
     receipt, so you'd lose the fee with no result. Waiting on a
     router-side fix. Alternative service?"
   - `unverified` → proceed but surface a brief caveat in your
     response ("this service isn't formally verified for Stellar charge
     mode; proceeding anyway — let me know if the call fails after
     payment").
4. Never override the user's explicit instruction to call a `session`
   service, but do warn them loudly before doing it.

## Service record shape

Discover enriches each record with a `payment_mode` field (one of
`charge`, `session`, `unverified`) derived from `verified_mode`. This
is the field the LLM should branch on — it normalizes the router's
raw `verified_mode` string (which can be missing or literally
`"false"`) into a fixed vocabulary.

```json
{
  "id": "exa_search",
  "name": "Exa – Search the web",
  "category": "search",
  "description": "Search the web",
  "public_path": "/v1/services/exa/search",
  "method": "POST",
  "price": "$0.005/request",
  "payment_method": "stellar",
  "network": "stellar-mainnet",
  "asset": "USDC",
  "status": "active",
  "methods": { "stellar": { "intents": ["charge", "channel"] } },
  "docs": {
    "homepage": "https://docs.exa.ai",
    "llms_txt": "https://docs.exa.ai/llms.txt"
  },
  "verified_mode": "charge",
  "payment_mode": "charge"
}
```

### `docs` field — upstream API documentation

The router forwards request bodies as-is without transformation. Clients
must know each upstream API's request format. The `docs` field provides
the upstream's own documentation:

| Sub-field | What it is | How the agent should use it |
|---|---|---|
| `llms_txt` | LLM-readable docs (69/88 providers) | **Read this first.** Fetch it and parse the API schema to construct the correct request body. |
| `api_reference` | Full API reference (8/88 providers) | Detailed endpoint docs — use when `llms_txt` is missing or insufficient. |
| `homepage` | Docs homepage (82/88 providers) | Fallback — browse or scrape if neither of the above is available. |

**Decision rule**: if `docs.llms_txt` exists, fetch and read it before
calling the service. If not, check `docs.api_reference`. If neither
exists, warn the user that you may need them to supply the request body
format, or try `docs.homepage`.

19 providers have no `llms_txt` — these include Google Gemini, Google
Maps, Nansen, Parallel, Allium, AgentMail, and several Tempo-proxied
third-party APIs.

## How to run

```bash
# List all services
npx tsx skills/discover/run.ts

# Filter by category
npx tsx skills/discover/run.ts --category search

# Match a free-text intent (uses simple keyword match)
npx tsx skills/discover/run.ts --query "web search"

# JSON output for piping
npx tsx skills/discover/run.ts --json
```

## Full end-to-end example

```bash
# Discover which service to use — capture path, method, and the
# catalog-advertised payment expectations so pay-per-call can refuse
# a 402 that tries to redirect funds or inflate the price.
SERVICE_JSON=$(npx tsx skills/discover/run.ts --query "web search" --pick-one --json)
SERVICE=$(echo "$SERVICE_JSON" | jq -r '.public_path')
METHOD=$(echo "$SERVICE_JSON" | jq -r '.method')
EXPECT_AMT=$(echo "$SERVICE_JSON" | jq -r '.expect.amount_usdc // empty')
EXPECT_TO=$(echo "$SERVICE_JSON" | jq -r '.expect.pay_to // empty')

# Call it — pay-per-call handles the 402 → pay → retry loop.
# The --expect-* flags cross-check the 402 challenge against the
# catalog. Any drift aborts before signing.
npx tsx skills/pay-per-call/run.ts "https://apiserver.mpprouter.dev$SERVICE" \
  --method "$METHOD" \
  --body '{"query": "Summarize https://stripe.com/docs"}' \
  ${EXPECT_AMT:+--expect-amount "$EXPECT_AMT"} \
  ${EXPECT_TO:+--expect-pay-to "$EXPECT_TO"}
```

## Anti-patterns

- ❌ Don't hardcode service paths — the catalog is the source of truth.
- ❌ Don't pay twice for one call — credentials are single-use and HMAC-bound to amount/currency/recipient.
- ❌ Don't use testnet — MPP Router is mainnet-only.
- ❌ Don't cache the catalog for more than a minute — prices and service availability can change.
