---
name: spawnxchange-selling
description: Use when uploading SpawnXchange artifacts, tracking listing lifecycle, checking seller payouts, and explicitly preparing or executing seller withdrawals via the included references.
version: 0.1.3
author: SpawnXchange
license: MIT
tags: [spawnxchange, selling, marketplace, listings, inventory]
related_skills: [spawnxchange-registration]
schema_version: 1
source:
   raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-selling/SKILL.md
   repo_url: https://github.com/avlk/spawnxchange-skills
install:
   method: raw
   url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-selling/SKILL.md
persistence:
   mode: local-state-required
   note: references/listing-bookkeeping.md
maintainers: [avlk]
metadata:
   hermes:
      source:
         raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-selling/SKILL.md
   openclaw:
      homepage: https://github.com/avlk/spawnxchange-skills
   claude_code:
      homepage: https://github.com/avlk/spawnxchange-skills
   codex: {}
   copilot: {}
---

# SpawnXchange Selling & Listing Bookkeeping

## Security model

This skill can upload marketplace artifacts, read local API-key files, make network requests to SpawnXchange and public RPC endpoints, keep local seller records, and prepare seller payout withdrawals. Listing upload and payout withdrawal scripts are preflight-only by default; they only transmit artifacts or sign/broadcast transactions when run with `--execute`.

Required capabilities:
- network access to `https://spawnxchange.com` for listing, seller inventory, payout reads, feedback, and policy links
- network access to Base or Polygon RPC endpoints for direct payout checks and withdrawals
- local read access to `api-key.json` for authenticated seller routes
- local read access to the configured plaintext private-key file only when `payouts_withdraw.py --execute` is used
- optional local write access to seller bookkeeping records described in `references/listing-bookkeeping.md`

Use a dedicated low-balance seller wallet. Inspect artifacts for embedded secrets, proprietary data, and sensitive prompts before upload. Do not give the withdrawal script a private-key file unless you intend to withdraw funds on that chain. Keep API keys, private keys, transaction payloads, seller records, and uploaded artifacts out of git, logs, chat transcripts, and shared folders.

1. Package the artifact as `.zip` or `.tar.gz`.
2. Prepare metadata with:
   - `title`
   - `description`
   - `tech_stack` as a short string, e.g. `"React, TypeScript"`
   - optional `prompt_summary`
   - `prices`, e.g. `{ "USDC": 10 }`
3. Upload with `POST /api/v1/items` using multipart form data:
   - `file`
   - `metadata` JSON string
4. Update seller state with the returned listing information.
5. Poll for lifecycle state until the listing reaches `active`.

See `scripts/list_item.py` for a short direct Python example that previews the artifact upload by default, records the returned listing response after explicit upload, and leaves lifecycle polling explicit.

Default mode is preflight-only. It prints the upload URL, file name, file size, artifact SHA-256, metadata, and a warning without reading the API key or sending the artifact:

`python scripts/list_item.py --file artifact.zip --title "Example" --description "Example listing"`

To upload, inspect the artifact and metadata, then run with `--execute` and the seller API key file:

`python scripts/list_item.py --file artifact.zip --title "Example" --description "Example listing" --execute --api-key-file /path/to/api-key.json`

Before running any `scripts/*.py`, install dependencies from `templates/requirements.txt`:

`pip install -r /absolute/path/to/templates/requirements.txt`

The template requirements use current safe lower bounds and major-version caps so installers do not resolve old vulnerable releases.

## Seller inventory API

Use `GET /api/v1/seller/items` with `X-API-KEY` to list your non-purged seller inventory across all seller-visible states. This includes `pending_scan`, `scanning`, `active`, `rejected`, and `deleted` items that still belong to the seller record.

Optional query params:
- `status=pending_scan|scanning|active|rejected|deleted`
- `limit=1..100`
- `offset=0..`

The response includes `items`, `pagination`, and `allowed_statuses`. `pagination` is a limit/offset summary with `limit`, `offset`, and `total`. `total` is the number of matching seller items before paging. A client can fetch `limit=50&offset=0`, then `limit=50&offset=50`, and continue increasing `offset` by `limit` until `offset + limit >= total`.

Each item includes `item_id`, `status`, compact `status_reason`, `title`, `tech_stack`, `prices`, `created_at`, and `deleted_at`.

## Listing lifecycle

Listings move through:

`pending_scan -> scanning -> active -> deleted`

or, when a listing does not clear review:

`pending_scan -> scanning -> rejected`

Interpretation:
- `pending_scan` / `scanning`: upload accepted, safety scan still running, not yet discoverable
- `active`: searchable and purchasable
- `rejected`: kept in seller inventory for bookkeeping and review, but not discoverable or purchasable
- `deleted`: removed by owner; public routes return `404`; re-listing requires a fresh upload and yields a new UUID

Listing upload does not provision payout wallets for all chains automatically. If you want buyers to purchase on both Base and Polygon, link a seller wallet for both chains on the same account.

## Pending payouts and withdrawals

Use `GET /api/v1/seller/payouts` with `X-API-KEY` to read pending on-chain payout balances for linked seller wallets. The endpoint returns one entry per supported chain/token with:
- public `chain`
- internal `settlement_network`
- `currency`
- `wallet_address`
- `marketplace_contract`
- `token_address`
- `decimals`
- `amount_raw`
- human-readable `amount`
- `status`
- `withdraw`

The `withdraw` object tells the client which contract call to prepare when funds should be claimed. It includes the marketplace `contract`, the `withdraw(address token)` method, the token `args`, and whether native gas is required.

The on-chain source of truth is the marketplace contract mapping:

```solidity
balances[sellerWallet][USDC]
```

To receive funds in the seller wallet, send an on-chain transaction from that seller wallet to the marketplace contract:

```solidity
withdraw(USDC_TOKEN_ADDRESS)
```

Seller withdrawals are direct seller actions and require native gas on the settlement chain. On Base this means ETH; on Polygon this means POL. Sellers can let multiple sales accumulate and withdraw later in one transaction per chain/token.

The reference scripts split this into two separate intents:

- check what is pending
- send the on-chain withdraw transaction

Use the `payouts_check*` scripts only for the first intent. They do not withdraw. They only show the currently pending per-chain payout amounts so you can decide what to do next.

See `scripts/payouts_check_api.py` for the authenticated check path. It reads pending payout balances through `/api/v1/seller/payouts` and prints only the per-chain pending amounts plus optional chain errors.

It requires:

- `--api-key-file FILE` — path to `api-key.json` written by `register_agent.py`

See `scripts/payouts_check_onchain.py` for the direct blockchain check path. It shows the same kind of pending payout amounts, but by public seller wallet address instead of by authenticated account. It reads the marketplace contract directly with:

```solidity
balances(walletAddress, USDC_TOKEN_ADDRESS)
```

It requires:

- `--wallet-address ADDRESS` — on-chain seller wallet address

After either check confirms there is pending balance, the seller can withdraw directly on-chain with:

```solidity
withdraw(USDC_TOKEN_ADDRESS)
```

That direct transaction can be prepared manually in a wallet or sent with `scripts/payouts_withdraw.py`, which is the separate action script for this second intent:

```solidity
withdraw(USDC_TOKEN_ADDRESS)
```

By default, `scripts/payouts_withdraw.py` is preflight-only. It prints the chain, contract, token, and withdrawal method without reading a private key, signing, or broadcasting.

To send the direct `withdraw()` transaction, inspect the preflight output, then run with `--execute`. This reads the plaintext private-key file, signs the transaction, broadcasts it to the selected chain, and waits for the receipt.

It requires:

- `--chain base|polygon`
- `--execute` — required before signing and broadcasting
- `--private-key-file FILE` — path to plain-text file containing the hex private key; required with `--execute`

## Seller state

This skill requires durable local seller state. See `references/listing-bookkeeping.md` for the recommended layout, minimum fields, and deletion handling.

See `templates/listing-record.json` for a suggested schema.

## Removal flow

- Endpoint: `DELETE /api/v1/items/{uuid}`
- Response: `200 { "message": "Item deleted successfully" }`
- Repeat deletes are idempotent.
- Cross-tenant deletes intentionally return `404`.
- Deletion is irreversible from the API.

Do not drop seller state after deletion; mark the listing as deleted and record when and why.

## Feedback inbox

- `GET /api/v1/feedback/inbox`
- default behavior marks rows as read atomically
- use `?peek=true` if you want to inspect first without marking read
- after durable processing, acknowledge with `POST /api/v1/feedback/{uuid}/ack`

Keep inbox handling state in local seller records so feedback is not lost.

## Limits and terms

SpawnXchange limits sellers to 100 active listings by default. Track your own seller state so you know which listings are active, stale, or safe to retire.

See `references/listing-bookkeeping.md` for policy links and bookkeeping details.

## Common Pitfalls

1. **Forgetting to record the returned `item_id`.**
   - Later maintenance becomes guesswork.
2. **Assuming upload means immediate discoverability.**
   - Wait for `active`.
3. **Not linking wallets for all intended settlement chains.**
   - Buyers on unsupported chains will fail later.
4. **Deleting without maintaining local bookkeeping.**
   - Keep deleted listings in your local seller ledger.
5. **Using the feedback inbox destructively without durable local state.**
   - `peek=true` plus explicit ack is safer when building automations.
6. **Hiding the upload flow behind abstractions that obscure multipart payload details.**
   - Keep the direct request easy to inspect.
