# spanDEX Integration Reference

## Architecture

spanDEX is a **meta-aggregator library** (not a DEX). It queries multiple DEX aggregators in parallel, simulates each quote on-chain, and returns the best result.

- **Package:** `@spandex/core` (MIT license)
- **GitHub:** https://github.com/withfabricxyz/spandex
- **Docs:** https://spandex.sh
- **Creator:** Jonny Mack (@_nonlinear), Fabric team

## Library API used by the script

| Function | Purpose |
|----------|---------|
| `createConfig` | Setup with providers, RPC clients, options |
| `getQuotes` | Fetch + simulate all providers in parallel |
| `selectQuote` | Pick winner by strategy (bestPrice/fastest/estimatedGas/priority) |
| `sortQuotesByPerformance` | Rank quotes by metric for fallback ordering |
| `buildCalls` | Build approval + swap TX array (critical for V4/DERC20 compatibility) |
| `getPricing` | USD prices from provider metadata |
| `netOutputs` | Extract actual output from TX receipt logs |

## Critical lessons

### 1. Use `buildCalls()`, not manual TX construction
Manual `estimateGas({account: "0x..."})` (string address) breaks Uniswap V4 pool settlement. `buildCalls()` + `walletClient.sendTransaction()` handles account context correctly through viem's Account object. This is the root cause of Clanker V4 sell failures when constructing TXs manually.

### 2. Simulation succeeds ≠ estimateGas succeeds
The library's simulation uses `simulateCalls` with state overrides (batched approve + swap). Manual `estimateGas` on just the swap TX can fail with valid approvals due to account context differences.

### 3. `netOutputs` > balance checks
Post-swap balance reads have a race condition (RPC node may not have indexed the transfer). `netOutputs` parses TX receipt logs directly — always accurate.

### 4. `executeQuote` has a footgun
It passes `swap.swapperAccount` (string) to `walletClient.sendTransaction({account})`, overriding the Account object and triggering `eth_sendTransaction` (JSON-RPC mode) instead of local signing. The script bypasses this with `buildCalls` + manual send.

## Gas configuration

- **Base sequencer orders by priority fee** (confirmed OP Stack docs)
- Default 0.03 gwei priority fee = "instant" tier (~$0.02-0.05 per swap)
- Formula: `maxFeePerGas = baseFee × 2 + priorityFee`

## KyberSwap Limit Orders

- **API:** `https://limit-order.kyberswap.com`
- **Contract (Base):** `0xcab2FA2eeab7065B45CBcF6E3936dDE2506b4f6C`
- **Flow:** POST sign-message → sign EIP-712 → POST order. Gasless.
- Works with all token types including Clanker/DERC20 (approval to LO contract, not router)

## Provider details

| Provider | Fee | Notes |
|----------|-----|-------|
| Fabric | 0-0.1% | Built by spanDEX team |
| KyberSwap | 0% | Best V4/DERC20 support, limit orders |
| Odos | 0.03% | Multi-hop routing |
| Velora | 15% integrator fee | MEV protection |
| LI.FI | 0.25% | Cross-chain capable |
| Relay | varies | Cross-chain, intent-based |
| 0x | 0.15% | Not included (requires API key) |
