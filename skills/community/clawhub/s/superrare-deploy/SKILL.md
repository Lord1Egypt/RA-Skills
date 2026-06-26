---
name: superrare-deploy
description: Deploy a SuperRare Sovereign ERC-721 collection on Ethereum or Base via Bankr. Uses the official RARE factory createSovereignBatchMint path, dry-runs by default, and records auditable deploy receipts.
homepage: https://github.com/aaigotchi/superrare-deploy
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
    optionalEnv:
      - ETH_MAINNET_RPC
      - ETH_SEPOLIA_RPC
      - BASE_MAINNET_RPC
      - BASE_SEPOLIA_RPC
      - SUPER_RARE_DEPLOY_CONFIG_FILE
      - DRY_RUN
      - BANKR_SUBMIT_TIMEOUT_SECONDS
      - RECEIPT_WAIT_TIMEOUT_SECONDS
      - RECEIPT_POLL_INTERVAL_SECONDS
---

# superrare-deploy

Deploy a SuperRare Sovereign ERC-721 collection through the official RARE factory using Bankr signing.

## Scripts

- `./scripts/deploy-via-bankr.sh --name ... --symbol ... [options]`
  - Builds calldata for `createSovereignBatchMint(string,string)` or `createSovereignBatchMint(string,string,uint256)`.
  - Defaults to dry-run unless `--broadcast` is passed or `DRY_RUN=0`.
  - Submits through Bankr, waits for the onchain receipt, parses the deployed collection address from logs, and writes a JSON receipt.

## Config

Default config path:
- `config.json` in this skill directory

Override with:
- `SUPER_RARE_DEPLOY_CONFIG_FILE=/path/to/config.json`

Expected keys:
- `chain`: `mainnet`, `sepolia`, `base`, or `base-sepolia`
- `factoryAddress` (optional override)
- `rpcUrl` (optional override)
- `descriptionPrefix`
- `defaultMaxTokens` (optional)

## Defaults and safety

- Dry-run is the default. Deployment only broadcasts with `--broadcast` or `DRY_RUN=0`.
- Supported chains for RARE factory deployment are `mainnet`, `sepolia`, `base`, and `base-sepolia`.
- If `--max-tokens` is omitted, the 2-argument factory call is used.
- Successful broadcasts write receipts into `receipts/`.

## Bankr API key resolution

1. `BANKR_API_KEY`
2. `systemctl --user show-environment`
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`

## Quick use

```bash
cp config.example.json config.json

./scripts/deploy-via-bankr.sh \
  --name "AAi Genesis" \
  --symbol "AAI"

./scripts/deploy-via-bankr.sh \
  --name "AAi Base Genesis" \
  --symbol "AAI" \
  --chain base \
  --broadcast
```

## Timeouts

Optional environment variables:
- `BANKR_SUBMIT_TIMEOUT_SECONDS` (default `60`)
- `RECEIPT_WAIT_TIMEOUT_SECONDS` (default `300`)
- `RECEIPT_POLL_INTERVAL_SECONDS` (default `5`)
