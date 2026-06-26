---
name: spandex-trader
description: Trade tokens on Base using spanDEX, the open-source meta-aggregator. Supports market swaps (races 6 providers for best price with automatic fallback), limit orders via KyberSwap, balance checks, and provider comparison. Works with all token types including Clanker V4, Flaunch DERC20, and standard ERC-20. Use when the user wants to swap tokens, place limit orders, check wallet balances, or execute trades on Base chain. Triggers on "swap", "buy", "sell", "trade", "limit order", "spanDEX", "best price", "meta-aggregator".
---

# spanDEX Trader

Trade on Base chain using [spanDEX](https://spandex.sh) — the free, open-source meta-aggregator by [@_nonlinear](https://x.com/_nonlinear) / [Fabric](https://github.com/withfabricxyz/spandex).

Races 6 DEX aggregators (Fabric, KyberSwap, Odos, Velora, LI.FI, Relay) per swap, simulates on-chain, picks the winner, and executes with automatic fallback if the best-priced provider fails.

## Setup

**Prerequisites:** Node.js 18+, npm

```bash
# Install dependencies (run once in skill directory)
cd <skill-dir>/scripts && npm init -y && npm i viem @spandex/core
```

**Required env vars:**
| Var | Purpose |
|-----|---------|
| `BASE_RPC_URL` | Base chain RPC endpoint (Alchemy, Infura, dRPC, etc.) |
| `SPANDEX_PRIVATE_KEY` | Wallet private key (hex). OR use `SPANDEX_KEY_PATH` for file-based key |

**Optional env vars:**
| Var | Default | Purpose |
|-----|---------|---------|
| `SPANDEX_KEY_PATH` | — | Path to file containing private key (alternative to raw key) |
| `SPANDEX_APP_ID` | `spandex-trader-skill` | App identifier for provider APIs |
| `SPANDEX_STRATEGY` | `bestPrice` | Default quote strategy |
| `SPANDEX_PRIORITY_GWEI` | `0.03` | Priority fee floor (gwei) for Base sequencer |
| `SPANDEX_SKIP_LOCK` | — | Set `1` to disable anti-double-execution lock |
| `SPANDEX_DEBUG` | — | Enable debug logging |

## Commands

All output is JSON. TOKEN can be a contract address or alias (USDC, WETH, ETH, DAI, USDT).

```bash
# Compare prices across all 6 providers
node scripts/spandex_trade.mjs quote --sell USDC --buy 0xTOKEN --amount 50

# Execute swap (best price, automatic fallback)
node scripts/spandex_trade.mjs swap --sell USDC --buy 0xTOKEN --amount 50
node scripts/spandex_trade.mjs swap --sell USDC --buy 0xTOKEN --amount 50 --slippage 500 --dry-run

# KyberSwap limit orders (gasless EIP-712)
node scripts/spandex_trade.mjs limit --sell 0xTOKEN --buy USDC --sell-amount 1000000 --buy-amount 50 --expiry 7d
node scripts/spandex_trade.mjs orders --status active
node scripts/spandex_trade.mjs cancel-order --order-id 123

# Wallet
node scripts/spandex_trade.mjs balance
node scripts/spandex_trade.mjs balance --token 0xTOKEN
node scripts/spandex_trade.mjs providers
```

## Slippage defaults

Auto-applied based on token pair:
- Major ↔ Major (USDC/WETH/ETH): **0.5%** (50 bps)
- Major ↔ Microcap: **3%** (300 bps)
- Microcap ↔ Microcap: **5%** (500 bps)

Override with `--slippage <bps>`.

## Execution flow

1. `getQuotes()` — fetch + simulate from all 6 providers in parallel
2. `sortQuotesByPerformance()` — rank by output amount (best first)
3. For each quote: `buildCalls()` → `sendTransaction()` with priority fee → if fail, try next provider
4. `netOutputs()` — extract actual output from TX receipt logs
5. Final balance verification

## Key behaviors

- **Anti-double-execution:** 120s lockfile per token prevents accidental duplicate swaps
- **Fallback routing:** If best-price provider fails execution, automatically tries next
- **V4/DERC20 compatible:** Uses `buildCalls()` for proper Clanker V4 and Flaunch DERC20 settlement
- **No API keys needed:** All 6 providers work without registration

## Token compatibility by provider

| Provider | Standard ERC-20 | Clanker V4 | Flaunch DERC20 |
|----------|----------------|------------|----------------|
| KyberSwap | ✅ | ✅ | ✅ |
| LI.FI | ✅ | ✅ | ✅ |
| Fabric | ✅ | ⚠️ | ⚠️ |
| Odos | ✅ | ❌ | ❌ |
| Velora | ✅ | ❌ | ❌ |
| Relay | ✅ | ⚠️ | ⚠️ |

For detailed integration notes and architecture, see `references/INTEGRATION.md`.
