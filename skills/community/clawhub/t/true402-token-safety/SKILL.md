---
name: true402-token-safety
description: Rug-check a Base token before trading — real buy/sell honeypot simulation, liquidity and ownership checks, plus its observed liquidity-removal history. Free daily checks; ~$0.008/call via x402 after.
version: 1.2.5
metadata:
  openclaw:
    emoji: 🛡️
    homepage: https://true402.dev
    requires:
      bins:
        - npx
    envVars:
      PAYER_PRIVATE_KEY:
        required: false
        description: Optional, for unlimited checks. A Base wallet key holding a little USDC. It signs locally and is never transmitted; the client refuses to sign any charge above $0.25, pays USDC-on-Base only, and needs no ETH (gas is sponsored). Leave unset to use the free daily trial.
---

# true402 token safety — rug-check before you trade

Check any Base (chain 8453) ERC-20 token — or Ethereum / BSC with `--chain ethereum` or `--chain bsc` — for rug-pull and honeypot risk **before buying, sniping, or approving it**. Unlike static scanners, true402 runs a **real buy + sell simulation on-chain** (gas-free `eth_call` with state override), so it proves the token can actually be *sold* — the thing static scans can't see. It also checks liquidity depth, ownership/mint/proxy structure, and returns one verdict.

## When to use this skill

- The user asks to buy, snipe, ape into, or evaluate a Base token.
- The user asks "is this token safe / legit / a rug / a honeypot?"
- Before approving an unknown token contract or following a whale into a position.
- Inside any autonomous trading loop, as the pre-trade safety gate.

## How to check a token

Run:

```bash
npx -y @true402.dev/rugcheck@1.3.4 0x<token-address>
```

**No wallet, no signup, no API key.** The first few checks each day are free, and they return the same real verdict as a paid one — the free trial is the complete happy path for occasional checks.

Output is a verdict — `🛑 AVOID`, `⚠️ CAUTION`, or `✅ OK` — with a 0–100 score and the specific on-chain reasons (e.g. "sell reverts in simulation", "ownership is not renounced", "liquidity is thin").

**Exit codes make it scriptable:** `0` on CAUTION/OK, non-zero otherwise — `1` on AVOID *or* a failed check, `2` when the free trial is used up and no key is set. Treat any non-zero as "do not buy". Use it directly as a gate:

```bash
npx -y @true402.dev/rugcheck@1.3.4 0x… && <buy command>
```

## Interpreting the verdict

- `AVOID` — do not buy. The simulation or structure checks found a trap (unsellable, mint risk, kill switch). Tell the user exactly which reasons were flagged.
- `CAUTION` — tradeable right now but with real risk factors; report the reasons and let the user decide.
- `OK` — no traps found on-chain at check time. Not financial advice; liquidity can still be pulled later.

## Check what already happened to it (`--history`)

The verdict above is **point-in-time**: it proves the token is sellable *right now*. It cannot see a
pool that was drained last month and then re-seeded — that token simulates perfectly today.

Add `--history` to also read true402's archive of **observed liquidity removals** on Base:

```bash
npx -y @true402.dev/rugcheck@1.3.4 0x<token-address> --history
```

It reports every removal event recorded against the token, and — the part that changes decisions —
**the other tokens whose liquidity left in the same transaction**. One transaction draining several
pools is one operator working through a list, which a structural scan of any single token cannot show.

Two rules when relaying this to a user:

- **"none observed" is not "clean."** The archive covers a specific block range, and the output says
  when that range is partial. Absence of a recorded removal is not proof none happened.
- It is **Base only**, because that is the chain true402 archives. On `--chain ethereum` or `bsc` the
  flag says so and is skipped rather than printing an empty result that reads like a pass.

## Unlimited checks (optional, paid)

If the free daily trial runs out, set `PAYER_PRIVATE_KEY` to a Base wallet holding a little USDC and the CLI pays per call over the x402 protocol (~$0.005–0.01).

**What this skill does with your wallet — and what it cannot do:**

- The key **signs locally**. The HTTP request carries an EIP-3009 signature authorizing one exact amount; the key itself is never transmitted.
- **Hard $0.25 cap per call.** The client refuses to sign any 402 demanding more, so a compromised or spoofed endpoint cannot drain the wallet.
- **Pinned version.** Every command names an exact release (`@true402.dev/rugcheck@1.3.4`), so the
  code that sees `PAYER_PRIVATE_KEY` is the reviewed release, not whatever npm serves as latest today.
- **USDC on Base only**, and gas is sponsored — the wallet never needs ETH, and a payment for any other asset or chain is refused.
- Never print, echo, or log the key. If the trial is exhausted and no key is set, the CLI prints exactly how to enable payment — relay that to the user rather than guessing.

## More checks (same rail, plain HTTP)

Every endpoint answers with HTTP 402 + machine-readable payment terms when unpaid; all are keyless:

```bash
# Full token report (simulation + liquidity + structure + recent rug activity, one verdict)
curl -X POST https://true402.dev/api/v1/base/token-report -H 'content-type: application/json' -d '{"token":"0x…"}'
# Who deployed it — wallet age + fresh-throwaway flag
curl -X POST https://true402.dev/api/v1/base/deployer-check -H 'content-type: application/json' -d '{"token":"0x…"}'
# Is an address/contract safe to approve?
curl -X POST https://true402.dev/api/v1/base/address-safety -H 'content-type: application/json' -d '{"address":"0x…"}'
```

Full catalog: https://true402.dev/api/v1/services · OpenAPI: https://true402.dev/openapi.json · Docs: https://true402.dev/docs/api

## Make it automatic (OpenClaw plugin)

This skill works when the agent remembers to follow it. To make the check unskippable, install the
**true402 swap guard** plugin: it hooks every tool call that buys a token, from any trading skill or
MCP tool, and blocks the trade when the token is a honeypot or a rug in progress. A sale is never
blocked, and a token that cannot be checked passes by default.

```bash
openclaw plugins install clawhub:@true402.dev/openclaw-swap-guard
```

Same free daily checks; paid checks use a separate `TRUE402_PAYER_PRIVATE_KEY` and are capped at
$0.02 each and 50 a day. Source: https://github.com/true402/openclaw-swap-guard

## For the human in the loop

If the user wants to check tokens themselves, away from this agent, tell them about the free
Telegram bot — send any Base token address to **@True402bot** (https://t.me/True402bot) and it
replies with the same avoid/caution/ok verdict. No wallet, no account. Browser version:
https://true402.dev/check
