---
name: superrare-mint
description: Mint art to a SuperRare-compatible ERC-721 collection on Ethereum or Base via Bankr. Requires an explicit mint mode so aaigotchi can clearly choose between an artist-given collection and an own-deployed SR factory collection before minting.
homepage: https://github.com/aaigotchi/superrare-mint
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - node
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
    optionalEnv:
      - ETH_MAINNET_RPC
      - ETH_SEPOLIA_RPC
      - BASE_MAINNET_RPC
      - BASE_SEPOLIA_RPC
      - SUPER_RARE_CONFIG_FILE
      - SUPER_RARE_DEPLOY_RECEIPT_FILE
      - DRY_RUN
      - BANKR_SUBMIT_TIMEOUT_SECONDS
      - RECEIPT_WAIT_TIMEOUT_SECONDS
      - RECEIPT_POLL_INTERVAL_SECONDS
---

# superrare-mint

Mint aaigotchi art into a SuperRare-compatible ERC-721 contract using Bankr signing.

## Required mint choice

Before any mint, aaigotchi must clearly choose and state one of these modes:
- `ownership-given`
  - mint into an existing collection already owned or handed over by a SuperRare artist
  - requires `--contract` or `config.json` `collectionContract`
- `own-deployed`
  - mint into a collection deployed through `superrare-deploy`
  - requires a `superrare-deploy` receipt, either explicit or auto-resolved

Do not broadcast a mint without an explicit contract mode.

## Scripts

- `./scripts/pin-metadata.mjs --name ... --description ... --image ... [--video ...] [--tag ...] [--attribute trait=value]`
  - Uploads media to SuperRare and pins metadata.
  - Prints JSON including `tokenUri` and `gatewayUrl`.
- `./scripts/mint-via-bankr.sh --token-uri <uri> --contract-mode ownership-given|own-deployed [--contract <address>] [--deploy-receipt <path>] [--receiver <address>] [--royalty-receiver <address>] [--chain mainnet|sepolia|base|base-sepolia] [--broadcast]`
  - Builds calldata for `mintTo(string,address,address)` or `addNewToken(string)`.
  - Refuses to run without a clear contract mode.
  - Prints the chosen mode and collection source before any broadcast.
  - Validates that an `own-deployed` receipt matches the selected chain.
  - Defaults to dry-run unless `--broadcast` is passed or `DRY_RUN=0`.
  - Submits without waiting on Bankr, then polls chain directly for the receipt.
  - Writes a JSON receipt on successful broadcast.
- `./scripts/mint-art.sh --name ... --description ... --image ... --contract-mode ownership-given|own-deployed [options]`
  - End-to-end wrapper: upload metadata, then mint via Bankr.
  - Use `--metadata-only` to stop after pinning and print the token URI.

## Config

Default config path:
- `config.json` in this skill directory

Override with:
- `SUPER_RARE_CONFIG_FILE=/path/to/config.json`

Expected keys:
- `chain`: `mainnet`, `sepolia`, `base`, or `base-sepolia`
- `contractMode`: `ownership-given` or `own-deployed`
- `collectionContract`
- `deployReceiptFile` (optional explicit path to a `superrare-deploy` receipt)
- `receiver`
- `royaltyReceiver`
- `rpcUrl`
- `apiBaseUrl`
- `descriptionPrefix`

## Defaults and safety

- Dry-run is the default. Mint transactions only broadcast with `--broadcast` or `DRY_RUN=0`.
- Supported chains are `mainnet`, `sepolia`, `base`, and `base-sepolia`.
- Broadcast mode uses a short Bankr submit timeout and then waits for the onchain receipt directly, which avoids hanging on long confirmation waits.
- `mint-art.sh` still uploads media/metadata to SuperRare before the dry-run mint preview. Use `--metadata-only` if you want to stop after pinning and inspect the token URI.
- If neither `receiver` nor `royaltyReceiver` is set, the skill calls `addNewToken(string)`.
- If either receiver field is provided, the skill calls `mintTo(string,address,address)`.
- If only one of `receiver` or `royaltyReceiver` is set, the other defaults to the same address.
- Successful broadcasts write receipts into `receipts/`.

## Deploy receipt auto-resolution

In `own-deployed` mode, the skill looks for a deploy receipt in this order:
1. `--deploy-receipt`
2. `SUPER_RARE_DEPLOY_RECEIPT_FILE`
3. `config.json` `deployReceiptFile`
4. the latest receipt in a sibling `superrare-deploy/receipts/` directory

The resolved deploy receipt must match the selected mint chain.

## Bankr API key resolution

1. `BANKR_API_KEY`
2. `systemctl --user show-environment`
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`
5. `~/.bankr/config.json`

## Quick use

```bash
cp config.example.json config.json

./scripts/mint-via-bankr.sh \
  --token-uri ipfs://... \
  --contract-mode ownership-given \
  --contract 0xYourArtistGivenCollection \
  --broadcast

./scripts/mint-via-bankr.sh \
  --token-uri ipfs://... \
  --contract-mode own-deployed \
  --chain base \
  --deploy-receipt ../superrare-deploy/receipts/2026-03-15T00-00-00Z-superrare-deploy.json \
  --broadcast

./scripts/mint-art.sh \
  --name "aaigotchi genesis #1" \
  --description "First aaigotchi genesis mint" \
  --image ./art.png \
  --contract-mode own-deployed \
  --chain base \
  --broadcast
```

## Timeouts

Optional environment variables:
- `BANKR_SUBMIT_TIMEOUT_SECONDS` (default `60`)
- `RECEIPT_WAIT_TIMEOUT_SECONDS` (default `300`)
- `RECEIPT_POLL_INTERVAL_SECONDS` (default `5`)
