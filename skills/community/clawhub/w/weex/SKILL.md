---
name: WEEX API
description: Automated trading tool for WEEX API, supporting futures and spot trading, including natural language order placement, order cancellation, order query, market data and account data retrieval.
metadata:
  version: "1.0.0"
---

# WEEX API

Use:
- `scripts/weex_contract_api.py` for contract
- `scripts/weex_spot_api.py` for spot

For private endpoints:

```bash
export WEEX_API_KEY="..."
export WEEX_API_SECRET="..."
export WEEX_API_PASSPHRASE="..."
export WEEX_API_BASE="https://api-contract.weex.com"
export WEEX_LOCALE="en-US"
```

## Fast Path

```bash
# Contract
python3 scripts/weex_contract_api.py list-endpoints --pretty
python3 scripts/weex_contract_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_contract_api.py poll-ticker --symbol BTCUSDT --interval 2 --count 30 --pretty

# Spot
python3 scripts/weex_spot_api.py list-endpoints --pretty
python3 scripts/weex_spot_api.py ticker --symbol BTCUSDT --pretty
```

## Natural Language Order

Natural language is interpreted by the agent layer.  
Scripts no longer parse keywords from free text.

The agent must convert user intent into structured fields, then call deterministic commands:

```bash
# Contract V3
python3 scripts/weex_contract_api.py place-order \
  --symbol ETHUSDT --side SELL --position-side SHORT --type LIMIT \
  --quantity 0.001 --price 10000 --time-in-force GTC --confirm-live --pretty

# Spot V3
python3 scripts/weex_spot_api.py place-order \
  --symbol ETHUSDT --side BUY --order-type LIMIT \
  --quantity 0.001 --price 999 --time-in-force GTC --confirm-live --pretty
```

## Safety Policy

- Never send mutating requests without `--confirm-live`.
- Default flow is direct live execution (no dry-run step).
- If instruction is ambiguous or missing fields, ask only for missing fields.

## Regenerating API Definitions

Local contract and spot definitions are generated from the live WEEX V3 docs:

```bash
python3 scripts/generate_weex_api_definitions.py --product all
```

## References

- `references/spot-endpoints.md`
- `references/spot-api-definitions.json` (machine-readable local spot interface definitions)
- `references/spot-api-definitions.md` (human-readable local spot interface definitions)
- `references/contract-api-definitions.json` (machine-readable local interface definitions)
- `references/contract-api-definitions.md` (human-readable local interface definitions)
- `references/contract-endpoints.md`
- `references/auth-and-signing.md`
- `references/websocket.md`
