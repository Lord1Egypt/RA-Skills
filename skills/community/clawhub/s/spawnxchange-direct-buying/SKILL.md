---
name: spawnxchange-direct-buying
description: Use when completing public SpawnXchange direct purchases through /api/v1/items/{uuid}/acquire, verifying artifact delivery, and maintaining buyer state via the included references.
version: 0.1.4
author: SpawnXchange
license: MIT
tags: [spawnxchange, direct-buying, marketplace, x402, purchase]
related_skills: [spawnxchange-registration, spawnxchange-selling, spawnxchange-buying]
schema_version: 1
source:
   raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-direct-buying/SKILL.md
   repo_url: https://github.com/avlk/spawnxchange-skills
install:
   method: raw
   url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-direct-buying/SKILL.md
persistence:
   mode: local-state-required
   note: references/purchase-store.md
maintainers: [avlk]
metadata:
   hermes:
      source:
         raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-direct-buying/SKILL.md
   openclaw:
      homepage: https://github.com/avlk/spawnxchange-skills
   claude_code:
      homepage: https://github.com/avlk/spawnxchange-skills
   codex: {}
   copilot: {}
---

# SpawnXchange Direct Buying

## When to Use

Use this skill to:
- search public SpawnXchange listings
- inspect machine-readable chain availability before attempting purchase
- buy without a pre-existing SpawnXchange account
- handle the `/api/v1/items/{uuid}/acquire` x402 flow
- verify delivery and keep buyer state consistent for future reuse

If you already have a SpawnXchange identity and API key and want the authenticated buy route, use `spawnxchange-buying` instead.

Use public search first: `GET /api/v1/search?q={query}`. Optionally add `tech_stack`, `min_price`, and `max_price`.

Discovery contract:
- `GET /api/v1/search` returns only active listings that are currently purchasable on at least one supported chain
- `GET /api/v1/search` returns at most 20 results per request
- each search result includes top-level `available_chains`
- `GET /api/v1/items/{uuid}` returns public item detail with the same top-level `available_chains` field
- an active item can remain visible at item detail with `available_chains: []` when it is temporarily not purchasable

## Security model

This skill can authorize real wallet-backed USDC purchases when the executable example is run with `--execute`.

Required capabilities:
- network access to `https://spawnxchange.com` for search, purchase prompts, completion, and policy links
- network access required by the x402 client and EVM settlement libraries while producing the payment proof
- local read access to the configured plaintext private-key file when `--execute` is used
- optional local write access to the buyer purchase ledger and artifact cache described in `references/purchase-store.md`

Use a dedicated low-balance wallet. Keep private keys, payment headers, signed download URLs, purchase records, and cached artifacts out of git, logs, chat transcripts, and shared folders.

## Direct purchase route

Use `POST /api/v1/items/{uuid}/acquire`.

Prompt request:
- no auth header required
- send `{}` as the default prompt body
- optional advanced hint: send only `{ "chain": "base" | "polygon" }` if you need to pin the purchase chain up front
- do not send prompt-time `currency`, `policy_accepted`, or `license_accepted`

Completion request:
- retry the same route with `PAYMENT-SIGNATURE`
- use the server-published completion example from the `PAYMENT-REQUIRED` header extensions instead of hard-coding the payload shape
- `currency` defaults to `USDC` when omitted; only override it if the server-published completion example or a future contract revision says otherwise
- include `policy_accepted: true` and `license_accepted: true` only when intentionally completing the purchase
- successful responses return `{ order_id, download_url, expires_in, buyer_account }`

## Response handling

- `200` + `order_id`, `download_url`, `expires_in`: purchase completed
- `402`: correct paid flow; answer the x402 challenge and retry the same route with `PAYMENT-SIGNATURE`
- `403 self_purchase_forbidden`: you targeted your own listing or the wrong identity pairing

After success, verify the returned download URL before claiming completion. This skill requires durable buyer state; see `references/purchase-store.md` for storage details.

## Which x402 scheme to use

The challenge returns `accepts[]`.
- Use canonical `exact`.
- `accepts[].network` is a transport-level CAIP-2 chain id such as `eip155:8453` or `eip155:137`, not the public request slugs `base` or `polygon`.


## Implementation pattern

Recommended pattern:
- perform `POST /api/v1/items/{uuid}/acquire` yourself with `requests` and inspect the `402` quote before signing
- treat the signing step as explicit consent to the displayed payment plus the current SpawnXchange Terms and buyer license
- if you receive `402` and are intentionally executing the purchase, feed the response headers/body into the x402 client library
- read the server-published completion example from the `PAYMENT-REQUIRED` header extensions
- reuse the generated `PAYMENT-SIGNATURE` header on the retry request

## Executable example

See `scripts/acquire_item.py` for the public direct-purchase reference flow.

Default mode is quote-only. It does not read a private key, sign, pay, or accept terms:

`python scripts/acquire_item.py --item-id <uuid> --chain base`

To complete a purchase, inspect the quote output, then run with `--execute`. This authorizes the displayed payment and accepts the current SpawnXchange Terms and buyer license for that purchase:

`python scripts/acquire_item.py --item-id <uuid> --chain base --execute --private-key-file /path/to/plaintext-key.txt`

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

The executable example verifies the returned download URL before printing the executed result. Treat that verification as delivery reachability only; still inspect the artifact before integrating it into a project.

Buyers with completed orders can later submit item feedback via `POST /api/v1/items/{uuid}/feedback`.
- rating-only submissions auto-approve
- text feedback enters moderation
- only one submission per `(item, buyer)`

Record feedback status in the same local purchase record if you submit it.

## Common Pitfalls

1. **Treating 403 and 402 as the same problem.**
   - `403 self_purchase_forbidden` is the wrong actor pairing; `402` is the correct paid flow.
2. **Sending prompt-time `currency` or legal fields to `/api/v1/items/{uuid}/acquire`.**
   - The public acquire prompt is intentionally minimal; only `chain` remains as an advanced hint.
3. **Ignoring the server-published completion example.**
   - Read the `PAYMENT-REQUIRED` header extensions instead of duplicating the request shape in multiple places.
4. **Not maintaining local purchase state.**
   - This leads to duplicate buys.
5. **Using `--execute` as a casual retry flag.**
   - `--execute` is payment authorization and legal acceptance for the current quote. Re-run quote mode if item, chain, amount, or terms changed.
