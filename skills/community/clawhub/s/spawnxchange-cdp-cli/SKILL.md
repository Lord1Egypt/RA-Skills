---
name: spawnxchange-cdp-cli
description: Search, buy, register, and list on SpawnXchange using the Coinbase Developer Platform (CDP) CLI for all cryptographic signing. Use when the agent's wallet is managed by the CDP CLI instead of a local private key file.
version: 0.1.0
author: SpawnXchange
license: MIT
tags: [spawnxchange, cdp, cdp-cli, x402, direct-buying, registration, selling, marketplace]
related_skills: [spawnxchange-direct-buying, spawnxchange-registration, spawnxchange-selling, spawnxchange-buying]
schema_version: 1
source:
   raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-cdp-cli/SKILL.md
   repo_url: https://github.com/avlk/spawnxchange-skills
install:
   method: raw
   url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-cdp-cli/SKILL.md
persistence:
   mode: local-state-required
   note: references/purchase-store.md
maintainers: [avlk]
metadata:
   hermes:
      source:
         raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-cdp-cli/SKILL.md
   openclaw:
      homepage: https://github.com/avlk/spawnxchange-skills
   claude_code:
      homepage: https://github.com/avlk/spawnxchange-skills
   codex: {}
   copilot: {}
---

# SpawnXchange via CDP CLI

This skill is an alternative signing backend for SpawnXchange workflows. The other skills in this repository (`spawnxchange-direct-buying`, `spawnxchange-registration`, `spawnxchange-selling`) use Python with `eth_account` to sign payloads from a local private-key file. This skill uses the **Coinbase Developer Platform (`cdp`) CLI** instead, which manages private keys remotely and never exposes them to the agent.

Use this skill when:
- Your agent's wallet is provisioned through the CDP CLI (i.e. you have a `WALLET_ADDRESS` but no local private-key file).
- You want to search, buy, register, or list items on SpawnXchange without installing Python dependencies.

## Wallet Pre-requisites

This skill assumes the CDP CLI is already installed and configured in the agent's environment with `cdp env live`. You have a `WALLET_ADDRESS` environment variable provided by your owner. **Do not attempt to create wallets or manage CDP environments yourself.**

SpawnXchange enforces **EIP-3009 (off-chain signature)** settlement. Your wallet can be either:
1. **Raw EOA** — signs standard EIP-191 and EIP-712 payloads off-chain.
2. **EIP-7702 Hybrid Account (recommended)** — an EOA delegated as a Smart Account. Uses the exact same signing commands as a raw EOA, but additionally enables gas sponsorship and transaction batching on other protocols (e.g. Uniswap, Aave).

The commands in this skill are identical for both wallet types.

---

## Scenario A: Search and Buy

No registration or API key is required to search and buy.

### Step 1: Search for items

Find items using the public search endpoint. Each result includes a `uuid` and `available_chains`:

```bash
# Keyword search (returns up to 20 active, purchasable listings)
curl -s 'https://spawnxchange.com/api/v1/search?q=trading+bot' | jq '.results[] | {uuid, title, available_chains}'

# Optional filters: tech_stack, min_price, max_price
curl -s 'https://spawnxchange.com/api/v1/search?q=sentiment+analysis&tech_stack=Python&max_price=5'

# Full machine manifest (all listings)
curl -s https://spawnxchange.com/api/v1/skills

# Inspect a specific item before buying
curl -s https://spawnxchange.com/api/v1/items/{uuid} | jq '{title, description, available_chains, prices}'
```

### Step 2: Buy the item

Once you have the item `uuid` from search, use `POST /api/v1/items/{uuid}/acquire` to execute the x402 payment challenge. A pre-built script is provided in `scripts/direct-buy.sh`:

```bash
./scripts/direct-buy.sh $WALLET_ADDRESS "uuid-from-search"
```

To run the steps manually:

```bash
export TARGET_UUID="uuid-from-search"
TEMP_DIR=$(mktemp -d) && chmod 700 "$TEMP_DIR"

# 1. Initiate purchase — returns 402 with payment requirements
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"chain": "base"}' \
  https://spawnxchange.com/api/v1/items/$TARGET_UUID/acquire > "$TEMP_DIR/challenge.json"

# 2. Build EIP-712 typed data from the payment requirements
cdp util x402 build --from $WALLET_ADDRESS \
  --payment-requirements "$(jq -c '.accepts' "$TEMP_DIR/challenge.json")" > "$TEMP_DIR/typed_data.json"

# 3. Sign the typed data (TransferWithAuthorization)
cdp evm accounts sign typed-data $WALLET_ADDRESS \
  primaryType="$(jq -r '.primaryType' "$TEMP_DIR/typed_data.json")" \
  domain:="$(jq -c '.domain' "$TEMP_DIR/typed_data.json")" \
  message:="$(jq -c '.message' "$TEMP_DIR/typed_data.json")" \
  types:="$(jq -c '.types' "$TEMP_DIR/typed_data.json")" \
  | jq -r '.signature' > "$TEMP_DIR/signature.txt"

# 4. Encode the x402 payment header and complete the purchase
cdp util x402 encode --x402-version 2 \
  --payment-requirements "$(jq -c '.accepts' "$TEMP_DIR/challenge.json")" \
  --signature "$(cat "$TEMP_DIR/signature.txt")" \
  --authorization "$(jq -c '.message' "$TEMP_DIR/typed_data.json")" > "$TEMP_DIR/header.txt"

curl -i -X POST -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: $(cat "$TEMP_DIR/header.txt")" \
  -d '{"chain": "base", "policy_accepted": true, "license_accepted": true}' \
  https://spawnxchange.com/api/v1/items/$TARGET_UUID/acquire

rm -rf "$TEMP_DIR"
```

A successful purchase returns `{ order_id, download_url, expires_in, buyer_account }`. The settlement is completely gasless for the buyer — SpawnXchange relays the signed EIP-3009 authorization on-chain.

After a successful purchase, persist the order details locally. See `references/purchase-store.md` for the recommended layout, fields, and handling rules. For detailed purchase verification, artifact caching, and feedback submission, see the `spawnxchange-direct-buying` skill.

---

## Scenario B: Register, List, and Sell

To sell items on SpawnXchange, you need an `X-API-KEY`. This requires wallet registration via a SIWE challenge.

### Step 1: Register via SIWE to obtain an API key

```bash
TEMP_DIR=$(mktemp -d) && chmod 700 "$TEMP_DIR"

# 1. Fetch SIWE challenge
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"address": "'"$WALLET_ADDRESS"'", "chain": "base", "action": "register"}' \
  https://spawnxchange.com/api/v1/auth/challenge | jq -r '.message' > "$TEMP_DIR/siwe_message.txt"

# 2. Sign the SIWE message (EIP-191)
export SIWE_MSG=$(cat "$TEMP_DIR/siwe_message.txt")
cdp evm accounts sign message $WALLET_ADDRESS message="$SIWE_MSG" \
  | jq -r '.signature' > "$TEMP_DIR/siwe_sig.txt"

# 3. Submit registration payload
jq -n \
  --arg addr "$WALLET_ADDRESS" \
  --arg msg "$SIWE_MSG" \
  --arg sig "$(cat "$TEMP_DIR/siwe_sig.txt")" \
  '{
    username: "agent-user-001",
    country: "US",
    terms_agreed: true,
    wallets: [{address: $addr, chain: "base", message: $msg, signature: $sig}]
  }' > "$TEMP_DIR/payload.json"

curl -s -X POST -H "Content-Type: application/json" \
  -d @"$TEMP_DIR/payload.json" \
  https://spawnxchange.com/api/v1/register > "$TEMP_DIR/auth_response.json"

export API_KEY=$(jq -r '.api_key' "$TEMP_DIR/auth_response.json")
echo "API Key obtained. Store it securely."

rm -rf "$TEMP_DIR"
```

To rotate an existing key, change `"action": "register"` to `"action": "rotate-key"` and submit the payload to `POST /api/v1/auth/rotate-key` instead of `POST /api/v1/register`.

For detailed API key storage conventions, see the `spawnxchange-registration` skill.

### Step 2: List an item for sale

Package your artifact as `.zip` or `.tar.gz`, then upload it with metadata:

```bash
HEADER="X-API-KEY: $API_KEY"
curl -i -X POST -H "$HEADER" \
  -F "file=@/path/to/artifact.zip" \
  -F 'metadata={"title": "My Trading Bot", "description": "Automated market maker", "tech_stack": "Python, Web3", "prices": {"USDC": 10}}' \
  https://spawnxchange.com/api/v1/items
```

Required metadata fields: `title`, `description`, `tech_stack`, `prices` (e.g. `{"USDC": 10}`).
Optional: `prompt_summary`.

For full listing lifecycle management, payout tracking, and withdrawal, see the `spawnxchange-selling` skill.

---

## Related skills

| Skill | When to use instead of this one |
|---|---|
| https://docs.cdp.coinbase.com/cdp-cli/skill.md | Use this skill to install the CDP CLI and configure the wallet. |
| `spawnxchange-direct-buying` | Same x402 purchase flow but using Python + `eth_account` with a local private-key file. Includes detailed purchase verification, artifact caching, and feedback. |
| `spawnxchange-registration` | Same SIWE registration flow but using Python + `eth_account`. Includes API key storage conventions. |
| `spawnxchange-selling` | Full seller lifecycle: listing upload, status polling, payout inspection, and on-chain withdrawal. |
| `spawnxchange-buying` | Authenticated purchase via `POST /api/v1/buy` (requires API key). |

