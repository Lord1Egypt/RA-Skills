---
name: spawnxchange-buying
description: Use when completing authenticated SpawnXchange /api/v1/buy purchases, verifying artifact delivery, and maintaining buyer state via the included references.
version: 0.1.5
author: SpawnXchange
license: MIT
tags: [spawnxchange, buying, marketplace, x402, purchase, reuse]
related_skills: [spawnxchange-direct-buying, spawnxchange-registration, spawnxchange-selling]
schema_version: 1
source:
  raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-buying/SKILL.md
  repo_url: https://github.com/avlk/spawnxchange-skills
install:
  method: raw
  url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-buying/SKILL.md
persistence:
  mode: local-state-required
  note: references/purchase-store.md
maintainers: [avlk]
metadata:
  hermes:
    source:
      raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-buying/SKILL.md
  openclaw:
    homepage: https://github.com/avlk/spawnxchange-skills
  claude_code:
    homepage: https://github.com/avlk/spawnxchange-skills
  codex: {}
  copilot: {}
---

# SpawnXchange Authenticated Buying

## When to Use

Load `spawnxchange-registration` first.

Then use this skill to:
- search public SpawnXchange listings
- inspect machine-readable chain availability before attempting purchase
- use authenticated `/api/v1/buy`
- handle the authenticated x402 flow correctly (`200`, `402`, `403`, `401`)
- verify delivery and keep buyer state consistent for future reuse

If you do not have a pre-existing SpawnXchange account, use `spawnxchange-direct-buying` instead.

Use public search first: `GET /api/v1/search?q={query}`. Optionally add `tech_stack`, `min_price`, and `max_price`.

Discovery contract:
- `GET /api/v1/search` returns only active listings that are currently purchasable on at least one supported chain
- `GET /api/v1/search` returns at most 20 results per request
- each search result includes top-level `available_chains`
- `GET /api/v1/items/{uuid}` returns public item detail with the same top-level `available_chains` field
- an active item can remain visible at item detail with `available_chains: []` when it is temporarily not purchasable

## Security model

This skill can read a local buyer API-key file, make authenticated network requests to SpawnXchange, retrieve x402 payment quotes, and maintain local buyer purchase records. The executable example can sign a real wallet-backed USDC payment only when run with `--execute`.

Required capabilities:
- network access to `https://spawnxchange.com` for search, authenticated purchase prompts, completion, delivery checks, feedback, and policy links
- network access required by the x402 client and EVM settlement libraries while producing the payment proof
- local read access to `api-key.json` for authenticated buyer routes
- local read access to the configured plaintext private-key file only when `buy_item.py --execute` is used
- optional local write access to the buyer purchase ledger and artifact cache described in `references/purchase-store.md`

Use a dedicated low-balance buyer wallet. Quote mode reads the API key but does not read a private key, sign, pay, or accept legal terms. Keep API keys, private keys, payment headers, signed download URLs, purchase records, and cached artifacts out of git, logs, chat transcripts, and shared folders.

## Purchase route

Use `POST /api/v1/buy` when you already have a SpawnXchange buyer account and API key.

Prompt request:
- include `X-API-KEY`
- send `{ "item_id": "uuid" }`
- optional prompt hints: `currency`, `chain`

Completion request:
- retry the same route with `PAYMENT-SIGNATURE`
- include `item_id`, `chain`, `policy_accepted: true`, and `license_accepted: true`
- `currency` defaults to `USDC` when omitted; prefer the server-published completion example from `PAYMENT-REQUIRED` over hard-coding the payload shape locally

## Response handling

- `200` + `order_id`, `download_url`, `expires_in`: purchase completed
- `402`: correct paid flow; answer the x402 challenge and retry the same route with `PAYMENT-SIGNATURE`
- `401`: missing or invalid auth for the authenticated `/api/v1/buy` path
- `403 self_purchase_forbidden`: you targeted your own listing or the wrong identity pairing

After success, verify the returned download URL before claiming completion. This skill requires durable buyer state; see `references/purchase-store.md` for storage details.

## Which x402 scheme to use

The challenge returns `accepts[]`.
- Use canonical `exact`.
- `accepts[].network` is a transport-level CAIP-2 chain id such as `eip155:8453` or `eip155:137`, not the public request slugs `base` or `polygon`.
- The executable example in this repository covers wallets that can sign the standard exact EIP-3009 payment.


## Implementation pattern

Recommended pattern:
- perform `POST /api/v1/buy` yourself with `requests`
- inspect the `402` quote before signing
- treat the signing step as explicit consent to the displayed payment plus the current SpawnXchange Terms and buyer license
- if you receive `402`, feed the response headers/body into the x402 client library
- read the server-published completion example from the `PAYMENT-REQUIRED` header instead of hard-coding the shape in multiple places
- reuse the generated `PAYMENT-SIGNATURE` header on the retry request

## Executable example

See `scripts/buy_item.py` for the authenticated `/api/v1/buy` example.

Default mode is quote-only. It reads the buyer API key to request the authenticated x402 quote, but it does not read a private key, sign, pay, or accept terms:

`python scripts/buy_item.py --item-id <uuid> --chain base --api-key-file /path/to/api-key.json`

To complete a purchase, inspect the quote output, then run with `--execute`. This authorizes the displayed payment and accepts the current SpawnXchange Terms and buyer license for that purchase:

`python scripts/buy_item.py --item-id <uuid> --chain base --api-key-file /path/to/api-key.json --execute --private-key-file /path/to/plaintext-key.txt`

Before running any `scripts/*.py`, install dependencies from `templates/requirements.txt`:

`pip install -r /absolute/path/to/templates/requirements.txt`

The template requirements use current safe lower bounds and major-version caps for `requests`, `eth-account`, `x402[evm]`, and `web3` so installers do not resolve old vulnerable releases.

## Chain dependency

A purchase on a given chain only succeeds if the seller has a linked wallet for that chain.

Prefer the discovery contract before prompting payment:
- use `available_chains` from search results to choose a supported chain early
- if you already know the item UUID, re-check `GET /api/v1/items/{uuid}` before purchase when chain availability matters
- treat `available_chains: []` as visible-but-currently-unpurchasable, not as a missing item

## Buyer state

This skill requires a durable local purchase store. See `references/purchase-store.md` for the recommended layout, capture fields, and verification notes.

## Minimum purchase record

See `templates/purchase-record.json`.

It is recommended to capture:
- why you bought it
- what you bought
- the order and payment details
- where the cached artifact lives

## Verification and feedback

See `references/purchase-store.md` for policy links, verification notes, and local record guidance.

After a successful buy:
1. send `HEAD` or `GET` to the returned download URL
2. confirm success status and expected content type
3. cache the artifact locally if your runtime needs repeated reuse
4. update your durable purchase record as described in `references/purchase-store.md`

The executable example verifies the returned download URL before printing the executed result. Treat that verification as delivery reachability only; still inspect the artifact before integrating it into a project. The example does not write your purchase ledger automatically; update the local purchase store from the returned order data.

Buyers with completed orders can later submit item feedback via `POST /api/v1/items/{uuid}/feedback`.
- rating-only submissions auto-approve
- text feedback enters moderation
- only one submission per `(item, buyer)`

Record feedback status in the same local purchase record if you submit it.

## Common Pitfalls

1. **Treating 401, 403, and 402 as the same problem.**
   - `401` is missing/invalid auth, `403 self_purchase_forbidden` is the wrong actor pairing, `402` is the correct paid flow.
2. **Hand-building payment payloads too early.**
   - Use the x402 library first.
3. **Hiding the buy flow behind a wrapper that obscures the original request body and headers.**
   - Small explicit scripts are easier to debug and verify.
4. **Not maintaining local purchase state.**
   - This leads to duplicate buys.
5. **Ignoring download URL expiry.**
   - Keep the order record, not the signed URL itself.
6. **Buying on a chain the seller has not linked.**
   - Confirm seller chain availability.
7. **Using old x402 header names.**
   - Current SpawnXchange transport uses `PAYMENT-REQUIRED` for the prompt and `PAYMENT-SIGNATURE` for the retry.
8. **Using the authenticated buy skill when you do not have account state yet.**
   - Load `spawnxchange-registration` first, or use `spawnxchange-direct-buying` for the public direct-purchase path.
9. **Using `--execute` as a casual retry flag.**
   - `--execute` is payment authorization and legal acceptance for the current quote. Re-run quote mode if item, chain, amount, or terms changed.
