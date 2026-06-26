---
name: tempo-stable-uniswap-swaps
description: Tempo stablecoin and token swap operations for agents. Use when working with pathUSD/USDC.e balances, swapping between USDC.e and pathUSD, or executing any-token swaps via Uniswap on Tempo with quote, Permit2 approvals, simulation, and broadcast.
---

# Tempo Stable + Uniswap Swaps

Use this skill for low-friction Tempo execution with Foundry (`cast`) and Uniswap Trade API.

## One-File Mode (Clawhub-Friendly)

Use this `SKILL.md` alone. No other files are required.

If scripts are unavailable, run the command playbooks in this file directly.

## Network + Tokens

- Chain: Tempo mainnet (`chainId=4217`)
- RPC: `https://rpc.presto.tempo.xyz`
- `pathUSD`: `0x20C0000000000000000000000000000000000000`
- `USDC.e`: `0x20c000000000000000000000b9537d11c60e8b50`
- `TDOGE`: `0x20C000000000000000000000d5d5815Ae71124d1`
- Permit2: `0x000000000022D473030F116dDEE9F6B43aC78BA3`

## Foundry Prereq Check (Required)

Check:

```bash
command -v cast && cast --version
```

Install if missing:

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

## pathUSD vs USDC.e

- `pathUSD` is Tempo-native infrastructure stablecoin used in routing/fees.
- `USDC.e` is bridged stablecoin liquidity.
- Do not attempt exact full-balance `pathUSD` transfers; leave fee headroom.

## Required Tools + Env

- Tools: `cast`, `curl`, `jq`
- Env:
  - `PRIVATE_KEY`
  - `UNISWAP_API_KEY`
  - Optional: `RPC_URL` (default above)

## Quick Balance Checks

```bash
WALLET=$(cast wallet address --private-key "$PRIVATE_KEY")
cast call 0x20C0000000000000000000000000000000000000 \
  "balanceOf(address)(uint256)" "$WALLET" --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}"
cast call 0x20c000000000000000000000b9537d11c60e8b50 \
  "balanceOf(address)(uint256)" "$WALLET" --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}"
```

## Transfer pathUSD

```bash
cast send 0x20C0000000000000000000000000000000000000 \
  "transfer(address,uint256)" <TO> <AMOUNT_RAW> \
  --private-key "$PRIVATE_KEY" --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}" --gas-limit 100000
```

## Swap Any Token on Tempo via Uniswap (Exact Input)

1. Quote:

```bash
curl -sS https://trade-api.gateway.uniswap.org/v1/quote \
  -H 'content-type: application/json' \
  -H "x-api-key: $UNISWAP_API_KEY" \
  --data '{
    "type":"EXACT_INPUT",
    "amount":"<AMOUNT_IN_RAW>",
    "tokenInChainId":4217,
    "tokenOutChainId":4217,
    "tokenIn":"<TOKEN_IN>",
    "tokenOut":"<TOKEN_OUT>",
    "swapper":"<WALLET>",
    "slippageTolerance":2.5
  }'
```

2. Ensure approvals:
`TOKEN_IN -> Permit2`:

```bash
cast send <TOKEN_IN> "approve(address,uint256)" \
  0x000000000022D473030F116dDEE9F6B43aC78BA3 \
  0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff \
  --private-key "$PRIVATE_KEY" --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}" --gas-limit 900000
```

`Permit2 -> spender` (spender from quote `permitData.values.spender`):

```bash
EXP=$(( $(date +%s) + 31536000 ))
cast send 0x000000000022D473030F116dDEE9F6B43aC78BA3 \
  "approve(address,address,uint160,uint48)" \
  <TOKEN_IN> <SPENDER> 1461501637330902918203684832716283019655932542975 "$EXP" \
  --private-key "$PRIVATE_KEY" --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}" --gas-limit 900000
```

3. Build swap tx from quote object (`POST /v1/swap` with `{ "quote": <quote_object> }`), then simulate:

```bash
curl -s "${RPC_URL:-https://rpc.presto.tempo.xyz}" -H 'content-type: application/json' --data \
'{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"from":"<WALLET>","to":"<SWAP_TO>","data":"<SWAP_DATA>"},"latest"]}'
```

4. Broadcast:

```bash
cast send <SWAP_TO> "<SWAP_DATA>" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${RPC_URL:-https://rpc.presto.tempo.xyz}" \
  --gas-limit <GAS_LIMIT> --gas-price <MAX_FEE_PER_GAS>
```

## Known Errors

- `AllowanceExpired(...)`: set Permit2 allowance for token+spender.
- `InsufficientAllowance`: approve token to Permit2.
- Quote exists but swap reverts: refresh quote and retry.
- Full `pathUSD` transfer fails: leave fee headroom.

## Optional Script

If available, use:

```bash
scripts/uniswap_exact_input_swap.sh --token-in <TOKEN_IN> --token-out <TOKEN_OUT> --amount-in <RAW_AMOUNT>
```
