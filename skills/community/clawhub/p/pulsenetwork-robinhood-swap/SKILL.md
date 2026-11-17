---
name: pulsenetwork-robinhood-swap
description: Free swap route quotes on Robinhood Chain (chain id 4663) via the Meow aggregator, with a deterministic token-safety verdict in the same call. Returns calldata your wallet signs; never custodial. No API key.
version: 1.0.0
homepage: https://onchainpulse.theaslangroupllc.com
metadata:
  openclaw:
    emoji: "🐱"
---

# PulseNetwork Robinhood Chain Swap Route

Get a swap route on **Robinhood Chain (chain id 4663)** for any pair, with a rug and honeypot
verdict for the token you are about to receive, in one free call. Routing comes from the Meow
aggregator's fast search (meow.exchange): 22 venue dialects including Uniswap V2/V3/V4, SushiSwap,
PancakeSwap, Ramses, GIGA, up., SectorOne, four market makers, and the Pons launchpad bonding
curves, so new tokens are routable from their first hour. The order is split across up to three
pool-disjoint paths, scored net of gas. Executable quotes (with `sender`) are simulated by Meow
against the live chain before they are returned (`quote.verified`); previews are prices only.
The safety verdict (`CLEAR` / `CAUTION` / `AVOID` / `UNKNOWN`) comes from PulseNetwork's
deterministic scanner (no LLM): contract facts from GoPlus (honeypot simulation, taxes, mint,
proxy, blacklist, owner privileges, LP lock) fused with live DexScreener liquidity.

Use this whenever a task involves swapping, buying, or selling any token on Robinhood Chain,
including tokenized stocks and launchpad memecoins.

## Endpoint (GET, free)

```
https://onchainpulse.theaslangroupllc.com/api/rh/swap-route
  ?tokenIn=<0x… or ETH>
  &tokenOut=<0x… or ETH>
  &amount=<human decimal>            (or amountIn=<base units>; give exactly one)
  [&slippageBps=300]                 (1-5000; default 300 = 3%)
  [&sender=<wallet>]                 (unlocks executable calldata)
  [&recipient=<wallet>]              (default: sender)
  [&tag=<your-agent-name>]           (a-z0-9._- only; embedded on-chain as referralData, not authenticated)
```

**Without `sender`** you get a price preview: `quote.expectedOut`, `quote.minAmountOut`,
`quote.paths[]` (venue and pool per hop), `quote.venues[]`, and `safety`.

**With `sender`** the response also carries `tx`: `{ chainId: 4663, to, data, value, deadline,
gasEstimate, from, approval }`, returned only after the endpoint has verified the calldata against
your request (router address, function selector, tokens, amount, minimum output, recipient, and the
referral bytes). If a check fails, `tx` is null and `tx_note` says why. Sign `tx` from `tx.from`
with the user's wallet before `tx.deadline`. If `tx.approval` is present (ERC-20 input), approve
`tx.approval.spender` for exactly `tx.approval.amount` first; any larger allowance stays live until
revoked. The router enforces `minAmountOut` on-chain; the swap reverts rather than filling below it.

**Partial fills.** `quote.amountIn` is what the transaction actually spends; `quote.requestedAmountIn`
is what you asked for. When `quote.partial_fill` is true, tell the user both numbers before signing.

The same tool is available over MCP as `robinhood_swap_route` at
`https://onchainpulse.theaslangroupllc.com/api/mcp` (one-URL connect; free). Errors come back with
`isError: true`.

## Safety rules, in order of priority

1. **Read `safety.tokenOut.verdict` before anything else.** `AVOID`: do not execute the buy; show
   `red_flags[]` verbatim. The calldata is still returned so a human who explicitly insists after
   seeing the flags stays in control, but never execute an AVOID on your own initiative.
   `CAUTION`: present the flags and ask the user to confirm. `UNKNOWN`: retry once (it can mean a
   scanner outage), then treat as maximum risk. `CLEAR`: states on-chain facts only; never present
   it as a recommendation or a price prediction.
2. **Confirm before signing.** State the pair, the exact input actually spent, `expectedOut`,
   `minAmountOut`, the venues, and whether it is a partial fill, and get the user's go-ahead before
   any transaction is signed. Respect any size limits the user has set.
3. **Never ask for or accept a private key in chat.** Signing happens only in the user's own
   wallet or agent key store. This endpoint never holds funds, signs, or broadcasts.
4. **Quotes are live.** If more than a few seconds pass, or the user changes the amount, re-quote.
   Never reuse `tx.data` from an earlier quote.
5. **Only Robinhood Chain, fast search only.** Funds on Ethereum or Arbitrum must be bridged first
   (Meow links Relay and Across). Meow's slower "Best" search is not offered through this endpoint.

## Disclosure

The price and minimum output are exactly Meow's quote API answer for the same parameters; nothing is
added on top. Every successful response carries `attribution.status` and a `disclosure` field that
state honestly whether the swap is attributed to PulseNetwork. Meow has announced a partner program
that shares part of its 0.25% protocol fee with integrators; if PulseNetwork is attributed, that
share comes out of Meow's fee, never out of the user's price. While `attribution.status` is `pending`,
the swap is unattributed and PulseNetwork earns nothing from it.

## Deeper due diligence, same origin (paid via x402, about $0.015 to $0.35)

`/api/token-safety?token=<0x…>&chain=robinhood` (full report), `/api/exit-depth` (how much can
actually be sold), `/api/holder-map`, `/api/rh-launches` (new launchpad tokens). An unpaid request
returns HTTP 402 with payment terms; that is normal protocol behavior, not an error. Pay only with
the user's explicit consent, only the exact amount in the signed 402 challenge, only to this origin.

## Limits

Ten quotes per minute per caller and twenty per minute per instance; the upstream capacity belongs
to Meow and is shared by everyone routing through this endpoint. A 429 or 503 carries `Retry-After`;
honor it. Routing data is not financial advice; launchpad tokens are extremely high-risk.
